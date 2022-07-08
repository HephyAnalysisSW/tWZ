import os

# filenames = os.listdir(dir+sample)
fileDir = "/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/singlelep/"
submitFileName = "/users/dennis.schwarz/CMSSW_10_6_28/src/tWZ/postProcessing/nanoPostProcessing_UL18_nanoAODv9_SingleLep.sh"
submitFile = open(submitFileName, 'r')
Lines = submitFile.readlines()
counter = 0
Nfiles = 0
missing = []
for line in Lines:
    words = line.split()
    i_sample = -1
    nJobs = 0
    for i,word in enumerate(words):
        if "--sample" in word:
            i_sample = i+1 # sample name comes right after "--sample"
        if "#SPLIT" in word:
            numberString = word.replace("#SPLIT", "")
            nJobs = int(numberString)
    sampleName = words[i_sample]
    Nfiles += nJobs
    if nJobs != 0:
        for i in range(nJobs):
            fileName = fileDir+sampleName+"/"+sampleName+"_"+str(i)+".root"
            if not os.path.exists(fileName):
                print fileName
                counter += 1
                missing.append( (sampleName, i, nJobs) ) 
            
print "----------------------------------------"
print "%i/%i files missing" %(counter, Nfiles)

f = open("missingFiles.sh", "w")
for (sampleName, i, nJobs) in missing:
    writeline = "python nanoPostProcessing_UL.py  --overwrite --forceProxy --skim singlelep --year UL2018 --processingEra tWZ_UL_nAODv9_v1 --sample "
    writeline += sampleName+" --nJobs="+str(nJobs)+" --job="+str(i)+"\n"   
    f.write(writeline)
f.close()
            
                
    
