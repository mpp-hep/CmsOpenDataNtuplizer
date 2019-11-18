import os
import argparse
from multiprocessing import Pool

import numpy as np
import h5py

path = '/home/oliverkn/pro/opendata_v2/6021'

input_file = os.path.join(path, 'data.hdf5')
hdf5_file = h5py.File(input_file, "r")

print('loading')
data = hdf5_file['data'][()]
n_tot = hdf5_file['n_tot'][()]

print('saving')
output_file = os.path.join(path, 'data_nc.hdf5')
hdf5_file = h5py.File(output_file, "w")
hdf5_file.create_dataset('data', data=data)
hdf5_file.create_dataset('n_tot', data=n_tot)
hdf5_file.close()

print('done')
