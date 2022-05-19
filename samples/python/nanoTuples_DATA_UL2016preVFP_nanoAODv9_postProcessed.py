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
    directory_ = locations.data_UL2016_preVFP

logger.info("Loading data samples from directory %s", directory_)


def getSample(pd, runName, lumi):
    runs = ["Run2016Bver1_preVFP", "Run2016Bver2_preVFP", "Run2016C_preVFP", "Run2016D_preVFP", "Run2016E_preVFP", "Run2016F_preVFP"]
    dirlist = [directory_+"/"+pd+"_"+run for run in runs]
    sample      = Sample.fromDirectory(name=(pd + '_' + runName), treeName="Events", texName=(pd + ' (' + runName + ')'), directory=dirlist)
    sample.lumi = lumi
    return sample

allSamples = []

DoubleEG_Run2016                  = getSample('DoubleEG',         'Run2016',           (19.5)*1000)
DoubleMuon_Run2016                = getSample('DoubleMuon',       'Run2016',           (19.5)*1000)
SingleElectron_Run2016            = getSample('SingleElectron',   'Run2016',           (19.5)*1000)
SingleMuon_Run2016                = getSample('SingleMuon',       'Run2016',           (19.5)*1000)
MuonEG_Run2016                    = getSample('MuonEG',           'Run2016',           (19.5)*1000)
allSamples += [MuonEG_Run2016, DoubleEG_Run2016, DoubleMuon_Run2016, SingleElectron_Run2016, SingleMuon_Run2016]

Run2016_preVFP = Sample.combine("Run2016_preVFP", [MuonEG_Run2016, DoubleEG_Run2016, DoubleMuon_Run2016, SingleElectron_Run2016, SingleMuon_Run2016], texName = "Run2016")
Run2016_preVFP.lumi = (19.5)*1000
allSamples.append(Run2016_preVFP)

for s in allSamples:
  s.color   = ROOT.kBlack
  s.isData  = True
