import ROOT
import os
from tWZ.Tools.helpers import getObjFromFile

class leptonFakerate:
    def __init__(self, year, mode = "MC"):
        
        # Check inputs
        if not year in ["UL2016", "UL2016preVFP", "UL2017", "UL2018"]:
            raise Exception("Lepton fakerate not known for era %s "%year)
        if not mode in ["MC", "DATA", "BRIL", "tunePtCone", "tunePtConeMC"]:
            raise Exception("mode switch in lepton fakerate must be 'MC or 'DATA' ")
            
            
        # Define map locations 
        self.mode = mode
        self.year = year
        self.dataDir = "$CMSSW_BASE/src/tWZ/Tools/data/leptonFakerate/"
        filepath_elec_DATA = self.dataDir+"LeptonFakerate__"+self.year+"__elec.root"
        filepath_muon_DATA = self.dataDir+"LeptonFakerate__"+self.year+"__muon.root"
        filepath_elec_MC   = self.dataDir+"LeptonFakerate__MC__"+self.year+"__elec.root"
        filepath_muon_MC   = self.dataDir+"LeptonFakerate__MC__"+self.year+"__muon.root"
        filepath_elec_BRIL = self.dataDir+"LeptonFakerate__"+self.year+"__elec__BRIL.root"
        filepath_muon_BRIL = self.dataDir+"LeptonFakerate__"+self.year+"__muon__BRIL.root"
        filepath_elec_tunePtCone = self.dataDir+"LeptonFakerate__"+self.year+"__elec__tunePtCone.root"
        filepath_muon_tunePtCone = self.dataDir+"LeptonFakerate__"+self.year+"__muon__tunePtCone.root"
        filepath_elec_tunePtConeMC   = self.dataDir+"LeptonFakerate__MC__"+self.year+"__elec__tunePtCone.root"
        filepath_muon_tunePtConeMC   = self.dataDir+"LeptonFakerate__MC__"+self.year+"__muon__tunePtCone.root"
                
        # Store needed maps in dictionary
        self.SFmaps = {
            "muon": {
                "MC"        :   getObjFromFile(filepath_muon_MC,"Fakerate_MC"),
                "MC_stat"   :   getObjFromFile(filepath_muon_MC,"Fakerate_MC_stat"),
                "DATA"      :   getObjFromFile(filepath_muon_DATA,"Fakerate_v3"),
                "DATA_stat" :   getObjFromFile(filepath_muon_DATA,"Fakerate_v3_stat"),
                "BRIL"      :   getObjFromFile(filepath_muon_BRIL,"Fakerate_v3"),
                "BRIL_stat" :   getObjFromFile(filepath_muon_BRIL,"Fakerate_v3_stat"),
                "tunePtCone"      :   getObjFromFile(filepath_muon_tunePtCone,"Fakerate_v3"),
                "tunePtCone_stat" :   getObjFromFile(filepath_muon_tunePtCone,"Fakerate_v3_stat"),
                "tunePtConeMC"      :   getObjFromFile(filepath_muon_tunePtConeMC,"Fakerate_MC"),
                "tunePtConeMC_stat" :   getObjFromFile(filepath_muon_tunePtConeMC,"Fakerate_MC_stat"),
            },
            "elec": {
                "MC"        :   getObjFromFile(filepath_elec_MC,"Fakerate_MC"),
                "MC_stat"   :   getObjFromFile(filepath_elec_MC,"Fakerate_MC_stat"),
                "DATA"      :   getObjFromFile(filepath_elec_DATA,"Fakerate_v3"),
                "DATA_stat" :   getObjFromFile(filepath_elec_DATA,"Fakerate_v3_stat"),
                "BRIL"      :   getObjFromFile(filepath_elec_BRIL,"Fakerate_v3"),
                "BRIL_stat" :   getObjFromFile(filepath_elec_BRIL,"Fakerate_v3_stat"),
                "tunePtCone"      :   getObjFromFile(filepath_elec_tunePtCone,"Fakerate_v3"),
                "tunePtCone_stat" :   getObjFromFile(filepath_elec_tunePtCone,"Fakerate_v3_stat"),
                "tunePtConeMC"      :   getObjFromFile(filepath_elec_tunePtConeMC,"Fakerate_MC"),
                "tunePtConeMC_stat" :   getObjFromFile(filepath_elec_tunePtConeMC,"Fakerate_MC_stat"),                
            },
        }
    
    def getFactor(self, pdgId, pt, eta_, unc='sys', sigma=0):
        # Set boundaries
        eta = abs(eta_)
        if eta > 2.39:
            eta = 2.39 
        if pt > 100:
            pt = 100
                        
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
        error = 0.0
        if uncert == "stat":
            error = self.SFmaps[lepton][self.mode+"_stat"].GetBinContent(ptbin, etabin)
        # print fakerate, "+-", error*sigma
        return fakerate + error*sigma
