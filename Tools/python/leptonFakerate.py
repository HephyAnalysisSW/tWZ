import ROOT
import os
from tWZ.Tools.helpers import getObjFromFile

class leptonFakerate:
    def __init__(self, year, mode = "SF", dataMC = "MC"):
        
        # Check inputs
        if not year in ["UL2016", "UL2016preVFP", "UL2017", "UL2018"]:
            raise Exception("Lepton fakerate not known for era %s "%year)
        if not mode in ["SF", "SF_noLooseSel", "SF_noLooseWP"]:
            raise Exception("Lepton fakerate not know for mode %s "%mode)
        if not dataMC in ["MC", "DATA"]:
            raise Exception("dataMC switch in lepton fakerate must be 'MC or 'DATA' ")
            
            
        # Define map locations 
        self.dataMC = dataMC
        self.year = year
        self.mode = mode
        self.dataDir = "$CMSSW_BASE/src/tWZ/Tools/data/leptonFakerate/"
        suffix = ""
        if "noLooseSel" in mode:
            suffix = "noLooseSel"
        elif "noLooseWP" in mode:
            suffix = "noLooseWP"
        filepath_elec_DATA = self.dataDir+"LeptonFakerate__"+self.year+"__elec__"+suffix+".root"
        filepath_muon_DATA = self.dataDir+"LeptonFakerate__"+self.year+"__muon__"+suffix+".root"
        filepath_elec_MC   = self.dataDir+"LeptonFakerate__MC__"+self.year+"__elec__"+suffix+".root"
        filepath_muon_MC   = self.dataDir+"LeptonFakerate__MC__"+self.year+"__muon__"+suffix+".root"

        # Store needed maps in dictionary
        self.SFmaps = {
            "muon": {
                "MC"   :   getObjFromFile(filepath_muon_MC,"Fakerate_MC"),
                "DATA" :   getObjFromFile(filepath_muon_DATA,"Fakerate_v1"),
            },
            "elec": {
                "MC"   :   getObjFromFile(filepath_elec_MC,"Fakerate_MC"),
                "DATA" :   getObjFromFile(filepath_elec_DATA,"Fakerate_v1"),
            },
        }
    
    def getFactor(self, pdgId, pt, eta_, unc='sys', sigma=0):
        # Set boundaries
        eta = abs(eta_)
        if eta > 2.399:
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

        ptbin = self.SFmaps[lepton][self.dataMC].GetXaxis().FindBin(pt)
        etabin  = self.SFmaps[lepton][self.dataMC].GetYaxis().FindBin(eta)
        fakerate = self.SFmaps[lepton][self.dataMC].GetBinContent(ptbin, etabin)
        return fakerate
        # err = self.SFmaps[lepton][uncert].GetBinContent(etabin, ptbin)
        # return SF+sigma*err
