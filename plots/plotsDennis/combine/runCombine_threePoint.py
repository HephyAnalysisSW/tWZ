import os
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

def getShapesCommand(dataCard_dir, infile, poi_list, freeze_list, set_list, range_list, outname, additionalOptions):
    cmd = "combine INROOTFILE -M FitDiagnostics --saveShapes --saveWithUnc --numToysForShape 2000   --redefineSignalPOIs POILIST --freezeParameters FREEZELIST --setParameters SETLIST --setParameterRanges RANGELIST --preFitValue 0 --plots -n OUTNAME"
    cmd += additionalOptions
    if "cminDefaultMinimizerStrategy" in additionalOptions:
        outname += "_minimizerStrategy"
    if "ignoreCovWarning" in additionalOptions:
        outname += "_ignoreCovWarning"
    cmd = cmd.replace("INROOTFILE", dataCard_dir+infile)
    cmd = cmd.replace("POILIST", poi_list)
    cmd = cmd.replace("FREEZELIST", freeze_list)
    cmd = cmd.replace("SETLIST", set_list)
    cmd = cmd.replace("RANGELIST", range_list)
    cmd = cmd.replace("OUTNAME", outname+"_SHAPES")
    return cmd

def getImpactCommands(dataCard_dir, infile, poi_list, freeze_list, set_list, range_list, outname, doSignalInjection):
    base_cmd =  "combineTool.py -M Impacts -d INROOTFILE -m 125 -t -1 --redefineSignalPOIs POILIST --freezeParameters FREEZELIST --setParameters SETLIST --setParameterRanges RANGELIST"
    if doSignalInjection:
        base_cmd = base_cmd.replace("-t -1", "")
    base_cmd = base_cmd.replace("INROOTFILE", dataCard_dir+infile)
    base_cmd = base_cmd.replace("POILIST", poi_list)
    base_cmd = base_cmd.replace("FREEZELIST", freeze_list)
    base_cmd = base_cmd.replace("SETLIST", set_list)
    base_cmd = base_cmd.replace("RANGELIST", range_list)

    json_name = outname.replace(".", "")+".json"
    pdf_name = outname.replace(".", "")

    cmds = []
    cmds.append(base_cmd+" --doInitialFit --robustFit 1")
    cmds.append(base_cmd+" --robustFit 1 --doFits")
    cmds.append(base_cmd+" -o "+json_name)
    cmds.append("plotImpacts.py -i "+json_name+" -o "+pdf_name)
    return cmds

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
argParser.add_argument('--NjetSplit',        action='store_true', default=False)
argParser.add_argument('--scaleCorrelation', action='store_true', default=False)
argParser.add_argument('--signalInjectionLight',  action='store_true', default=False)
argParser.add_argument('--signalInjectionHeavy',  action='store_true', default=False)
argParser.add_argument('--signalInjectionMixed',  action='store_true', default=False)
argParser.add_argument('--signalInjectionWZjets',  action='store_true', default=False)
argParser.add_argument('--minimizerStrategy',action='store_true', default=False)
argParser.add_argument('--ignoreCovWarning', action='store_true', default=False)
args = argParser.parse_args()

nRegions = 4 if args.NjetSplit else 3
if args.region != "all":
    nRegions = 1


allWCnames = ["cHq1Re11", "cHq1Re22", "cHq1Re33", "cHq3Re11", "cHq3Re22", "cHq3Re33"]
if args.light:
    allWCnames = ["cHq1Re1122", "cHq1Re33", "cHq3Re1122", "cHq3Re33"]

WCsInFit = []
WCsFloat = []
WCsMargin = []

uncertaintyGroups = ["btag","jet","lepton","lumi","nonprompt","other_exp","rate_bkg","rate_sig","theory"]

logger.info( "Run combine")

if args.year not in ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]:
    raise RuntimeError( "Year %s is not knwon", args.year)
logger.info( "Year = %s", args.year )

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
if args.NjetSplit:           dirname_suffix+="_NjetSplit"
if args.scaleCorrelation:    dirname_suffix+="_scaleCorrelation"
if args.signalInjectionLight:     dirname_suffix+="_signalInjectionLight"
if args.signalInjectionHeavy:     dirname_suffix+="_signalInjectionHeavy"
if args.signalInjectionMixed:     dirname_suffix+="_signalInjectionMixed"
if args.signalInjectionWZjets:     dirname_suffix+="_signalInjectionWZjets"

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
    outname += "_2D-"+args.twoD if args.twoD is not None else "_1D-"+args.oneD
    outname += "_float" if args.float else "_margin"
    if args.freeze is not None:
        outname += "_freeze-"+args.freeze
    if args.statOnly:
        outname += "_statOnly"
    # create a list of POIs
    poi_list = ""
    for i, wcname in enumerate(WCsInFit):
        if i > 0:
            poi_list += ","
        poi_list += "k_"+wcname
    # create a list of parameters to freeze
    freeze_list = "r"
    for i, wcname in enumerate(WCsMargin):
        freeze_list += ",k_"+wcname
    if args.statOnly:
        freeze_list += ",allConstrainedNuisances"
    # create a list and set r=1 and marginalized WCs to 0
    set_list = "r=1"
    for i, wcname in enumerate(WCsMargin):
        set_list += ",k_"+wcname+"=0"
    # create a list of parameter ranges
    range_list = ""
    for i, wcname in enumerate(WCsInFit):
        if wcname in ["cHq3Re11", "cHq3Re1122"]:
            range = "-0.5,0.5"
        else:
            range = "-7,7"
            # range = "-3,3" if args.twoD is not None else "-5,5"
        if i > 0:
            range_list += ":"
        range_list += "k_"+wcname+"="+range
    # Number of scaned EFT point
    Npoints = "10201" if args.twoD is not None else "200"
    # Npoints = "40401" if args.twoD is not None else "200"
    # Now put together combine command
    cmd_combine =  "combine -M MultiDimFit INROOTFILE --algo=grid --points NPOINTS -m 125 -t -1 -n OUTNAME --redefineSignalPOIs POILIST --freezeParameters FREEZELIST --setParameters SETLIST --setParameterRanges RANGELIST --verbose -1 --saveToys --saveWorkspace"
    if args.signalInjectionLight or args.signalInjectionHeavy or args.signalInjectionMixed or args.signalInjectionWZjets:
        cmd_combine = cmd_combine.replace("-t -1", "")
    cmd_combine = cmd_combine.replace("INROOTFILE", infile)
    cmd_combine = cmd_combine.replace("NPOINTS", Npoints)
    cmd_combine = cmd_combine.replace("OUTNAME", outname)
    cmd_combine = cmd_combine.replace("POILIST", poi_list)
    cmd_combine = cmd_combine.replace("FREEZELIST", freeze_list)
    cmd_combine = cmd_combine.replace("SETLIST", set_list)
    cmd_combine = cmd_combine.replace("RANGELIST", range_list)
    if args.freeze is not None:
        cmd_combine += " --freezeNuisanceGroups="
        for i, group in enumerate(freezeGroups):
            if i > 0:
                cmd_combine += ","
            cmd_combine += group
    logger.info( "-----------------------------------------------------------" )
    logger.info( "Run combine in region %s", region )
    logger.info( "Command = %s", cmd_combine )
    os.system(cmd_combine)
    if args.impacts:
        logger.info( "Also create impact plot" )
        impact_dir = dataCard_dir+"Impacts__"+outname.replace(".", "")+"/"
        if not os.path.exists( impact_dir ): os.makedirs( impact_dir )
        os.chdir(impact_dir)
        doSignalInjection = False
        if args.signalInjectionLight or args.signalInjectionHeavy or args.signalInjectionMixed or args.signalInjectionWZjets:
            doSignalInjection = True
        cmds_impact = getImpactCommands(dataCard_dir, infile, poi_list, freeze_list, set_list, range_list, outname, doSignalInjection)
        for cmd in cmds_impact:
            logger.info( "Command = %s", cmd )
            os.system(cmd)
        os.chdir(dataCard_dir)
    if args.postFit:
        logger.info( "Also run FitDiagnostics and save shapes" )
        additionalOptions = ""
        if args.minimizerStrategy:
            additionalOptions += " --cminDefaultMinimizerStrategy 0 "
        if args.ignoreCovWarning:
            additionalOptions += " --ignoreCovWarning "

        cmd_shapes = getShapesCommand(dataCard_dir, infile, poi_list, freeze_list, set_list, range_list, outname, additionalOptions)
        logger.info( "Command = %s", cmd_shapes )
        os.system(cmd_shapes)


logger.info( "-----------------------------------------------------------" )
os.chdir(this_dir)
logger.info( "Done." )
