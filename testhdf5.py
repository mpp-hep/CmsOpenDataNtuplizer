import os
import argparse
from hlf_ntuplizer import *

from multiprocessing import Pool, Value
import time

if __name__ == '__main__':
    # hdf5_file = h5py.File('test.hdf5', "w")
    # hdf5_file.create_dataset('n_tot', data=(200,23))
    # hdf5_file.create_dataset('header', data=('a', 'b'))
    # hdf5_file.close()
    #
    f = h5py.File('/home/oliverkn/Downloads/bla.hdf5', "r")
    print(f['shape'][0])
