from RootTools.core.standard import *

# from tWZ.samples.nanoTuples_DATA_UL2016_nanoAODv9_postProcessed_singlelep import Run2016
# from tWZ.samples.nanoTuples_DATA_UL2016preVFP_nanoAODv9_postProcessed_singlelep import Run2016_preVFP
# from tWZ.samples.nanoTuples_DATA_UL2017_nanoAODv9_postProcessed_singlelep import Run2017
from tWZ.samples.nanoTuples_DATA_UL2018_nanoAODv9_postProcessed_singlelep import Run2018


# RunII      = Sample.combine( "RunII", [Run2016, Run2016_preVFP, Run2017, Run2018], texName = "RunII" ) 
# RunII.lumi = Run2016.lumi + Run2016_preVFP.lumi + Run2017.lumi + Run2018.lumi

lumi_year  = {
    # "2016":        Run2016.lumi, 
    # "2016_preVFP": Run2016_preVFP.lumi, 
    # "2017":        Run2017.lumi, 
    "2018":        Run2018.lumi,
    # "RunII":       RunII.lumi,
}

# import tWZ.samples.nanoTuples_UL2016_nanoAODv9_postProcessed_singlelep as UL2016
# import tWZ.samples.nanoTuples_UL2016preVFP_nanoAODv9_postProcessed_singlelep as UL2016preVFP
# import tWZ.samples.nanoTuples_UL2017_nanoAODv9_postProcessed_singlelep as UL2017
import tWZ.samples.nanoTuples_UL2018_nanoAODv9_postProcessed_singlelep as UL2018


WZTo3LNu       = Sample.combine( "WZTo3LNu", [UL2018.WZTo3LNu] )
ZZ             = Sample.combine( "ZZ", [UL2018.ZZ] )
WW             = Sample.combine( "WW", [UL2018.WW] )
TTbar          = Sample.combine( "TTbar", [UL2018.TTbar], texName = "t/t#bar{t}")
DY             = Sample.combine( "DY", [UL2018.DY], texName = "Drell-Yan")
QCD_MuEnriched = Sample.combine( "QCD_MuEnriched", [UL2018.QCD_MuEnriched] )
QCD_EMEnriched = Sample.combine( "QCD_EMEnriched", [UL2018.QCD_EMEnriched] )
QCD_bcToE      = Sample.combine( "QCD_bcToE", [UL2018.QCD_bcToE] )
