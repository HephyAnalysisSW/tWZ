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
from tWZ.Tools.leptonFakerate            import leptonFakerate

# Analysis
from Analysis.Tools.helpers              import deltaPhi, deltaR
from Analysis.Tools.puProfileCache       import *
from Analysis.Tools.puReweighting        import getReweightingFunction
from Analysis.Tools.leptonJetArbitration     import cleanJetsAndLeptons
from Analysis.Tools.WeightInfo           import WeightInfo
from Analysis.Tools.LeptonSF_UL          import LeptonSF
from Analysis.Tools.EGammaSF             import EGammaSF

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
argParser.add_argument('--plot_directory', action='store', default='EFT_UL_v11')
argParser.add_argument('--era',            action='store', type=str, default="UL2018")
argParser.add_argument('--selection',      action='store', default='trilepT-minDLmass12-onZ1-njet4p-btag1p')
argParser.add_argument('--sys',            action='store', default='central')
argParser.add_argument('--nicePlots',      action='store_true', default=False)
argParser.add_argument('--twoD',           action='store_true', default=False)
argParser.add_argument('--triplet',        action='store_true', default=False)
argParser.add_argument('--doTTbarReco',    action='store_true', default=False)
argParser.add_argument('--applyFakerate',  action='store_true', default=False)
argParser.add_argument('--nonpromptOnly',  action='store_true', default=False)
argParser.add_argument('--splitnonprompt', action='store_true', default=False)
argParser.add_argument('--splitTTX',       action='store_true', default=False)
argParser.add_argument('--useDataSF',      action='store_true', default=False)
argParser.add_argument('--useBRILSF',      action='store_true', default=False)
argParser.add_argument('--tunePtCone',     action='store_true', default=False)
argParser.add_argument('--noLeptonSF',     action='store_true', default=False)
argParser.add_argument('--reduceEFT',      action='store_true', default=False)
argParser.add_argument('--SMpoint',        action='store_true', default=False)
argParser.add_argument('--threePoint',     action='store_true', default=False)
argParser.add_argument('--WZreweight',     action='store_true', default=False)


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
    "Fakerate_UP", "Fakerate_DOWN",
    "Trigger_UP", "Trigger_DOWN",
    "Prefire_UP", "Prefire_DOWN",
    "LepReco_UP", "LepReco_DOWN",
    "LepIDstat_2016preVFP_UP", "LepIDstat_2016preVFP_DOWN",
    "LepIDstat_2016_UP", "LepIDstat_2016_DOWN",
    "LepIDstat_2017_UP", "LepIDstat_2017_DOWN",
    "LepIDstat_2018_UP", "LepIDstat_2018_DOWN",
    "LepIDsys_UP", "LepIDsys_DOWN",
    "BTag_b_UP", "BTag_b_DOWN", # not needed when running single sources
    "BTag_l_UP", "BTag_l_DOWN", # not needed when running single sources
    "BTag_b_correlated_UP", "BTag_b_correlated_DOWN",
    "BTag_l_correlated_UP", "BTag_l_correlated_DOWN",
    "BTag_b_uncorrelated_2016preVFP_UP", "BTag_b_uncorrelated_2016preVFP_DOWN",
    "BTag_l_uncorrelated_2016preVFP_UP", "BTag_l_uncorrelated_2016preVFP_DOWN",
    "BTag_b_uncorrelated_2016_UP", "BTag_b_uncorrelated_2016_DOWN",
    "BTag_l_uncorrelated_2016_UP", "BTag_l_uncorrelated_2016_DOWN",
    "BTag_b_uncorrelated_2017_UP", "BTag_b_uncorrelated_2017_DOWN",
    "BTag_l_uncorrelated_2017_UP", "BTag_l_uncorrelated_2017_DOWN",
    "BTag_b_uncorrelated_2018_UP", "BTag_b_uncorrelated_2018_DOWN",
    "BTag_l_uncorrelated_2018_UP", "BTag_l_uncorrelated_2018_DOWN",
    "PU_UP", "PU_DOWN",
    "JES_UP", "JES_DOWN",
    "JER_UP", "JER_DOWN",
    "Lumi_uncorrelated_2016_UP", "Lumi_uncorrelated_2016_DOWN",
    "Lumi_uncorrelated_2017_UP", "Lumi_uncorrelated_2017_DOWN",
    "Lumi_uncorrelated_2018_UP", "Lumi_uncorrelated_2018_DOWN",
    "Lumi_correlated_161718_UP", "Lumi_correlated_161718_DOWN",
    "Lumi_correlated_1718_UP", "Lumi_correlated_1718_DOWN",
    "Scale_UPUP", "Scale_UPNONE", "Scale_NONEUP", "Scale_NONEDOWN", "Scale_DOWNNONE", "Scale_DOWNDOWN", # first is mu_r, second is mu_f
    "ISR_UP", "ISR_DOWN",
    "FSR_UP", "FSR_DOWN",
]

for i in range(100):
    variations.append("PDF_"+str(i+1))

print variations

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
    if "Fakerate" in args.sys:
        logger.info( "Running sys variation %s, this varies the Data!", args.sys)
    else:
        logger.info( "Running sys variation %s, noData is set to 'True'", args.sys)
        args.noData = True


################################################################################
# Some info messages
if args.small:                        args.plot_directory += "_small"
if args.reduceEFT:                    args.plot_directory += "_reduceEFT"
if args.threePoint:                   args.plot_directory += "_threePoint"
if args.SMpoint:                      args.plot_directory += "_SMpoint"
if args.noData:                       args.plot_directory += "_noData"
if args.WZreweight:                   args.plot_directory += "_WZreweight"
if args.nonpromptOnly:                args.plot_directory += "_nonpromptOnly"
if args.splitnonprompt:               args.plot_directory += "_splitnonprompt"
if args.splitTTX:                     args.plot_directory += "_splitTTX"
if args.noLeptonSF:                   args.plot_directory += "_noLeptonSF"
if args.applyFakerate:                args.plot_directory += "_FakeRateSF"
if args.useDataSF:                    args.plot_directory += "_useDataSF"
if args.useBRILSF:                    args.plot_directory += "_useBRILSF"
if args.tunePtCone:                   args.plot_directory += "_tunePtCone"
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

if args.noData:
    logger.info( "Running without data")
else:
    logger.info( "Data included in analysis cycle")

if args.applyFakerate:
    logger.info( "Apply Fake rate")
else:
    logger.info( "Do not apply Fake Rate")
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
    # 'DOWNNONE' translates to muR=Down, muF=none
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
# get PDF weight
def getPDFWeight(event, sys):
    index = -1
    if "PDF_" in sys:
        index = int(sys.split("_")[1])
    else:
        return 1.0

    if index == -1 or index > event.nPDF-1:
        print "PDF INDEX IS WRONG"
    return event.PDF_Weight[index]
################################################################################
# get Parton Shower weight
def getPSWeight(event, sys):
    # General: For ISR and FSR "up" and "down" refer to the value of alpha_s.
    # Thus, up is the scales multiplied by 0.5 (alpha_s goes up) and
    # 'down' is the variation with a factor of 2 (alpha_s goes down).

    # In nanoAODv9 the weights are stored like this:
    PSweights = {
        "ISR_DOWN": 0,
        "ISR_UP"  : 2,
        "FSR_DOWN": 1,
        "FSR_UP"  : 3,
    }

    # If this is a TopNanoAOD sample, all PS weights are stored and scheme is different
    # Description of all weights is here:
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/HowToPDF#Parton_shower_weights
    # (first two weights of the are not in TopNanoAOD and indices move by 2)
    if event.nPS == 44:
        PSweights = {
            "ISR_DOWN" : 25,
            "ISR_UP"   : 24,
            "FSR_DOWN" : 3,
            "FSR_UP"   : 2,
        }

    if sys not in PSweights.keys():
        print "PS VARIATION NOT FOUND"
        return 1.0


    if PSweights[sys] > event.nPS-1:
        print "PS INDEX IS WRONG"
        return 1.0

    return event.PS_Weight[PSweights[sys]]
################################################################################
# get Lumi factor
# Uncorrelated 2016      1.0%
# Uncorrelated 2017      2.0%
# Uncorrelated 2018      1.5%
# Correlated 2017,2018      0.6%,0.2%
# Correlated 2016,2017,2018   0.6%,0.9%,2.0%
def getLumiWeight(event, sys):
    variation = 0.0
    if event.year == 2016:
        if "uncorrelated_2016" in sys:
            variation = 0.01
        elif "correlated_161718" in sys:
            variation = 0.006
    elif event.year == 2017:
        if "uncorrelated_2017" in sys:
            variation = 0.02
        elif "correlated_1718" in sys:
            variation = 0.006
        elif "correlated_161718" in sys:
            variation = 0.009
    elif event.year == 2018:
        if "uncorrelated_2018" in sys:
            variation = 0.015
        elif "correlated_1718" in sys:
            variation = 0.002
        elif "correlated_161718" in sys:
            variation = 0.02
    LumiSF = 1.0
    if "_UP" in sys:
        LumiSF += variation
    elif "_DOWN" in sys:
        LumiSF -= variation
    return LumiSF

################################################################################
# Add a selection selectionModifier

if args.sys in jet_variations.keys():
    selectionModifier = jetSelectionModifier(jet_variations[args.sys])
else:
    selectionModifier = None

################################################################################
# Define the MC samples
from tWZ.samples.nanoTuples_ULRunII_nanoAODv9_postProcessed import *

if args.era == "UL2016":
    # mc = [UL2016.TWZ_NLO_DR, UL2016.TTZ, UL2016.TTX_rare, UL2016.TZQ, UL2016.WZTo3LNu, UL2016.triBoson, UL2016.ZZ, UL2016.nonprompt_3l]
    mc = [UL2016.TWZ_NLO_DR, UL2016.TTX_rare, UL2016.TZQ, UL2016.triBoson, UL2016.nonprompt_3l]
    samples_eft = [UL2016.TTZ_EFT, UL2016.WZ_EFT, UL2016.ZZ_EFT]
    if args.applyFakerate:
        mc = [UL2016.TWZ_NLO_DR, UL2016.TTZ, UL2016.TTX_rare, UL2016.TZQ, UL2016.WZTo3LNu, UL2016.triBoson, UL2016.ZZ, UL2016.nonprompt_3l]
        samples_eft = []
        if args.splitTTX:
            mc = [UL2016.TWZ_NLO_DR, UL2016.TTZ, UL2016.TTX_rare_noTTW, UL2016.TTW, UL2016.TZQ, UL2016.WZTo3LNu, UL2016.triBoson, UL2016.ZZ, UL2016.nonprompt_3l]
        if args.nonpromptOnly:
            if args.splitnonprompt:
                mc = [UL2016.WW, UL2016.Top, UL2016.DY]
            else:
                mc = [UL2016.nonprompt_3l]
elif args.era == "UL2016preVFP":
    # mc = [UL2016preVFP.TWZ_NLO_DR, UL2016preVFP.TTZ, UL2016preVFP.TTX_rare, UL2016preVFP.TZQ, UL2016preVFP.WZTo3LNu, UL2016preVFP.triBoson, UL2016preVFP.ZZ, UL2016preVFP.nonprompt_3l]
    mc = [UL2016preVFP.TWZ_NLO_DR, UL2016preVFP.TTX_rare, UL2016preVFP.TZQ, UL2016preVFP.triBoson, UL2016preVFP.nonprompt_3l]
    samples_eft = [UL2016preVFP.TTZ_EFT, UL2016preVFP.WZ_EFT, UL2016preVFP.ZZ_EFT]
    if args.applyFakerate:
        mc = [UL2016preVFP.TWZ_NLO_DR, UL2016preVFP.TTZ, UL2016preVFP.TTX_rare, UL2016preVFP.TZQ, UL2016preVFP.WZTo3LNu, UL2016preVFP.triBoson, UL2016preVFP.ZZ, UL2016preVFP.nonprompt_3l]
        samples_eft = []
        if args.splitTTX:
            mc = [UL2016preVFP.TWZ_NLO_DR, UL2016preVFP.TTZ, UL2016preVFP.TTX_rare_noTTW, UL2016preVFP.TTW, UL2016preVFP.TZQ, UL2016preVFP.WZTo3LNu, UL2016preVFP.triBoson, UL2016preVFP.ZZ, UL2016preVFP.nonprompt_3l]
        if args.nonpromptOnly:
            if args.splitnonprompt:
                mc = [UL2016preVFP.WW, UL2016preVFP.Top, UL2016preVFP.DY]
            else:
                mc = [UL2016preVFP.nonprompt_3l]
elif args.era == "UL2017":
    # mc = [UL2017.TWZ_NLO_DR, UL2017.TTZ, UL2017.TTX_rare, UL2017.TZQ, UL2017.WZTo3LNu, UL2017.triBoson, UL2017.ZZ, UL2017.nonprompt_3l]
    mc = [UL2017.TWZ_NLO_DR, UL2017.TTX_rare, UL2017.TZQ, UL2017.triBoson, UL2017.nonprompt_3l]
    samples_eft = [UL2017.TTZ_EFT, UL2017.WZ_EFT, UL2017.ZZ_EFT]
    if args.applyFakerate:
        mc = [UL2017.TWZ_NLO_DR, UL2017.TTZ, UL2017.TTX_rare, UL2017.TZQ, UL2017.WZTo3LNu, UL2017.triBoson, UL2017.ZZ, UL2017.nonprompt_3l]
        samples_eft = []
        if args.splitTTX:
            mc = [UL2017.TWZ_NLO_DR, UL2017.TTZ, UL2017.TTX_rare_noTTW, UL2017.TTW, UL2017.TZQ, UL2017.WZTo3LNu, UL2017.triBoson, UL2017.ZZ, UL2017.nonprompt_3l]
        if args.nonpromptOnly:
            if args.splitnonprompt:
                mc = [UL2017.WW, UL2017.Top, UL2017.DY]
            else:
                mc = [UL2017.nonprompt_3l]
elif args.era == "UL2018":
    # mc = [UL2018.TWZ_NLO_DR, UL2018.TTZ, UL2018.TTX_rare, UL2018.TZQ, UL2018.WZTo3LNu, UL2018.triBoson, UL2018.ZZ, UL2018.nonprompt_3l]
    mc = [UL2018.TWZ_NLO_DR, UL2018.TTX_rare, UL2018.TZQ, UL2018.triBoson, UL2018.nonprompt_3l]
    samples_eft = [UL2018.TTZ_EFT, UL2018.WZ_EFT, UL2018.ZZ_EFT]
    if args.applyFakerate:
        mc = [UL2018.TWZ_NLO_DR, UL2018.TTZ, UL2018.TTX_rare, UL2018.TZQ, UL2018.WZTo3LNu, UL2018.triBoson, UL2018.ZZ, UL2018.nonprompt_3l]
        samples_eft = []
        if args.splitTTX:
            mc = [UL2018.TWZ_NLO_DR, UL2018.TTZ, UL2018.TTX_rare_noTTW, UL2018.TTW, UL2018.TZQ, UL2018.WZTo3LNu, UL2018.triBoson, UL2018.ZZ, UL2018.nonprompt_3l]
        if args.nonpromptOnly:
            samples_eft = []
            if args.splitnonprompt:
                mc = [UL2018.WW, UL2018.Top, UL2018.DY]
            else:
                mc = [UL2018.nonprompt_3l]
elif args.era == "ULRunII":
    # mc = [TWZ_NLO_DR, TTZ, TTX_rare, TZQ, WZTo3LNu, triBoson, ZZ, nonprompt_3l]
    mc = [TWZ_NLO_DR, TTX_rare, TZQ, triBoson, nonprompt_3l]
    samples_eft = [TTZ_EFT, WZ_EFT, ZZ_EFT]
    if args.applyFakerate:
        mc = [TWZ_NLO_DR, TTZ, TTX_rare, TZQ, WZTo3LNu, triBoson, ZZ, nonprompt_3l]
        samples_eft = []
        if args.splitTTX:
            mc = [TWZ_NLO_DR, TTZ, TTX_rare_noTTW, TTW, TZQ, WZTo3LNu, triBoson, ZZ, nonprompt_3l]
        if args.nonpromptOnly:
            if args.splitnonprompt:
                mc = [WW, Top, DY]
            else:
                mc = [nonprompt_3l]




################################################################################
for sample in mc+samples_eft:
    sample.scale  = 1
    if args.reduceEFT:
        if "_EFT" in sample.name:
            sample.normalization = 1.
            sample.reduceFiles( factor = 10 )
            sample.scale /= sample.normalization
if args.nicePlots:
    mc += samples_eft
################################################################################
# EFT reweight

# WeightInfo
eftweights = []
for sample in samples_eft:
    print "Reading weight function for", sample.name
    w = WeightInfo(sample.reweight_pkl)
    w.set_order(2)
    eftweights.append(w)

# define which Wilson coefficients to plot
#cHq1Re11 cHq1Re22 cHq1Re33 cHq3Re11 cHq3Re22 cHq3Re33 cHuRe11 cHuRe22 cHuRe33 cHdRe11 cHdRe22 cHdRe33 cHudRe11 cHudRe22 cHudRe33

Npoints = 21
if args.threePoint:
    Npoints = 3


if args.nicePlots:
    Npoints = 0

WCs = []
WC_setup = [
    ('cHq1Re11',     ROOT.kRed),
    ('cHq1Re22',     ROOT.kRed),
    ('cHq1Re33',     ROOT.kRed),
    ('cHq1Re1122',   ROOT.kRed),
    ('cHq1Re1133',   ROOT.kRed),
    ('cHq1Re2233',   ROOT.kRed),
    ('cHq1Re112233', ROOT.kRed),
    ('cHq3Re11',     ROOT.kBlue),
    ('cHq3Re22',     ROOT.kBlue),
    ('cHq3Re33',     ROOT.kBlue),
    ('cHq3Re1122',   ROOT.kBlue),
    ('cHq3Re1133',   ROOT.kBlue),
    ('cHq3Re2233',   ROOT.kBlue),
    ('cHq3Re112233', ROOT.kBlue),
]
for i_wc, (WCname, color) in enumerate(WC_setup):
    for i in range(Npoints):
        minval = -10.
        maxval = 10.
        if 'cHq3Re11' in WCname:
            minval = -0.2
            maxval = 0.2
        if args.threePoint:
            minval = -1.0
            maxval = 1.0

        value = minval + ((maxval-minval)/(Npoints-1))*i
        WCs.append( (WCname, value, color) )

params =  []
for i_sample, sample in enumerate(samples_eft):
    for i_wc, (WC, WCval, color) in enumerate(WCs):
        if WC=="cHq1Re1122":
            params.append({'legendText':'%s=%3.4f'%(WC, WCval), 'color':color,  'WC':{'cHq1Re11':WCval, 'cHq1Re22':WCval}, 'sample': sample, 'i_sample': i_sample})
        elif WC=="cHq1Re1133":
            params.append({'legendText':'%s=%3.4f'%(WC, WCval), 'color':color,  'WC':{'cHq1Re11':WCval, 'cHq1Re33':WCval}, 'sample': sample, 'i_sample': i_sample})
        elif WC=="cHq1Re2233":
            params.append({'legendText':'%s=%3.4f'%(WC, WCval), 'color':color,  'WC':{'cHq1Re22':WCval, 'cHq1Re33':WCval}, 'sample': sample, 'i_sample': i_sample})
        elif WC=="cHq1Re112233":
            params.append({'legendText':'%s=%3.4f'%(WC, WCval), 'color':color,  'WC':{'cHq1Re11':WCval, 'cHq1Re22':WCval, 'cHq1Re33':WCval}, 'sample': sample, 'i_sample': i_sample})
        elif WC=="cHq3Re1122":
            params.append({'legendText':'%s=%3.4f'%(WC, WCval), 'color':color,  'WC':{'cHq3Re11':WCval, 'cHq3Re22':WCval}, 'sample': sample, 'i_sample': i_sample})
        elif WC=="cHq3Re1133":
            params.append({'legendText':'%s=%3.4f'%(WC, WCval), 'color':color,  'WC':{'cHq3Re11':WCval, 'cHq3Re33':WCval}, 'sample': sample, 'i_sample': i_sample})
        elif WC=="cHq3Re2233":
            params.append({'legendText':'%s=%3.4f'%(WC, WCval), 'color':color,  'WC':{'cHq3Re22':WCval, 'cHq3Re33':WCval}, 'sample': sample, 'i_sample': i_sample})
        elif WC=="cHq3Re112233":
            params.append({'legendText':'%s=%3.4f'%(WC, WCval), 'color':color,  'WC':{'cHq3Re11':WCval, 'cHq3Re22':WCval, 'cHq3Re33':WCval}, 'sample': sample, 'i_sample': i_sample})
        else:
            params.append({'legendText':'%s=%3.4f'%(WC, WCval), 'color':color,  'WC':{WC:WCval} , 'sample': sample, 'i_sample': i_sample})

#### 2D scan
if args.twoD:
    minval1  = -4.0
    maxval1  = 4.0
    minval2  = -4.0
    maxval2  = 4.0
    Npoints1 = 21
    Npoints2 = 21
    WC1  = 'cHq1Re1122'
    WC1a = 'cHq1Re11'
    WC1b = 'cHq1Re22'
    WC2  = 'cHq1Re33'
    if args.triplet:
        WC1  = 'cHq3Re1122'
        WC1a = 'cHq3Re11'
        WC1b = 'cHq3Re22'
        WC2  = 'cHq3Re33'
        minval1 = -0.2
        maxval1 = 0.2
    params = []
    for i in range(Npoints1):
        value1 = minval1 + ((maxval1-minval1)/(Npoints1-1))*i
        for j in range(Npoints2):
            value2 = minval2 + ((maxval2-minval2)/(Npoints2-1))*j
            for i_sample, sample in enumerate(samples_eft):
                params.append({'legendText':'%s=%3.4f, %s=%3.4f'%(WC1,value1,WC2,value2), 'color':ROOT.kRed,  'WC':{WC1a:value1, WC1b:value1, WC2:value2} , 'sample': sample, 'i_sample': i_sample})
####

for i_param, param in enumerate(params):
    param['style']    = styles.lineStyle( param['color'] )

# Creating a list of weights
plotweights = []
# Add MC weights
weight_mc = []
for sample in mc:
    weight_ = lambda event, sample: 1. # Add event.weight and lumi weight to sample.weight later
    weight_mc.append(weight_)
plotweights.append(weight_mc)

# Add data weight
if not args.noData:
    plotweights.append([lambda event, sample: event.weight])
# Add EFT weight
for param in params:
    i_sample = param['i_sample']
    eft_weight = eftweights[i_sample].get_weight_func(**param['WC'])
    plotweights.append([eft_weight])

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

try:
  data_sample = eval(datastring)
except Exception as e:
  logger.error( "Didn't find %s", datastring )
  raise e

lumi_scale                 = lumi_year[lumistring]/1000.
data_sample.scale          = 1.

if args.small:
    for sample in mc + [data_sample]:
        sample.normalization = 1.
        sample.reduceFiles( to = 1 )
        sample.scale /= sample.normalization
    for param in params[i_sample]:
        param['sample'].normalization = 1.
        param['sample'].reduceFiles( to = 1 )
        param['sample'].scale /= sample.normalization

################################################################################
# Lepton SF
muonWP = "medium"
elecWP = "tight"

leptonSF = {
    "UL2016preVFP":  LeptonSF("UL2016_preVFP", muonWP, elecWP),
    "UL2016":  LeptonSF("UL2016", muonWP, elecWP),
    "UL2017":  LeptonSF("UL2017", muonWP, elecWP),
    "UL2018":  LeptonSF("UL2018", muonWP, elecWP),
}


################################################################################
# FakerateSF
if args.useDataSF:
    fakeratemode = "DATA"
    if args.useBRILSF:
        fakeratemode = "BRIL"
    if args.tunePtCone:
        fakeratemode = "tunePtCone"
else:
    fakeratemode = "MC"
    if args.useBRILSF:
        raise RuntimeError( "BRIL SF is not implemented for MC")
    if args.tunePtCone:
        fakeratemode = "tunePtConeMC"

leptonFakerates = {
    "UL2016preVFP":  leptonFakerate("UL2016preVFP", fakeratemode),
    "UL2016":  leptonFakerate("UL2016", fakeratemode),
    "UL2017":  leptonFakerate("UL2017", fakeratemode),
    "UL2018":  leptonFakerate("UL2018", fakeratemode),
}

################################################################################
# ElectronRecoSF
ElectronRecoSFs = {
    "UL2016preVFP":  EGammaSF("UL2016_preVFP"),
    "UL2016":  EGammaSF("UL2016"),
    "UL2017":  EGammaSF("UL2017"),
    "UL2018":  EGammaSF("UL2018"),
}


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
    if "mt2ll100" in args.selection and args.noData: lines += [(0.55, 0.5, 'M_{T2}(ll) > 100 GeV')] # Manually put the mt2ll > 100 GeV label
    return [tex.DrawLatex(*l) for l in lines]

def drawPlots(plots, mode, dataMCScale):
    for log in [False, True]:
        plot_directory_ = os.path.join(plot_directory, 'analysisPlots', args.plot_directory, args.era, mode + ("_log" if log else ""), args.selection)
        for plot in plots:
            if not max(l.GetMaximum() for l in sum(plot.histos,[])): continue # Empty plot
            if not args.noData:
                if mode == "all": plot.histos[1][0].legendText = "Data"
                if mode == "SF":  plot.histos[1][0].legendText = "Data (SF)"

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
                  drawObjects = drawObjects( not args.noData, dataMCScale , lumi_scale ) + _drawObjects,
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

def tunePtCone(sample, event):
    if args.tunePtCone:
        f_mu = 0.933
        f_el = 0.91
        idx1 = event.l1_index
        idx2 = event.l2_index
        idx3 = event.l3_index
        # Lepton 1
        if event.l1_passFO and not event.l1_passTight:
            if abs(event.lep_pdgId[idx1]) == 11:
                event.l1_ptConeGhent        = f_el*event.l1_ptConeGhent
                event.l1_ptCone             = f_el*event.l1_ptCone
                event.lep_ptConeGhent[idx1] = f_el*event.lep_ptConeGhent[idx1]
                event.lep_ptCone[idx1]      = f_el*event.lep_ptCone[idx1]
            elif abs(event.lep_pdgId[idx1]) == 13:
                event.l1_ptConeGhent        = f_mu*event.l1_ptCone
                event.l1_ptCone             = f_mu*event.l1_ptCone
                event.lep_ptConeGhent[idx1] = f_mu*event.lep_ptConeGhent[idx1]
                event.lep_ptCone[idx1]      = f_mu*event.lep_ptCone[idx1]
        # Lepton 2
        if event.l2_passFO and not event.l2_passTight:
            if abs(event.lep_pdgId[idx2]) == 11:
                event.l2_ptConeGhent        = f_el*event.l2_ptConeGhent
                event.l2_ptCone             = f_el*event.l2_ptCone
                event.lep_ptConeGhent[idx2] = f_el*event.lep_ptConeGhent[idx2]
                event.lep_ptCone[idx2]      = f_el*event.lep_ptCone[idx2]
            elif abs(event.lep_pdgId[idx2]) == 13:
                event.l2_ptConeGhent        = f_mu*event.l2_ptCone
                event.l2_ptCone             = f_mu*event.l2_ptCone
                event.lep_ptConeGhent[idx2] = f_mu*event.lep_ptConeGhent[idx2]
                event.lep_ptCone[idx2]      = f_mu*event.lep_ptCone[idx2]
        # Lepton 3
        if event.l3_passFO and not event.l3_passTight:
            if abs(event.lep_pdgId[idx3]) == 11:
                event.l3_ptConeGhent        = f_el*event.l3_ptConeGhent
                event.l3_ptCone             = f_el*event.l3_ptCone
                event.lep_ptConeGhent[idx3] = f_el*event.lep_ptConeGhent[idx3]
                event.lep_ptCone[idx3]      = f_el*event.lep_ptCone[idx3]
            elif abs(event.lep_pdgId[idx3]) == 13:
                event.l3_ptConeGhent        = f_mu*event.l3_ptCone
                event.l3_ptCone             = f_mu*event.l3_ptCone
                event.lep_ptConeGhent[idx3] = f_mu*event.lep_ptConeGhent[idx3]
                event.lep_ptCone[idx3]      = f_mu*event.lep_ptCone[idx3]
sequence.append(tunePtCone)

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
    # Only apply SF when also cutting on WP
    if "trilepT" in args.selection or "qualepT" in args.selection:
        # Search for variation type and direction
        # Statistical should only be applied for the corresponding year
        uncert = "syst"
        sigma = 0
        if args.sys == "LepIDsys_UP":
            uncert = "syst"
            sigma = 1
        elif args.sys == "LepIDsys_DOWN":
            uncert = "syst"
            sigma = -1
        elif args.sys == "LepIDstat_2016preVFP_UP" and event.year == 2016 and event.preVFP:
            uncert = "stat"
            sigma = 1
        elif args.sys == "LepIDstat_2016preVFP_DOWN" and event.year == 2016 and event.preVFP:
            uncert = "stat"
            sigma = -1
        elif args.sys == "LepIDstat_2016_UP" and event.year == 2016 and not event.preVFP:
            uncert = "stat"
            sigma = 1
        elif args.sys == "LepIDstat_2016_DOWN" and event.year == 2016 and not event.preVFP:
            uncert = "stat"
            sigma = -1
        elif args.sys == "LepIDstat_2017_UP" and event.year == 2017:
            uncert = "stat"
            sigma = 1
        elif args.sys == "LepIDstat_2017_DOWN" and event.year == 2017:
            uncert = "stat"
            sigma = -1
        elif args.sys == "LepIDstat_2018_UP" and event.year == 2018:
            uncert = "stat"
            sigma = 1
        elif args.sys == "LepIDstat_2018_DOWN" and event.year == 2018:
            uncert = "stat"
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
                if event.preVFP:
                    SF *= leptonSF["UL2016preVFP"].getSF(pdgId, pt, eta, uncert, sigma)
                else:
                    SF *= leptonSF["UL2016"].getSF(pdgId, pt, eta, uncert, sigma)
            elif event.year == 2017:
                    SF *= leptonSF["UL2017"].getSF(pdgId, pt, eta, uncert, sigma)
            elif event.year == 2018:
                    SF *= leptonSF["UL2018"].getSF(pdgId, pt, eta, uncert, sigma)
    if args.noLeptonSF:
        SF=1.0
    event.reweightLeptonMVA = SF
sequence.append( getLeptonSF )

def getElectronRecoSF(sample, event):
    if sample.isData:
        return
    SF = 1
    # decide if central or variation
    var = "sf"
    if args.sys == "LepReco_UP":
        var = "sfup"
    elif args.sys == "LepReco_DOWN":
        var = "sfdown"
    # Go through the 3 leptons and multiply SF
    idx1 = event.l1_index
    idx2 = event.l2_index
    idx3 = event.l3_index
    for i in [idx1, idx2, idx3]:
        pdgId = event.lep_pdgId[i]
        if abs(pdgId)==11:
            eta = event.lep_eta[i]+event.Electron_deltaEtaSC[event.lep_eleIndex[i]]
            pt = event.lep_pt[i]
            if pt < 20:
                WP = "RecoBelow20"
            else:
                WP = "RecoAbove20"
            if event.year == 2016 and event.preVFP:
                SF *= ElectronRecoSFs["UL2016preVFP"].getSF(pt, eta, var, WP)
            elif event.year == 2016 and not event.preVFP:
                SF *= ElectronRecoSFs["UL2016"].getSF(pt, eta, var, WP)
            elif event.year == 2017:
                SF *= ElectronRecoSFs["UL2017"].getSF(pt, eta, var, WP)
            elif event.year == 2018:
                SF *= ElectronRecoSFs["UL2018"].getSF(pt, eta, var, WP)
    # print SF
    event.reweightElectronRecoSF = SF
sequence.append( getElectronRecoSF )

def getLeptonFakeRate( sample, event ):
    sigma = 0
    if args.sys == "Fakerate_UP":
        sigma = 1.0
    if args.sys == "Fakerate_DOWN":
        sigma = -1.0
    SF = 1.0
    Nfakes = 0
    if args.useDataSF and not sample.isData:
        event.reweightLeptonFakerate = 1.0
        return
    if args.applyFakerate:
        idx1 = event.l1_index
        idx2 = event.l2_index
        idx3 = event.l3_index
        for i in [idx1, idx2, idx3]:
            if event.lep_passFO[i] and not event.lep_passTight[i]:
                Nfakes += 1
                pdgId = event.lep_pdgId[i]
                eta = event.lep_eta[i]
                pt = event.lep_ptConeGhent[i] if event.lep_passFO[i] and not event.lep_passTight[i] else event.lep_pt[i]
                # Get year
                if event.year == 2016:
                    if event.preVFP:
                        yearstring = "UL2016preVFP"
                    else:
                        yearstring = "UL2016"
                elif event.year == 2017:
                    yearstring = "UL2017"
                elif event.year == 2018:
                    yearstring = "UL2018"
                # Get fake rate from map
                fakerate = leptonFakerates[yearstring].getFactor(pdgId, pt, eta, "stat", sigma )

                if fakerate > 0.9:
                    fakerate = 0.9
                SF *= fakerate/(1-fakerate)
    sign = -1 if (Nfakes > 0 and (Nfakes % 2) == 0) else 1 # for two failing leptons there is a negative sign
    event.reweightLeptonFakerate = sign*SF
    # print Nfakes, event.reweightLeptonFakerate
sequence.append(getLeptonFakeRate)

def getSYSweight(sample, event):
    # Scales
    if args.sys in ["Scale_UPUP", "Scale_UPNONE", "Scale_NONEUP", "Scale_DOWNDOWN", "Scale_DOWNNONE", "Scale_NONEDOWN"]:
        event.reweightScale = getScaleWeight(event, args.sys)
    else:
        event.reweightScale = 1.0
    # PDF
    if "PDF_" in args.sys:
        event.reweightPDF = getPDFWeight(event, args.sys)
    else:
        event.reweightPDF = 1.0
    # Lumi
    if "Lumi_" in args.sys:
        event.reweightLumi = getLumiWeight(event, args.sys)
    else:
        event.reweightLumi = 1.0
    # Parton Shower
    if "ISR_" in args.sys or "FSR_" in args.sys:
        event.reweightPS = getPSWeight(event, args.sys)
    else:
        event.reweightPS = 1.0

sequence.append( getSYSweight )

def getNjetWZreweight(sample, event):
    # numbers from 4 top analysis AN v12
    # https://cms.cern.ch/iCMS/jsp/db_notes/noteInfo.jsp?cmsnoteid=CMS%20AN-2021/182
    event.reweightNjetWZ = 1
    if args.WZreweight:
        if "WZ_EFT" in sample.name:
            if event.nJetGood == 0:
                event.reweightNjetWZ = 1.07
            elif event.nJetGood == 1:
                event.reweightNjetWZ = 0.85
            elif event.nJetGood == 2:
                event.reweightNjetWZ = 0.93
            elif event.nJetGood == 3:
                event.reweightNjetWZ = 1.08
            elif event.nJetGood == 4:
                event.reweightNjetWZ = 1.33
            elif event.nJetGood == 5:
                event.reweightNjetWZ = 1.89
            elif event.nJetGood > 5:
                event.reweightNjetWZ = 2.69
sequence.append( getNjetWZreweight )

def getEFTnormweight(sample, event):
    normweight = 1.0
    if "TTZ_EFT" in sample.name:
        normweight = 0.84
    elif "WZ_EFT" in sample.name:
        normweight = 0.64
    elif "ZZ_EFT" in sample.name:
        normweight = 0.60
    event.EFTnormweight = normweight
sequence.append( getEFTnormweight )

def getMlb(sample, event):
    lepton = ROOT.TLorentzVector()
    if not 'qualep' in args.selection:
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
    if idx_l1 >= 0 and idx_l2 >=0:
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
        else:
            lepton.SetPtEtaPhiM(event.lep_pt[idx_l2], event.lep_eta[idx_l2], event.lep_phi[idx_l2], lepmass)

        event.cosThetaStar = cosThetaStarNew(lepton, Z)
    else:
        event.cosThetaStar = float('nan')
sequence.append( getCosThetaStar )

def getDiBosonAngles(sample, event):
    lep1,lep2,boson = ROOT.TLorentzVector(),ROOT.TLorentzVector(),ROOT.TLorentzVector()
    # Get lep1 and lep2 from Z boson
    idx_l1 = event.Z1_l1_index
    idx_l2 = event.Z1_l2_index
    if idx_l1 >= 0 and idx_l2 >=0:
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
    if "qualep" in args.selection:
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

    if idx_l1 >= 0 and idx_l2 >=0:
        event.Theta = getTheta(lep1, lep2, boson)
        event.theta = gettheta(lep1, lep2, boson)
        event.phi = getphi(lep1, lep2, boson)
    else:
        event.Theta = float('nan')
        event.theta = float('nan')
        event.phi = float('nan')
sequence.append( getDiBosonAngles )

def getbScoresLepton(sample, event):
    fakelepton_btagscores = []
    if event.l1_passFO and not event.l1_passTight:
        fakelepton_btagscores.append(event.lep_jetBTag[event.l1_index])
    if event.l2_passFO and not event.l2_passTight:
        fakelepton_btagscores.append(event.lep_jetBTag[event.l2_index])
    if event.l3_passFO and not event.l3_passTight:
        fakelepton_btagscores.append(event.lep_jetBTag[event.l3_index])
    event.fakelepton_btagscores = fakelepton_btagscores
sequence.append(getbScoresLepton)

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

def Nlep( event, sample ):
    Nlep_tight = 0
    if event.l1_passTight: Nlep_tight+=1
    if event.l2_passTight: Nlep_tight+=1
    if event.l3_passTight: Nlep_tight+=1
    if event.l4_passTight: Nlep_tight+=1
    event.Nlep_tight = Nlep_tight

    Nlep = 0
    Nlep_passFO = 0
    Nlep_passTight = 0

    for i in range(len(event.lep_pt)):
        Nlep += 1
        if event.lep_passFO[i]:
            Nlep_passFO += 1
        if event.lep_passTight[i]:
            Nlep_passTight += 1
    event.Nlep = Nlep
    event.Nlep_passFO = Nlep_passFO
    event.Nlep_passTight = Nlep_passTight

sequence.append( Nlep )

def getJetId( event, sample ):
    jetIds = []
    for i in range(event.nJetGood):
        jetIds.append(event.JetGood_jetId[i])
    event.jetIds = jetIds
sequence.append(getJetId)


################################################################################
# Read variables

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
]

if "qualep" in args.selection:
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
    'nScale/I', 'Scale[Weight/F]',
    'nPDF/I', VectorTreeVariable.fromString('PDF[Weight/F]',nMax=150),
    'nPS/I', 'PS[Weight/F]',
]

read_variables_eft = [
    "np/I", VectorTreeVariable.fromString("p[C/F]",nMax=200)
]


################################################################################
# MVA

################################################################################
# define 3l selections
# if "lepVeto" in args.selection:
#     mu_string  = lepString('mu','VL')
# else:
#     mu_string  = lepString('mu','L') + "&&lep_mediumId"
#
# ele_string = lepString('ele','L')


mu_string  = "lep_pt>10&&abs(lep_eta)<2.4&&abs(lep_pdgId)==13&&lep_passFO"
ele_string = "lep_pt>10&&abs(lep_eta)<2.4&&abs(lep_pdgId)==11&&lep_passFO"

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
if 'qualep' in args.selection:
    allModes = ['mumumumu','mumuee','eeee']

print "Working on channels:", allModes

for i_mode, mode in enumerate(allModes):
    yields[mode] = {}
    if not args.noData:
        data_sample.texName = "data"
        data_sample.setSelectionString([getLeptonSelection(mode)])
        data_sample.name           = "data"
        data_sample.style          = styles.errorStyle(ROOT.kBlack)

    for sample in mc: sample.style = styles.fillStyle(sample.color)

    ###### SYS #################################################################
    if args.sys in jet_variations:
        new_variables = ['%s/F'%v for v in jetSelectionModifier(jet_variations[args.sys],'list')]
        read_variables_MC += new_variables
        read_variables    += new_variables

    weightnames = ['weight', 'reweightBTag_SF', 'reweightPU', 'reweightL1Prefire' , 'reweightTrigger', 'reweightLeptonFakerate', 'reweightLeptonMVA', 'reweightElectronRecoSF']
    weightnames += ['reweightScale', 'reweightPDF', 'reweightLumi', 'reweightPS']
    weightnames += ['EFTnormweight']
    weightnames += ['reweightNjetWZ']

    # weightnames = ['weight']

    sys_weights = {
        "BTag_b_UP"     : ('reweightBTag_SF','reweightBTag_SF_b_Up'),
        "BTag_b_DOWN"   : ('reweightBTag_SF','reweightBTag_SF_b_Down'),
        "BTag_l_UP"     : ('reweightBTag_SF','reweightBTag_SF_l_Up'),
        "BTag_l_DOWN"   : ('reweightBTag_SF','reweightBTag_SF_l_Down'),
        "BTag_b_correlated_UP"                : ('reweightBTag_SF','reweightBTag_SF_b_Up_Correlated'),
        "BTag_b_correlated_DOWN"              : ('reweightBTag_SF','reweightBTag_SF_b_Down_Correlated'),
        "BTag_l_correlated_UP"                : ('reweightBTag_SF','reweightBTag_SF_l_Up_Correlated'),
        "BTag_l_correlated_DOWN"              : ('reweightBTag_SF','reweightBTag_SF_l_Down_Correlated'),
        "BTag_b_uncorrelated_2016preVFP_UP"   : ('reweightBTag_SF','reweightBTag_SF_b_Up_Uncorrelated_2016preVFP'),
        "BTag_b_uncorrelated_2016preVFP_DOWN" : ('reweightBTag_SF','reweightBTag_SF_b_Down_Uncorrelated_2016preVFP'),
        "BTag_b_uncorrelated_2016_UP"         : ('reweightBTag_SF','reweightBTag_SF_b_Up_Uncorrelated_2016'),
        "BTag_b_uncorrelated_2016_DOWN"       : ('reweightBTag_SF','reweightBTag_SF_b_Down_Uncorrelated_2016'),
        "BTag_b_uncorrelated_2017_UP"         : ('reweightBTag_SF','reweightBTag_SF_b_Up_Uncorrelated_2017'),
        "BTag_b_uncorrelated_2017_DOWN"       : ('reweightBTag_SF','reweightBTag_SF_b_Down_Uncorrelated_2017'),
        "BTag_b_uncorrelated_2018_UP"         : ('reweightBTag_SF','reweightBTag_SF_b_Up_Uncorrelated_2018'),
        "BTag_b_uncorrelated_2018_DOWN"       : ('reweightBTag_SF','reweightBTag_SF_b_Down_Uncorrelated_2018'),
        "BTag_l_uncorrelated_2016preVFP_UP"   : ('reweightBTag_SF','reweightBTag_SF_l_Up_Uncorrelated_2016preVFP'),
        "BTag_l_uncorrelated_2016preVFP_DOWN" : ('reweightBTag_SF','reweightBTag_SF_l_Down_Uncorrelated_2016preVFP'),
        "BTag_l_uncorrelated_2016_UP"         : ('reweightBTag_SF','reweightBTag_SF_l_Up_Uncorrelated_2016'),
        "BTag_l_uncorrelated_2016_DOWN"       : ('reweightBTag_SF','reweightBTag_SF_l_Down_Uncorrelated_2016'),
        "BTag_l_uncorrelated_2017_UP"         : ('reweightBTag_SF','reweightBTag_SF_l_Up_Uncorrelated_2017'),
        "BTag_l_uncorrelated_2017_DOWN"       : ('reweightBTag_SF','reweightBTag_SF_l_Down_Uncorrelated_2017'),
        "BTag_l_uncorrelated_2018_UP"         : ('reweightBTag_SF','reweightBTag_SF_l_Up_Uncorrelated_2018'),
        "BTag_l_uncorrelated_2018_DOWN"       : ('reweightBTag_SF','reweightBTag_SF_l_Down_Uncorrelated_2018'),
        'Trigger_UP'    : ('reweightTrigger','reweightTriggerUp'),
        'Trigger_DOWN'  : ('reweightTrigger','reweightTriggerDown'),
        'PU_UP'         : ('reweightPU','reweightPUUp'),
        'PU_DOWN'       : ('reweightPU','reweightPUDown'),
        'Prefire_UP'    : ('reweightL1Prefire','reweightL1PrefireUp'),
        'Prefire_DOWN'  : ('reweightL1Prefire','reweightL1PrefireDown'),
        # For leptonID, leptonReco SF, PDF, scales, parton shower, and Lumi this is set in the sequence
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

    weightnames_data = ['reweightLeptonFakerate'] # For data only the lepton fake rate should be re-weighted
    getters_data = map( operator.attrgetter, weightnames_data)
    def weight_function_data( event, sample):
        # Calculate weight, this becomes: w = event.weightnames[0]*event.weightnames[1]*...
        w = reduce(operator.mul, [g(event) for g in getters_data], 1)
        return w

    for sample in mc:
        sample.read_variables = read_variables_MC
        sample.setSelectionString([getLeptonSelection(mode)])
        sample.weight = weight_function

    if not args.noData:
        data_sample.weight = weight_function_data

    for param in params:
        param['sample'].read_variables = read_variables_MC + read_variables_eft
        param['sample'].setSelectionString([getLeptonSelection(mode)])
        param['sample'].weight = weight_function

    if not args.noData:
        stack = Stack(mc, data_sample, *[ [ param['sample'] ] for param in params ])
        noneftidxs = [0,1]
        if args.nicePlots:
            stack = Stack(mc, data_sample)
    else:
        stack = Stack(mc, *[ [ param['sample'] ] for param in params ])
        noneftidxs = [0]
        if args.nicePlots:
            stack = Stack(mc)

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
        name = "N_LepID",
        texX = 'Number of leptons passing the tight ID (out of first 4)', texY = 'Number of Events',
        attribute = lambda event, sample: event.Nlep_tight,
        binning=[5,-0.5,4.5],
    ))

    plots.append(Plot(
        name = "N_Lep",
        texX = 'Number of leptons ', texY = 'Number of Events',
        attribute = lambda event, sample: event.Nlep,
        binning=[7,-0.5,6.5],
    ))

    plots.append(Plot(
        name = "N_Lep_passFO",
        texX = 'Number of leptons passing FO', texY = 'Number of Events',
        attribute = lambda event, sample: event.Nlep_passFO,
        binning=[7,-0.5,6.5],
    ))

    plots.append(Plot(
        name = "N_Lep_passTight",
        texX = 'Number of leptons passing Tight', texY = 'Number of Events',
        attribute = lambda event, sample: event.Nlep_passTight,
        binning=[7,-0.5,6.5],
    ))

    plots.append(Plot(
        name = "l1_pt",
        texX = 'Leading lepton p_{T} (GeV)', texY = 'Number of Events / 10 GeV',
        addOverFlowBin='both',
        attribute = TreeVariable.fromString( "l1_pt/F" ),
        binning=[40, 0, 400],
    ))

    plots.append(Plot(
        name = "l2_pt",
        texX = 'Subleading lepton p_{T} (GeV)', texY = 'Number of Events / 10 GeV',
        addOverFlowBin='both',
        attribute = TreeVariable.fromString( "l2_pt/F" ),
        binning=[40, 0, 400],
    ))

    plots.append(Plot(
        name = "l3_pt",
        texX = 'Trailing lepton p_{T} (GeV)', texY = 'Number of Events / 10 GeV',
        addOverFlowBin='both',
        attribute = TreeVariable.fromString( "l3_pt/F" ),
        binning=[40, 0, 400],
    ))

    plots.append(Plot(
        name = "l1_conept",
        texX = 'Leading lepton p_{T}^{cone} (GeV)', texY = 'Number of Events / 10 GeV',
        addOverFlowBin='both',
        attribute = lambda event, sample: event.l1_ptConeGhent if event.l1_passFO and not event.l1_passTight else event.l1_pt,
        binning=[40, 0, 400],
    ))

    plots.append(Plot(
        name = "l2_conept",
        texX = 'Subleading lepton p_{T}^{cone} (GeV)', texY = 'Number of Events / 10 GeV',
        addOverFlowBin='both',
        attribute = lambda event, sample: event.l2_ptConeGhent if event.l2_passFO and not event.l2_passTight else event.l2_pt,
        binning=[40, 0, 400],
    ))

    plots.append(Plot(
        name = "l3_conept",
        texX = 'Trailing lepton p_{T}^{cone} (GeV)', texY = 'Number of Events / 10 GeV',
        addOverFlowBin='both',
        attribute = lambda event, sample: event.l3_ptConeGhent if event.l3_passFO and not event.l3_passTight else event.l3_pt,
        binning=[40, 0, 400],
    ))

    plots.append(Plot(
        name = "fake_bscore_closest",
        texX = 'b tag score closest jet for fake leptons', texY = 'Number of Events',
        attribute = lambda event, sample: event.fakelepton_btagscores,
        binning=[40, 0, 1.0],
    ))


    if args.doTTbarReco:
        plots.append(Plot(
            name = "minimax",
            texX = 'minimax', texY = 'Number of Events',
            attribute = lambda event, sample: event.minimax,
            binning=[40,0,600],
            addOverFlowBin='upper',
        ))

    if args.nicePlots:

        plots.append(Plot(
            name = "l1_eta",
            texX = 'Leading lepton #eta', texY = 'Number of Events',
            addOverFlowBin='both',
            attribute = TreeVariable.fromString( "l1_eta/F" ),
            binning=[30, -3, 3],
        ))

        plots.append(Plot(
            name = "l2_eta",
            texX = 'Subleading lepton #eta', texY = 'Number of Events',
            addOverFlowBin='both',
            attribute = TreeVariable.fromString( "l2_eta/F" ),
            binning=[30, -3, 3],
        ))

        plots.append(Plot(
            name = "l3_eta",
            texX = 'Trailing lepton #eta', texY = 'Number of Events',
            addOverFlowBin='both',
            attribute = TreeVariable.fromString( "l3_eta/F" ),
            binning=[30, -3, 3],
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
            name = "JetIds",
            texX = 'Jet ID', texY = 'Number of Events',
            attribute = lambda event, sample: event.jetIds,
            binning=[10, -1.5, 8.5],
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
            name = "SF_LeptonReco",
            texX = 'Lepton Reco SF', texY = 'Number of Events',
            attribute = lambda event, sample: event.reweightElectronRecoSF if not sample.isData else -1,
            addOverFlowBin='both',
            binning=[50, 0.5, 1.5],
        ))

        plots.append(Plot(
            name = "SF_Fakerate",
            texX = 'Fakerate SF', texY = 'Number of Events',
            attribute = lambda event, sample: event.reweightLeptonFakerate if not sample.isData else -1,
            addOverFlowBin='both',
            binning=[100, -1.0, 1.0],
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
            name = "l1_mvaTOPscore",
            texX = 'Leading lepton MVA score', texY = 'Number of Events',
            attribute = lambda event, sample: event.l1_mvaTOP,
            binning=[30, -1.5, 1.5],
        ))

        plots.append(Plot(
            name = "l1_mvaTOPscore_v2",
            texX = 'Leading lepton MVA v2 score', texY = 'Number of Events',
            attribute = lambda event, sample: event.l1_mvaTOPv2,
            binning=[30, -1.5, 1.5],
        ))

        plots.append(Plot(
            name = "l1_passFO",
            texX = 'Leading lepton FO ID', texY = 'Number of Events',
            attribute = lambda event, sample: event.l1_passFO,
            binning=[3, -1.5, 1.5],
        ))

        plots.append(Plot(
            name = "l1_passTight",
            texX = 'Leading lepton Tight ID', texY = 'Number of Events',
            attribute = lambda event, sample: event.l1_passTight,
            binning=[3, -1.5, 1.5],
        ))

        plots.append(Plot(
            name = "l2_mvaTOPscore_v2",
            texX = 'Subleading lepton MVA v2 score', texY = 'Number of Events',
            attribute = lambda event, sample: event.l2_mvaTOPv2,
            binning=[30, -1.5, 1.5],
        ))

        plots.append(Plot(
            name = "l2_passFO",
            texX = 'Subleading lepton FO ID', texY = 'Number of Events',
            attribute = lambda event, sample: event.l2_passFO,
            binning=[3, -1.5, 1.5],
        ))

        plots.append(Plot(
            name = "l2_passTight",
            texX = 'Subleading lepton Tight ID', texY = 'Number of Events',
            attribute = lambda event, sample: event.l2_passTight,
            binning=[3, -1.5, 1.5],
        ))

        plots.append(Plot(
            name = "l3_mvaTOPscore_v2",
            texX = 'Trailing lepton MVA v2 score', texY = 'Number of Events',
            attribute = lambda event, sample: event.l3_mvaTOPv2,
            binning=[30, -1.5, 1.5],
        ))

        plots.append(Plot(
            name = "l3_passFO",
            texX = 'Trailing lepton FO ID', texY = 'Number of Events',
            attribute = lambda event, sample: event.l3_passFO,
            binning=[3, -1.5, 1.5],
        ))

        plots.append(Plot(
            name = "l3_passTight",
            texX = 'Trailing lepton Tight ID', texY = 'Number of Events',
            attribute = lambda event, sample: event.l3_passTight,
            binning=[3, -1.5, 1.5],
        ))

        if args.doTTbarReco:
            plots.append(Plot(
                name = "m_toplep",
                texX = 'm_{lep. top}', texY = 'Number of Events',
                attribute = lambda event, sample: event.mtoplep,
                binning=[40,0,400],
                addOverFlowBin='upper',
            ))

            plots.append(Plot(
                name = "m_tophad",
                texX = 'm_{had. top}', texY = 'Number of Events',
                attribute = lambda event, sample: event.mtophad,
                binning=[40,0,400],
                addOverFlowBin='upper',
            ))

            plots.append(Plot(
                name = "chi2",
                texX = '#chi^{2}', texY = 'Number of Events',
                attribute = lambda event, sample: event.chi2,
                binning=[40,0,1000],
                addOverFlowBin='upper',
            ))

    plotting.fill(plots, read_variables = read_variables, sequence = sequence)


    ################################################################################
    # Get normalization yields from yield histogram
    for plot in plots:
        if plot.name == "Z_mother_grouped":
            for i, l in enumerate(plot.histos):
                for j, h in enumerate(l):
                    h.GetXaxis().SetBinLabel(1, "other")
                    h.GetXaxis().SetBinLabel(2, "1st")
                    h.GetXaxis().SetBinLabel(3, "2nd")
                    h.GetXaxis().SetBinLabel(4, "3rd")
                    h.GetXaxis().SetBinLabel(5, "W/Z/H")
                    h.GetXaxis().SetBinLabel(6, "gluon")
                    h.GetXaxis().SetBinLabel(7, "lepton")
        if plot.name == "ProductionMode":
            for i, l in enumerate(plot.histos):
                for j, h in enumerate(l):
                    h.GetXaxis().SetBinLabel(1, "other")
                    h.GetXaxis().SetBinLabel(2, "1st")
                    h.GetXaxis().SetBinLabel(3, "2nd")
                    h.GetXaxis().SetBinLabel(4, "3rd")
                    h.GetXaxis().SetBinLabel(5, "1st+g")
                    h.GetXaxis().SetBinLabel(6, "2nd+g")
                    h.GetXaxis().SetBinLabel(7, "3rd+g")
                    h.GetXaxis().SetBinLabel(8, "g+g")
        if plot.name == "ProductionModeWZ":
            for i, l in enumerate(plot.histos):
                for j, h in enumerate(l):
                    h.GetXaxis().SetBinLabel(1, "t channel")
                    h.GetXaxis().SetBinLabel(2, "s channel")
        if plot.name == "yield":
            for i, l in enumerate(plot.histos):
                for j, h in enumerate(l):
                    yields[mode][plot.stack[i][j].name] = h.GetBinContent(h.FindBin(0.5+i_mode))
                    if 'qualep' in args.selection:
                        h.GetXaxis().SetBinLabel(1, "#mu#mu#mu#mu")
                        h.GetXaxis().SetBinLabel(2, "#mu#muee")
                        h.GetXaxis().SetBinLabel(3, "eeee")
                    else:
                        h.GetXaxis().SetBinLabel(1, "#mu#mu#mu")
                        h.GetXaxis().SetBinLabel(2, "#mu#mue")
                        h.GetXaxis().SetBinLabel(3, "#muee")
                        h.GetXaxis().SetBinLabel(4, "eee")

    if args.noData: yields[mode]["data"] = 0

    yields[mode]["MC"] = sum(yields[mode][s.name] for s in mc  + samples_eft)
    dataMCScale        = yields[mode]["data"]/yields[mode]["MC"] if yields[mode]["MC"] != 0 else float('nan')


    if args.nicePlots and args.sys == "central":
        drawPlots(plots, mode, dataMCScale)

    allPlots[mode] = plots


################################################################################
# Add all different channels
yields["all"] = {}
for y in yields[allModes[0]]:
    try:    yields["all"][y] = sum(yields[c][y] for c in allModes)
    except: yields["all"][y] = 0
dataMCScale = yields["all"]["data"]/yields["all"]["MC"] if yields["all"]["MC"] != 0 else float('nan')

allPlots["all"] = copy.deepcopy(allPlots[allModes[0]])
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


if args.nicePlots and args.sys == "central":
    drawPlots(allPlots['all'], "all", dataMCScale)


# Write Result Hist in root file
if not args.nicePlots:
    plots_root = ["Z1_pt", "M3l", "l1_pt", "l2_pt", "l3_pt", "N_jets", "yield"]
    logger.info( "Now write results in root files." )
    for mode in allModes+["all"]:
        logger.info( "Write file for channel: %s", mode )
        plot_dir = os.path.join(plot_directory, 'analysisPlots', args.plot_directory, args.era, mode, args.selection)
        if not os.path.exists(plot_dir):
            try:
                os.makedirs(plot_dir)
            except:
                print 'Could not create', plot_dir
        outfilename = plot_dir+'/Results.root'
        if args.twoD:
            outfilename = plot_dir+'/Results_twoD.root'
            if args.triplet:
                outfilename = plot_dir+'/Results_twoD_triplet.root'
        print "Saving in", outfilename
        outfile = ROOT.TFile(outfilename, 'recreate')
        outfile.cd()
        for plot in allPlots[mode]:
            if plot.name in plots_root:
                for idx, histo_list in enumerate(plot.histos):
                    for j, h in enumerate(histo_list):
                        histname = h.GetName()
                        if "TWZ_NLO_DR" in histname: process = "tWZ"
                        elif "tWZToLL01j_lepWFilter" in histname: process = "tWZ"
                        elif "ttZ01j_lepWFilter" in histname: process = "ttZ"
                        elif "ttZ01j" in histname: process = "ttZ"
                        elif "TTZ_EFT" in histname: process = "ttZ"
                        elif "TTZ" in histname: process = "ttZ"
                        elif "TTX_rare_noTTW" in histname: process = "ttX_noTTW"
                        elif "TTX_rare" in histname: process = "ttX"
                        elif "TTW" in histname: process = "ttW"
                        elif "TZQ" in histname: process = "tZq"
                        elif "WZTo3LNu" in histname: process = "WZ"
                        elif "WZ_EFT" in histname: process = "WZ"
                        elif "WZ" in histname: process = "WZ"
                        elif "ZZ_EFT" in histname: process = "ZZ"
                        elif "ZZ" in histname: process = "ZZ"
                        elif "triBoson" in histname: process = "triBoson"
                        elif "nonprompt" in histname: process = "nonprompt"
                        elif "WW" in histname: process = "WW"
                        elif "Top" in histname: process = "tt+ST"
                        elif "DY" in histname: process = "DY"
                        elif "data" in histname: process = "data"
                        # Also add a string for the eft signal samples
                        n_noneft = len(noneftidxs)
                        if not args.nicePlots and idx not in noneftidxs:
                            h.Write(plot.name+"__"+process+"__"+params[idx-n_noneft]['legendText'])
                            if args.twoD:
                                string = params[idx-n_noneft]['legendText']
                                if string.count('=0.0000') == 2:
                                    h_SM = h.Clone()
                                    h_SM.Write(plot.name+"__"+process)
                            else:
                                if "=0.0000" in params[idx-n_noneft]['legendText']:
                                    h_SM = h.Clone()
                                    h_SM.Write(plot.name+"__"+process)
                        else:
                            h.Write(plot.name+"__"+process)
        outfile.Close()



logger.info( "Done with prefix %s and selectionString %s", args.selection, selection_string )
