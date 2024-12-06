import os
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

def getGoFCommand(infile, outname):
    cmd_data = "combine -M GoodnessOfFit INROOTFILE --algo=saturated --toysFrequentist --fixedSignalStrength 1 -n OUTNAME"
    cmd_data = cmd_data.replace("INROOTFILE", dataCard_dir+infile)
    cmd_data = cmd_data.replace("OUTNAME", outname+"_GOF_DATA")

    cmd_toys = "combine -M GoodnessOfFit INROOTFILE --algo=saturated --saveWorkspace --saveToys -t 500 --toysFrequentist --fixedSignalStrength 1 -n OUTNAME"
    cmd_toys = cmd_toys.replace("INROOTFILE", dataCard_dir+infile)
    cmd_toys = cmd_toys.replace("OUTNAME", outname+"_GOF")
    return cmd_data, cmd_toys


################################################################################
################################################################################
################################################################################

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
argParser.add_argument('--oneD',             action='store', type=str, default=None)
argParser.add_argument('--twoD',             action='store', type=str, default=None)
argParser.add_argument('--freeze',           action='store', type=str, default=None)
argParser.add_argument('--region',           action='store', type=str, default="all")
argParser.add_argument('--float',            action='store_true', default=False)
argParser.add_argument('--statOnly',         action='store_true', default=False)
argParser.add_argument('--impacts',          action='store_true', default=False)
argParser.add_argument('--postFit',          action='store_true', default=False)
argParser.add_argument('--light',            action='store_true', default=False)
argParser.add_argument('--minus',            action='store_true', default=False)
argParser.add_argument('--NjetSplit',        action='store_true', default=False)
argParser.add_argument('--scaleCorrelation', action='store_true', default=False)
argParser.add_argument('--signalInjectionLight',  action='store_true', default=False)
argParser.add_argument('--signalInjectionHeavy',  action='store_true', default=False)
argParser.add_argument('--signalInjectionMixed',  action='store_true', default=False)
argParser.add_argument('--signalInjectionWZjets',  action='store_true', default=False)
argParser.add_argument('--fluctuatePseudoData',  action='store_true', default=False)
argParser.add_argument('--unblind',          action='store_true', default=False)
argParser.add_argument('--noBB',          action='store_true', default=False)
argParser.add_argument('--minimizerStrategy',action='store_true', default=False)
argParser.add_argument('--ignoreCovWarning', action='store_true', default=False)
argParser.add_argument('--SM',               action='store_true', default=False)
args = argParser.parse_args()

nRegions = 4 if args.NjetSplit else 3
if args.region != "all":
    nRegions = 1


allWCnames = ["cHq1Re11", "cHq1Re22", "cHq1Re33", "cHq3Re11", "cHq3Re22", "cHq3Re33"]
if args.light:
    allWCnames = ["cHq1Re1122", "cHq1Re33", "cHq3Re1122", "cHq3Re33"]
    if args.minus:
        allWCnames = ["cHqMRe1122", "cHqMRe33", "cHq3MRe1122", "cHq3MRe33"]


WCsInFit = []
WCsFloat = []
WCsMargin = []

uncertaintyGroups = ["btag","jet","lepton","lumi","nonprompt","other_exp","rate_bkg","rate_sig","theory"]

logger.info( "Run combine")

if args.year not in ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]:
    raise RuntimeError( "Year %s is not knwon", args.year)
logger.info( "Year = %s", args.year )

if not args.SM:
    if args.oneD is not None and args.twoD is not None:
        raise RuntimeError( "Cannot set --oneD and --twoD, decide for one of the two")

    if args.oneD is None and args.twoD is None:
        raise RuntimeError( "Please set either --oneD or --twoD")

    if args.oneD is not None:
        if args.oneD not in allWCnames:
            raise RuntimeError( "Wilson coeffitient %s not known", args.oneD )
        WCsInFit.append(args.oneD)
        logger.info( "Fit WC = %s", args.oneD )

    if args.twoD is not None:
        if "-" not in args.twoD:
            raise RuntimeError( "Wilson coeffitients given in wrong format, expected --twoD=WC1-WC2" )
        wc1 = args.twoD.split("-")[0]
        wc2 = args.twoD.split("-")[1]
        WCsInFit.append(wc1)
        WCsInFit.append(wc2)
        logger.info( "Fit WCs (2D) = %s-%s", wc1, wc2 )

freezeGroups = []
if args.freeze is not None:
    if args.statOnly:
        raise RuntimeError( "Cannot run statOnly AND freeze nuisance groups" )
    for group in args.freeze.split("-"):
        if group not in uncertaintyGroups:
            raise RuntimeError( "Uncertainty group %s not known. You also might have used a wrong format: --freeze=btag-jec", group )
        else:
            freezeGroups.append(group)



if args.float:
    logger.info( "Float, let all other WCs float")
    for wc in allWCnames:
        if wc not in WCsInFit:
            WCsFloat.append(wc)
else:
    logger.info( "Marginalize, set all other WCs to 0")
    for wc in allWCnames:
        if wc not in WCsInFit:
            WCsMargin.append(wc)


logger.info( "Wilson coeffitients as POI: %s", WCsInFit)
logger.info( "Wilson coeffitients marginalized: %s", WCsMargin)
logger.info( "Wilson coeffitients floating in fit: %s", WCsFloat)
logger.info( "Deactivate these uncertainty groups: %s", freezeGroups)

logger.info( "Number of regions: %s", nRegions)


dirname_suffix = ""
if args.light:               dirname_suffix+="_light"
if args.minus:               dirname_suffix+="_minus"
if args.NjetSplit:           dirname_suffix+="_NjetSplit"
if args.scaleCorrelation:    dirname_suffix+="_scaleCorrelation"
if args.signalInjectionLight:     dirname_suffix+="_signalInjectionLight"
if args.signalInjectionHeavy:     dirname_suffix+="_signalInjectionHeavy"
if args.signalInjectionMixed:     dirname_suffix+="_signalInjectionMixed"
if args.signalInjectionWZjets:    dirname_suffix+="_signalInjectionWZjets"
if args.fluctuatePseudoData:      dirname_suffix+="_fluctuatePseudoData"
if args.unblind:                  dirname_suffix+="_UNBLINDED"
if args.noBB:                  dirname_suffix+="_noBB"
if args.SM:                  dirname_suffix+="_SM"

this_dir = os.getcwd()
dataCard_dir = this_dir+"/DataCards_threePoint"+dirname_suffix+"/"+args.year+"/"

os.chdir(dataCard_dir)
logger.info( "Run combine based on data cards in %s", dataCard_dir )
allRegions = []
if args.region == "all":
    allRegions = range(1, nRegions+1)+["combined"]
else:
    allRegions = [args.region]
for region in allRegions:
    infile = "topEFT_%s_%s_13TeV_%s.root"%(args.year, region, args.year)


    outname = "."+infile.replace(".root", "")
    if not args.SM:
        outname += "_2D-"+args.twoD if args.twoD is not None else "_1D-"+args.oneD
        outname += "_float" if args.float else "_margin"
    if args.freeze is not None:
        outname += "_freeze-"+args.freeze
    if args.statOnly:
        outname += "_statOnly"

    cmd_data, cmd_toys = getGoFCommand(infile, outname)
    logger.info( "Command (data) = %s", cmd_data )
    logger.info( "Command (toys) = %s", cmd_toys )
    # os.system(cmd_data)
    # os.system(cmd_toys)

logger.info( "-----------------------------------------------------------" )
os.chdir(this_dir)
logger.info( "Done." )
