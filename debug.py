import os
import argparse
from hlf_ntuplizer import *

from multiprocessing import Pool
import time

if __name__ == '__main__':
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

    print(ntuplizer.get_names())

    file = '/home/oliverkn/pro/real_data_test/test.root'
    result, names = ntuplizer.convert(file)
