import os

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--year',      action='store', default='UL2018')
argParser.add_argument('--data',      action='store_true', default=False)
args = argParser.parse_args()

shortyear = args.year.replace("20", "")

if args.year == "UL2016_preVFP" or args.year == "UL2016preVFP":
    shortyear = "UL16preVFP"
    args.year = "UL2016_preVFP"

version = "tWZ_UL_nAODv9_v3"

fileDir = "/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/"+version+"/"+args.year+"/trilep/"
submitFileName = "/users/dennis.schwarz/CMSSW_10_6_28/src/tWZ/postProcessing/nanoPostProcessing_"+shortyear+"_nanoAODv9.sh"
if args.data:
    submitFileName = "/users/dennis.schwarz/CMSSW_10_6_28/src/tWZ/postProcessing/nanoPostProcessing_"+shortyear+"_DATA_nanoAODv9.sh"


submitFile = open(submitFileName, 'r')
Lines = submitFile.readlines()
counter = 0
Nfiles = 0
missing = []
for line in Lines:
    words = line.split()
    i_sample = -1
    nJobs = 1
    for i, word in enumerate(words):
        if "--sample" in word:
            i_sample = i+1 # sample name comes right after "--sample"
        if "#SPLIT" in word:
            numberString = word.replace("#SPLIT", "")
            nJobs = int(numberString)
    if i_sample == -1:
        continue
    sampleName = words[i_sample]
    Nfiles += nJobs
    if nJobs != 0:
        for i in range(nJobs):
            fileName = fileDir+"/"+sampleName+"/"+sampleName+"_"+str(i)+".root"
            if not os.path.exists(fileName):
                print fileName
                counter += 1
                missing.append( (sampleName, i, nJobs) )

print "----------------------------------------"
print "%i/%i files missing" %(counter, Nfiles)

missingfilesname = "missingFiles_trilep_"+shortyear+".sh"
if args.data:
    missingfilesname = "missingFiles_trilep_DATA_"+shortyear+".sh"
f = open(missingfilesname, "w")
for (sampleName, i, nJobs) in missing:
    writeline = "python nanoPostProcessing_UL.py  --overwrite --forceProxy --skim trilep --year "+args.year+" --processingEra "+version+" --sample "+sampleName
    if nJobs != 1:
        writeline += " --nJobs="+str(nJobs)+" --job="+str(i)+"\n"
    f.write(writeline)
f.close()
print "Created new submit file", missingfilesname
