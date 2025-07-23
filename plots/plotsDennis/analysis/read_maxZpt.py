
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--min', action='store', type=int, default=18915350)
argParser.add_argument('--max', action='store', type=int, default=18915361)
args = argParser.parse_args()

path_dummy = "/scratch/dennis.schwarz/batch_output/batch.<ID>.out"

for i in range(args.min, args.max+1):
    print "=============================================================================================================="
    file_path = path_dummy.replace("<ID>", str(i))
    printed_command = False
    with open(file_path, "r") as file:
        for line in file:
            if "python EFT_UL.py --reduceEFT --onlyData --threePoint --selection=" in line and not printed_command:
                printed_command = True
                print line
            if "tWZ - INFO -  Max Z pt =" in line:
                print line
            if "tWZ - INFO -  Events above 1000 =" in line:
                print line
