import os
import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--year',           action='store', type=str)
argParser.add_argument('--process',        action='store', type=str)
args = argParser.parse_args()

eosdir = "/eos/vbc/experiments/cms/store/user/deschwar/topNanoAOD/v9-1-1/"

if args.year not in ["UL2016_preVFP", "UL2016", "UL2018"]:
    raise Exception("Year %s not known"%args.year)

if args.process not in ["TTZ_EFT", "WZ_EFT", "ZZ_EFT"]:
    raise Exception("Process %s not known"%args.process)

directories = {
    "UL2016_preVFP": {
        "TTZ_EFT": ["2016ULpreVFP/TTZToLL_5f_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv9-1-1_2016ULpreVFP/230426_103209/0000/"],
        "WZ_EFT" : ["2016ULpreVFP/WZTo3LNu_5f_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv9-1-1_2016ULpreVFP/230426_102536/0000/"],
        "ZZ_EFT" : ["2016ULpreVFP/ZZTo4L_5f_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv9-1-1_2016ULpreVFP/230426_102934/0000/"],
    },
    "UL2016": {
        "TTZ_EFT": ["2016ULpostVFP/TTZToLL_5f_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv9-1-1_2016ULpostVFP/230511_132730/0000//"],
        "WZ_EFT" : ["2016ULpostVFP/WZTo3LNu_5f_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv9-1-1_2016ULpostVFP/230511_142548/0000/"],
        "ZZ_EFT" : ["2016ULpostVFP/ZZTo4L_5f_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv9-1-1_2016ULpostVFP/230511_133542/0000/"],
    },
    "UL2018": {
        "TTZ_EFT": ["2018UL/TTZToLL_5f_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv9-1-1_2018UL/230406_130018/0000/","2018UL/TTZToLL_5f_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv9-1-1_2018UL/230406_130018/0001/"],
        "WZ_EFT" : ["2018UL/WZTo3LNu_5f_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv9-1-1_2018UL/230406_151850/0000/"],
        "ZZ_EFT" : ["2018UL/ZZTo4L_5f_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv9-1-1_2018UL/230406_152138/0000/"],
    },
}

counter_all = 0
counter_fail_all = 0

listofdamagedfiles = []

for dir in directories[args.year][args.process]:
    logger.info("Reading %s, %s", args.year, args.process)
    path = eosdir+dir
    logger.info("Scanning %s", path)
    for filename in os.listdir(path):
        if ".root" in filename:
            counter_sample = 0
            counter_fail_sample = 0
            file = ROOT.TFile(path+filename)
            tree = file.Get("Events")
            for event in file.Events:
                counter_all += 1
                counter_sample += 1
                if event.nLHEReweightingWeight < 119:
                    counter_fail_all += 1
                    counter_fail_sample += 1
            logger.info("   %s - %i of %i events wrong (%.2f percent)",filename, counter_fail_sample, counter_sample, 100*counter_fail_sample/counter_sample)
            if counter_fail_sample > 0:
                listofdamagedfiles.append(filename)
logger.info("%s of %s - %i of %i events wrong (%.2f percent)", args.process, args.year, counter_fail_all, counter_all, 100*counter_fail_all/counter_all)

for f in listofdamagedfiles:
    logger.info(f)
