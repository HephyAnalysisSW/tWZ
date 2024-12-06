import os

version = "v14"

selections = [
    "qualepT-minDLmass12-onZ1-onZ2",
    "trilepT-minDLmass12-onZ1-btag0-met60",
    "trilepT-minDLmass12-onZ1-njet3p-btag1p",
]

years = ["UL2016preVFP", "UL2016", "UL2017", "UL2018"]

systematics = {
    "BTag_b_correlated":              ("BTag_b_correlated_UP", "BTag_b_correlated_DOWN"),
    "BTag_l_correlated":              ("BTag_l_correlated_UP", "BTag_l_correlated_DOWN"),
    "BTag_b_uncorrelated_2016preVFP": ("BTag_b_uncorrelated_2016preVFP_UP", "BTag_b_uncorrelated_2016preVFP_DOWN"),
    "BTag_l_uncorrelated_2016preVFP": ("BTag_l_uncorrelated_2016preVFP_UP", "BTag_l_uncorrelated_2016preVFP_DOWN"),
    "BTag_b_uncorrelated_2016":       ("BTag_b_uncorrelated_2016_UP", "BTag_b_uncorrelated_2016_DOWN"),
    "BTag_l_uncorrelated_2016":       ("BTag_l_uncorrelated_2016_UP", "BTag_l_uncorrelated_2016_DOWN"),
    "BTag_b_uncorrelated_2017":       ("BTag_b_uncorrelated_2017_UP", "BTag_b_uncorrelated_2017_DOWN"),
    "BTag_l_uncorrelated_2017":       ("BTag_l_uncorrelated_2017_UP", "BTag_l_uncorrelated_2017_DOWN"),
    "BTag_b_uncorrelated_2018":       ("BTag_b_uncorrelated_2018_UP", "BTag_b_uncorrelated_2018_DOWN"),
    "BTag_l_uncorrelated_2018":       ("BTag_l_uncorrelated_2018_UP", "BTag_l_uncorrelated_2018_DOWN"),
    "Trigger_2016preVFP":             ("Trigger_2016preVFP_UP", "Trigger_2016preVFP_DOWN"),
    "Trigger_2016":                   ("Trigger_2016_UP", "Trigger_2016_DOWN"),
    "Trigger_2017":                   ("Trigger_2017_UP", "Trigger_2017_DOWN"),
    "Trigger_2018":                   ("Trigger_2018_UP", "Trigger_2018_DOWN"),
    "Prefire":                        ("Prefire_UP", "Prefire_DOWN"),
    "LepReco":                        ("LepReco_UP", "LepReco_DOWN"),
    "LepIDstat_elec_2016preVFP":      ("LepIDstat_elec_2016preVFP_UP", "LepIDstat_elec_2016preVFP_DOWN"),
    "LepIDstat_elec_2016":            ("LepIDstat_elec_2016_UP", "LepIDstat_elec_2016_DOWN"),
    "LepIDstat_elec_2017":            ("LepIDstat_elec_2017_UP", "LepIDstat_elec_2017_DOWN"),
    "LepIDstat_elec_2018":            ("LepIDstat_elec_2018_UP", "LepIDstat_elec_2018_DOWN"),
    "LepIDsys_elec":                  ("LepIDsys_elec_UP", "LepIDsys_elec_DOWN"),
    "LepIDstat_muon_2016preVFP":      ("LepIDstat_muon_2016preVFP_UP", "LepIDstat_muon_2016preVFP_DOWN"),
    "LepIDstat_muon_2016":            ("LepIDstat_muon_2016_UP", "LepIDstat_muon_2016_DOWN"),
    "LepIDstat_muon_2017":            ("LepIDstat_muon_2017_UP", "LepIDstat_muon_2017_DOWN"),
    "LepIDstat_muon_2018":            ("LepIDstat_muon_2018_UP", "LepIDstat_muon_2018_DOWN"),
    "LepIDsys_muon":                  ("LepIDsys_muon_UP", "LepIDsys_muon_DOWN"),
    "PU":                             ("PU_UP", "PU_DOWN"),
    "JES":                            ("JES_UP", "JES_DOWN"),
    "JER_2016preVFP":                 ("JER_2016preVFP_UP", "JER_2016preVFP_DOWN"),
    "JER_2016":                       ("JER_2016_UP", "JER_2016_DOWN"),
    "JER_2017":                       ("JER_2017_UP", "JER_2017_DOWN"),
    "JER_2018":                       ("JER_2018_UP", "JER_2018_DOWN"),
    "Unclustered_2016preVFP":         ("Unclustered_2016preVFP_UP", "Unclustered_2016preVFP_DOWN"),
    "Unclustered_2016":               ("Unclustered_2016_UP", "Unclustered_2016_DOWN"),
    "Unclustered_2017":               ("Unclustered_2017_UP", "Unclustered_2017_DOWN"),
    "Unclustered_2018":               ("Unclustered_2018_UP", "Unclustered_2018_DOWN"),
    "Lumi_uncorrelated_2016":         ("Lumi_uncorrelated_2016_UP", "Lumi_uncorrelated_2016_DOWN"),
    "Lumi_uncorrelated_2017":         ("Lumi_uncorrelated_2017_UP", "Lumi_uncorrelated_2017_DOWN"),
    "Lumi_uncorrelated_2018":         ("Lumi_uncorrelated_2018_UP", "Lumi_uncorrelated_2018_DOWN"),
    "Lumi_correlated_161718":         ("Lumi_correlated_161718_UP", "Lumi_correlated_161718_DOWN"),
    "Lumi_correlated_1718":           ("Lumi_correlated_1718_UP", "Lumi_correlated_1718_DOWN"),
    # "ISR":                            ("ISR_UP", "ISR_DOWN"),
    # "FSR":                            ("FSR_UP", "FSR_DOWN"),
    # "muR":                            ("Scale_UPNONE", "Scale_DOWNNONE"), # muR
    # "muF":                            ("Scale_NONEUP", "Scale_NONEDOWN"), # muF
    # "PDF":                            (), # TREAT DIFFERENTLY
}

for year in years:
    print "===================================================="
    print year
    for selection in selections:
        for sys in systematics.keys():
            sysUp, sysDown = systematics[sys]
            filename = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint_noData_"+sysUp+"/"+year+"/all/"+selection+"/Results.root"
            if not os.path.exists(filename):
                print filename
