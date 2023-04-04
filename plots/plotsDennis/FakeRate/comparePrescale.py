#!/usr/bin/env python
import ROOT, os
ROOT.gROOT.SetBatch(True)

from tWZ.Tools.triggerPrescale           import triggerPrescale


triggers = [
    "HLT_Mu3_PFJet40",
    "HLT_Mu8",
    "HLT_Mu17",
    "HLT_Mu20",
    "HLT_Mu27",
    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30",
    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30",
]

years = ["UL2016preVFP", "UL2016", "UL2017", "UL2018"]

prescales_mine = {
    "UL2016preVFP": triggerPrescale("UL2016preVFP", "mine"),
    "UL2016":       triggerPrescale("UL2016", "mine"),
    "UL2017":       triggerPrescale("UL2017", "mine"),
    "UL2018":       triggerPrescale("UL2018", "mine")
}

prescales_bril = {
    "UL2016preVFP": triggerPrescale("UL2016preVFP", "bril"),
    "UL2016":       triggerPrescale("UL2016", "bril"),
    "UL2017":       triggerPrescale("UL2017", "bril"),
    "UL2018":       triggerPrescale("UL2018", "bril")
}

for year in years:
    for trigger in triggers:
        p_mine = 1.0/prescales_mine[year].getWeight([trigger])
        p_bril = 1.0/prescales_bril[year].getWeight([trigger])        
        print year, trigger, p_mine, p_bril
