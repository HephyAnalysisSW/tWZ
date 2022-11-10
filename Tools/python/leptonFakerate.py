import ROOT
import os
from tWZ.Tools.helpers import getObjFromFile


filename = {
    "UL2018": "LeptonFakerate_UL2018.root",
}


class leptonFakerate:
    def __init__(self, year, mode = "SF"):
        # Define maps here 
        self.year = year
        self.mode = mode
        self.dataDir = "$CMSSW_BASE/src/tWZ/Tools/data/leptonFakerate/"
        filepath = self.dataDir+filename[year]

        self.SFmaps = {
            "muon": {
                "SF"            :  getObjFromFile(filepath,"fakerate__MC__muon"),
                "SF_noLooseSel" :  getObjFromFile(filepath,"fakerate__MC__muon__noLooseSel"),
                "SF_noLooseWP"  :  getObjFromFile(filepath,"fakerate__MC__muon__noLooseWP"),
            },
            "elec": {
                "SF"            :  getObjFromFile(filepath,"fakerate__MC__elec"),  
                "SF_noLooseSel" :  getObjFromFile(filepath,"fakerate__MC__elec__noLooseSel"),
                "SF_noLooseWP"  :  getObjFromFile(filepath,"fakerate__MC__elec__noLooseWP"),     
            },
        }
    
    def getFactor(self, pdgId, pt, eta_, unc='sys', sigma=0):
        # Set boundaries
        eta = abs(eta_)
        if eta > 2.4:
            eta = 2.39 
        if pt > 100:
            pt = 99
                        
        # Get uncertainty mode
        uncert = "sys"
        if unc == "stat":
            uncert = "stat"
        
        lepton = None
        if abs(pdgId)==11:
            lepton = "elec"
        elif abs(pdgId)==13:
            lepton = "muon"
        else: 
          raise Exception("Lepton Fakerate for PdgId %i not known"%pdgId)

        ptbin = self.SFmaps[lepton][self.mode].GetXaxis().FindBin(pt)
        etabin  = self.SFmaps[lepton][self.mode].GetYaxis().FindBin(eta)
        fakerate = self.SFmaps[lepton][self.mode].GetBinContent(ptbin, etabin)
        # print lepton, "--", pt, eta, "|", ptbin, etabin, "|", fakerate
        return fakerate
        # err = self.SFmaps[lepton][uncert].GetBinContent(etabin, ptbin)
        # return SF+sigma*err
