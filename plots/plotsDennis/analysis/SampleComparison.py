#!/usr/bin/env python
''' Analysis script for standard plots
'''
#
# Standard imports and batch mode
#
import ROOT, os
ROOT.gROOT.SetBatch(True)
c1 = ROOT.TCanvas() # do this to avoid version conflict in png.h with keras import ...
c1.Draw()
c1.Print('delete.png')
import itertools
import copy
import array
import operator
from math                                import sqrt, cos, sin, pi, atan2, cosh, exp

# RootTools
from RootTools.core.standard             import *

# MyRootTools
from MyRootTools.ttbarReconstruction.ttbarReco  import ttbarReco


# tWZ
from tWZ.Tools.user                      import plot_directory
from tWZ.Tools.cutInterpreter            import cutInterpreter
from tWZ.Tools.objectSelection_UL        import lepString, lepStringNoMVA
from tWZ.Tools.helpers                   import getCollection, cosThetaStarNew, getTheta, gettheta, getphi
from tWZ.Tools.leptonSF_topMVA           import leptonSF_topMVA

# Analysis
from Analysis.Tools.helpers              import deltaPhi, deltaR
from Analysis.Tools.puProfileCache       import *
from Analysis.Tools.puReweighting        import getReweightingFunction
from Analysis.Tools.leptonJetArbitration     import cleanJetsAndLeptons
from Analysis.Tools.WeightInfo           import WeightInfo

import Analysis.Tools.syncer
import numpy as np

################################################################################
# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--noData',         action='store_true', default=False, help='also plot data?')
argParser.add_argument('--small',          action='store_true', help='Run only on a small subset of the data?', )
#argParser.add_argument('--sorting',       action='store', default=None, choices=[None, "forDYMB"],  help='Sort histos?', )
argParser.add_argument('--dataMCScaling',  action='store_true', help='Data MC scaling?', )
argParser.add_argument('--plot_directory', action='store', default='SampleComparison_v1')
argParser.add_argument('--era',            action='store', type=str, default="UL2018")
argParser.add_argument('--selection',      action='store', default='trilepVL-minDLmass12-onZ1-njet4p-btag1p')
argParser.add_argument('--sys',            action='store', default='central')
argParser.add_argument('--nicePlots',      action='store_true', default=False)
argParser.add_argument('--twoD',           action='store_true', default=False)
argParser.add_argument('--triplet',        action='store_true', default=False)
argParser.add_argument('--doTTbarReco',    action='store_true', default=False)
args = argParser.parse_args()

################################################################################
# Logger
import tWZ.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

################################################################################
# Possible SYS variations
variations = [
    "Trigger_UP", "Trigger_DOWN",
    "LepID_UP", "LepID_DOWN",
    "BTag_b_UP", "BTag_b_DOWN",
    "BTag_l_UP", "BTag_l_DOWN",
    "PU_UP", "PU_DOWN",
    "JES_UP", "JES_DOWN",
]

jet_variations = {
    "JES_UP": "jesTotalUp",
    "JES_DOWN": "jesTotalDown",
    "JER_UP": "jerUp",
    "JER_DOWN": "jerDown",
}
################################################################################
# Check if we know the variation else don't use data!
if args.sys not in variations:
    if args.sys == "central":
        logger.info( "Running central samples (no sys variation)")
    else:
        raise RuntimeError( "Variation %s not among the known: %s", args.sys, ",".join( variations ) )
else:
    logger.info( "Running sys variation %s, noData is set to 'True'", args.sys)
    args.noData = True


################################################################################
# Some info messages
if args.small:                        args.plot_directory += "_small"
if args.sys is not 'central':         args.plot_directory += "_%s" %(args.sys)


logger.info( "Working in era %s", args.era)
if args.dataMCScaling:
    logger.info( "Data/MC scaling active")
else:
    logger.info( "Data/MC scaling not active")

if args.nicePlots:
    logger.info( "Only draw the plots")
else:
    logger.info( "Only saving into root file")

if args.twoD:
    logger.info( "Create EFT points in 2D")
else:
    logger.info( "Create EFT points in 1D")


################################################################################
# Selection modifier
def jetSelectionModifier( sys, returntype = "func"):
    #Need to make sure all jet variations of the following observables are in the ntuple
    variiedJetObservables = ['nJetGood', 'nBTag', 'met_pt']
    if returntype == "func":
        def changeCut_( string ):
            for s in variiedJetObservables:
                string = string.replace(s, s+'_'+sys)
                if "met_pt" in string:
                    string = string.replace("met_pt", "MET_T1_pt")
            return string
        return changeCut_
    elif returntype == "list":
        list = []
        for v in variiedJetObservables:
            string = v+'_'+sys
            if "met_pt" in string:
                string = string.replace("met_pt", "MET_T1_pt")
            list.append(string)    
        return list

def metSelectionModifier( sys, returntype = 'func'):
    #Need to make sure all MET variations of the following observables are in the ntuple
    variiedMetObservables = ['met_pt']
    if returntype == "func":
        def changeCut_( string ):
            for s in variiedMetObservables:
                string = string.replace(s, s+'_'+sys)
                if "met_pt" in string:
                    string = string.replace("met_pt", "MET_T1_pt")
            return string
        return changeCut_
    elif returntype == "list":
        list = []
        for v in variiedMetObservables:
            string = v+'_'+sys
            if "met_pt" in string:
                string = string.replace("met_pt", "MET_T1_pt")
            list.append(string)    
        return list

################################################################################
# Add a selection selectionModifier

if args.sys in jet_variations.keys():
    selectionModifier = jetSelectionModifier(jet_variations[args.sys])
else:
    selectionModifier = None

################################################################################
# Define the MC samples
from tWZ.samples.nanoTuples_ULRunII_nanoAODv9_postProcessed import *
import tWZ.samples.nanoTuples_Autumn18_nanoAODv6_private_SMEFTsim_fast_postProcessed as SMEFTsim_fast
import tWZ.samples.nanoTuples_RunII_nanoAODv6_private_postProcessed as EOY

if args.era == "UL2016":
    mc = [UL2016.TTZ]
    signals = []
elif args.era == "UL2016preVFP":
    mc = [UL2016preVFP.TTZ]
    signals = []
elif args.era == "UL2017":
    mc = [UL2017.TTZ]
    signals = []
elif args.era == "UL2018":
    mc = [UL2018.TTZ]
    signals = [SMEFTsim_fast.ttZ01j_lepWFilter, SMEFTsim_fast.ttZ01j, EOY.TTZ]
elif args.era == "ULRunII":
    mc = [TTZ]
    signals = []



# Creating a list of weights
plotweights = []
# Add MC weights
weight_mc = []
for sample in mc:
    weight_ = lambda event, sample: 1. # Add event.weight and lumi weight to sample.weight later
    weight_mc.append(weight_)
plotweights.append(weight_mc)


# Add signal weight
weight_sig = []
for sample in signals:
    weight_ = lambda event, sample: 1. # Add event.weight and lumi weight to sample.weight later
    weight_sig.append(weight_)
plotweights.append(weight_sig)

################################################################################
# Define the data sample
if   args.era == "UL2016": 
    datastring = "Run2016"
    lumistring = "2016"
elif args.era == "UL2016preVFP": 
    datastring = "Run2016_preVFP"
    lumistring = "2016_preVFP"
elif args.era == "UL2017": 
    datastring = "Run2017"
    lumistring = "2017"
elif args.era == "UL2018": 
    datastring = "Run2018"
    lumistring = "2018"
elif args.era == "ULRunII":
    datastring = "RunII"
    lumistring = "RunII"



lumi_scale                 = lumi_year[lumistring]/1000.

# Set up MC sample
for sample in mc+signals:
    sample.scale           = 1


if args.small:
    for sample in mc + signals:
        sample.normalization = 1.
        sample.reduceFiles( to = 1 )
        sample.scale /= sample.normalization
        
################################################################################
# Lepton SF
LeptonWP = "tight"
if "trilepVL" in args.selection:
    LeptonWP = "VL"
leptonSF16 = leptonSF_topMVA(2016, LeptonWP)
leptonSF17 = leptonSF_topMVA(2017, LeptonWP)
leptonSF18 = leptonSF_topMVA(2018, LeptonWP)

################################################################################
# Text on the plots
tex = ROOT.TLatex()
tex.SetNDC()
tex.SetTextSize(0.04)
tex.SetTextAlign(11) # align right

################################################################################
# Functions needed specifically for this analysis routine

def drawObjects( plotData, dataMCScale, lumi_scale ):
    lines = [
      (0.15, 0.95, 'CMS Preliminary' if plotData else 'CMS Simulation'),
      (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV) Scale %3.2f'% ( lumi_scale, dataMCScale ) ) if plotData else (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV)' % lumi_scale)
    ]
    return [tex.DrawLatex(*l) for l in lines]

def drawPlots(plots, mode, dataMCScale):
    for log in [False, True]:
        plot_directory_ = os.path.join(plot_directory, 'analysisPlots', args.plot_directory, args.era, mode + ("_log" if log else ""), args.selection)
        for plot in plots:
            if not max(l.GetMaximum() for l in sum(plot.histos,[])): continue # Empty plot

            _drawObjects = []
            n_stacks=len(plot.histos)
            if isinstance( plot, Plot):
                plotting.draw(plot,
                  plot_directory = plot_directory_,
                  ratio = None,
                  logX = False, logY = log, sorting = True,
                  yRange = (0.03, "auto") if log else (0.001, "auto"),
                  scaling = {0:1} if args.dataMCScaling else {},
                  legend = ( (0.18,0.88-0.03*sum(map(len, plot.histos)),0.9,0.88), 2),
                  drawObjects = drawObjects( False, dataMCScale , lumi_scale ) + _drawObjects,
                  copyIndexPHP = True, extensions = ["png", "pdf", "root"],
                )

def getDeepJetsWP(disc,year):
    WP_L = {2016:0.0614, 2017:0.0521, 2018:0.0494}
    WP_M = {2016:0.3093, 2017:0.3033, 2018:0.2770}
    WP_T = {2016:0.7221, 2017:0.7489, 2018:0.7264}
    wp = 0
    if disc > WP_L[year]: wp = 1
    if disc > WP_M[year]: wp = 2
    if disc > WP_T[year]: wp = 3
    return wp

def getClosestBJetindex( event, object, minBtagValue ):
    minDR = 100
    closestjet = ROOT.TLorentzVector()
    for i in range(event.nJetGood):
        btagscore = event.JetGood_btagDeepFlavB[i]
        if btagscore > minBtagValue:
            jet = ROOT.TLorentzVector()
            jetidx = event.JetGood_index[i]
            jet.SetPtEtaPhiM(event.Jet_pt[jetidx], event.Jet_eta[jetidx], event.Jet_phi[jetidx], event.Jet_mass[jetidx])
            if object.DeltaR(jet) < minDR:
                minDR = object.DeltaR(jet)
                closestjet = jet
    return closestjet

def getWlep( event ):
    Wlep = ROOT.TLorentzVector()
    lepton  = ROOT.TLorentzVector()
    met     = ROOT.TLorentzVector()
    lepton.SetPtEtaPhiM(event.lep_pt[event.nonZ1_l1_index], event.lep_eta[event.nonZ1_l1_index], event.lep_phi[event.nonZ1_l1_index], 0)
    met.SetPtEtaPhiM(event.met_pt, 0, event.met_phi, 0)

    lepton_pT = ROOT.TVector3(lepton.Px(), lepton.Py(), 0)
    neutrino_pT = ROOT.TVector3(met.Px(), met.Py(), 0)

    mass_w = 80.399
    mu = mass_w * mass_w / 2 + lepton_pT * neutrino_pT
    A = - (lepton_pT * lepton_pT)
    B = mu * lepton.Pz()
    C = mu * mu - lepton.E() * lepton.E() * (neutrino_pT * neutrino_pT)
    discriminant = B * B - A * C
    neutrinos = []
    if discriminant <= 0:
        # Take only real part of the solution for pz:
        neutrino = ROOT.TLorentzVector()
        neutrino.SetPxPyPzE(met.Px(),met.Py(),-B / A,0)
        neutrino.SetE(neutrino.P())
        neutrinos.append(neutrino)
    else:
        discriminant = sqrt(discriminant)
        neutrino1 = ROOT.TLorentzVector()
        neutrino1.SetPxPyPzE(met.Px(),met.Py(),(-B - discriminant) / A,0)
        neutrino1.SetE(neutrino1.P())
        neutrino2 = ROOT.TLorentzVector()
        neutrino2.SetPxPyPzE(met.Px(),met.Py(),(-B + discriminant) / A,0)
        neutrino2.SetE(neutrino2.P())
        if neutrino1.E() > neutrino2.E():
            neutrinos.append(neutrino1)
            neutrinos.append(neutrino2)
        else:
            neutrinos.append(neutrino2)
            neutrinos.append(neutrino1)

    Wleps = []
    for neu in neutrinos:
        Wlep = lepton + neu
        Wleps.append([Wlep, lepton, neu])
    return Wleps
################################################################################
# Define sequences
sequence       = []

# def readWeights(sample,event):
#     if event.year == 2016 and not event.preVFP:
#         yearstring = "2016"
#     elif event.year == 2016 and event.preVFP:
#         yearstring = "2016_preVFP"
#     elif event.year == 2017:
#         yearstring = "2017"
#     elif event.year == 2018:
#         yearstring = "2018"
#     lumi_weight = lumi_year[yearstring]/1000.
# 
#     print "-------------------------"
#     print "Weight  =", event.weight
#     print "Lumi    =", lumi_weight
#     return
# 
# sequence.append(readWeights)

def getLeptonSF(sample, event):
    if sample.isData:
        return 
    SF = 1    
    # Search for variation
    sigma = 0
    if args.sys == "LepID_UP":
        sigma = 1
    elif args.sys == "LepID_DOWN":
        sigma = -1
    # Go through the 3 leptons and multiply SF
    idx1 = event.l1_index
    idx2 = event.l2_index
    idx3 = event.l3_index
    for i in [idx1, idx2, idx3]:
        pdgId = event.lep_pdgId[i]
        eta = event.lep_eta[i]
        if abs(pdgId)==11:
            eta+=event.Electron_deltaEtaSC[event.lep_eleIndex[i]]
        pt = event.lep_pt[i]
        if event.year == 2016:
            SF *= leptonSF16.getSF(pdgId, pt, eta, "sys", sigma )
        elif event.year == 2017:
            SF *= leptonSF17.getSF(pdgId, pt, eta, "sys", sigma )
        elif event.year == 2018:
            SF *= leptonSF18.getSF(pdgId, pt, eta, "sys", sigma )
    event.reweightLeptonMVA = SF
sequence.append( getLeptonSF )

# def getSYSweight(sample, event):
#     print event.LHEScaleWeight[0], event.LHEScaleWeight[4], event.LHEScaleWeight[8]
# sequence.append( getSYSweight )

def getMlb(sample, event):
    lepton = ROOT.TLorentzVector()
    if not 'nLeptons4' in args.selection:
        lepton.SetPtEtaPhiM(event.lep_pt[event.nonZ1_l1_index], event.lep_eta[event.nonZ1_l1_index], event.lep_phi[event.nonZ1_l1_index], 0)
    else:
        lepton.SetPtEtaPhiM(0,0,0,0)

    # Get closest tight b:
    minBtagValue = 0.7221
    if   event.year == 2017: minBtagValue = 0.7489
    elif event.year == 2018: minBtagValue = 0.7264
    closestjet = ROOT.TLorentzVector()
    closestjet = getClosestBJetindex( event, lepton, minBtagValue )
    combination = closestjet + lepton
    event.mlb = combination.M()
sequence.append( getMlb )

def getCosThetaStar(sample, event):
    lepton = ROOT.TLorentzVector()
    Z = ROOT.TLorentzVector()
    Z.SetPtEtaPhiM(event.Z1_pt, event.Z1_eta, event.Z1_phi, event.Z1_mass)
    idx_l1 = event.Z1_l1_index
    idx_l2 = event.Z1_l2_index
    if abs(event.lep_pdgId[idx_l1]) == 11:
        lepmass = 0.0005
    elif abs(event.lep_pdgId[idx_l1]) == 13:
        lepmass = 0.1
    elif abs(event.lep_pdgId[idx_l1]) == 15:
        lepmass = 1.777
    else:
        print "Z does not decay into leptons"
        lepmass = 0

    charge_l1 = event.lep_pdgId[idx_l1]/abs(event.lep_pdgId[idx_l1])
    charge_l2 = event.lep_pdgId[idx_l2]/abs(event.lep_pdgId[idx_l2])
    if charge_l1 < 0 and charge_l2 > 0:
        lepton.SetPtEtaPhiM(event.lep_pt[idx_l1], event.lep_eta[idx_l1], event.lep_phi[idx_l1], lepmass)

    event.cosThetaStar = cosThetaStarNew(lepton, Z)
sequence.append( getCosThetaStar )

def getDiBosonAngles(sample, event):
    lep1,lep2,boson = ROOT.TLorentzVector(),ROOT.TLorentzVector(),ROOT.TLorentzVector()
    # Get lep1 and lep2 from Z boson
    idx_l1 = event.Z1_l1_index
    idx_l2 = event.Z1_l2_index
    if abs(event.lep_pdgId[idx_l1]) == 11:
        lepmass = 0.0005
    elif abs(event.lep_pdgId[idx_l1]) == 13:
        lepmass = 0.1
    elif abs(event.lep_pdgId[idx_l1]) == 15:
        lepmass = 1.777
    else:
        print "Z does not decay into leptons"
        lepmass = 0
    lep1.SetPtEtaPhiM(event.lep_pt[idx_l1], event.lep_eta[idx_l1], event.lep_phi[idx_l1], lepmass)
    lep2.SetPtEtaPhiM(event.lep_pt[idx_l2], event.lep_eta[idx_l2], event.lep_phi[idx_l2], lepmass)

    # For 2nd boson distinguish between cases
    if "nLeptons4" in args.selection:
        boson.SetPtEtaPhiM(event.Z2_pt, event.Z2_eta, event.Z2_phi, event.Z2_mass)
    elif "deepjet0" in args.selection:
        Wleps = getWlep(event)
        if len(Wleps) == 1:
            boson = Wleps[0][0]
        elif len(Wleps) == 2:
            boson = Wleps[0][0] if Wleps[0][0].Pt()>Wleps[1][0].Pt() else Wleps[1][0]
        else:
            print "[ERROR] getWlep should not return more than 2 options"
    else:
        boson.SetPtEtaPhiM(0,0,0,0)

    event.Theta = getTheta(lep1, lep2, boson)
    event.theta = gettheta(lep1, lep2, boson)
    event.phi = getphi(lep1, lep2, boson)
sequence.append( getDiBosonAngles )

# def getZorigin(event, sample):
#     pdgIds = []
#     mothersFound = []
#     productionModeWZ = 0
#     if sample.name != "data":
#         for i in range(event.nGenPart):
#             if i == 2 and abs(event.GenPart_pdgId[i])==24:
#                 productionModeWZ=1
#             if event.GenPart_pdgId[i] == 23:
#                 i_mother = event.GenPart_genPartIdxMother[i]
#                 Id_mother = event.GenPart_pdgId[i_mother]
#                 # If mother is still a Z, go further back until pdgId != 23
#                 if Id_mother == 23:
#                     foundMother = False
#                     while not foundMother:
#                         i_tmp = i_mother
#                         i_mother = event.GenPart_genPartIdxMother[i_tmp]
#                         Id_mother = event.GenPart_pdgId[i_mother]
#                         if Id_mother != 23:
#                             foundMother = True
#                 if i_mother not in mothersFound:
#                     pdgIds.append(Id_mother)
#                     mothersFound.append(i_mother)
#     event.MotherIds = pdgIds
#     event.Nmothers = len(pdgIds)
#     event.productionModeWZ = productionModeWZ
#     MotherList = []
#     # 0 = other
#     # 1,2,3 = 1st, 2nd, 3rd Generation Quarks
#     # 4 = W/Z/Higgs, 5 = Gluon, 6 = Lepton
#     for id in pdgIds:
#         if abs(id)==1 or abs(id)==2: # 1st gen
#             MotherList.append(1)
#         elif abs(id)==3 or abs(id)==4: # 2nd gen
#             MotherList.append(2)
#         elif abs(id)==5 or abs(id)==6: #3rd gen
#             MotherList.append(3)
#         elif abs(id)>=11 and abs(id)<=16: # lepton
#             MotherList.append(6)
#         elif abs(id)==9 or abs(id)==21: # gluon
#             MotherList.append(5)
#         elif abs(id)>=22 and abs(id)<=25: # W/Z/H
#             MotherList.append(4)
#         else:
#             MotherList.append(0)
#     event.MotherIdList = MotherList
# 
#     production = -1
#     if sample.name != "data":
#         ID1 = abs(event.GenPart_pdgId[0])
#         ID2 = abs(event.GenPart_pdgId[1])
#         if   ID1 in [1,2] and ID2 in [1,2]: production = 1
#         elif ID1 in [3,4] and ID2 in [3,4]: production = 2
#         elif ID1 in [5,6] and ID2 in [5,6]: production = 3
#         elif (ID1==21 and ID2 in [1,2]) or (ID2==21 and ID1 in [1,2]): production = 4
#         elif (ID1==21 and ID2 in [3,4]) or (ID2==21 and ID1 in [3,4]): production = 5
#         elif (ID1==21 and ID2 in [5,6]) or (ID2==21 and ID1 in [5,6]): production = 6
#         elif ID1==21 and ID2==21: production = 7
#         else: production = 0
#     event.productionMode = production
# sequence.append(getZorigin)

def getM3l( event, sample ):
    l = []
    for i in range(3):
        l.append(ROOT.TLorentzVector())
        l[i].SetPtEtaPhiM(event.lep_pt[i], event.lep_eta[i], event.lep_phi[i],0)
    event.m3l = (l[0] + l[1] + l[2]).M()
sequence.append( getM3l )


def getTTbarReco( event, sample ):
    event.mtophad = float('nan')
    event.mtoplep = float('nan')
    event.minimax = float('nan')
    event.chi2 = float('nan')
    
    if args.doTTbarReco and event.nJetGood>=4:
        lepton = ROOT.TLorentzVector()
        met    = ROOT.TLorentzVector()
        lepton.SetPtEtaPhiM(event.lep_pt[event.nonZ1_l1_index], event.lep_eta[event.nonZ1_l1_index], event.lep_phi[event.nonZ1_l1_index], 0)
        met.SetPtEtaPhiM(event.met_pt, 0, event.met_phi, 0)
        jets = []
        Njetsmax = 6
        if event.nJetGood < Njetsmax:
            Njetsmax = event.nJetGood
        for i in range(Njetsmax):
            jet = ROOT.TLorentzVector()
            jetidx = event.JetGood_index[i]
            jet.SetPtEtaPhiM(event.Jet_pt[jetidx], event.Jet_eta[jetidx], event.Jet_phi[jetidx], event.Jet_mass[jetidx])
            jets.append(jet)
        reco = ttbarReco(lepton, met, jets)
        reco.reconstruct()
        best_hypothesis = reco.best_hypothesis
        minimax = reco.minimax
        if best_hypothesis:
            event.mtophad = best_hypothesis['toplep'].M()
            event.mtoplep = best_hypothesis['tophad'].M()
            event.chi2 = best_hypothesis['chi2']
        if minimax:
            event.minimax = minimax
sequence.append( getTTbarReco )

################################################################################
# Read variables

read_variables = [
    "weight/F", "year/I", "preVFP/O", "met_pt/F", "met_phi/F", "nJetGood/I", "PV_npvsGood/I",  "nJet/I", "nBTag/I", 
    "l1_pt/F", "l1_eta/F" , "l1_phi/F", "l1_mvaTOP/F", "l1_mvaTOPv2/F", "l1_mvaTOPWP/I", "l1_mvaTOPv2WP/I", "l1_index/I",
    "l2_pt/F", "l2_eta/F" , "l2_phi/F", "l2_mvaTOP/F", "l2_mvaTOPv2/F", "l2_mvaTOPWP/I", "l2_mvaTOPv2WP/I", "l2_index/I",
    "l3_pt/F", "l3_eta/F" , "l3_phi/F", "l3_mvaTOP/F", "l3_mvaTOPv2/F", "l3_mvaTOPWP/I", "l3_mvaTOPv2WP/I", "l3_index/I",
    "JetGood[pt/F,eta/F,phi/F,area/F,btagDeepB/F,btagDeepFlavB/F,index/I]",
    "Jet[pt/F,eta/F,phi/F,mass/F,btagDeepFlavB/F]",
    "lep[pt/F,eta/F,phi/F,pdgId/I,muIndex/I,eleIndex/I,mediumId/O]",
    "Z1_l1_index/I", "Z1_l2_index/I", "nonZ1_l1_index/I", "nonZ1_l2_index/I",
    "Z1_phi/F", "Z1_pt/F", "Z1_mass/F", "Z1_cosThetaStar/F", "Z1_eta/F", "Z1_lldPhi/F", "Z1_lldR/F",
    "Muon[pt/F,eta/F,phi/F,dxy/F,dz/F,ip3d/F,sip3d/F,jetRelIso/F,miniPFRelIso_all/F,pfRelIso03_all/F,mvaTTH/F,pdgId/I,segmentComp/F,nStations/I,nTrackerLayers/I,mediumId/O,tightId/O,isPFcand/B,isTracker/B,isGlobal/B]",
    "Electron[pt/F,eta/F,phi/F,dxy/F,dz/F,ip3d/F,sip3d/F,jetRelIso/F,miniPFRelIso_all/F,pfRelIso03_all/F,mvaTTH/F,pdgId/I,vidNestedWPBitmap/I,deltaEtaSC/F]",
]

if "nLeptons4" in args.selection:
    read_variables.append("Z2_phi/F")
    read_variables.append("Z2_pt/F")
    read_variables.append("Z2_eta/F")
    read_variables.append("Z2_mass/F")

read_variables_MC = [
    "weight/F", 'reweightBTag_SF/F', 'reweightPU/F', 'reweightL1Prefire/F', 'reweightTrigger/F',
    "genZ1_pt/F", "genZ1_eta/F", "genZ1_phi/F",
    "Muon[genPartFlav/I]",
    VectorTreeVariable.fromString( "GenPart[pt/F,mass/F,phi/F,eta/F,pdgId/I,genPartIdxMother/I,status/I,statusFlags/I]", nMax=1000),
    'nGenPart/I',
    # 'LHEScaleWeight/F',
]

read_variables_eft = [
    "np/I", VectorTreeVariable.fromString("p[C/F]",nMax=200)
]


################################################################################
# MVA

################################################################################
# define 3l selections
if "lepVeto" in args.selection:
    mu_string  = lepString('mu','VL')
else:
    mu_string  = lepString('mu','T') + "&&lep_mediumId"
    
ele_string = lepString('ele','T')

# print mu_string
# print ele_string
def getLeptonSelection( mode ):
    if   mode=="mumumu":   return "Sum$({mu_string})==3&&Sum$({ele_string})==0".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="mumue":    return "Sum$({mu_string})==2&&Sum$({ele_string})==1".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="muee":     return "Sum$({mu_string})==1&&Sum$({ele_string})==2".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="eee":      return "Sum$({mu_string})==0&&Sum$({ele_string})==3".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="mumumumu": return "Sum$({mu_string})==4&&Sum$({ele_string})==0".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="mumuee":   return "Sum$({mu_string})==2&&Sum$({ele_string})==2".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="eeee":     return "Sum$({mu_string})==0&&Sum$({ele_string})==4".format(mu_string=mu_string,ele_string=ele_string)

################################################################################
# Set up channels and values for plotting
yields     = {}
allPlots   = {}
allPlots_SM= {}
allModes   = ['mumumu', 'mumue', 'muee', 'eee']
if 'nLeptons4' in args.selection:
    allModes = ['mumumumu','mumuee','eeee']

print "Working on channels:", allModes

for i_mode, mode in enumerate(allModes):
    yields[mode] = {}

    for sample in mc: sample.style = styles.fillStyle(sample.color)
    for i_sample, sample in enumerate(signals): 
        if   i_sample == 0: sample.style = styles.lineStyle(ROOT.kRed)
        elif i_sample == 2: sample.style = styles.lineStyle(ROOT.kGreen)  
        else              : sample.style = styles.lineStyle(ROOT.kAzure+7)  
        
    ###### SYS #################################################################
    if args.sys in jet_variations:
        new_variables = ['%s/F'%v for v in jetSelectionModifier(jet_variations[args.sys],'list')]
        read_variables_MC += new_variables
        read_variables    += new_variables

    # weightnames = ['weight', 'reweightBTag_SF', 'reweightPU', 'reweightL1Prefire' , 'reweightTrigger', 'reweightLeptonMVA']
    weightnames = ['weight']
    sys_weights = {
        "BTag_b_UP"     : ('reweightBTag_SF','reweightBTag_SF_b_Up'),
        "BTag_b_DOWN"   : ('reweightBTag_SF','reweightBTag_SF_b_Down'),
        "BTag_l_UP"     : ('reweightBTag_SF','reweightBTag_SF_l_Up'),
        "BTag_l_DOWN"   : ('reweightBTag_SF','reweightBTag_SF_l_Down'),
        'Trigger_UP'    : ('reweightTrigger','reweightTriggerUp'),
        'Trigger_DOWN'  : ('reweightTrigger','reweightTriggerDown'),
        'PU_UP'         : ('reweightPU','reweightPUUp'),
        'PU_DOWN'       : ('reweightPU','reweightPUDown'),
        # For lepton SF this is set in the sequence
    }

    if args.sys in sys_weights:
        oldname, newname = sys_weights[args.sys]
        for i, weight in enumerate(weightnames):
            if weight == oldname:
                weightnames[i] = newname
                read_variables_MC += ['%s/F'%(newname)]

    getters = map( operator.attrgetter, weightnames)
    def weight_function( event, sample):
        # Calculate weight, this becomes: w = event.weightnames[0]*event.weightnames[1]*...
        w = reduce(operator.mul, [g(event) for g in getters], 1)
        # Get Lumi weight and multiply to weight
        yearstring = ""
        if event.year == 2016 and not event.preVFP:
            yearstring = "2016"
        elif event.year == 2016 and event.preVFP:
            yearstring = "2016_preVFP"
        elif event.year == 2017:
            yearstring = "2017"
        elif event.year == 2018:
            yearstring = "2018"
        lumi_weight = lumi_year[yearstring]/1000.
        w *= lumi_weight
        return w


    for sample in mc+signals:
        sample.read_variables = read_variables_MC
        sample.setSelectionString([getLeptonSelection(mode)])
        sample.weight = weight_function


    stack = Stack(mc, signals)

    # Use some defaults
    selection_string = selectionModifier(cutInterpreter.cutString(args.selection)) if selectionModifier is not None else cutInterpreter.cutString(args.selection)
    Plot.setDefaults(stack = stack, weight = plotweights, selectionString = selection_string)

    ################################################################################
    # Now define the plots

    plots = []

    plots.append(Plot(
      name = 'yield', texX = '', texY = 'Number of Events',
      attribute = lambda event, sample: 0.5 + i_mode,
      binning=[4, 0, 4],
    ))

    plots.append(Plot(
        name = "Z1_pt",
        texX = 'p_{T}(Z_{1}) (GeV)', texY = 'Number of Events / 20 GeV',
        attribute = TreeVariable.fromString( "Z1_pt/F" ),
        binning=[50, 0, 1000],
    ))

    plots.append(Plot(
        name = "M3l",
        texX = 'M(3l) (GeV)', texY = 'Number of Events',
        attribute = lambda event, sample:event.m3l,
        binning=[25,0,500],
    ))
    
    plots.append(Plot(
        name = "l1_pt",
        texX = 'Leading lepton p_{T} (GeV)', texY = 'Number of Events / 40 GeV',
        attribute = TreeVariable.fromString( "l1_pt/F" ),
        binning=[25, 0, 1000],
    ))
    
    plots.append(Plot(
        name = "Z1_pt_rebin2",
        texX = 'p_{T}(Z_{1}) (GeV)', texY = 'Number of Events / 40 GeV',
        attribute = TreeVariable.fromString( "Z1_pt/F" ),
        binning=[25, 0, 1000],
    ))

    plots.append(Plot(
        name = "Z1_pt_rebin5",
        texX = 'p_{T}(Z_{1}) (GeV)', texY = 'Number of Events / 100 GeV',
        attribute = TreeVariable.fromString( "Z1_pt/F" ),
        binning=[10, 0, 1000],
    ))

    plots.append(Plot(
        name = "M_lb",
        texX = 'm_{lb} (GeV)', texY = 'Number of Events / 20 GeV',
        attribute = lambda event, sample: event.mlb,
        binning=[20, 0, 400],
    ))

    plots.append(Plot(
        name = "N_jets",
        texX = 'Number of jets', texY = 'Number of Events',
        attribute = lambda event, sample: event.nJetGood,
        binning=[16, -0.5, 15.5],
    ))
    
    plots.append(Plot(
        name = "N_bjets",
        texX = 'Number of b-tagged jets', texY = 'Number of Events',
        attribute = lambda event, sample: event.nBTag,
        binning=[16, -0.5, 15.5],
    ))
    

    plots.append(Plot(
        name = "CosThetaStar",
        texX = 'cos #theta*', texY = 'Number of Events',
        attribute = lambda event, sample: event.cosThetaStar,
        binning=[20, -1, 1],
    ))

    plots.append(Plot(
        name = "CosThetaStar_old",
        texX = 'cos #theta*', texY = 'Number of Events',
        attribute = lambda event, sample: event.Z1_cosThetaStar,
        binning=[20, -1, 1],
    ))

    plots.append(Plot(
        name = "theta",
        texX = '#theta', texY = 'Number of Events',
        attribute = lambda event, sample: event.theta,
        binning=[20, 0, pi],
    ))

    plots.append(Plot(
        name = "Theta",
        texX = '#Theta', texY = 'Number of Events',
        attribute = lambda event, sample: event.Theta,
        binning=[20, 0, pi],
    ))

    plots.append(Plot(
        name = "phi",
        texX = '#phi', texY = 'Number of Events',
        attribute = lambda event, sample: event.phi,
        binning=[20, -pi, pi],
    ))
    
    plots.append(Plot(
        name = "SF_Lepton",
        texX = 'Lepton SF', texY = 'Number of Events',
        attribute = lambda event, sample: event.reweightLeptonMVA if not sample.isData else -1,
        addOverFlowBin='both',
        binning=[50, 0.5, 1.5],
    ))

    plots.append(Plot(
        name = "SF_Btag",
        texX = 'b tagging SF', texY = 'Number of Events',
        attribute = lambda event, sample: event.reweightBTag_SF if not sample.isData else -1,
        addOverFlowBin='both',
        binning=[50, 0.5, 1.5],
    ))        
    
    plots.append(Plot(
        name = "SF_PU",
        texX = 'PU SF', texY = 'Number of Events',
        attribute = lambda event, sample: event.reweightPU if not sample.isData else -1,
        addOverFlowBin='both',
        binning=[50, 0.5, 1.5],
    ))              

    plots.append(Plot(
        name = "SF_L1",
        texX = 'L1 prefire SF', texY = 'Number of Events',
        attribute = lambda event, sample: event.reweightL1Prefire if not sample.isData else -1,
        addOverFlowBin='both',
        binning=[50, 0.5, 1.5],
    ))      
    
    plots.append(Plot(
        name = "SF_Trigger",
        texX = 'Trigger SF', texY = 'Number of Events',
        attribute = lambda event, sample: event.reweightTrigger if not sample.isData else -1,
        addOverFlowBin='both',
        binning=[50, 0.5, 1.5],
    ))              
    
    plots.append(Plot(
        name = "mvaTOPscore",
        texX = 'Leading lepton MVA score', texY = 'Number of Events',
        attribute = lambda event, sample: event.l1_mvaTOP,
        binning=[30, -1.5, 1.5],
    ))

    plots.append(Plot(
        name = "mvaTOPscore_v2",
        texX = 'Leading lepton MVA v2 score', texY = 'Number of Events',
        attribute = lambda event, sample: event.l1_mvaTOPv2,
        binning=[30, -1.5, 1.5],
    ))
                

    plotting.fill(plots, read_variables = read_variables, sequence = sequence)


    ################################################################################
    # Get normalization yields from yield histogram
    for plot in plots:
        if plot.name == "yield":
            for i, l in enumerate(plot.histos):
                for j, h in enumerate(l):
                    yields[mode][plot.stack[i][j].name] = h.GetBinContent(h.FindBin(0.5+i_mode))
                    if 'nLeptons4' in args.selection:
                        h.GetXaxis().SetBinLabel(1, "#mu#mu#mu#mu")
                        h.GetXaxis().SetBinLabel(2, "#mu#muee")
                        h.GetXaxis().SetBinLabel(3, "eeee")
                    else:
                        h.GetXaxis().SetBinLabel(1, "#mu#mu#mu")
                        h.GetXaxis().SetBinLabel(2, "#mu#mue")
                        h.GetXaxis().SetBinLabel(3, "#muee")
                        h.GetXaxis().SetBinLabel(4, "eee")

    yields[mode]["data"] = 0

    yields[mode]["MC"] = sum(yields[mode][s.name] for s in mc)
    dataMCScale        = yields[mode]["data"]/yields[mode]["MC"] if yields[mode]["MC"] != 0 else float('nan')


    drawPlots(plots, mode, dataMCScale)

    allPlots[mode] = plots


################################################################################
# Add all different channels
yields["all"] = {}
for y in yields[allModes[0]]:
    try:    yields["all"][y] = sum(yields[c][y] for c in allModes)
    except: yields["all"][y] = 0
dataMCScale = yields["all"]["data"]/yields["all"]["MC"] if yields["all"]["MC"] != 0 else float('nan')

allPlots["all"] = allPlots[allModes[0]]
for plot in allPlots['all']:
    for i_mode,mode in enumerate(allModes):
        if i_mode == 0:
            continue
        tmp = allPlots[mode]
        for plot2 in (p for p in tmp if p.name == plot.name):
            for i, j in enumerate(list(itertools.chain.from_iterable(plot.histos))):
                for k, l in enumerate(list(itertools.chain.from_iterable(plot2.histos))):
                    if i==k:
                        j.Add(l)


drawPlots(allPlots['all'], "all", dataMCScale)

logger.info( "Done with prefix %s and selectionString %s", args.selection, cutInterpreter.cutString(args.selection) )
