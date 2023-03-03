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
# from tWZ.Tools.leptonSF_topMVA           import leptonSF_topMVA
from tWZ.Tools.triggerPrescale           import triggerPrescale

# Analysis
from Analysis.Tools.helpers              import deltaPhi, deltaR
from Analysis.Tools.puProfileCache       import *
from Analysis.Tools.puReweighting        import getReweightingFunction
from Analysis.Tools.leptonJetArbitration     import cleanJetsAndLeptons
from Analysis.Tools.WeightInfo           import WeightInfo
from Analysis.Tools.LeptonSF_UL          import LeptonSF

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
argParser.add_argument('--plot_directory', action='store', default='FakeRate_v10')
argParser.add_argument('--era',            action='store', type=str, default="UL2018")
argParser.add_argument('--selection',      action='store', default='singlelepFO-vetoAddLepFO-vetoMET')
argParser.add_argument('--sys',            action='store', default='central')
argParser.add_argument('--channel',        action='store', default='muon')
argParser.add_argument('--noPreScale',     action='store_true')
argParser.add_argument('--prescalemode',   action='store', type=str, default="mine")
argParser.add_argument('--noLargeWeights', action='store_true')
argParser.add_argument('--reduce',         action='store_true')

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
    "PU_UP", "PU_DOWN",
    "JES_UP", "JES_DOWN",
    "Scale_UPUP", "Scale_UPNONE", "Scale_NONEUP", "Scale_NONEDOWN", "Scale_DOWNNONE", "Scale_DOWNDOWN",
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
if args.noData:                       args.plot_directory += "_noData"
if args.prescalemode == "ghent":      args.plot_directory += "_GHENTprescale"
if args.prescalemode == "bril":       args.plot_directory += "_BRILprescale"
if args.noPreScale:                   args.plot_directory += "_noPreScale"
if args.noLargeWeights:               args.plot_directory += "_noLargeWeights"
if args.reduce:                       args.plot_directory += "_reduce"
if args.sys is not 'central':         args.plot_directory += "_%s" %(args.sys)


logger.info( "Working in era %s", args.era)
if args.dataMCScaling:
    logger.info( "Data/MC scaling active")
else:
    logger.info( "Data/MC scaling not active")

if args.noData:
    logger.info( "Running without data")
else:
    logger.info( "Data included in analysis cycle")

if args.channel == "muon":
    logger.info( "Running MUON channel")
elif args.channel == "elec":
    logger.info( "Running ELECTRON channel")
else:
    logger.info( "Channel %s not defined!", args.channel)
    
################################################################################
# Define trigger list based on channel
triggerlist = []
if args.channel == "muon":
    triggerlist = ["HLT_Mu3_PFJet40","HLT_Mu8","HLT_Mu17","HLT_Mu20","HLT_Mu27"]
    # if args.era == "UL2016" or args.era == "UL2016preVFP":
    #     triggerlist = ["HLT_Mu3_PFJet40","HLT_Mu8","HLT_Mu17"]
elif args.channel == "elec":
    triggerlist = ["HLT_Ele8_CaloIdM_TrackIdM_PFJet30","HLT_Ele17_CaloIdM_TrackIdM_PFJet30"]
    
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
# get scale weight
def getScaleWeight(event, sys):
    # Sometimes the nominal entry [4] is missing, so be careful
    weights_9point = {
        "Scale_DOWNDOWN": 0,
        "Scale_DOWNNONE": 1,
        "Scale_NONEDOWN": 3,
        "Scale_NONEUP"  : 5,
        "Scale_UPNONE"  : 7,
        "Scale_UPUP"    : 8,
    }
    weights_8point = {
        "Scale_DOWNDOWN": 0,
        "Scale_DOWNNONE": 1,
        "Scale_NONEDOWN": 3,
        "Scale_NONEUP"  : 4,
        "Scale_UPNONE"  : 6,
        "Scale_UPUP"    : 7,
    }
    index = -1
    if event.nScale == 9:
        index = weights_9point[sys]
    elif event.nScale == 8:
        index = weights_8point[sys]
    else:
        print "UNEXPECTED NUMBER OF SCALE WEIGHTS:", event.nScale,", not applying any weight"
        return 1.0
    return event.Scale_Weight[index]
################################################################################
# Add a selection selectionModifier

if args.sys in jet_variations.keys():
    selectionModifier = jetSelectionModifier(jet_variations[args.sys])
else:
    selectionModifier = None

################################################################################
# Define the MC samples
from tWZ.samples.nanoTuples_ULRunII_nanoAODv9_postProcessed_singlelep import *

if args.era == "UL2016":
    if args.channel == "muon":
        mc = [UL2016.QCD_MuEnriched, UL2016.WZ, UL2016.ZZ, UL2016.WW, UL2016.TTbar, UL2016.DY, UL2016.WJetsToLNu]
    elif args.channel == "elec":
        mc = [UL2016.QCD_EMEnriched, UL2016.QCD_bcToE, UL2016.WZ, UL2016.ZZ, UL2016.WW, UL2016.TTbar, UL2016.DY, UL2016.WJetsToLNu]
elif args.era == "UL2016preVFP":
    if args.channel == "muon":
        mc = [UL2016preVFP.QCD_MuEnriched, UL2016preVFP.WZ, UL2016preVFP.ZZ, UL2016preVFP.WW, UL2016preVFP.TTbar, UL2016preVFP.DY, UL2016preVFP.WJetsToLNu]
    elif args.channel == "elec":
        mc = [UL2016preVFP.QCD_EMEnriched, UL2016preVFP.QCD_bcToE, UL2016preVFP.WZ, UL2016preVFP.ZZ, UL2016preVFP.WW, UL2016preVFP.TTbar, UL2016preVFP.DY, UL2016preVFP.WJetsToLNu]
elif args.era == "UL2017":
    if args.channel == "muon":
        mc = [UL2017.QCD_MuEnriched, UL2017.WZ, UL2017.ZZ, UL2017.WW, UL2017.TTbar, UL2017.DY, UL2017.WJetsToLNu]
    elif args.channel == "elec":
        mc = [UL2017.QCD_EMEnriched, UL2017.QCD_bcToE, UL2017.WZ, UL2017.ZZ, UL2017.WW, UL2017.TTbar, UL2017.DY, UL2017.WJetsToLNu]
elif args.era == "UL2018":
    if args.channel == "muon":
        mc = [UL2018.QCD_MuEnriched, UL2018.WZ, UL2018.ZZ, UL2018.WW, UL2018.TTbar, UL2018.DY, UL2018.WJetsToLNu]
    elif args.channel == "elec":
        mc = [UL2018.QCD_EMEnriched, UL2018.QCD_bcToE, UL2018.WZ, UL2018.ZZ, UL2018.WW, UL2018.TTbar, UL2018.DY, UL2018.WJetsToLNu]
elif args.era == "ULRunII":
    if args.channel == "muon":
        mc = [QCD_MuEnriched, WZ, ZZ, WW, TTbar, DY, WJetsToLNu]
    elif args.channel == "elec":
        mc = [QCD_EMEnriched, QCD_bcToE, WZ, ZZ, WW, TTbar, DY, WJetsToLNu]

################################################################################
# Binning for Maps
boundaries_pt = [0, 20, 30, 45, 120]
boundaries_eta = [0, 1.2, 2.1, 2.4]
if args.channel == "elec":
    boundaries_eta = [0, 0.8, 1.44, 2.4]
    

################################################################################
# Creating a list of weights
plotweights = []
weights_SM = []
# Add MC weights
weight_mc = []
for sample in mc:
    weight_ = lambda event, sample: 1. # Add event.weight and lumi weight to sample.weight later
    weight_mc.append(weight_)
plotweights.append(weight_mc)

# Add data weight
if not args.noData:
    plotweights.append([lambda event, sample: event.weight])

################################################################################
# Define the data sample

if args.channel == "muon":
    datastring = "SingleMuon_"
elif args.channel == "elec":
    datastring = "SingleElectron_"
    if args.era == "UL2018":
        datastring = "EGamma_"
    

if   args.era == "UL2016": 
    datastring += "Run2016"
    lumistring = "2016"
elif args.era == "UL2016preVFP": 
    datastring += "Run2016_preVFP"
    lumistring = "2016_preVFP"
elif args.era == "UL2017": 
    datastring += "Run2017"
    lumistring = "2017"
elif args.era == "UL2018": 
    datastring += "Run2018"
    lumistring = "2018"
elif args.era == "ULRunII":
    datastring += "RunII"
    lumistring = "RunII"


try:
  data_sample = eval(datastring)
except Exception as e:
  logger.error( "Didn't find %s", datastring )
  raise e

lumi_scale                 = lumi_year[lumistring]/1000.
data_sample.scale          = 1.

# Set up MC sample
for sample in mc:
    sample.scale           = 1

if args.small:
    for sample in mc + [data_sample]:
        sample.normalization = 1.
        sample.reduceFiles( to = 1 )
        sample.scale /= sample.normalization

if args.reduce:
    for sample in mc:
        if sample.name == "TTbar":
            sample.normalization = 1.
            sample.reduceFiles( factor = 10 )
            sample.scale /= sample.normalization
            
################################################################################
# Lepton SF
muonWP = "medium"
elecWP = "tight"

leptonSF = {
    "UL2016preVFP":  LeptonSF("UL2016_preVFP", muonWP, elecWP),
    "UL2016":        LeptonSF("UL2016",        muonWP, elecWP),
    "UL2017":        LeptonSF("UL2017",        muonWP, elecWP),
    "UL2018":        LeptonSF("UL2018",        muonWP, elecWP),
}



################################################################################
# Trigger prescale weights for MC
prescalemode = args.prescalemode
prescale16preVFP = triggerPrescale("UL2016preVFP", prescalemode)
prescale16       = triggerPrescale("UL2016", prescalemode)
prescale17       = triggerPrescale("UL2017", prescalemode)
prescale18       = triggerPrescale("UL2018", prescalemode)

################################################################################
# Text on the plots
tex = ROOT.TLatex()
tex.SetNDC()
tex.SetTextSize(0.04)
tex.SetTextAlign(11) # align right

################################################################################
# Functions needed specifically for this analysis routine

def drawObjects( plotData, lumi_scale ):
    lines = [
      (0.15, 0.95, 'CMS Preliminary' if plotData else 'CMS Simulation'),
      (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV)'% ( lumi_scale) ) if plotData else (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV)' % lumi_scale)
    ]
    if "mt2ll100" in args.selection and args.noData: lines += [(0.55, 0.5, 'M_{T2}(ll) > 100 GeV')] # Manually put the mt2ll > 100 GeV label
    return [tex.DrawLatex(*l) for l in lines]

def drawPlots(plots):
    for log in [False, True]:
        plot_directory_ = os.path.join(plot_directory, 'FakeRate', args.plot_directory, args.era, args.channel + ("_log" if log else ""), args.selection)
        for plot in plots:
            if not max(l.GetMaximum() for l in sum(plot.histos,[])): continue # Empty plot
            if not args.noData:
                plot.histos[1][0].legendText = "Data"


            _drawObjects = []
            n_stacks=len(plot.histos)
            if isinstance( plot, Plot):
                plotting.draw(plot,
                  plot_directory = plot_directory_,
                  ratio = {'histos': [[i+1,0] for i in range(n_stacks-1)], 'yRange':(0.1,1.9)} if not args.noData else None,
                  logX = False, logY = log, sorting = True,
                  yRange = (0.03, "auto") if log else (0.001, "auto"),
                  scaling = {0:1} if args.dataMCScaling else {},
                  legend = ( (0.18,0.88-0.03*sum(map(len, plot.histos)),0.9,0.88), 2),
                  drawObjects = drawObjects( not args.noData, lumi_scale ) + _drawObjects,
                  copyIndexPHP = True, extensions = ["png", "pdf", "root"],
                )
                
def getPassedTriggers( event ):
    passedtriggers = {
        "HLT_Ele8_CaloIdM_TrackIdM_PFJet30": event.HLT_Ele8_CaloIdM_TrackIdM_PFJet30,
        "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": event.HLT_Ele17_CaloIdM_TrackIdM_PFJet30,
        "HLT_Mu3_PFJet40": event.HLT_Mu3_PFJet40,
        "HLT_Mu8": event.HLT_Mu8,
        "HLT_Mu17": event.HLT_Mu17,
        "HLT_Mu20": event.HLT_Mu20,
        "HLT_Mu27": event.HLT_Mu27,
    }
    passedlist = []
    for trigger in triggerlist:
        if passedtriggers[trigger]:
            passedlist.append(trigger)
    return passedlist
    
def passedOfflineCut( event, triggername ):
    # cuts = {
    #     "HLT_Ele8_CaloIdM_TrackIdM_PFJet30": (15,45,8,30),
    #     "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": (25,100,17,30),
    #     "HLT_Mu3_PFJet40": (10,32,3,45),
    #     "HLT_Mu8": (15,100,8,30),
    #     "HLT_Mu17": (32,100,17,30),
    #     "HLT_Mu20": (32,100,20,30),
    #     "HLT_Mu27": (45,100,27,30),  
    # } 
    cuts = {
        "HLT_Ele8_CaloIdM_TrackIdM_PFJet30": (0,1000,9,30),
        "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": (0,1000,18,30),
        "HLT_Mu3_PFJet40": (0,1000,4,45),
        "HLT_Mu8": (0,1000,9,30),
        "HLT_Mu17": (0,1000,18,30),
        "HLT_Mu20": (0,1000,21,30),
        "HLT_Mu27": (0,1000,28,30),  
    }      
    if triggername not in cuts.keys():
        raise RuntimeError( "Trigger %s not defined for additional cuts", triggername)
    (ptcone_min, ptcone_max, leppt_min, jetpt_min) = cuts[triggername]
    
    # get max pt of a jet that is well separated from the lepton
    maxjet_pt_separated = 0
    for i in range(event.nJetGood):
        dEta = event.l1_eta - event.JetGood_eta[i]
        dPhi = deltaPhi(event.l1_phi, event.JetGood_phi[i])
        if sqrt(dEta*dEta+dPhi*dPhi) > 0.7:
            if event.JetGood_pt[i] > maxjet_pt_separated:
                maxjet_pt_separated = event.JetGood_pt[i]
    # get cone pt 
    ptcone = event.l1_ptConeGhent if event.l1_passFO and not event.l1_passTight else event.l1_pt
    # check cuts 
    if (ptcone > ptcone_min) and (ptcone < ptcone_max) and (event.l1_pt > leppt_min) and (maxjet_pt_separated > jetpt_min):
        return True 
    else:
        return False

# def looseSelection(lepindex, event):
#     if args.noLooseSel:
#         return True    
# 
#     if lepindex < 0:
#         return False
# 
#     if event.lep_sip3d[lepindex] > 8:
#         return False
#     if event.lep_pfRelIso03_all[lepindex] > 0.4:
#         return False
# 
#     # elec
#     if abs(event.lep_pdgId[lepindex]) == 11:
#         eleindex = event.lep_eleIndex[lepindex]
#         if not event.Electron_convVeto[eleindex]:
#             return False
#         # if event.Electron_tightCharge[eleindex] < 1:
#         #     return False
#         if ord(event.Electron_lostHits[eleindex]) > 1:
#             return False
# 
#         passID = False
#         # if event.Electron_mvaFall17V2Iso_WP80:
#         if event.lep_jetBTag[lepindex] < 0.1:
#             jetPtRatio = 1/(event.Electron_jetRelIso[eleindex]+1)
#             if (event.year == 2016 and jetPtRatio > 0.5) or (event.year in [2017,2018] and jetPtRatio > 0.4):
#                 passID = True
#         if event.l1_mvaTOPv2WP >= 4:
#             passID = True   
#         if not passID:
#             return False
# 
#     # muon
#     if abs(event.lep_pdgId[lepindex]) == 13:
#         muindex = event.lep_muIndex[lepindex]
#         passID = False
#         if event.lep_jetBTag[lepindex] < 0.025:
#             jetPtRatio = 1/(event.Muon_jetRelIso[muindex]+1)
#             if jetPtRatio > 0.45:
#                 passID = True
#         if event.l1_mvaTOPv2WP >= 4:
#             passID = True   
#         if not passID:
#             return False                
# 
#     return True

    
################################################################################
# Define sequences
sequence       = []

def leptonVariables(event, sample):
    pdgid = event.lep_pdgId[event.l1_index]
    event.pdgid = pdgid
    
sequence.append(leptonVariables)


def applyTriggerPrescales(sample, event):
    if args.noPreScale or sample.isData:
        event.reweightTriggerPrescale = 1.0
    else:
        passedlist = getPassedTriggers(event)
        passedlist_plusOffline = []
        for trigger in passedlist:
            if passedOfflineCut(event, trigger):
                passedlist_plusOffline.append(trigger)          
        weight = 1.0
        if event.year == 2016:
            if event.preVFP:
                weight = prescale16preVFP.getWeight(passedlist_plusOffline)
            else:
                weight = prescale16.getWeight(passedlist_plusOffline)
        elif event.year == 2017:
            weight = prescale17.getWeight(passedlist_plusOffline)
        elif event.year == 2018:
            weight = prescale18.getWeight(passedlist_plusOffline)
        event.reweightTriggerPrescale = weight
        # print "-----------------------------"
        # print passedlist
        # print passedlist_plusOffline
        # print weight
sequence.append( applyTriggerPrescales )

def applyAdditionalCuts(sample, event):
    # print "----------------"
    passedlist = getPassedTriggers(event)
    passedTriggersAndCuts = []

    for trigger in passedlist:
        if passedOfflineCut(event, trigger):
            passedTriggersAndCuts.append(trigger)
    
    event.passedCuts = True if len(passedTriggersAndCuts) > 0 else False
    
    # kill large weights
    if args.noLargeWeights and event.weight > 100:
        event.passedCuts = False
    ####
    id = event.lep_pdgId[event.l1_index]
    event.passedLoose = event.passedCuts and event.l1_passFO
    event.passedTight = event.passedCuts and event.l1_passFO and event.l1_passTight
    event.tightLepton = event.l1_passTight # also store information about lepton independent from trigger
    event.passedTriggers = passedTriggersAndCuts
    
sequence.append( applyAdditionalCuts )
    
def getMTfix(sample, event):
    pTfix = 35.
    dphi = deltaPhi(event.MET_phi,event.l1_phi)
    MTfix = sqrt( 2*pTfix*event.MET_pt*(1-cos(dphi)) )
    event.MTfix = MTfix
sequence.append(getMTfix)

def getBin(sample, event):
    Nbins_pt = len(boundaries_pt)
    Nbins_eta = len(boundaries_eta)
    pt = event.l1_ptConeGhent if event.l1_passFO and not event.l1_passTight else event.l1_pt
    eta = event.l1_eta
    bin_pt = 0
    bin_eta = 0
    for i in range(Nbins_pt):
        if pt > boundaries_pt[i]:
            bin_pt += 1
    for j in range(Nbins_eta):
        if abs(eta) > boundaries_eta[j]:
            bin_eta += 1
    event.bin_pt = bin_pt
    event.bin_eta = bin_eta
    # print "----------------------------"
    # print boundaries_pt, boundaries_eta
    # print pt, eta, event.bin_pt, event.bin_eta
sequence.append(getBin)

def getMediumID(sample, event):
    mediumId = -1
    if abs(event.lep_pdgId[event.l1_index]) == 13:
        if event.lep_mediumId[event.l1_index]:
            mediumId = 1
        else:
            mediumId = 0
    event.mediumID = mediumId
sequence.append(getMediumID)


def getClosestJetFlavor(sample, event):
    mindR = 0.7
    bscore_closest = 0.0
    foundjet = False
    for i in range(event.nJetGood):
        dEta = event.l1_eta - event.JetGood_eta[i]
        dPhi = deltaPhi(event.l1_phi, event.JetGood_phi[i])
        dR = sqrt(dEta*dEta+dPhi*dPhi)
        if dR < mindR:
            mindR = dR
            bscore_closest = event.JetGood_btagDeepFlavB[i]
            foundjet = True
    event.dR_closest = mindR 
    event.bscore_closest_custom = bscore_closest
    if event.l1_index >= 0:
        event.bscore_closest = event.lep_jetBTag[event.l1_index]
    else:
        event.bscore_closest = float('nan')
sequence.append(getClosestJetFlavor)

def getLeptonSF(sample, event):
    if sample.isData:
        return 
    SF = 1
    # Only apply if lepton passes tight criterion
    if event.l1_passTight:
        # Search for variation type and direction
        uncert = "syst"
        if args.sys == "LepIDstat_UP" or args.sys == "LepIDstat_DOWN":
            uncert = "stat"
        sigma = 0
        if args.sys == "LepIDstat_UP" or args.sys == "LepIDsys_UP":
            sigma = 1
        elif args.sys == "LepIDstat_DOWN" or args.sys == "LepIDsys_DOWN":
            sigma = -1
        idx1 = event.l1_index
        pdgId = event.lep_pdgId[idx1]
        eta = event.lep_eta[idx1]
        if abs(pdgId)==11:
            eta+=event.Electron_deltaEtaSC[event.lep_eleIndex[idx1]]
        pt = event.lep_pt[idx1]
        if event.year == 2016:
            if event.preVFP:
                SF *= leptonSF["UL2016preVFP"].getSF(pdgId, pt, eta, uncert, sigma)
            else:
                SF *= leptonSF["UL2016"].getSF(pdgId, pt, eta, uncert, sigma)
        elif event.year == 2017:
                SF *= leptonSF["UL2017"].getSF(pdgId, pt, eta, uncert, sigma)
        elif event.year == 2018:
                SF *= leptonSF["UL2018"].getSF(pdgId, pt, eta, uncert, sigma)
    event.reweightLeptonMVA = SF
sequence.append( getLeptonSF )

################################################################################
# Read variables

read_variables = [
    "weight/F", "year/I", "preVFP/O", "met_pt/F", "met_phi/F", "nJetGood/I", "PV_npvsGood/I",  "nJet/I", "nBTag/I", 
    "l1_pt/F", "l1_eta/F" , "l1_phi/F", "l1_mvaTOP/F", "l1_mvaTOPv2/F", "l1_mvaTOPWP/I", "l1_mvaTOPv2WP/I", "l1_index/I", "l1_passFO/O", "l1_passTight/O", "l1_ptCone/F", "l1_ptConeGhent/F",
    # "l2_pt/F", "l2_eta/F" , "l2_phi/F", "l2_mvaTOP/F", "l2_mvaTOPv2/F", "l2_mvaTOPWP/I", "l2_mvaTOPv2WP/I", "l2_index/I",
    # "l3_pt/F", "l3_eta/F" , "l3_phi/F", "l3_mvaTOP/F", "l3_mvaTOPv2/F", "l3_mvaTOPWP/I", "l3_mvaTOPv2WP/I", "l3_index/I",
    # "l4_pt/F", "l4_eta/F" , "l4_phi/F", "l4_mvaTOP/F", "l4_mvaTOPv2/F", "l4_mvaTOPWP/I", "l4_mvaTOPv2WP/I", "l4_index/I",
    "MET_pt/F", "MET_phi/F",
    "JetGood[pt/F,eta/F,phi/F,area/F,btagDeepB/F,btagDeepFlavB/F,index/I]",
    "Jet[pt/F,eta/F,phi/F,mass/F,btagDeepFlavB/F]",
    "lep[pt/F,eta/F,phi/F,pdgId/I,muIndex/I,eleIndex/I,mediumId/O,ptCone/F,ptConeGhent/F,jetBTag/F,sip3d/F,pfRelIso03_all/F,passFO/O,passTight/O]",
    # "Z1_l1_index/I", "Z1_l2_index/I", "nonZ1_l1_index/I", "nonZ1_l2_index/I",
    # "Z1_phi/F", "Z1_pt/F", "Z1_mass/F", "Z1_cosThetaStar/F", "Z1_eta/F", "Z1_lldPhi/F", "Z1_lldR/F",
    "Muon[pt/F,eta/F,phi/F,dxy/F,dz/F,ip3d/F,sip3d/F,jetRelIso/F,miniPFRelIso_all/F,pfRelIso03_all/F,mvaTTH/F,pdgId/I,segmentComp/F,nStations/I,nTrackerLayers/I,mediumId/O,tightId/O,isPFcand/B,isTracker/B,isGlobal/B]",
    "Electron[pt/F,eta/F,phi/F,dxy/F,dz/F,ip3d/F,sip3d/F,jetRelIso/F,miniPFRelIso_all/F,pfRelIso03_all/F,mvaTTH/F,pdgId/I,vidNestedWPBitmap/I,deltaEtaSC/F,convVeto/O,tightCharge/I,lostHits/b,mvaFall17V2Iso_WP80/O]",
    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30/O","HLT_Ele17_CaloIdM_TrackIdM_PFJet30/O","HLT_Mu3_PFJet40/O","HLT_Mu8/O","HLT_Mu17/O","HLT_Mu20/O","HLT_Mu27/O",
]

read_variables_MC = [
    "weight/F", 'reweightBTag_SF/F', 'reweightPU/F', 'reweightL1Prefire/F', #'reweightTrigger/F',
    # "genZ1_pt/F", "genZ1_eta/F", "genZ1_phi/F",
    "Muon[genPartFlav/I]",
    VectorTreeVariable.fromString( "GenPart[pt/F,mass/F,phi/F,eta/F,pdgId/I,genPartIdxMother/I,status/I,statusFlags/I]", nMax=1000),
    'nGenPart/I',
    # 'nScale/I', 'Scale[Weight/F]',
    # 'nPDF/I', VectorTreeVariable.fromString('PDF[Weight/F]',nMax=150),    
]



################################################################################
# MVA

################################################################################
# Set up plotting

if not args.noData:
    data_sample.texName = "data"
    data_sample.name           = "data"
    data_sample.style          = styles.errorStyle(ROOT.kBlack)

for sample in mc: sample.style = styles.fillStyle(sample.color)

###### SYS #################################################################
if args.sys in jet_variations:
    new_variables = ['%s/F'%v for v in jetSelectionModifier(jet_variations[args.sys],'list')]
    read_variables_MC += new_variables
    read_variables    += new_variables

weightnames = ['weight', 'reweightPU', 'reweightL1Prefire', 'reweightTriggerPrescale', 'reweightLeptonMVA'] #'reweightTrigger']
# weightnames = ['weight']
sys_weights = {
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
    # Multiply Scale weight 
    if "Scale_" in args.sys:
        scale_weight = getScaleWeight(event, args.sys)
        w *= scale_weight
    return w


for sample in mc:
    sample.read_variables = read_variables_MC
    sample.weight = weight_function


if not args.noData:
    stack = Stack(mc, data_sample)
else:
    stack = Stack(mc)


# Use some defaults
selection_string = cutInterpreter.cutString(args.selection)
    
if args.channel == "muon":
    selection_string += "&&(abs(lep_pdgId[l1_index])==13)&&lep_mediumId[l1_index]"
elif args.channel == "elec":
    selection_string += "&&(abs(lep_pdgId[l1_index])==11)"

Plot.setDefaults(stack = stack, weight = plotweights, selectionString = selection_string)
Plot2D.setDefaults(stack = stack, weight = plotweights, selectionString = selection_string)

################################################################################
# Now define the plots

plots = []
plots2D = []

plots.append(Plot(
    name = "dR_closest",
    texX = '#Delta R(lepton, next jet)', texY = 'Number of Events',
    attribute = lambda event, sample: event.dR_closest if event.passedLoose else float('nan'),
    addOverFlowBin='upper',
    binning=[10, 0, 1.0],
))

plots.append(Plot(
    name = "bscore_closest",
    texX = 'b tag score closest jet', texY = 'Number of Events',
    attribute = lambda event, sample: event.bscore_closest if event.passedLoose else float('nan'),
    addOverFlowBin='upper',
    binning=[40, 0, 1.0],
))

plots.append(Plot(
    name = "bscore_closest_custom",
    texX = 'b tag score closest jet', texY = 'Number of Events',
    attribute = lambda event, sample: event.bscore_closest_custom if event.passedLoose else float('nan'),
    addOverFlowBin='upper',
    binning=[40, 0, 1.0],
))

plots.append(Plot(
    name = "Weight",
    texX = 'Weight', texY = 'Number of Events',
    attribute = lambda event, sample: event.weight,
    addOverFlowBin='upper',
    binning=[100, 0, 1.1],
))

plots.append(Plot(
    name = "Weight_large",
    texX = 'Weight (large range)', texY = 'Number of Events',
    attribute = lambda event, sample: event.weight,
    addOverFlowBin='upper',
    binning=[100, 0, 100],
))

plots.append(Plot(
    name = "LargeWeight_lep_pt",
    texX = 'Lepton p_{T} (GeV)', texY = 'Number of Events / 40 GeV',
    attribute = lambda event, sample: event.l1_pt if event.passedLoose and event.weight > 100. else float('nan'),
    binning=[25, 0, 400],
))

plots.append(Plot(
    name = "LargeWeight_lep_eta",
    texX = 'Lepton #eta', texY = 'Number of Events',
    attribute = lambda event, sample: event.l1_eta if event.passedLoose and event.weight > 100.  else float('nan'),
    binning=[30, -3, 3],
))

plots.append(Plot(
    name = "LargeWeight_mvaWP",
    texX = 'MVA WP', texY = 'Number of Events / 40 GeV',
    attribute = lambda event, sample: event.l1_mvaTOPv2WP if event.passedLoose and event.weight > 100. else float('nan'),
    binning=[5, -0.5, 4.5],
))

plots.append(Plot(
    name = "Prescale",
    texX = 'Trigger prescale weight', texY = 'Number of Events',
    attribute = lambda event, sample: event.reweightTriggerPrescale,
    binning=[100, 0, 1.1],
))

plots.append(Plot(
    name = "L_MediumId",
    texX = 'Medium ID', texY = 'Number of Events',
    attribute = lambda event, sample: event.mediumID if event.passedLoose else float('nan'),
    binning=[3, -1.5, 1.5],
))

plots.append(Plot(
    name = "L_lep_pt",
    texX = 'Loose Lepton p_{T} (GeV)', texY = 'Number of Events / 40 GeV',
    attribute = lambda event, sample: event.l1_pt if event.passedLoose else float('nan'),
    binning=[25, 0, 400],
))

plots.append(Plot(
    name = "L_cone_pt",
    texX = 'Loose Lepton cone p_{T} (GeV)', texY = 'Number of Events / 40 GeV',
    attribute = lambda event, sample: (event.l1_ptConeGhent if event.l1_passFO and not event.l1_passTight else event.l1_pt) if event.passedLoose else float('nan'),
    binning=[25, 0, 150],
))

plots.append(Plot(
    name = "L_cone_pt_edit",
    texX = 'Loose Lepton cone p_{T} (GeV)', texY = 'Number of Events / 40 GeV',
    attribute = lambda event, sample: event.l1_ptCone if event.passedLoose else float('nan'),
    binning=[25, 0, 150],
))

plots.append(Plot(
    name = "L_lep_eta",
    texX = 'Loose Lepton #eta', texY = 'Number of Events',
    attribute = lambda event, sample: event.l1_eta if event.passedLoose else float('nan'),
    binning=[30, -3, 3],
))

plots.append(Plot(
    name = "L_MTfix",
    texX = 'Loose m_{T}^{fix}', texY = 'Number of Events',
    attribute = lambda event, sample: event.MTfix if event.passedLoose else float('nan'),
    binning=[10, 0, 140],
))

###############################

plots.append(Plot(
    name = "T_MediumId",
    texX = 'Medium ID', texY = 'Number of Events',
    attribute = lambda event, sample: event.mediumID if event.passedTight else float('nan'),
    binning=[3, -1.5, 1.5],
))

plots.append(Plot(
    name = "T_lep_pt",
    texX = 'Tight Lepton p_{T} (GeV)', texY = 'Number of Events / 40 GeV',
    attribute = lambda event, sample: event.l1_pt if event.passedTight else float('nan'),
    binning=[25, 0, 400],
))

plots.append(Plot(
    name = "T_cone_pt",
    texX = 'Tight Lepton cone p_{T} (GeV)', texY = 'Number of Events / 40 GeV',
    attribute = lambda event, sample: (event.l1_ptConeGhent if event.l1_passFO and not event.l1_passTight else event.l1_pt) if event.passedTight else float('nan'),
    binning=[25, 0, 150],
))

plots.append(Plot(
    name = "T_lep_eta",
    texX = 'Tight Lepton #eta', texY = 'Number of Events',
    attribute = lambda event, sample: event.l1_eta if event.passedTight else float('nan'),
    binning=[30, -3, 3],
))

plots.append(Plot(
    name = "T_MTfix",
    texX = 'Tight m_{T}^{fix}', texY = 'Number of Events',
    attribute = lambda event, sample: event.MTfix if event.passedTight else float('nan'),
    binning=[10, 0, 140],
))
###############################
list_of_binned_plots = []
for i in range(len(boundaries_pt)):
    for j in range(len(boundaries_eta)):
        ptbin = i+1
        etabin = j+1
        suffix = "__BIN_pt%s_eta%s" %(ptbin, etabin)
        plots.append(Plot(
            name = "L_lep_pt"+suffix,
            texX = 'Loose Lepton p_{T} (GeV)', texY = 'Number of Events',
            attribute = lambda event, sample, i_pt=ptbin, i_eta=etabin: event.l1_pt if (event.passedLoose and event.bin_pt==i_pt and event.bin_eta==i_eta ) else float('nan'),
            binning=[25, 0, 400],
        ))
        
        plots.append(Plot(
            name = "L_cone_pt"+suffix,
            texX = 'Loose Lepton cone p_{T} (GeV)', texY = 'Number of Events',
            attribute = lambda event, sample, i_pt=ptbin, i_eta=etabin: (event.l1_ptConeGhent if event.l1_passFO and not event.l1_passTight else event.l1_pt)  if (event.passedLoose and event.bin_pt==i_pt and event.bin_eta==i_eta ) else float('nan'),
            binning=[25, 0, 150],
        ))
        
        plots.append(Plot(
            name = "L_lep_eta"+suffix,
            texX = 'Loose Lepton #eta', texY = 'Number of Events',
            attribute = lambda event, sample, i_pt=ptbin, i_eta=etabin: event.l1_eta if (event.passedLoose and event.bin_pt==i_pt and event.bin_eta==i_eta ) else float('nan'),
            binning=[30, -3, 3],
        ))
        plots.append(Plot(
            name = "L_MTfix"+suffix,
            texX = 'Loose m_{T}^{fix}', texY = 'Number of Events',
            attribute = lambda event, sample, i_pt=ptbin, i_eta=etabin: event.MTfix if (event.passedLoose and event.bin_pt==i_pt and event.bin_eta==i_eta ) else float('nan'),
            binning=[10, 0, 140],
        ))
        plots.append(Plot(
            name = "T_lep_pt"+suffix,
            texX = 'Tight Lepton p_{T} (GeV)', texY = 'Number of Events',
            attribute = lambda event, sample, i_pt=ptbin, i_eta=etabin: event.l1_pt if (event.passedTight and event.bin_pt==i_pt and event.bin_eta==i_eta ) else float('nan'),
            binning=[25, 0, 400],
        ))
        
        plots.append(Plot(
            name = "T_cone_pt"+suffix,
            texX = 'Tight Lepton cone p_{T} (GeV)', texY = 'Number of Events',
            attribute = lambda event, sample, i_pt=ptbin, i_eta=etabin: (event.l1_ptConeGhent if event.l1_passFO and not event.l1_passTight else event.l1_pt) if (event.passedTight and event.bin_pt==i_pt and event.bin_eta==i_eta ) else float('nan'),
            binning=[25, 0, 150],
        ))
        
        plots.append(Plot(
            name = "T_lep_eta"+suffix,
            texX = 'Tight Lepton #eta', texY = 'Number of Events',
            attribute = lambda event, sample, i_pt=ptbin, i_eta=etabin: event.l1_eta if (event.passedTight and event.bin_pt==i_pt and event.bin_eta==i_eta ) else float('nan'),
            binning=[30, -3, 3],
        ))
        plots.append(Plot(
            name = "T_MTfix"+suffix,
            texX = 'Tight m_{T}^{fix}', texY = 'Number of Events',
            attribute = lambda event, sample, i_pt=ptbin, i_eta=etabin: event.MTfix if (event.passedTight and event.bin_pt==i_pt and event.bin_eta==i_eta ) else float('nan'),
            binning=[10, 0, 140],
        ))
        list_of_binned_plots.append("L_MTfix"+suffix)
        list_of_binned_plots.append("M_MTfix"+suffix)
        list_of_binned_plots.append("T_MTfix"+suffix)
###############################
list_of_trigger_plots = []
for trigger in triggerlist:
    suffix = "__TRIGGER_"+trigger
    plots.append(Plot(
        name = "T_MTfix"+suffix,
        texX = 'Tight m_{T}^{fix}', texY = 'Number of Events',
        attribute = lambda event, sample, tr=trigger: event.MTfix if (event.tightLepton and tr in event.passedTriggers ) else float('nan'),
        binning=[16, 0, 160],
    ))
    list_of_trigger_plots.append("T_MTfix"+suffix)
###############################
binning_pt  = Binning.fromThresholds(boundaries_pt)
binning_eta = Binning.fromThresholds(boundaries_eta)

plots2D.append(Plot2D(
    name = "lep_pt_eta_loose",
    texX = 'Lepton cone p_{T} (GeV)', texY = 'Lepton #eta',
    attribute = (
        lambda event, sample: (event.l1_ptConeGhent if event.l1_passFO and not event.l1_passTight else event.l1_pt) if event.passedLoose else float('nan'), 
        lambda event, sample: abs(event.l1_eta)    if event.passedLoose else float('nan'),
    ),
    binning = [binning_pt, binning_eta],
))


plots2D.append(Plot2D(
    name = "lep_pt_eta_tight",
    texX = 'Lepton cone p_{T} (GeV)', texY = 'Lepton #eta',
    attribute = (
        lambda event, sample: (event.l1_ptConeGhent if event.l1_passFO and not event.l1_passTight else event.l1_pt) if event.passedTight else float('nan'), 
        lambda event, sample: abs(event.l1_eta)    if event.passedTight else float('nan'),
    ),
    binning = [binning_pt, binning_eta],
))

       

plotting.fill(plots+plots2D, read_variables = read_variables, sequence = sequence)


################################################################################
# Draw Plots
drawPlots(plots)


################################################################################


plots_root = ["lep_pt_eta_loose", "lep_pt_eta_tight"] + list_of_binned_plots + list_of_trigger_plots

# Write Result Hist in root file
print "Now write results in root file."
plot_dir = os.path.join(plot_directory, 'FakeRate', args.plot_directory, args.era, args.channel, args.selection)
if not os.path.exists(plot_dir):
    try:
        os.makedirs(plot_dir)
    except:
        print 'Could not create', plot_dir
outfilename = plot_dir+'/Results.root'
print "Saving in", outfilename
outfile = ROOT.TFile(outfilename, 'recreate')
outfile.cd()
for plot in plots+plots2D:
    if plot.name in plots_root:
        for idx, histo_list in enumerate(plot.histos):
            for j, h in enumerate(histo_list):
                histname = h.GetName()
                process = histname
                if "TWZ_NLO_DR" in histname: process = "tWZ"
                elif "tWZToLL01j_lepWFilter" in histname: process = "tWZ"
                elif "TTZ" in histname: process = "ttZ"
                elif "ttZ01j" in histname: process = "ttZ"
                elif "ttZ01j_lepWFilter" in histname: process = "ttZ"
                elif "TTX_rare" in histname: process = "ttX"
                elif "TZQ" in histname: process = "tZq"
                elif "WZTo3LNu" in histname: process = "WZ"
                elif "WZ" in histname: process = "WZ"
                elif "ZZ" in histname: process = "ZZ"
                elif "triBoson" in histname: process = "triBoson"
                elif "nonprompt" in histname: process = "nonprompt"
                elif "data" in histname: process = "data"
                elif "MuEnriched" in histname: process = "QCD_MuEnriched"
                elif "EMEnriched" in histname: process = "QCD_EMEnriched"
                elif "bcToE" in histname: process = "QCD_bcToE"
                elif "DY" in histname: process = "DY"
                elif "WW" in histname: process = "WW"
                elif "TTbar" in histname: process = "TTbar"
                elif "WJetsToLNu": process = "Wjets"
                h.Write(plot.name+"__"+process)
outfile.Close()



logger.info( "Done with prefix %s and selectionString %s", args.selection, selection_string )
