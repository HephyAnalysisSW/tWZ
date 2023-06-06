import os

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--card',             action='store', type=str, default="")
args = argParser.parse_args()



cmd1 = "combineTool.py -M Impacts -d DATACARD.root -m 125 --doInitialFit --robustFit 1 --rMax 1 --rMin -1"
cmd2 = "combineTool.py -M Impacts -d DATACARD.root -m 125 --robustFit 1 --doFits --rMax 1 --rMin -1"
cmd3 = "combineTool.py -M Impacts -d DATACARD.root -m 125 -o impacts_datacard.json"
cmd4 = "plotImpacts.py -i impacts_datacard.json -o impacts_datacard"

this_dir = os.getcwd()
tmp_dir = this_dir+"/impacts"
if os.path.exists( tmp_dir ): os.system( "rm -r "+tmp_dir )


os.makedirs(tmp_dir)
os.chdir(tmp_dir)
os.system( cmd1.replace("DATACARD", "../"+args.card) )
os.system( cmd2.replace("DATACARD", "../"+args.card) )
os.system( cmd3.replace("DATACARD", "../"+args.card) )
os.system( cmd4 )
os.chdir(this_dir)
