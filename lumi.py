import ROOT
from DataFormats.FWLite import Events, Handle, Lumis
import argparse

from FWCore.PythonUtilities.LumiList   import LumiList

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, help="file containing the list of input files", required=True)
args = parser.parse_args()

goodLumis = LumiList(url = 'http://opendata.cern.ch/record/1002/files/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt')
print "all good lumis"
print goodLumis

lumis = Lumis(args.input)
for lum in lumis:
    runsLumisDict = {}
    runList = runsLumisDict.setdefault (lum.aux().run(), [])
    runList.append( lum.aux().id().luminosityBlock() )
    myLumis = LumiList(runsAndLumis = runsLumisDict)
    if myLumis.getLumis() in goodLumis.getLumis():
        print "good lumi"
        print myLumis
    else:
        print "bad lumi"
        print myLumis