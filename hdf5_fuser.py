import os
import argparse
import glob

import numpy as np
import h5py
import pickle

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help="directory containing the hdf5 files", required=True)
    parser.add_argument('-o', '--output', type=str, help="output file", required=True)
    args = parser.parse_args()

    data_fused = None

    for f in os.listdir(args.input):

        file_path = os.path.join(args.input, f)

        if not (os.path.isfile(file_path) and f.endswith('.hdf5')):
            continue

        print('loading: ' + f)

        # load hdf5 file
        hdf5_file = h5py.File(file_path, "r")
        data = hdf5_file['data'].value
        hdf5_file.close()

        if data_fused is None:
            data_fused = data
        else:
            data_fused = np.append(data_fused, data, axis=0)

    print('loading finished. shape: ' + str(data_fused.shape))

    print('saving to: ' + args.output)
    # np.save(args.output, data_fused)

    hdf5_file = h5py.File(args.output, "w")
    hdf5_file.create_dataset('data', data=data_fused, compression='gzip')
    hdf5_file.close()

    print('finished')
