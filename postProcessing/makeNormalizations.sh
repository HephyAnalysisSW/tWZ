rm jobsNormalizations.sh

#python makeNormalizations.py --sampleFile Samples.nanoAOD.UL16_nanoAODAPVv9
#python makeNormalizations.py --sampleFile Samples.nanoAOD.UL16_nanoAODv9
#python makeNormalizations.py --sampleFile Samples.nanoAOD.UL17_nanoAODv9
#python makeNormalizations.py --sampleFile Samples.nanoAOD.UL18_nanoAODv9
python makeNormalizations.py --sampleFile Samples.nanoAOD.UL16_privateDennis_nanoAODAPVv9 --TopNanoAOD
python makeNormalizations.py --sampleFile Samples.nanoAOD.UL16_privateDennis_nanoAODv9 --TopNanoAOD
python makeNormalizations.py --sampleFile Samples.nanoAOD.UL17_privateDennis_nanoAODv9 --TopNanoAOD
python makeNormalizations.py --sampleFile Samples.nanoAOD.UL18_privateDennis_nanoAODv9 --TopNanoAOD
