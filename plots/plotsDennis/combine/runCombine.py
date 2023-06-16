import os
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
argParser.add_argument('--wc',               action='store', type=str, default="cHq1Re11")
argParser.add_argument('--mode',             action='store', type=str, default="default")
args = argParser.parse_args()

nRegions = 3
nEFTpoints = 21

logger.info( "Run combine")


if args.year not in ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]:
    raise RuntimeError( "Year %s is not knwon", args.year)
logger.info( "Year = %s", args.year )

if args.wc not in ["cHq1Re11", "cHq1Re22", "cHq1Re33", "cHq3Re11", "cHq3Re22", "cHq3Re33"]:
    raise RuntimeError( "WC %s is not knwon", args.wc)
logger.info( "WC = %s", args.wc )

if args.mode not in ["default", "statOnly", "noScales", "noRates", "noBtag", "noJEC", "noLepton", "noLumi", "noPS", "noFakerate"]:
    raise RuntimeError( "Mode %s is not known ", args.mode)
logger.info( "Mode = %s", args.mode )

logger.info( "Number of regions: %s", nRegions)
logger.info( "Number of EFT points: %s", nEFTpoints)


this_dir = os.getcwd()
dataCard_dir = this_dir+"/DataCards/"+args.year+"/"
if "default" not in args.mode: dataCard_dir = this_dir+"/DataCards_"+args.mode+"/"+args.year+"/"

os.chdir(dataCard_dir)
nTotal = nEFTpoints*(nRegions+1)
nDone = 0
nTimesTenPercent = 1
logger.info( "Run combine based on data cards in %s", dataCard_dir )
for i in range(nEFTpoints):
    for r in range(nRegions)+["combined"]:
        region = r+1 if isinstance(r, int) else r
        f_root = "topEFT_%s_%s_13TeV_%s.root "%(args.wc, str(region), str(i))
        cmd_combine =  "combine -M MultiDimFit "
        cmd_combine += f_root
        cmd_combine += " -n "
        cmd_combine += ".part3E_%s_%s_%s "%(str(i), str(region), args.wc)
        cmd_combine += "--saveNLL --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --expectSignal=1 --cminDefaultMinimizerStrategy=0 --cminDefaultMinimizerTolerance=0.0001 --freezeParameters r  --setParameterRanges r=-10,10"
        logger.info( "Run combine in region %s at EFT point %s", region, i )
        logger.info( "Command = %s", cmd_combine )
        os.system(cmd_combine)
        if i == 11:
            cmd_combine2 =  "combine -M FitDiagnostics "
            cmd_combine2 += f_root
            cmd_combine2 += " --saveShapes --saveWithUnc --numToysForShape 2000  --preFitValue 1 --setParameterRanges r=0.99,1.01 -n "
            cmd_combine2 += f_root.replace(".root", "")
            logger.info( "Run full diagnostics" )
            logger.info( "Command = %s", cmd_combine2 )
            os.system(cmd_combine2)
        nDone += 1
        if nDone > nTimesTenPercent*nTotal/10:
            logger.info( "  %i percent done (%i/%i cards)", nTimesTenPercent*10, nDone, nTotal )
            nTimesTenPercent += 1

os.chdir(this_dir)
logger.info( "Done." )

# combine_cmd = "combine <NAME> -M FitDiagnostics --saveShapes --saveWithUnc --numToysForShape 2000  --preFitValue 1 --setParameterRanges r=0.01,10 -n <OUTNAME>"
