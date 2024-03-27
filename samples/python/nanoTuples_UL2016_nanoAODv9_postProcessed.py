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
    directory_ = locations.mc_UL2016

logger.info("Loading MC samples from directory %s", directory_)

def make_dirs( dirs ):
    return [ os.path.join( directory_, dir_ ) for dir_ in dirs ]

dirs = {}

dirs['WZ']               = ["WZ"]
WZ = Sample.fromDirectory(name="WZ", treeName="Events", isData=False, color=color.WZ, texName="WZ", directory=make_dirs( dirs['WZ']))

dirs['ZZ']               = ["ZZ"]
ZZ = Sample.fromDirectory(name="ZZ", treeName="Events", isData=False, color=color.ZZ, texName="ZZ", directory=make_dirs( dirs['ZZ']))

dirs['ZZ_powheg']               = ["ZZ_powheg"]
ZZ_powheg = Sample.fromDirectory(name="ZZ_powheg", treeName="Events", isData=False, color=color.ZZ, texName="ZZ", directory=make_dirs( dirs['ZZ_powheg']))

dirs['WW']               = ["WW"]
# dirs['VVTo2L2Nu']        = ["VVTo2L2Nu"] # NOT YET THERE IN UL
WW = Sample.fromDirectory(name="WW", treeName="Events", isData=False, color=color.WW, texName="WW", directory=make_dirs( dirs['WW']))

dirs['WZTo3LNu']               = ["WZTo3LNu"]
WZTo3LNu = Sample.fromDirectory(name="WZTo3LNu", treeName="Events", isData=False, color=color.WZ, texName="WZ", directory=make_dirs( dirs['WZTo3LNu']))

dirs['WZTo3LNu_powheg']               = ["WZTo3LNu_powheg"]
WZTo3LNu_powheg = Sample.fromDirectory(name="WZTo3LNu_powheg", treeName="Events", isData=False, color=color.WZ, texName="WZ", directory=make_dirs( dirs['WZTo3LNu_powheg']))


dirs['triBoson']         = ["WWW_4F","WWZ_4F","WZZ","ZZZ"]
triBoson = Sample.fromDirectory(name="triBoson", treeName="Events", isData=False, color=color.triBoson, texName="VVV", directory=make_dirs( dirs['triBoson']))

# TWZ (nominal)
dirs['TWZ_NLO_DR']             = ['tWll_thad_Wlept_DR', 'tWll_tlept_Wlept_DR', 'tWll_tlept_Whad_DR']
TWZ_NLO_DR  = Sample.fromDirectory(name="TWZ_NLO_DR", treeName="Events", isData=False, color=color.TWZ, texName="tWZ(NLO)", directory=make_dirs( dirs['TWZ_NLO_DR']))

dirs['TWZ_NLO_DS']             = ['tWll_thad_Wlept_DS', 'tWll_tlept_Wlept_DS', 'tWll_tlept_Whad_DS']
TWZ_NLO_DS  = Sample.fromDirectory(name="TWZ_NLO_DS", treeName="Events", isData=False, color=color.TWZ, texName="tWZ(NLO)", directory=make_dirs( dirs['TWZ_NLO_DS']))

# TTZ
dirs['TTZToLLNuNu']     = ['TTZToLLNuNu', 'TTZToLLNuNu_m1to10']
dirs['TTZToQQ']         = ['TTZToQQ']
dirs['TTZ']             = ['TTZToLLNuNu', 'TTZToLLNuNu_m1to10', "TTZToQQ"]
TTZToLLNuNu = Sample.fromDirectory(name="ToLLNuNu", treeName="Events", isData=False, color=color.TTZ, texName="t#bar{t}Z #rightarrow ll#nu#nu", directory=make_dirs( dirs['TTZToLLNuNu']))
TTZ         = Sample.fromDirectory(name="TTZ",      treeName="Events", isData=False, color=color.TTZ, texName="t#bar{t}Z", directory=make_dirs( dirs['TTZ']))

# TTX
dirs['TZQ']             = ['tZq_ll']
TZQ = Sample.fromDirectory(name="TZQ", treeName="Events", isData=False, color=color.TZQ, texName="tZQ", directory=make_dirs( dirs['TZQ']))

dirs['TTH']             = ['TTHTobb', 'TTHnobb']
#dirs['THX']             = ['THW', 'THQ'] # NOT YET THERE IN UL
dirs['TTW']             = ['TTWToLNu', 'TTWToQQ']
dirs['TTVV']            = ['TTWW', 'TTWZ','TTZZ']
# ADD THW AND THQ TO TTX_rare
dirs['TTX_rare']        = ["TTTT", "TTHTobb", "TTHnobb"] + dirs['TTW'] + dirs['TTVV'] # same as TTX_rare but without tZq_ll
TTX_rare = Sample.fromDirectory(name="TTX_rare", treeName="Events", isData=False, color=color.TTX_rare, texName="t/t#bar{t}+(t#bar{t}/H/W/VV)", directory=make_dirs( dirs['TTX_rare']))

dirs['TTX_rare_noTTW']        = ["TTTT", "TTHTobb", "TTHnobb"] + dirs['TTVV']
TTX_rare_noTTW = Sample.fromDirectory(name="TTX_rare_noTTW", treeName="Events", isData=False, color=color.TTX_rare, texName="t/t#bar{t}+(t#bar{t}/H/VV)", directory=make_dirs( dirs['TTX_rare_noTTW']))

TTH      = Sample.fromDirectory(name="TTH", treeName="Events", isData=False, color=color.TTX_rare, texName="t#bar{t}H", directory=make_dirs( dirs['TTH']))

TTW  = Sample.fromDirectory(name="TTW", treeName="Events", isData=False, color=color.TTW, texName="t#bar{t}W", directory=make_dirs( dirs['TTW']))
dirs['TTTT']            = ['TTTT']
TTTT = Sample.fromDirectory(name="TTTT", treeName="Events", isData=False, color=color.TTTT, texName="t#bar{t}W", directory=make_dirs( dirs['TTTT']))

dirs['TTW_EWK']        = ["TTW_EWK"]
TTW_EWK = Sample.fromDirectory(name="TTW_EWK", treeName="Events", isData=False, color=color.TTW, texName="t#bar{t}W (EWK)", directory=make_dirs( dirs['TTW_EWK']))

# TT
dirs['TTLep']           = ['TTLep_pow_CP5']
TTLep = Sample.fromDirectory(name="TTLep",      treeName="Events", isData=False, color=color.TTZ, texName="t#bar{t}Lep", directory=make_dirs( dirs['TTLep']))
dirs['singleTop']       = ['TBar_tch_pow', 'TBar_tWch', 'T_tch_pow', 'T_tWch']
dirs['Top']             = dirs['TTLep'] + dirs['singleTop']
Top  = Sample.fromDirectory(name="Top", treeName="Events", isData=False, color=color.TTJets, texName="t/t#bar{t}", directory=make_dirs(dirs['Top']))

# DY
dirs['DY_LO']           = [ 'DYJetsToLL_M10to50_LO', 'DYJetsToLL_M50']
DY  = Sample.fromDirectory(name="DY", treeName="Events", isData=False, color=color.DY, texName="DY", directory=make_dirs(dirs['DY_LO']))

# ADD VVTo2L2Nu TO NONPROMPT ONCE AVAILABLE
dirs['nonprompt_3l']    = dirs['WW'] + dirs['singleTop'] + dirs['DY_LO'] + dirs['TTLep']
dirs['nonprompt_4l']    = dirs['WW'] + dirs['singleTop'] + dirs['TZQ'] + dirs["WZ"] + dirs['DY_LO'] + dirs['TTLep']
nonprompt_3l = Sample.fromDirectory(name="nonprompt_3l", treeName="Events", isData=False, color=color.nonprompt, texName="nonprompt_3l", directory=make_dirs( dirs['nonprompt_3l']))
nonprompt_4l = Sample.fromDirectory(name="nonprompt_4l", treeName="Events", isData=False, color=color.nonprompt, texName="nonprompt_4l", directory=make_dirs( dirs['nonprompt_4l']))

# TTGamma
dirs['TTGamma'] = ["TTGammaDilep","TTGammaHadronic","TTGammaSinglelep"]
TTGamma  = Sample.fromDirectory(name="TTGamma", treeName="Events", isData=False, color=color.TTG, texName="t#bar{t}#gamma", directory=make_dirs(dirs['TTGamma']))

# ZGamma
dirs['ZGamma'] = ["Zgamma"]
ZGamma  = Sample.fromDirectory(name="ZGamma", treeName="Events", isData=False, color=color.ZG, texName="Z#gamma", directory=make_dirs(dirs['ZGamma']))

# ggToZZ
dirs['ggToZZ'] = ["ggToZZ_2e2mu","ggToZZ_2e2nu","ggToZZ_2e2tau","ggToZZ_2mu2nu","ggToZZ_2mu2tau","ggToZZ_4e","ggToZZ_4mu","ggToZZ_4tau"]
ggToZZ  = Sample.fromDirectory(name="ggToZZ", treeName="Events", isData=False, color=color.ZZ, texName="ggToZZ", directory=make_dirs(dirs['ggToZZ']))

# HToZZ
dirs['HToZZ'] = ["VHToNonbb","VBF_HToZZTo4L","ggToHToZZTo2L2Q","ggToHToZZTo4L"]
HToZZ  = Sample.fromDirectory(name="HToZZ", treeName="Events", isData=False, color=color.ZG, texName="HToZZ", directory=make_dirs(dirs['HToZZ']))




# EFT samples
dirs['ZZ_EFT'] = ['ZZ_EFT']
ZZ_EFT  = Sample.fromDirectory(name="ZZ_EFT", treeName="Events", isData=False, color=color.ZZ, texName="ZZ", directory=make_dirs(dirs['ZZ_EFT']))
ZZ_EFT.reweight_pkl = "/groups/hephy/cms/dennis.schwarz/www/gridpacks/ZZ-vec_reweight_card.pkl"
dirs['WZ_EFT'] = ['WZ_EFT']
WZ_EFT  = Sample.fromDirectory(name="WZ_EFT", treeName="Events", isData=False, color=color.WZ, texName="WZ", directory=make_dirs(dirs['WZ_EFT']))
WZ_EFT.reweight_pkl = "/groups/hephy/cms/dennis.schwarz/www/gridpacks/WZ-vec_reweight_card.pkl"
dirs['TTZ_EFT'] = ['TTZ_EFT']
TTZ_EFT  = Sample.fromDirectory(name="TTZ_EFT", treeName="Events", isData=False, color=color.TTZ, texName="t#bar{t}Z", directory=make_dirs(dirs['TTZ_EFT']))
TTZ_EFT.reweight_pkl = "/groups/hephy/cms/dennis.schwarz/www/gridpacks/ttZ01j-vec_reweight_card.pkl"
