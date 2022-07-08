import ROOT 

samples = [
    "DYJetsToLL_M10to50_LO","TBar_tWch","TTSingleLep_pow_CP5","TTZToLLNuNu","WW","ZZZ","tWll_tlept_Wlept_DS",
    "DYJetsToLL_M50","TBar_tch_pow","TTTT","TTZToLLNuNu_m1to10","WWW_4F","tWll_thad_Wlept_DR","tZq_ll",
    "TTHTobb","TTWToLNu","TTZToQQ","WWZ_4F","tWll_thad_Wlept_DS",
    "TTHad_pow_CP5","TTWToQQ","TTZZ","WZ","tWll_tlept_Whad_DR",
    "TTHnobb","TTWW","T_tWch","WZZ","tWll_tlept_Whad_DS",
    "TTLep_pow_CP5","TTWZ","T_tch_pow","ZZ","tWll_tlept_Wlept_DR",
]

path = "/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/"

samples.sort()

for sample in samples:
    print "--------------------------"
    print sample
    file = ROOT.TFile(path+sample+"/"+sample+"_0.root")
    tree = file.Get("Events")
    for event in file.Events:
        print event.nScale
        for i in range(event.nScale):
            print i, event.Scale_Weight[i]
        break
    

names=['/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_7.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_6.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_5.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_17.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_15.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_16.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_9.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_19.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_18.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_8.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_12.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_10.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_13.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_20.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_4.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_0.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_11.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_3.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_2.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_1.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu/TTZToLLNuNu_14.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu_m1to10/TTZToLLNuNu_m1to10_5.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu_m1to10/TTZToLLNuNu_m1to10_6.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu_m1to10/TTZToLLNuNu_m1to10_3.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu_m1to10/TTZToLLNuNu_m1to10_1.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu_m1to10/TTZToLLNuNu_m1to10_0.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu_m1to10/TTZToLLNuNu_m1to10_2.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToLLNuNu_m1to10/TTZToLLNuNu_m1to10_4.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_4.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_19.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_22.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_5.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_7.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_18.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_21.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_6.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_16.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_13.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_12.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_2.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_0.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_20.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_15.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_1.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_8.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_11.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_14.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_9.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_10.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_3.root', '/scratch-cbe/users/dennis.schwarz/tWZ/nanoTuples/tWZ_UL_nAODv9_v1/UL2018/trilep/TTZToQQ/TTZToQQ_17.root']

for name in names:
    print "--------------------------"
    print name
    file = ROOT.TFile(name)
    tree = file.Get("Events")
    for event in file.Events:
        print event.nScale
        for i in range(event.nScale):
            print i, event.Scale_Weight[i]
        break
