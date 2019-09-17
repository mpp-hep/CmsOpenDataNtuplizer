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
    hdf5_file = h5py.File(file_path, "r")
    data = hdf5_file['data'].value
    hdf5_file.close()
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help="directory containing the hdf5 files", required=True)
    parser.add_argument('-o', '--output', type=str, help="output file", required=True)
    parser.add_argument('-n', '--n', type=str, help="number of threads", required=True)
    args = parser.parse_args()

    data_fused = None

    p = Pool(int(args.n))

    file_path_list = [os.path.join(args.input, f) for f in os.listdir(args.input)]

    res = p.map(load, file_path_list)

    print('loading finished. number of files loaded: ' + str(len(res)))
    print('concatenating files')
    data_fused = np.concatenate(res, axis=0)

    print('concatenation finished. shape: ' + str(data_fused.shape))

    print('saving to: ' + args.output)

    hdf5_file = h5py.File(args.output, "w")
    hdf5_file.create_dataset('data', data=data_fused, compression='gzip')
    hdf5_file.close()

    print('finished')
