import os
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
argParser.add_argument('--light',            action='store_true', default=False)
argParser.add_argument('--NjetSplit',        action='store_true', default=False)
argParser.add_argument('--scaleCorrelation', action='store_true', default=False)
args = argParser.parse_args()


logger.info( "Create three point data cards using the Combine Harvester")

if args.year not in ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]:
    raise RuntimeError( "Year %s is not knwon", args.year)
logger.info( "Year = %s", args.year )

nRegions = 4 if args.NjetSplit else 3
logger.info( "Number of regions: %s", nRegions)

if args.light:
    logger.info( "Use combined wilson coefficients for 1st and 2nd generation" )

if args.scaleCorrelation:
    logger.info( "Correlate scales of Diboson" )
################################################################################
## Run Combine Harvester
cmd_harvester = "CreateCards_topEFT_threePoint "+args.year+" notlight notnjetSplit notscaleCorrelation"

dirname_suffix = ""
if args.light:
    cmd_harvester = cmd_harvester.replace("notlight", "light")
    dirname_suffix+="_light"
if args.NjetSplit:
    cmd_harvester = cmd_harvester.replace("notnjetSplit", "njetSplit")
    dirname_suffix+="_NjetSplit"
if args.scaleCorrelation:
    cmd_harvester = cmd_harvester.replace("notscaleCorrelation", "scaleCorrelation")
    dirname_suffix+="_scaleCorrelation"

this_dir = os.getcwd()
dataCard_dir = this_dir+"/DataCards_threePoint"+dirname_suffix+"/"+args.year+"/"

if not os.path.exists( dataCard_dir ): os.makedirs( dataCard_dir )

# if args.year == "ULRunII":
#     logger.info( "No need to run CombineHarvester" )
#     logger.info( "Check if all years are there.." )
#     for y in ["UL2016preVFP", "UL2016", "UL2017", "UL2018"]:
#         for r in range(nRegions):
#             region = r+1
#             filename = dataCard_dir.replace("ULRunII", y)+"topEFT_%s_%s_13TeV_%s.txt"%(y, str(region), y)
#             if not os.path.exists(filename):
#                 raise RuntimeError( "Could not find file for "+y+" and region "+region)
#
# else:
logger.info( "Will create data cards in directory %s", dataCard_dir )
os.chdir(dataCard_dir)
logger.info( "Running command: %s", cmd_harvester )
os.system(cmd_harvester)
os.chdir(this_dir)

################################################################################
## If RunII is selected, first combine all the years
# if args.year=="ULRunII":
#     logger.info( "Combine regions of all years" )
#     os.chdir(dataCard_dir)
#     for r in range(nRegions):
#         region = r+1
#         cardname16preVFP = dataCard_dir.replace("ULRunII", "UL2016preVFP")+"topEFT_UL2016preVFP_%s_13TeV_UL2016preVFP.txt"%(str(region))
#         cardname16 = dataCard_dir.replace("ULRunII", "UL2016")+"topEFT_UL2016_%s_13TeV_UL2016.txt"%(str(region))
#         cardname17 = dataCard_dir.replace("ULRunII", "UL2017")+"topEFT_UL2017_%s_13TeV_UL2017.txt"%(str(region))
#         cardname18 = dataCard_dir.replace("ULRunII", "UL2018")+"topEFT_UL2018_%s_13TeV_UL2018.txt"%(str(region))
#         cmd_runIIcombine = "combineCards.py "+cardname16preVFP+" "+cardname16+" "+cardname17+" "+cardname18
#         cmd_runIIcombine += "> topEFT_%s_%s_13TeV_%s.txt"%(args.year, str(region), args.year)
#         os.system(cmd_runIIcombine)
#     os.chdir(this_dir)

################################################################################
## Combine cards of the regions
logger.info( "Combine regions" )
os.chdir(dataCard_dir)
cmd_regions = "combineCards.py "
for r in range(nRegions):
    region = r+1
    cardname = "topEFT_%s_%s_13TeV_%s.txt"%(args.year,str(region),args.year)
    cmd_regions += cardname+" "
cmd_regions += "> topEFT_%s_combined_13TeV_%s.txt"%(args.year,args.year)
os.system(cmd_regions)
os.chdir(this_dir)

################################################################################
## Include MC stat uncertainty
logger.info( "Add line in order to include MC stat uncertainty" )
os.chdir(dataCard_dir)
lineToAdd = "* autoMCStats 0 1"
for r in range(nRegions)+["combined"]:
    region = r+1 if isinstance(r, int) else r
    cardname = "topEFT_%s_%s_13TeV_%s.txt"%(args.year,str(region),args.year)
    with open(cardname, 'a') as file:
        file.write('\n')
        file.write(lineToAdd)
os.chdir(this_dir)

################################################################################
## Convert to workspace
logger.info( "Convert cards to workspace using AnalyticAnomalousCoupling model" )
os.chdir(dataCard_dir)
for r in range(nRegions)+["combined"]:
    region = r+1 if isinstance(r, int) else r
    cmd_workspace = "text2workspace.py "
    cardname = "topEFT_%s_%s_13TeV_%s.txt"%(args.year,str(region),args.year)
    cmd_workspace += cardname+" "
    cmd_workspace += "-P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative "
    cmd_workspace += "-o "+cardname.replace(".txt", ".root")+" "
    cmd_workspace += "--X-allow-no-signal "
    if args.light:
        cmd_workspace += "--PO eftOperators=cHq1Re1122,cHq1Re33,cHq3Re1122,cHq3Re33"
    else:
        cmd_workspace += "--PO eftOperators=cHq1Re11,cHq1Re22,cHq1Re33,cHq3Re11,cHq3Re22,cHq3Re33"
    os.system(cmd_workspace)
os.chdir(this_dir)
logger.info( "Done." )
################################################################################
