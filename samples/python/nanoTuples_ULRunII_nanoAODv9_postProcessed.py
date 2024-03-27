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

ZZ_EFT          = Sample.combine( "ZZ_EFT", [UL2016preVFP.ZZ_EFT, UL2016.ZZ_EFT, UL2017.ZZ_EFT, UL2018.ZZ_EFT] )
WZ_EFT          = Sample.combine( "WZ_EFT", [UL2016preVFP.WZ_EFT, UL2016.WZ_EFT, UL2017.WZ_EFT, UL2018.WZ_EFT] )
TTZ_EFT         = Sample.combine( "TTZ_EFT", [UL2016preVFP.TTZ_EFT, UL2016.TTZ_EFT, UL2017.TTZ_EFT, UL2018.TTZ_EFT] )
ZZ_EFT.reweight_pkl = "/groups/hephy/cms/dennis.schwarz/www/gridpacks/ZZ-vec_reweight_card.pkl"
WZ_EFT.reweight_pkl = "/groups/hephy/cms/dennis.schwarz/www/gridpacks/WZ-vec_reweight_card.pkl"
TTZ_EFT.reweight_pkl = "/groups/hephy/cms/dennis.schwarz/www/gridpacks/ttZ01j-vec_reweight_card.pkl"

TWZ_NLO_DR     = Sample.combine( "TWZ_NLO_DR", [UL2016preVFP.TWZ_NLO_DR, UL2016.TWZ_NLO_DR, UL2017.TWZ_NLO_DR, UL2018.TWZ_NLO_DR] )
TWZ_NLO_DS     = Sample.combine( "TWZ_NLO_DS", [UL2016preVFP.TWZ_NLO_DS, UL2016.TWZ_NLO_DS, UL2017.TWZ_NLO_DS, UL2018.TWZ_NLO_DS] )
TTZ            = Sample.combine( "TTZ", [UL2016preVFP.TTZ, UL2016.TTZ, UL2017.TTZ, UL2018.TTZ] )
TTX_rare       = Sample.combine( "TTX_rare", [UL2016preVFP.TTX_rare, UL2016.TTX_rare, UL2017.TTX_rare, UL2018.TTX_rare] )
TTX_rare_noTTW = Sample.combine( "TTX_rare_noTTW", [UL2016preVFP.TTX_rare_noTTW, UL2016.TTX_rare_noTTW, UL2017.TTX_rare_noTTW, UL2018.TTX_rare_noTTW] )
TTH            = Sample.combine( "TTH", [UL2016preVFP.TTH, UL2016.TTH, UL2017.TTH, UL2018.TTH] )
TZQ            = Sample.combine( "TZQ", [UL2016preVFP.TZQ, UL2016.TZQ, UL2017.TZQ, UL2018.TZQ] )
WZ             = Sample.combine( "WZ", [UL2016preVFP.WZ, UL2016.WZ, UL2017.WZ, UL2018.WZ] )
WZTo3LNu       = Sample.combine( "WZTo3LNu", [UL2016preVFP.WZTo3LNu, UL2016.WZTo3LNu, UL2017.WZTo3LNu, UL2018.WZTo3LNu] )
WZTo3LNu_powheg= Sample.combine( "WZTo3LNu_powheg", [UL2016preVFP.WZTo3LNu_powheg, UL2016.WZTo3LNu_powheg, UL2017.WZTo3LNu_powheg, UL2018.WZTo3LNu_powheg] )
triBoson       = Sample.combine( "triBoson", [UL2016preVFP.triBoson, UL2016.triBoson, UL2017.triBoson, UL2018.triBoson] )
ZZ             = Sample.combine( "ZZ", [UL2016preVFP.ZZ, UL2016.ZZ, UL2017.ZZ, UL2018.ZZ] )
ZZ_powheg      = Sample.combine( "ZZ_powheg", [UL2016preVFP.ZZ_powheg, UL2016.ZZ_powheg, UL2017.ZZ_powheg, UL2018.ZZ_powheg] )
nonprompt_3l   = Sample.combine( "nonprompt_3l", [UL2016preVFP.nonprompt_3l, UL2016.nonprompt_3l, UL2017.nonprompt_3l, UL2018.nonprompt_3l] )
Top            = Sample.combine( "Top", [UL2016preVFP.Top, UL2016.Top, UL2017.Top, UL2018.Top], texName = "t/t#bar{t}+ST")
TTLep          = Sample.combine( "TTLep", [UL2016preVFP.TTLep, UL2016.TTLep, UL2017.TTLep, UL2018.TTLep],texName = "t#bar{t}")
TTTT           = Sample.combine( "TTTT", [UL2016preVFP.TTTT, UL2016.TTTT, UL2017.TTTT, UL2018.TTTT], texName = "t#bar{t}t#bar{t}")
TTW            = Sample.combine( "TTW", [UL2016preVFP.TTW, UL2016.TTW, UL2017.TTW, UL2018.TTW], texName = "t#bar{t}W")
TTW_EWK        = Sample.combine( "TTW_EWK", [UL2016preVFP.TTW_EWK, UL2016.TTW_EWK, UL2017.TTW_EWK, UL2018.TTW_EWK] )
TTZ            = Sample.combine( "TTZ", [UL2016preVFP.TTZ, UL2016.TTZ, UL2017.TTZ, UL2018.TTZ], texName = "t#bar{t}Z")
DY             = Sample.combine( "DY", [UL2016preVFP.DY, UL2016.DY, UL2017.DY, UL2018.DY], texName = "Drell-Yan")
WW             = Sample.combine( "WW", [UL2016preVFP.WW, UL2016.WW, UL2017.WW, UL2018.WW], texName = "WW")
TTGamma        = Sample.combine( "TTGamma", [UL2016preVFP.TTGamma, UL2016.TTGamma, UL2017.TTGamma, UL2018.TTGamma], texName = "t#bar{t}#gamma")
ZGamma         = Sample.combine( "ZGamma", [UL2016preVFP.ZGamma, UL2016.ZGamma, UL2017.ZGamma, UL2018.ZGamma], texName = "Z#gamma")
ggToZZ         = Sample.combine( "ggToZZ", [UL2016preVFP.ggToZZ, UL2016.ggToZZ, UL2017.ggToZZ, UL2018.ggToZZ], texName = "ggToZZ")
HToZZ          = Sample.combine( "HToZZ", [UL2016preVFP.HToZZ, UL2016.HToZZ, UL2017.HToZZ, UL2018.HToZZ], texName = "HToZZ")
