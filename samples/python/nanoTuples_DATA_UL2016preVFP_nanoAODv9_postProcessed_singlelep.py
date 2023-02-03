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
    directory_ = locations.data_singlelep_UL2016_preVFP

logger.info("Loading data samples from directory %s", directory_)

def getSample(pd, runName, lumi):
    runs = ["Run2016Bver1_preVFP", "Run2016Bver2_preVFP", "Run2016C_preVFP", "Run2016D_preVFP", "Run2016E_preVFP", "Run2016F_preVFP"]
    dirlist = [directory_+"/"+pd+"_"+run for run in runs]
    sample      = Sample.fromDirectory(name=(pd + '_' + runName), treeName="Events", texName=(pd + ' (' + runName + ')'), directory=dirlist)
    sample.lumi = lumi
    return sample

allSamples = []

SingleElectron_Run2016_preVFP            = getSample('SingleElectron',   'Run2016_preVFP',           (19.5)*1000)
SingleMuon_Run2016_preVFP                = getSample('SingleMuon',       'Run2016_preVFP',           (19.5)*1000)
allSamples += [SingleElectron_Run2016_preVFP, SingleMuon_Run2016_preVFP]

Run2016_preVFP = Sample.combine("Run2016_preVFP", [SingleElectron_Run2016_preVFP, SingleMuon_Run2016_preVFP], texName = "Run2016_preVFP")
Run2016_preVFP.lumi = (19.5)*1000
allSamples.append(Run2016_preVFP)

for s in allSamples:
  s.color   = ROOT.kBlack
  s.isData  = True
