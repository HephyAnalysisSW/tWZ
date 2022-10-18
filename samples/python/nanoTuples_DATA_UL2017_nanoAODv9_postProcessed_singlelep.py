import copy, os, sys
from RootTools.core.Sample import Sample 
import ROOT

# Logging
import logging
logger = logging.getLogger(__name__)

# Data directory
try:
    directory_ = sys.modules['__main__'].directory_
except:
    import tWZ.samples.UL_nanoAODv9_locations as locations
    directory_ = locations.data_singlelep_UL2017

logger.info("Loading data samples from directory %s", directory_)

def getSample(pd, runName, lumi):
    runs = ["Run2017B","Run2017C","Run2017D","Run2017E","Run2017F"]
    dirlist = [directory_+"/"+pd+"_"+run for run in runs]
    sample      = Sample.fromDirectory(name=(pd + '_' + runName), treeName="Events", texName=(pd + ' (' + runName + ')'), directory=dirlist)
    sample.lumi = lumi
    return sample

allSamples = []

SingleElectron_Run2017          = getSample('SingleElectron',   'Run2017',       (41.5)*1000)
SingleMuon_Run2017              = getSample('SingleMuon',       'Run2017',       (41.5)*1000)
allSamples += [SingleMuon_Run2017, SingleElectron_Run2017]

Run2017 = Sample.combine("Run2017", [SingleMuon_Run2017, SingleMuon_Run2017], texName = "Run2017")
Run2017.lumi  = (41.5)*1000

allSamples += [Run2017]

for s in allSamples:
  s.color   = ROOT.kBlack
  s.isData  = True
