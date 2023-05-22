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



if args.year not in ["UL2016_preVFP", "UL2018"]:
    raise Exception("Year %s not known"%args.year)

if args.process not in ["TTZ_EFT", "WZ_EFT", "ZZ_EFT"]:
    raise Exception("Process %s not known"%args.process)

path = "/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v2/"



samples = []
for i in range(100):
    samples.append(path+args.year+"/trilep/"+args.process+"/"+args.process+"_"+str(i)+".root")

logger.info("Reading %s, %s", args.year, args.process)

counter_all = 0
counter_valid_all = 0

for sample in samples:
    counter_sample = 0
    counter_valid_sample = 0
    file = ROOT.TFile(sample)
    tree = file.Get("Events")
    for event in file.Events:
        counter_all += 1
        counter_sample += 1
        if event.EFT_valid:
            counter_valid_all += 1
            counter_valid_sample += 1
    logger.info("   %s - %i of %i events valid (%.2f percent)",sample, counter_valid_sample, counter_sample, 100*counter_valid_sample/counter_sample)
logger.info("%s of %s - %i of %i events valid (%.2f percent)", args.process, args.year, counter_valid_all, counter_all, 100*counter_valid_all/counter_all)
