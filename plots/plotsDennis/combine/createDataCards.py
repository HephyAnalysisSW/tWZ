import os
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
argParser.add_argument('--wc',               action='store', type=str, default="cHq1Re11")
args = argParser.parse_args()

nRegions = 3
nEFTpoints = 21

logger.info( "Create data cards using the Combine Harvester")


if args.year not in ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]:
    raise RuntimeError( "Year %s is not knwon", args.year)
logger.info( "Year = %s", args.year )

if args.wc not in ["cHq1Re11", "cHq1Re22", "cHq1Re33", "cHq3Re11", "cHq3Re22", "cHq3Re33"]:
    raise RuntimeError( "WC %s is not knwon", args.wc)
logger.info( "WC = %s", args.wc )

logger.info( "Number of regions: %s", nRegions)
logger.info( "Number of EFT points: %s", nEFTpoints)

################################################################################
## Run Combine Harvester
cmd_harvester = "CreateCards_topEFT "+args.year+" "+args.wc
this_dir = os.getcwd()
dataCard_dir = this_dir+"/DataCards/"+args.year+"/"
logger.info( "Will create data cards in directory %s", dataCard_dir )
os.chdir(dataCard_dir)
logger.info( "Running command: %s", cmd_harvester )
os.system(cmd_harvester)
os.chdir(this_dir)

################################################################################
## Combine cards of the regions
logger.info( "Combine regions" )
os.chdir(dataCard_dir)
for i in range(nEFTpoints):
    cmd_regions = "combineCards.py "
    for r in range(nRegions):
        region = r+1
        cardname = "topEFT_%s_%s_13TeV_%s.txt"%(args.wc, str(region), str(i))
        cmd_regions += cardname+" "
    cmd_regions += "> topEFT_%s_combined_13TeV_%s.txt"%(args.wc, str(i))
    os.system(cmd_regions)
os.chdir(this_dir)

################################################################################
## Convert to workspace
logger.info( "Convert cards to workspace" )
os.chdir(dataCard_dir)
nTotal = nEFTpoints*(nRegions+1)
nDone = 0
nTimesTenPercent = 1
for i in range(nEFTpoints):
    for r in range(nRegions)+["combined"]:
        region = r+1 if isinstance(r, int) else r
        cmd_workspace = "text2workspace.py "
        cardname = "topEFT_%s_%s_13TeV_%s.txt"%(args.wc, str(region), str(i))
        cmd_workspace += cardname+" -m "+str(i)+" -o "+cardname.replace(".txt", ".root")
        os.system(cmd_workspace)
        nDone += 1
        if nDone > nTimesTenPercent*nTotal/10:
            logger.info( "  %i percent done (%i/%i cards)", nTimesTenPercent*10, nDone, nTotal )
            nTimesTenPercent += 1
os.chdir(this_dir)


logger.info( "Done." )
