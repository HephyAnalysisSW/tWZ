
def getTriggerSelString(year, mode):
    triggers = []
    if year in ["UL2016", "UL2016_preVFP"]:
        triggers_MET = [
            "HLT_MET200",
            "HLT_PFMET300",
            "HLT_PFMET170_HBHECleaned",
            "HLT_PFMET120_PFMHT120_IDTight",
        ]
        triggers_HT = [
            "HLT_PFHT300_PFMET110",
            "HLT_PFHT350_DiPFJetAve90_PFAlphaT0p53",
            "HLT_PFHT400_DiPFJetAve90_PFAlphaT0p52",
            "HLT_PFHT400_SixJet30_DoubleBTagCSV_p056",
            "HLT_PFHT900",
            "HLT_PFHT650_WideJetMJJ900DEtaJJ1p5",
            "HLT_CaloJet500_NoJetID",
        ]
    elif year == "UL2017":
        triggers_MET = [
            "HLT_PFMET140_PFMHT140_IDTight",
        ]
        triggers_HT = [
            "HLT_PFJet500",
            "HLT_PFHT500_PFMET100_PFMHT100_IDTight",
            "HLT_PFHT700_PFMET85_PFMHT85_IDTight",
            "HLT_PFHT800_PFMET75_PFMHT75_IDTight",
            "HLT_CaloJet500_NoJetID",
            "HLT_AK8PFJet500",
        ]
    elif year == "UL2018":
        triggers_MET = [
            "HLT_CaloMET350_HBHECleaned",
            "HLT_PFMET120_PFMHT120_IDTight",
            "HLT_PFMET250_HBHECleaned",
            "HLT_PFMET200_HBHE_BeamHaloCleaned",
            "HLT_PFMETTypeOne140_PFMHT140_IDTight",
            "HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned",
        ]
        triggers_HT = [
            "HLT_CaloJet500_NoJetID",
            "HLT_AK8PFJet500",
            "HLT_AK8PFJet400_TrimMass30",
            "HLT_DiJet110_35_Mjj650_PFMET110",
            "HLT_PFHT800_PFMET75_PFMHT75_IDTight",
            "HLT_PFHT700_PFMET85_PFMHT85_IDTight",
            "HLT_PFHT500_PFMET100_PFMHT100_IDTight",
            "HLT_PFHT1050",
            "HLT_PFJet500",
            "HLT_TripleJet110_35_35_Mjj650_PFMET110"
        ]

    if mode == "MET":
        return "(%s)"%"||".join(triggers_MET)
    elif mode == "HT":
        return "(!(%s)"%"||".join(triggers_MET)+"&&(%s)"%"||".join(triggers_HT)+")"
