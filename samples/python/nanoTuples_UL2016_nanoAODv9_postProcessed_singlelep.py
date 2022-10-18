import copy, os, sys
from RootTools.core.Sample import Sample
import ROOT

# Logging
import logging
logger = logging.getLogger(__name__)

from tWZ.samples.color import color

# Data directory
try:
    directory_ = sys.modules['__main__'].directory_
except:
    import tWZ.samples.UL_nanoAODv9_locations as locations
    directory_ = locations.mc_singlelep_UL2016

logger.info("Loading MC samples from directory %s", directory_)

def make_dirs( dirs ):
    return [ os.path.join( directory_, dir_ ) for dir_ in dirs ]

dirs = {}

dirs['ZZ']               = ["ZZ"]
ZZ = Sample.fromDirectory(name="ZZ", treeName="Events", isData=False, color=color.ZZ, texName="ZZ", directory=make_dirs( dirs['ZZ']))

dirs['WW']               = ["WW"]
# dirs['VVTo2L2Nu']        = ["VVTo2L2Nu"] # NOT YET THERE IN UL
WW = Sample.fromDirectory(name="WW", treeName="Events", isData=False, color=color.WW, texName="WW", directory=make_dirs( dirs['WW']))

dirs['WZTo3LNu']               = ["WZTo3LNu"]
WZTo3LNu = Sample.fromDirectory(name="WZTo3LNu", treeName="Events", isData=False, color=color.WZ, texName="WZ", directory=make_dirs( dirs['WZTo3LNu']))


# TT
dirs['TTbar'] = ['TTLep_pow_CP5', 'TTSingleLep_pow_CP5']
TTbar = Sample.fromDirectory(name="TTbar",      treeName="Events", isData=False, color=color.TTJets, texName="t#bar{t}", directory=make_dirs( dirs['TTbar']))

# DY
dirs['DY_LO']           = [ 'DYJetsToLL_M10to50_LO', 'DYJetsToLL_M50']
DY  = Sample.fromDirectory(name="DY", treeName="Events", isData=False, color=color.DY, texName="DY", directory=make_dirs(dirs['DY_LO']))

# W+jets
dirs['WJetsToLNu']    = ['WJetsToLNu'] 
WJetsToLNu = Sample.fromDirectory(name="WJetsToLNu", treeName="Events", isData=False, color=color.WJetsToLNu, texName="W+jets", directory=make_dirs( dirs['WJetsToLNu']))

# QCD 
dirs['QCD_MuEnriched'] =  [
    'QCD_MuEnriched_15to20',
    'QCD_MuEnriched_20to30',
    'QCD_MuEnriched_30to50',
    'QCD_MuEnriched_50to80',
    'QCD_MuEnriched_80to120',
    'QCD_MuEnriched_120to170',
    'QCD_MuEnriched_170to300',
    'QCD_MuEnriched_300to470',
    'QCD_MuEnriched_470to600',
    'QCD_MuEnriched_600to800',
    'QCD_MuEnriched_800to1000',
    'QCD_MuEnriched_1000toInf',
]

dirs['QCD_EMEnriched'] =  [
    'QCD_EMEnriched_15to20',
    'QCD_EMEnriched_20to30',
    'QCD_EMEnriched_30to50',
    'QCD_EMEnriched_50to80',
    'QCD_EMEnriched_80to120',
    'QCD_EMEnriched_120to170',
    'QCD_EMEnriched_170to300',
    'QCD_EMEnriched_300toInf',
]

dirs['QCD_bcToE'] =  [
    'QCD_bcToE_15to20',
    'QCD_bcToE_20to30',
    'QCD_bcToE_30to80',
    'QCD_bcToE_80to170',
    'QCD_bcToE_170to250',
    'QCD_bcToE_250toInf',
]

dirs['QCD'] = dirs['QCD_MuEnriched'] + dirs['QCD_EMEnriched'] + dirs['QCD_bcToE']

QCD_MuEnriched = Sample.fromDirectory(name="QCD_MuEnriched", treeName="Events", isData=False, color=color.QCD+10, texName="QCD MuEnriched", directory=make_dirs( dirs['QCD_MuEnriched']))
QCD_EMEnriched = Sample.fromDirectory(name="QCD_EMEnriched", treeName="Events", isData=False, color=color.QCD+5, texName="QCD EmEnriched", directory=make_dirs( dirs['QCD_EMEnriched']))
QCD_bcToE      = Sample.fromDirectory(name="QCD_bcToE", treeName="Events", isData=False, color=color.QCD-5, texName="QCD bcToE", directory=make_dirs( dirs['QCD_bcToE']))
QCD            = Sample.fromDirectory(name="QCD", treeName="Events", isData=False, color=color.QCD, texName="QCD multijet", directory=make_dirs( dirs['QCD']))
