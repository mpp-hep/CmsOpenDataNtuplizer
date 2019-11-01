import os
import argparse
from multiprocessing import Pool

import numpy as np
import h5py


def load(file_path):
    if not (os.path.isfile(file_path) and file_path.endswith('.hdf5')):
        return None

    print('loading: ' + file_path)

    # load hdf5 file
    try:
        hdf5_file = h5py.File(file_path, "r")
        data = hdf5_file['data'][()]
        n_tot = hdf5_file['n_tot'][()]
        # header = hdf5_file['header'][()]
        hdf5_file.close()
    except:
        print('failed to load: ' + file_path)
        return None

    return (data, n_tot)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help="directory containing the hdf5 files", required=True)
    parser.add_argument('-o', '--output', type=str, help="output file", required=True)
    parser.add_argument('-n', '--n', type=str, help="number of threads", required=True)
    args = parser.parse_args()

    file_path_list = [os.path.join(args.input, f) for f in os.listdir(args.input)]

    p = Pool(int(args.n))
    res = p.map(load, file_path_list)
    res = [x for x in res if x is not None]  # filter out None values

    data_list = [x[0] for x in res]
    n_tot_list = [x[1] for x in res]

    print('loading finished. number of files loaded: ' + str(len(res)))

    n_tot_sum = np.sum(n_tot_list)
    print('n_tot: ' + str(n_tot_sum))

    print('concatenating files')
    data_fused = np.concatenate(data_list, axis=0)
    print('concatenation finished. shape: ' + str(data_fused.shape))

    print('saving to: ' + args.output)
    hdf5_file = h5py.File(args.output, "w")
    hdf5_file.create_dataset('data', data=data_fused, compression='gzip')
    hdf5_file.create_dataset('n_tot', data=n_tot_sum)
    hdf5_file.close()
    print('finished')

