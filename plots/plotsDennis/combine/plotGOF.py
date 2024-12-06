import ROOT
import os
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

################################################################################
################################################################################
################################################################################

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
argParser.add_argument('--region',           action='store', type=str, default="all")
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

logger.info( "Get GOF file from dir %s", dataCard_dir )

allRegions = []
if args.region == "all":
    allRegions = range(1, nRegions+1)+["combined"]
else:
    allRegions = [args.region]

hist = ROOT.TH1F("test_stat", "", 100, 0, 100)


# Optionally, draw the histogram
hist.Draw()
for region in allRegions:
    # First get test statistic from toys
    infile = "higgsCombine.topEFT_%s_%s_13TeV_%s_GOF.GoodnessOfFit.mH120.123456.root"%(args.year, region, args.year)
    file = ROOT.TFile(infile)
    tree = file.Get("limit")
    for entry in tree:
        limit = entry.limit
        hist.Fill(limit)
    # now get data GOF
    infile_data = infile.replace("GOF", "GOF_DATA").replace(".123456.", ".")
    file_data = ROOT.TFile(infile_data)
    tree_data = file_data.Get("limit")
    for entry in tree:
        value = entry.limit

    bin = hist.FindBin(value)
    lastbin = hist.GetSize()-2
    pValue = hist.Integral(bin, lastbin)/hist.Integral(1, lastbin)
    print pValue

logger.info( "-----------------------------------------------------------" )
os.chdir(this_dir)
logger.info( "Done." )
