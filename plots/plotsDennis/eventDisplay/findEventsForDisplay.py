import ROOT, os
from RootTools.core.standard             import *
from Analysis.Tools.helpers              import deltaPhi, deltaR
from tWZ.Tools.cutInterpreter            import cutInterpreter
import numpy as np

def printEventProperties(event):
    print("--------------------------------------------------------------------")
    print("  Lepton 1: pt = %.2f, eta = %.2f, pdgId = %i"%(event.l1_pt, event.l1_eta, event.lep_pdgId[event.l1_index]))
    print("  Lepton 2: pt = %.2f, eta = %.2f, pdgId = %i"%(event.l2_pt, event.l2_eta, event.lep_pdgId[event.l2_index]))
    print("  Lepton 3: pt = %.2f, eta = %.2f, pdgId = %i"%(event.l3_pt, event.l3_eta, event.lep_pdgId[event.l3_index]))
    print("  Z cand: pt = %.2f, mass = %.2f"%(event.Z1_pt, event.Z1_mass))
    print("  Njets = %i"%(event.nJetGood))

    print("  Run = %i, lumiBlock = %i, event = %i" %(int(event.run), int(event.luminosityBlock), int(event.event)))



from tWZ.samples.nanoTuples_ULRunII_nanoAODv9_postProcessed import *
sample = eval("Run2018")

read_variables = [
    "weight/F", "year/I", "preVFP/O", "met_pt/F", "met_phi/F", "nJetGood/I", "PV_npvsGood/I",  "nJet/I", "nBTag/I",
    "l1_pt/F", "l1_eta/F" , "l1_phi/F", "l1_mvaTOP/F", "l1_mvaTOPv2/F", "l1_mvaTOPWP/I", "l1_mvaTOPv2WP/I", "l1_index/I", "l1_passFO/O", "l1_passTight/O", "l1_ptCone/F", "l1_ptConeGhent/F",
    "l2_pt/F", "l2_eta/F" , "l2_phi/F", "l2_mvaTOP/F", "l2_mvaTOPv2/F", "l2_mvaTOPWP/I", "l2_mvaTOPv2WP/I", "l2_index/I", "l2_passFO/O", "l2_passTight/O", "l2_ptCone/F", "l2_ptConeGhent/F",
    "l3_pt/F", "l3_eta/F" , "l3_phi/F", "l3_mvaTOP/F", "l3_mvaTOPv2/F", "l3_mvaTOPWP/I", "l3_mvaTOPv2WP/I", "l3_index/I", "l3_passFO/O", "l3_passTight/O", "l3_ptCone/F", "l3_ptConeGhent/F",
    "l4_pt/F", "l4_eta/F" , "l4_phi/F", "l4_mvaTOP/F", "l4_mvaTOPv2/F", "l4_mvaTOPWP/I", "l4_mvaTOPv2WP/I", "l4_index/I", "l4_passFO/O", "l4_passTight/O", "l4_ptCone/F", "l4_ptConeGhent/F",
    "JetGood[pt/F,eta/F,phi/F,area/F,btagDeepB/F,btagDeepFlavB/F,index/I,jetId/I]",
    "Jet[pt/F,eta/F,phi/F,mass/F,btagDeepFlavB/F,jetId/I]",
    "lep[pt/F,eta/F,phi/F,pdgId/I,muIndex/I,eleIndex/I,mediumId/O,ptCone/F,ptConeGhent/F,mvaTOPv2WP/I,jetBTag/F,sip3d/F,pfRelIso03_all/F,passFO/O,passTight/O]",
    "Z1_l1_index/I", "Z1_l2_index/I", "nonZ1_l1_index/I", "nonZ1_l2_index/I",
    "Z1_phi/F", "Z1_pt/F", "Z1_mass/F", "Z1_cosThetaStar/F", "Z1_eta/F", "Z1_lldPhi/F", "Z1_lldR/F",
    "Muon[pt/F,eta/F,phi/F,dxy/F,dz/F,ip3d/F,sip3d/F,jetRelIso/F,miniPFRelIso_all/F,pfRelIso03_all/F,mvaTTH/F,pdgId/I,segmentComp/F,nStations/I,nTrackerLayers/I,mediumId/O,tightId/O,isPFcand/B,isTracker/B,isGlobal/B]",
    "Electron[pt/F,eta/F,phi/F,dxy/F,dz/F,ip3d/F,sip3d/F,jetRelIso/F,miniPFRelIso_all/F,pfRelIso03_all/F,mvaTTH/F,pdgId/I,vidNestedWPBitmap/I,deltaEtaSC/F,convVeto/O,lostHits/b]",

    "run/i",
    "luminosityBlock/i",
    "event/l",
]

selection_string = "trilepT-minDLmass12-onZ1-njet3p-btag1p"



r = sample.treeReader( variables = read_variables, sequence = [], selectionString = cutInterpreter.cutString(selection_string) )
r.start()
eventCount = 0
count_threshold = 10000
while r.run():
    event = r.event

    if event.nBTag != 2:
        continue
    pdgId_list = [abs(event.lep_pdgId[event.l1_index]), abs(event.lep_pdgId[event.l2_index]), abs(event.lep_pdgId[event.l3_index]) ]
    if pdgId_list.count(11) != 2 or  pdgId_list.count(13) != 1:
        continue
    if abs(event.Z1_mass-91) > 5:
        continue
    if event.l3_pt < 30:
        continue
    if event.nJetGood != 4:
        continue
    printEventProperties(event)

    ############################################################################
    eventCount+=1
    if eventCount >= count_threshold:
        count_threshold += 10000
        print "Processed", eventCount, "events"
