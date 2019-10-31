import os
import argparse
from hlf_ntuplizer import *

from multiprocessing import Pool, Value
import time
import random

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help="file containing the list of input files", required=True)
    parser.add_argument('-o', '--output', type=str, help="output directory", required=True)
    parser.add_argument('-n', '--n', type=str, help="number of threads", required=True)
    parser.add_argument('-ntot', '--ntot', type=int, help="number of events", required=True)
    args = parser.parse_args()

    with open(args.input) as f:
        file_list = f.readlines()

    file_list = [x.strip() for x in file_list]

    # shuffle list (just in case)
    random.shuffle(file_list)

    n_tot_target = args.ntot
    n_tot = Value('i', 0)


    def convert_file(file):
        if n_tot.value >= n_tot_target:
            return

        # output file
        idx = file.rfind('/')
        name = file[idx + 1:-5]
        output_file = os.path.join(args.output, name + '.hdf5')

        if os.path.isfile(output_file):
            print('file already exists: ' + output_file)
            return

        start = time.time()

        # creating hlf ntuplizer
        ntuplizer = Ntuplizer()
        ntuplizer.register_selector(MuonSelector())
        ntuplizer.register_quantity_module(JetModule())
        ntuplizer.register_quantity_module(BTagModule())
        ntuplizer.register_quantity_module(MaxLeptonModule())
        ntuplizer.register_quantity_module(MuonsModule())
        ntuplizer.register_quantity_module(LeptonModule('ele', 'recoGsfElectrons_gsfElectrons__RECO.obj'))
        ntuplizer.register_quantity_module(ParticleCountModule('neu', 130))
        ntuplizer.register_quantity_module(ParticleCountModule('ch', 211))
        ntuplizer.register_quantity_module(ParticleCountModule('photon', 22))

        # running ntuplizer
        result, names, n_events = ntuplizer.convert(file)

        print('output shape: ' + str(result.shape))

        with n_tot.get_lock():
            n_tot.value += result.shape[0]
            print('N_tot: %d (%d %)' % (n_tot.value, n_tot.value / n_tot_target * 100))

        print('saving output to file: ' + output_file)
        hdf5_file = h5py.File(output_file, "w")
        hdf5_file.create_dataset('data', data=result, compression='gzip')
        hdf5_file.create_dataset('header', data=ntuplizer.get_names())
        hdf5_file.create_dataset('shape', data=result.shape[0])
        hdf5_file.close()

        print('time taken: ' + str(int(time.time() - start)))


    p = Pool(int(args.n))
    p.map(convert_file, file_list)
