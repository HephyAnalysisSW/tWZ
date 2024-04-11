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
    directory_triggerSF_ = sys.modules['__main__'].directory_triggerSF_
    directory_singlelep_ = sys.modules['__main__'].directory_singlelep_
except:
    import tWZ.samples.UL_nanoAODv9_locations as locations
    directory_ = locations.mc_UL2017
    directory_triggerSF_ = locations.mc_triggerSF_UL2017
    directory_singlelep_ = locations.mc_singlelep_UL2017

logger.info("Loading MC samples from directory %s", directory_)

def make_dirs( dirs ):
    return [ os.path.join( directory_, dir_ ) for dir_ in dirs ]

def make_dirs_singlelep( dirs ):
    return [ os.path.join( directory_singlelep_, dir_ ) for dir_ in dirs ]

def make_dirs_triggerSF( dirs ):
    return [ os.path.join( directory_triggerSF_, dir_ ) for dir_ in dirs ]

dirs = {}



dirs['ZZ_powheg']               = ["ZZ_powheg"]
ZZ_powheg = Sample.fromDirectory(name="ZZ_powheg", treeName="Events", isData=False, color=color.ZZ, texName="ZZ", directory=make_dirs_triggerSF( dirs['ZZ_powheg']))


dirs['WZTo3LNu']               = ["WZTo3LNu"]
WZTo3LNu = Sample.fromDirectory(name="WZTo3LNu", treeName="Events", isData=False, color=color.WZ, texName="WZ", directory=make_dirs_triggerSF( dirs['WZTo3LNu']))

dirs['WZTo3LNu_powheg']               = ["WZTo3LNu_powheg"]
WZTo3LNu_powheg = Sample.fromDirectory(name="WZTo3LNu_powheg", treeName="Events", isData=False, color=color.WZ, texName="WZ", directory=make_dirs_triggerSF( dirs['WZTo3LNu_powheg']))


# TTZ
dirs['TTZToLLNuNu']     = ['TTZToLLNuNu', 'TTZToLLNuNu_m1to10']
dirs['TTZToQQ']         = ['TTZToQQ']
dirs['TTZ']             = ['TTZToLLNuNu', 'TTZToLLNuNu_m1to10', "TTZToQQ"]
TTZToLLNuNu = Sample.fromDirectory(name="ToLLNuNu", treeName="Events", isData=False, color=color.TTZ, texName="t#bar{t}Z #rightarrow ll#nu#nu", directory=make_dirs_triggerSF( dirs['TTZToLLNuNu']))
TTZ         = Sample.fromDirectory(name="TTZ",      treeName="Events", isData=False, color=color.TTZ, texName="t#bar{t}Z", directory=make_dirs_triggerSF( dirs['TTZ']))
