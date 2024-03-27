import os
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
args = argParser.parse_args()


logger.info( "Create three point data cards using the Combine Harvester")

if args.year not in ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]:
    raise RuntimeError( "Year %s is not knwon", args.year)
logger.info( "Year = %s", args.year )

nRegions = 2
logger.info( "Number of regions: %s", nRegions)

################################################################################
## Run Combine Harvester
cmd_harvester = "CreateCards_FakerateClosureMConly "+args.year


this_dir = os.getcwd()
dataCard_dir = this_dir+"/DataCards_FakerateClosureMConly/"+args.year+"/"

if not os.path.exists( dataCard_dir ): os.makedirs( dataCard_dir )

logger.info( "Will create data cards in directory %s", dataCard_dir )
os.chdir(dataCard_dir)
logger.info( "Running command: %s", cmd_harvester )
os.system(cmd_harvester)
os.chdir(this_dir)

################################################################################
## Combine cards of the regions
logger.info( "Combine regions" )
os.chdir(dataCard_dir)
cmd_regions = "combineCards.py "
for r in range(nRegions):
    region = r+1
    cardname = "FakerateClosureMConly_%s_%s_13TeV_%s.txt"%(args.year,str(region),args.year)
    cmd_regions += cardname+" "
cmd_regions += "> FakerateClosureMConly_%s_combined_13TeV_%s.txt"%(args.year,args.year)
os.system(cmd_regions)
os.chdir(this_dir)

################################################################################
## Include MC stat uncertainty
logger.info( "Add line in order to include MC stat uncertainty" )
os.chdir(dataCard_dir)
lineToAdd = "* autoMCStats 0 1"
for r in range(nRegions)+["combined"]:
    region = r+1 if isinstance(r, int) else r
    cardname = "FakerateClosureMConly_%s_%s_13TeV_%s.txt"%(args.year,str(region),args.year)
    with open(cardname, 'a') as file:
        file.write('\n')
        file.write(lineToAdd)
os.chdir(this_dir)

################################################################################
## Convert to workspace
logger.info( "Convert cards to workspace" )
os.chdir(dataCard_dir)
for r in range(nRegions)+["combined"]:
    region = r+1 if isinstance(r, int) else r
    cmd_workspace = "text2workspace.py --X-allow-no-signal "
    cardname = "FakerateClosureMConly_%s_%s_13TeV_%s.txt"%(args.year,str(region),args.year)
    cmd_workspace += cardname+" "
    cmd_workspace += "-o "+cardname.replace(".txt", ".root")+" "
    os.system(cmd_workspace)
os.chdir(this_dir)
logger.info( "Done." )
################################################################################
