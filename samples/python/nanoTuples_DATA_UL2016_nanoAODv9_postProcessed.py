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
    directory_ = locations.data_UL2016

logger.info("Loading data samples from directory %s", directory_)

def getSample(pd, runName, lumi):
    runs = ["Run2016F", "Run2016G", "Run2016H"]
    dirlist = [directory_+"/"+pd+"_"+run for run in runs]
    sample      = Sample.fromDirectory(name=(pd + '_' + runName), treeName="Events", texName=(pd + ' (' + runName + ')'), directory=dirlist)
    sample.lumi = lumi
    return sample


allSamples = []

DoubleEG_Run2016                  = getSample('DoubleEG',         'Run2016',           (16.5)*1000)
DoubleMuon_Run2016                = getSample('DoubleMuon',       'Run2016',           (16.5)*1000)
SingleElectron_Run2016            = getSample('SingleElectron',   'Run2016',           (16.5)*1000)
SingleMuon_Run2016                = getSample('SingleMuon',       'Run2016',           (16.5)*1000)
MuonEG_Run2016                    = getSample('MuonEG',           'Run2016',           (16.5)*1000)
allSamples += [MuonEG_Run2016, DoubleEG_Run2016, DoubleMuon_Run2016, SingleElectron_Run2016, SingleMuon_Run2016]

Run2016 = Sample.combine("Run2016", [MuonEG_Run2016, DoubleEG_Run2016, DoubleMuon_Run2016, SingleElectron_Run2016, SingleMuon_Run2016], texName = "Run2016")
Run2016.lumi = (16.5)*1000
allSamples.append(Run2016)

for s in allSamples:
  s.color   = ROOT.kBlack
  s.isData  = True
