from RootTools.core.standard import *

from tWZ.samples.nanoTuples_DATA_UL2016_nanoAODv9_postProcessed import Run2016
from tWZ.samples.nanoTuples_DATA_UL2016preVFP_nanoAODv9_postProcessed import Run2016_preVFP
from tWZ.samples.nanoTuples_DATA_UL2017_nanoAODv9_postProcessed import Run2017
from tWZ.samples.nanoTuples_DATA_UL2018_nanoAODv9_postProcessed import Run2018


RunII      = Sample.combine( "RunII", [Run2016, Run2016_preVFP, Run2017, Run2018], texName = "RunII" ) 
RunII.lumi = Run2016.lumi + Run2016_preVFP.lumi + Run2017.lumi + Run2018.lumi

lumi_year  = {
    "2016":        Run2016.lumi, 
    "2016_preVFP": Run2016_preVFP.lumi, 
    "2017":        Run2017.lumi, 
    "2018":        Run2018.lumi,
    "RunII":       RunII.lumi,
}

import tWZ.samples.nanoTuples_UL2016_nanoAODv9_postProcessed as UL2016
import tWZ.samples.nanoTuples_UL2016preVFP_nanoAODv9_postProcessed as UL2016preVFP
import tWZ.samples.nanoTuples_UL2017_nanoAODv9_postProcessed as UL2017
import tWZ.samples.nanoTuples_UL2018_nanoAODv9_postProcessed as UL2018


TWZ_NLO_DR   = Sample.combine( "TWZ_NLO_DR", [UL2016preVFP.TWZ_NLO_DR, UL2016.TWZ_NLO_DR, UL2017.TWZ_NLO_DR, UL2018.TWZ_NLO_DR] )
TWZ_NLO_DS   = Sample.combine( "TWZ_NLO_DS", [UL2016preVFP.TWZ_NLO_DS, UL2016.TWZ_NLO_DS, UL2017.TWZ_NLO_DS, UL2018.TWZ_NLO_DS] )
TTZ          = Sample.combine( "TTZ", [UL2016preVFP.TTZ, UL2016.TTZ, UL2017.TTZ, UL2018.TTZ] )
TTX_rare     = Sample.combine( "TTX_rare", [UL2016preVFP.TTX_rare, UL2016.TTX_rare, UL2017.TTX_rare, UL2018.TTX_rare] )
TTH          = Sample.combine( "TTH", [UL2016preVFP.TTH, UL2016.TTH, UL2017.TTH, UL2018.TTH] )
TZQ          = Sample.combine( "TZQ", [UL2016preVFP.TZQ, UL2016.TZQ, UL2017.TZQ, UL2018.TZQ] )
WZ           = Sample.combine( "WZ", [UL2016preVFP.WZ, UL2016.WZ, UL2017.WZ, UL2018.WZ] )
WZTo3LNu     = Sample.combine( "WZTo3LNu", [UL2016preVFP.WZTo3LNu, UL2016.WZTo3LNu, UL2017.WZTo3LNu, UL2018.WZTo3LNu] )
triBoson     = Sample.combine( "triBoson", [UL2016preVFP.triBoson, UL2016.triBoson, UL2017.triBoson, UL2018.triBoson] )
ZZ           = Sample.combine( "ZZ", [UL2016preVFP.ZZ, UL2016.ZZ, UL2017.ZZ, UL2018.ZZ] )
nonprompt_3l = Sample.combine( "nonprompt_3l", [UL2016preVFP.nonprompt_3l, UL2016.nonprompt_3l, UL2017.nonprompt_3l, UL2018.nonprompt_3l] )
Top          = Sample.combine( "Top", [UL2016preVFP.Top, UL2016.Top, UL2017.Top, UL2018.Top], texName = "t/t#bar{t}+ST")
TTLep        = Sample.combine( "TTLep", [UL2016preVFP.TTLep, UL2016.TTLep, UL2017.TTLep, UL2018.TTLep],texName = "t#bar{t}")
TTTT         = Sample.combine( "TTTT", [UL2016preVFP.TTTT, UL2016.TTTT, UL2017.TTTT, UL2018.TTTT], texName = "t#bar{t}t#bar{t}")
TTW          = Sample.combine( "TTW", [UL2016preVFP.TTW, UL2016.TTW, UL2017.TTW, UL2018.TTW], texName = "t#bar{t}W")
TTZ          = Sample.combine( "TTZ", [UL2016preVFP.TTZ, UL2016.TTZ, UL2017.TTZ, UL2018.TTZ], texName = "t#bar{t}Z")
DY           = Sample.combine( "DY", [UL2016preVFP.DY, UL2016.DY, UL2017.DY, UL2018.DY], texName = "Drell-Yan")
WW           = Sample.combine( "WW", [UL2016preVFP.WW, UL2016.WW, UL2017.WW, UL2018.WW], texName = "WW")