#!/usr/bin/env python
import os
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--channel',        action='store',      default='muon')
argParser.add_argument('--year',           action='store',      default='UL2018')
args = argParser.parse_args()

logger.info("Script to run combine fits in fakerate measurement")

inputdir = "/groups/hephy/cms/dennis.schwarz/www/tWZ/Fakerate/CombineInput/datacards/"
outputdir = "/groups/hephy/cms/dennis.schwarz/www/tWZ/Fakerate/Fits/"

prefix = "Fakerate_"
year = args.year
channel = args.channel

boundaries_pt = [0, 20, 30, 45, 120]
boundaries_eta = [0, 1.2, 2.1, 2.4]
if args.channel == "elec":
    boundaries_eta = [0, 0.8, 1.44, 2.4]
WPs = ["LOOSE", "TIGHT"]

text2workspace_cmd = 'text2workspace.py <TXTFILE> -m 0 -o <ROOTFILE>'
combine_cmd = "combine <NAME> -M FitDiagnostics --saveShapes --saveWithUnc --numToysForShape 2000  --preFitValue 1 --setParameterRanges r=0.1,10 -n <OUTNAME>"

logger.info("Comands to run:")
logger.info("  - %s", text2workspace_cmd)
logger.info("  - %s", combine_cmd)

filenames = []
for i in range(len(boundaries_pt)):
    for j in range(len(boundaries_eta)):
        ptbin = i+1
        etabin = j+1
        if ptbin >= 6 or etabin >= 4:
            continue
        for WP in WPs:
            filenames.append(inputdir+prefix+year+"_"+channel+"_PT"+str(ptbin)+"_ETA"+str(etabin)+"_"+WP+"_1_13TeV_0.txt")

current_dir = os.getcwd()
os.chdir(outputdir)
for f in filenames:
    logger.info("Reading file %s", f)
    
    # construct name of root file
    f_root = f.replace("txt", "root")
    # construct and run text2workspace command
    cmd_t2w = text2workspace_cmd.replace("<TXTFILE>",f).replace("<ROOTFILE>", f_root)
    os.system(cmd_t2w)
    # construct and run combine command
    outname = "."+f.replace(inputdir,"").replace(".txt","").replace(prefix,"")
    cmd = combine_cmd.replace("<NAME>", f_root).replace("<OUTNAME>", outname)
    os.system(cmd)
    
    logger.info("Done.")
    logger.info("----------------------------")
    
os.chdir(current_dir)
