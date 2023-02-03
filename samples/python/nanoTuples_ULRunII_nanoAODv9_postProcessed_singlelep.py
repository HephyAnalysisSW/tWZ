from RootTools.core.standard import *

# Data 2016preVFP
from tWZ.samples.nanoTuples_DATA_UL2016preVFP_nanoAODv9_postProcessed_singlelep import Run2016_preVFP
from tWZ.samples.nanoTuples_DATA_UL2016preVFP_nanoAODv9_postProcessed_singlelep import SingleElectron_Run2016_preVFP
from tWZ.samples.nanoTuples_DATA_UL2016preVFP_nanoAODv9_postProcessed_singlelep import SingleMuon_Run2016_preVFP

# Data 2016
from tWZ.samples.nanoTuples_DATA_UL2016_nanoAODv9_postProcessed_singlelep import Run2016
from tWZ.samples.nanoTuples_DATA_UL2016_nanoAODv9_postProcessed_singlelep import SingleElectron_Run2016
from tWZ.samples.nanoTuples_DATA_UL2016_nanoAODv9_postProcessed_singlelep import SingleMuon_Run2016

# Data 2017
from tWZ.samples.nanoTuples_DATA_UL2017_nanoAODv9_postProcessed_singlelep import Run2017
from tWZ.samples.nanoTuples_DATA_UL2017_nanoAODv9_postProcessed_singlelep import SingleElectron_Run2017
from tWZ.samples.nanoTuples_DATA_UL2017_nanoAODv9_postProcessed_singlelep import SingleMuon_Run2017

# Data 2018
from tWZ.samples.nanoTuples_DATA_UL2018_nanoAODv9_postProcessed_singlelep import Run2018
from tWZ.samples.nanoTuples_DATA_UL2018_nanoAODv9_postProcessed_singlelep import EGamma_Run2018
from tWZ.samples.nanoTuples_DATA_UL2018_nanoAODv9_postProcessed_singlelep import SingleMuon_Run2018


RunII      = Sample.combine( "RunII", [Run2016, Run2016_preVFP, Run2017, Run2018], texName = "RunII" ) 
RunII.lumi = Run2016.lumi + Run2016_preVFP.lumi + Run2017.lumi + Run2018.lumi

lumi_year  = {
    "2016":        Run2016.lumi, 
    "2016_preVFP": Run2016_preVFP.lumi, 
    "2017":        Run2017.lumi, 
    "2018":        Run2018.lumi,
    "RunII":       RunII.lumi,
}

import tWZ.samples.nanoTuples_UL2016preVFP_nanoAODv9_postProcessed_singlelep as UL2016preVFP
import tWZ.samples.nanoTuples_UL2016_nanoAODv9_postProcessed_singlelep as UL2016
import tWZ.samples.nanoTuples_UL2017_nanoAODv9_postProcessed_singlelep as UL2017
import tWZ.samples.nanoTuples_UL2018_nanoAODv9_postProcessed_singlelep as UL2018

WZ             = Sample.combine( "WZ", [UL2016.WZ, UL2016preVFP.WZ, UL2017.WZ, UL2018.WZ] )
ZZ             = Sample.combine( "ZZ", [UL2016.ZZ, UL2016preVFP.ZZ, UL2017.ZZ, UL2018.ZZ] )
WW             = Sample.combine( "WW", [UL2016.WW, UL2016preVFP.WW, UL2017.WW, UL2018.WW] )
TTbar          = Sample.combine( "TTbar", [UL2016.TTbar, UL2016preVFP.TTbar, UL2017.TTbar, UL2018.TTbar], texName = "t/t#bar{t}")
DY             = Sample.combine( "DY", [UL2016.DY, UL2016preVFP.DY, UL2017.DY, UL2018.DY], texName = "Drell-Yan")
WJetsToLNu     = Sample.combine( "WJetsToLNu", [UL2016.WJetsToLNu, UL2016preVFP.WJetsToLNu, UL2017.WJetsToLNu, UL2018.WJetsToLNu], texName = "W+jets")
QCD_MuEnriched = Sample.combine( "QCD_MuEnriched", [UL2016.QCD_MuEnriched, UL2016preVFP.QCD_MuEnriched, UL2017.QCD_MuEnriched, UL2018.QCD_MuEnriched] )
QCD_EMEnriched = Sample.combine( "QCD_EMEnriched", [UL2016.QCD_EMEnriched, UL2016preVFP.QCD_EMEnriched, UL2017.QCD_EMEnriched, UL2018.QCD_EMEnriched] )
QCD_bcToE      = Sample.combine( "QCD_bcToE", [UL2016.QCD_bcToE, UL2016preVFP.QCD_bcToE, UL2017.QCD_bcToE, UL2018.QCD_bcToE] )
