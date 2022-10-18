import ROOT
import os
from tWZ.Tools.helpers import getObjFromFile


filename = {
    "UL2018": "LeptonFakerate_UL2018.root",
}


class leptonFakerate:
    def __init__(self, year):
        # Define maps here 
        self.year = year
        self.dataDir = "$CMSSW_BASE/src/tWZ/Tools/data/leptonFakerate/"
        filepath = self.dataDir+filename[year]

        self.SFmaps = {
            "muon": {
                "SF" :  getObjFromFile(filepath,"fakerate__MC__muon"),
            },
            "elec": {
                "SF" :  getObjFromFile(filepath,"fakerate__MC__elec"),        
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

        ptbin = self.SFmaps[lepton]["SF"].GetXaxis().FindBin(pt)
        etabin  = self.SFmaps[lepton]["SF"].GetYaxis().FindBin(eta)
        fakerate = self.SFmaps[lepton]["SF"].GetBinContent(ptbin, etabin)
        # print lepton, "--", pt, eta, "|", ptbin, etabin, "|", fakerate
        return fakerate
        # err = self.SFmaps[lepton][uncert].GetBinContent(etabin, ptbin)
        # return SF+sigma*err
