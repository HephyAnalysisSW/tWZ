## DY
#python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --reduceSizeBy 2 --sample DYJetsToLL_M50_LO #SPLIT40
##python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample DYJetsToLL_M50 #SPLIT40
#python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --reduceSizeBy 2 --sample DYJetsToLL_M10to50_LO #SPLIT40

## full stats
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample DYJetsToLL_M50_LO #SPLIT40
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample DYJetsToLL_M10to50_LO #SPLIT40
#
## HT binned samples ##
## high mass #
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --LHEHTCut 70 --sample DYJetsToLL_M50_LO #SPLIT40
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample DYJetsToLL_M50_HT70to100 #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample DYJetsToLL_M50_HT100to200 #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample DYJetsToLL_M50_HT200to400 #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample DYJetsToLL_M50_HT400to600 DYJetsToLL_M50_HT400to600_ext #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample DYJetsToLL_M50_HT600to800 #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample DYJetsToLL_M50_HT800to1200 #SPLIT10
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample DYJetsToLL_M50_HT1200to2500 #SPLIT10
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample DYJetsToLL_M50_HT2500toInf #SPLIT10
# low mass #
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --LHEHTCut 70 --sample DYJetsToLL_M10to50_LO #SPLIT40
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample DYJetsToLL_M4to50_HT70to100 #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample DYJetsToLL_M4to50_HT100to200 #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample DYJetsToLL_M4to50_HT200to400 #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample DYJetsToLL_M4to50_HT400to600 #SPLIT10
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample DYJetsToLL_M4to50_HT600toInf #SPLIT10
#
# top
#python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --reduceSizeBy 3 --sample TTLep_pow #SPLIT80
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --flagTTBar --sample TTLep_pow  #SPLIT80
#python nanoPostProcessing.py  --overwrite --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --flagTTBar --sample TTSingleLep_pow #SPLIT80
#python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --flagTTGamma --sample TTGLep #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --reduceSizeBy 5 --sample TToLeptons_sch_amcatnlo #SPLIT20
python nanoPostProcessing.py --overwrite --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample T_tWch #SPLIT20
python nanoPostProcessing.py --overwrite --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample TBar_tWch #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --reduceSizeBy 15 --sample T_tch_pow #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --reduceSizeBy 15 --sample TBar_tch_pow #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample tZq_ll #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample tWll #SPLIT11
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample TTWToLNu #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample TTWToQQ #SPLIT14
##python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample TTW_LO #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample TTZToLLNuNu #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample TTZToLLNuNu_m1to10 #SPLIT10
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample TTZToQQ #SPLIT20
##python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample TTZ_LO #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample TTHbbLep #SPLIT10
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample TTHnobb_pow #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample THQ #SPLIT5
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample THW #SPLIT5
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample TTTT #SPLIT5
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample tWnunu #SPLIT5

##
##
## di/multi boson



python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample VVTo2L2Nu #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample WZTo3LNu_amcatnlo #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample WZTo2L2Q #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample WZTo1L3Nu #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample WWTo1L1Nu2Q #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample WWToLNuQQ #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample ZZTo4L #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample ZZTo2Q2Nu #SPLIT10
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --reduceSizeBy 5 --sample ZZTo2L2Q #SPLIT20
# additional samples for ARC studies
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample WWTo2L2Nu #SPLIT20
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample ZZTo2L2Nu #SPLIT20
##
###python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample WW #SPLIT5
###python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample ZZ #SPLIT5
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample WWW_4F #SPLIT5
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample WWZ #SPLIT5
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample WZZ #SPLIT5
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample ZZZ #SPLIT5
##
### rare
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample TTWZ #SPLIT5
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample TTWW #SPLIT5
python nanoPostProcessing.py  --forceProxy --skim trilep --nanoAODv4 --year 2018 --processingEra tWZ_nAODv4 --sample TTZZ #SPLIT5
