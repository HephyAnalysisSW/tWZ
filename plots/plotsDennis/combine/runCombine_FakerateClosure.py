import os
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

def getShapesCommand(dataCard_dir, infile, outname):
    cmd = "combine INROOTFILE -M FitDiagnostics --saveShapes --saveWithUnc --numToysForShape 2000   --freezeParameters r --setParameters r=1 --preFitValue 0 --plots -n OUTNAME"
    cmd = cmd.replace("INROOTFILE", dataCard_dir+infile)
    cmd = cmd.replace("OUTNAME", outname+"_SHAPES")
    return cmd

def getImpactCommands(dataCard_dir, infile, outname):
    base_cmd =  "combineTool.py -M Impacts -d INROOTFILE -m 125 --freezeParameters r --setParameters r=1"
    base_cmd = base_cmd.replace("INROOTFILE", dataCard_dir+infile)

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
argParser.add_argument('--impacts',          action='store_true', default=False)
argParser.add_argument('--postFit',          action='store_true', default=False)
args = argParser.parse_args()

nRegions = 2

logger.info( "Run combine")

if args.year not in ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]:
    raise RuntimeError( "Year %s is not knwon", args.year)
logger.info( "Year = %s", args.year )

logger.info( "Number of regions: %s", nRegions)

this_dir = os.getcwd()
dataCard_dir = this_dir+"/DataCards_FakerateClosure/"+args.year+"/"


os.chdir(dataCard_dir)
logger.info( "Run combine based on data cards in %s", dataCard_dir )
for r in range(nRegions)+["combined"]:
    region = r+1 if isinstance(r, int) else r
    infile = "FakerateClosure_%s_%s_13TeV_%s.root"%(args.year, str(region), args.year)
    outname = "."+infile.replace(".root", "")

    # Now put together combine command
    cmd_combine =  "combine -M MultiDimFit INROOTFILE -m 125 -n OUTNAME --freezeParameters r --setParameters r=1 --verbose -1 --saveToys --saveWorkspace"
    cmd_combine = cmd_combine.replace("INROOTFILE", infile)
    cmd_combine = cmd_combine.replace("OUTNAME", outname)

    logger.info( "-----------------------------------------------------------" )
    logger.info( "Run combine in region %s", region )
    logger.info( "Command = %s", cmd_combine )
    os.system(cmd_combine)
    if args.impacts:
        if region == "combined":
            logger.info( "Also create impact plot" )
            impact_dir = dataCard_dir+"Impacts__"+outname.replace(".", "")+"/"
            if not os.path.exists( impact_dir ): os.makedirs( impact_dir )
            os.chdir(impact_dir)
            cmds_impact = getImpactCommands(dataCard_dir, infile, outname)
            for cmd in cmds_impact:
                logger.info( "Command = %s", cmd )
                os.system(cmd)
            os.chdir(dataCard_dir)
    if args.postFit:
        logger.info( "Also run FitDiagnostics and save shapes" )
        cmd_shapes = getShapesCommand(dataCard_dir, infile, outname)
        logger.info( "Command = %s", cmd_shapes )
        os.system(cmd_shapes)


logger.info( "-----------------------------------------------------------" )
os.chdir(this_dir)
logger.info( "Done." )
