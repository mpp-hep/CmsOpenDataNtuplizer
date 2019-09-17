cd ~/private/cmssw10_6_2/CMSSW_10_6_2/bin
cmsenv
cd ~/private/ntuplizer/
python parallel.py --input list_Run2012B-22Jan2013-v1.txt --output /eos/home-o/oknapp/run_b --n 6 > out.txt &

cd /eos/home-o/oknapp/run_b/
ls -l | grep ^- | wc -l

python hdf5_fuser.py --input /eos/home-o/oknapp/run_b --output /eos/home-o/oknapp/run_b.hdf5 --n 100
