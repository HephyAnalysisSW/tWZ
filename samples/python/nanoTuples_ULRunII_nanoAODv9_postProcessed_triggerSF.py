from RootTools.core.standard import *

from tWZ.samples.nanoTuples_DATA_UL2016_nanoAODv9_postProcessed_triggerSF import Run2016
from tWZ.samples.nanoTuples_DATA_UL2016preVFP_nanoAODv9_postProcessed_triggerSF import Run2016_preVFP
from tWZ.samples.nanoTuples_DATA_UL2017_nanoAODv9_postProcessed_triggerSF import Run2017
from tWZ.samples.nanoTuples_DATA_UL2018_nanoAODv9_postProcessed_triggerSF import Run2018



lumi_year  = {
    "2016":        Run2016.lumi,
    "2016_preVFP": Run2016_preVFP.lumi,
    "2017":        Run2017.lumi,
    "2018":        Run2018.lumi,
}

import tWZ.samples.nanoTuples_UL2016_nanoAODv9_postProcessed_triggerSF as UL2016
import tWZ.samples.nanoTuples_UL2016preVFP_nanoAODv9_postProcessed_triggerSF as UL2016preVFP
import tWZ.samples.nanoTuples_UL2017_nanoAODv9_postProcessed_triggerSF as UL2017
import tWZ.samples.nanoTuples_UL2018_nanoAODv9_postProcessed_triggerSF as UL2018
