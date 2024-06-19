#!/usr/bin/env python

import ROOT
import array
import Analysis.Tools.syncer
import os
import numpy as np

from math                                        import sqrt
from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--noData',           action='store_true', default=False)
argParser.add_argument('--signalInjectionLight',  action='store_true', default=False)
argParser.add_argument('--signalInjectionHeavy',  action='store_true', default=False)
argParser.add_argument('--signalInjectionMixed',  action='store_true', default=False)
argParser.add_argument('--signalInjectionWZjets',  action='store_true', default=False)
argParser.add_argument('--fluctuatePseudoData',  action='store_true', default=False)
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
argParser.add_argument('--light',            action='store_true', default=False)
argParser.add_argument('--NjetSplit',        action='store_true', default=False)
argParser.add_argument('--scaleCorrelation', action='store_true', default=False)
args = argParser.parse_args()

################################################################################
### Functions
def getRMS(nominal, variations):
    up   = nominal.Clone()
    down = nominal.Clone()
    Nbins = nominal.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        diff_sum2_up = 0
        diff_sum2_down = 0
        Nvars_up = 0
        Nvars_down = 0
        for var in variations:
            diff = var.GetBinContent(bin)-nominal.GetBinContent(bin)
            if diff > 0:
                diff_sum2_up += diff*diff
                Nvars_up += 1
            else:
                diff_sum2_down += diff*diff
                Nvars_down += 1
        rmsup = sqrt(diff_sum2_up/Nvars_up) if Nvars_up > 0 else 0
        rmsdown = sqrt(diff_sum2_down/Nvars_down) if Nvars_down > 0 else 0
        up.SetBinContent(bin, nominal.GetBinContent(bin)+rmsup)
        down.SetBinContent(bin, nominal.GetBinContent(bin)-rmsdown)
    return (up, down)

def getLinear(hist_plus, hist_minus):
    # Since the quadratic term does not change sign, we can get it from the
    # histograms where c = +1, c = 0, and c = -1
    # (1) c = +1 is SM + LIN + QUAD
    # (2) c = -1 is SM - LIN + QUAD

    # Thus, we can get the lin from
    # (1)-(2) = SM + LIN + QUAD - SM + LIN - QUAD
    #         = 2* LIN     | /2
    # ((1)-(2))/2 = LIN
    hist_lin = hist_plus.Clone(hist_plus.GetName()+"_quad")
    hist_lin.Add(hist_minus, -1)
    hist_lin.Scale(0.5)
    return hist_lin

def getQuadratic(hist_sm, hist_plus, hist_minus):
    # Since the quadratic term does not change sign, we can get it from the
    # histograms where c = +1, c = 0, and c = -1
    # (1) c = +1 is SM + LIN + QUAD
    # (2) c = -1 is SM - LIN + QUAD
    # (3) c =  0 is SM

    # Thus, we can get the quad from
    # (1)+(2) = SM + SM + QUAD + QUAD | -2*(3)
    # (1)+(2)-2*(3) = QUAD + QUAD     | /2
    # 0.5*[(1)+(2)-2*(3)] = QUAD
    hist_quad = hist_plus.Clone(hist_plus.GetName()+"_quad")
    hist_quad.Add(hist_minus)
    hist_quad.Add(hist_sm, -2)
    hist_quad.Scale(0.5)
    return hist_quad

def setPseudoDataErrors(hist):
    newhist = hist.Clone()
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        content = hist.GetBinContent(bin)
        newhist.SetBinError(bin, sqrt(content))
    return newhist

def fluctuatePseudoData(hist):
    newhist = hist.Clone(hist.GetName()+"_fluctuated")
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        content = hist.GetBinContent(bin)
        error = hist.GetBinError(bin)
        new_content = np.random.poisson(content)
        diff = new_content - content
        if abs(diff) > 0.5*error:
            if diff > 0:
                new_content = content + 0.5*error
            else:
                new_content = content - 0.5*error
        print(content, new_content, error)
        newhist.SetBinContent(bin, new_content)
        newhist.SetBinError(bin, sqrt(new_content))
    return newhist

def removeNegative(hist):
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        content = hist.GetBinContent(bin)
        if content < 0:
            hist.SetBinContent(bin, 0.01)
    return hist

def removeZeros(hist):
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        content = hist.GetBinContent(bin)
        if content < 0.01:
            hist.SetBinContent(bin, 0.01)
    return hist

def getHist(fname, hname, altbinning=False):
    bins  = [0, 60, 120, 180, 240, 300, 400, 1000]
    if altbinning:
        bins  = [0, 60, 120, 180, 1000]
    if "ULRunII" in fname:
        # Get histograms from each era
        hist_18 = getObjFromFile(fname.replace("/ULRunII/", "/UL2018/"), hname)
        hist_17 = getObjFromFile(fname.replace("/ULRunII/", "/UL2017/"), hname)
        hist_16 = getObjFromFile(fname.replace("/ULRunII/", "/UL2016/"), hname)
        hist_16preVFP = getObjFromFile(fname.replace("/ULRunII/", "/UL2016preVFP/"), hname)
        # add them
        hist = hist_18.Clone(hist_18.GetName()+"_RunIIcombination")
        hist.Add(hist_17)
        hist.Add(hist_16)
        hist.Add(hist_16preVFP)
    else:
        hist = getObjFromFile(fname, hname)
    hist = hist.Rebin(len(bins)-1, hist.GetName()+"_rebin", array.array('d',bins))
    hist = removeNegative(hist)
    if hist.Integral() < 0.01:
        hist = removeZeros(hist)
    return hist

def getCombinedSignal_SM(fname, hname, altbinning, rate=None, rate_process=None, sys_processes=[], fname_sys=None):
    signale = ["ttZ_sm", "WZTo3LNu", "ZZ_powheg"]
    for i_sig, sig in enumerate(signals):
        # If one of the signals should be varied, use alternative file
        filename = fname
        if sig in sys_processes:
            filename = fname_sys
        # If this is the first in the loop clone, otherwise Add to cloned
        if i_sig==0:
            hist = getHist(filename, hname.replace("sm", sig), altbinning)
            if sig == rate_process:
                hist.Scale(rate)
        else:
            tmp = getHist(filename, hname.replace("sm", sig), altbinning)
            if sig == rate_process:
                tmp.Scale(rate)
            hist.Add(tmp)
    return hist

def getCombinedSignal_EFT(fname, hname, altbinning, rate=None, rate_process=None, sys_processes=[], fname_sys=None):
    signals = ["ttZ", "WZ", "ZZ"]
    for i_sig, sig in enumerate(signals):
        # If one of the signals should be varied, use alternative file
        filename = fname
        if sig in sys_processes:
            filename = fname_sys
        # If this is the first in the loop clone, otherwise Add to cloned
        if i_sig==0:
            hist = getHist(filename, hname.replace("sm", sig), altbinning)
            if sig == rate_process:
                hist.Scale(rate)
        else:
            tmp = getHist(filename, hname.replace("sm", sig), altbinning)
            if sig == rate_process:
                tmp.Scale(rate)
            hist.Add(tmp)
    return hist

def getNonpromptFromCR(fname, histname, altbinning, backgrounds):
    # Get prompt backgrounds in CR
    firstbkg = True
    for bkg in backgrounds:
        # print fname, histname+"__"+bkg
        h_bkg = getHist(fname, histname+"__"+bkg, altbinning)
        if firstbkg:
            h_bkg_CR = h_bkg.Clone()
            firstbkg = False
        else:
            h_bkg_CR.Add(h_bkg)
    # Get nonprompt = Data in CR * fakerate and subtract backgrounds
    h_nonprompt = getHist(fname, histname+"__data", altbinning)
    h_nonprompt.Add(h_bkg_CR, -1)
    h_nonprompt = removeNegative(h_nonprompt) # make sure there are no negative bins
    return h_nonprompt

################################################################################
### Setup
logger.info( "Prepare input file for combine.")

if args.year not in ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]:
    raise RuntimeError( "Year %s is not knwon", args.year)
logger.info( "Year = %s", args.year )
if args.year == "ULRunII":
    logger.info( "For the RunII combination, histograms of the eras are added" )

if args.NjetSplit:
    logger.info( "Will split ttZ region in 3 jet and 4+ jet regions" )

if args.scaleCorrelation:
    logger.info( "Correlating QCD scales of Diboson processes" )

# regions
regions = ["WZ", "ZZ", "ttZ"]
if args.NjetSplit:
    regions = ["WZ", "ZZ", "ttZ_3jets", "ttZ_4jets"]


# histname
histname = "Z1_pt"

version = "v14"
logger.info( "Version = %s", version )

if args.noData:
    logger.info( "Use Asimov data (blind)" )
else:
    logger.info( "Use data (unblinded)" )

dataTag = "_noData" if args.noData else ""

# Directories
dirs = {
    "ZZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/"+args.year+"/all/qualepT-minDLmass12-onZ1-onZ2/",
    "WZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/"+args.year+"/all/trilepT-minDLmass12-onZ1-btag0-met60/",
    "ttZ":    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/"+args.year+"/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/",
    "WZ_CR":  "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_threePoint_FakeRateSF_useDataSF/"+args.year+"/all/trilepFOnoT-minDLmass12-onZ1-btag0-met60/",
    "ttZ_CR": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_threePoint_FakeRateSF_useDataSF/"+args.year+"/all/trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p/",
    "ttZ_3jets":    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/"+args.year+"/all/trilepT-minDLmass12-onZ1-njet3-btag1p/",
    "ttZ_4jets":    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/"+args.year+"/all/trilepT-minDLmass12-onZ1-njet4p-btag1p/",
    "ttZ_3jets_CR": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_threePoint_FakeRateSF_useDataSF/"+args.year+"/all/trilepFOnoT-minDLmass12-onZ1-njet3-btag1p/",
    "ttZ_4jets_CR": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_threePoint_FakeRateSF_useDataSF/"+args.year+"/all/trilepFOnoT-minDLmass12-onZ1-njet4p-btag1p/",
}

dirname_suffix = ""
if args.light:               dirname_suffix+="_light"
if args.NjetSplit:           dirname_suffix+="_NjetSplit"
if args.scaleCorrelation:    dirname_suffix+="_scaleCorrelation"
if args.signalInjectionLight:     dirname_suffix+="_signalInjectionLight"
if args.signalInjectionHeavy:     dirname_suffix+="_signalInjectionHeavy"
if args.signalInjectionMixed:     dirname_suffix+="_signalInjectionMixed"
if args.signalInjectionWZjets:     dirname_suffix+="_signalInjectionWZjets"
if args.fluctuatePseudoData:       dirname_suffix+="_fluctuatePseudoData"

outdir = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_threePoint"+dataTag+dirname_suffix+"/"+args.year+"/"
plotdir = plot_directory+"/PreFit_threePoint"+dirname_suffix+"/"

if not os.path.exists( outdir ): os.makedirs( outdir )
if not os.path.exists( plotdir ): os.makedirs( plotdir )


# Define backgrounds
processes = ["sm", "tWZ", "ttX", "tZq", "triBoson", "ggToZZ", "nonprompt"]
signals = ["WZ", "ZZ", "ttZ"]
processes_CR = ["ttZ_sm", "WZTo3LNu", "ZZ_powheg", "tWZ", "ttX", "tZq", "triBoson", "ggToZZ"]


WCnames = ["cHq1Re11", "cHq1Re22", "cHq1Re33", "cHq3Re11", "cHq3Re22", "cHq3Re33"]
WCnames_mixed = {}

if args.light:
    WCnames = ["cHq1Re1122", "cHq1Re33", "cHq3Re1122", "cHq3Re33"]
    WCnames_mixed = {
        "cHq1Re112233": ("cHq1Re1122", "cHq1Re33"),
        "cHq3Re112233": ("cHq3Re1122", "cHq3Re33"),
    }

processinfo = {
    "sm":        ("ttZ+WZ+ZZ", ROOT.kAzure+7),
    "ttZ":       ("ttZ", color.TTZ),
    "WZ":        ("WZ",  color.WZ),
    "ZZ":        ("ZZ", color.ZZ),
    "tWZ":       ("tWZ", color.TWZ),
    "ttX":       ("ttX", color.TTX_rare),
    "tZq":       ("tZq", color.TZQ),
    "triBoson":  ("Triboson", color.triBoson),
    "ggToZZ":    ("gg #rightarrow ZZ", color.ZZ),
    "nonprompt": ("Nonprompt", color.nonprompt),
}

lumi = {
    "UL2016preVFP": "19.5",
    "UL2016":       "16.5",
    "UL2017":       "41.5",
    "UL2018":       "60",
    "ULRunII":      "138",
}

# Define Systematics
sysnames = {
    "BTag_b_correlated":              ("_BTag_b_correlated_UP", "_BTag_b_correlated_DOWN"),
    "BTag_l_correlated":              ("_BTag_l_correlated_UP", "_BTag_l_correlated_DOWN"),
    "BTag_b_uncorrelated_2016preVFP": ("_BTag_b_uncorrelated_2016preVFP_UP", "_BTag_b_uncorrelated_2016preVFP_DOWN"),
    "BTag_l_uncorrelated_2016preVFP": ("_BTag_l_uncorrelated_2016preVFP_UP", "_BTag_l_uncorrelated_2016preVFP_DOWN"),
    "BTag_b_uncorrelated_2016":       ("_BTag_b_uncorrelated_2016_UP", "_BTag_b_uncorrelated_2016_DOWN"),
    "BTag_l_uncorrelated_2016":       ("_BTag_l_uncorrelated_2016_UP", "_BTag_l_uncorrelated_2016_DOWN"),
    "BTag_b_uncorrelated_2017":       ("_BTag_b_uncorrelated_2017_UP", "_BTag_b_uncorrelated_2017_DOWN"),
    "BTag_l_uncorrelated_2017":       ("_BTag_l_uncorrelated_2017_UP", "_BTag_l_uncorrelated_2017_DOWN"),
    "BTag_b_uncorrelated_2018":       ("_BTag_b_uncorrelated_2018_UP", "_BTag_b_uncorrelated_2018_DOWN"),
    "BTag_l_uncorrelated_2018":       ("_BTag_l_uncorrelated_2018_UP", "_BTag_l_uncorrelated_2018_DOWN"),
    "Fakerate":                       ("_Fakerate_UP", "_Fakerate_DOWN"), # THIS IS ONLY IN NONPROMPT
    "FakerateClosure_correlated_elec":              ("_FakerateClosure_correlated_elec_UP", "_FakerateClosure_correlated_elec_DOWN"),
    "FakerateClosure_uncorrelated_elec_2016preVFP": ("_FakerateClosure_uncorrelated_elec_2016preVFP_UP", "_FakerateClosure_uncorrelated_elec_2016preVFP_DOWN"),
    "FakerateClosure_uncorrelated_elec_2016":       ("_FakerateClosure_uncorrelated_elec_2016_UP", "_FakerateClosure_uncorrelated_elec_2016_DOWN"),
    "FakerateClosure_uncorrelated_elec_2017":       ("_FakerateClosure_uncorrelated_elec_2017_UP", "_FakerateClosure_uncorrelated_elec_2017_DOWN"),
    "FakerateClosure_uncorrelated_elec_2018":       ("_FakerateClosure_uncorrelated_elec_2018_UP", "_FakerateClosure_uncorrelated_elec_2018_DOWN"),
    "FakerateClosure_correlated_muon":              ("_FakerateClosure_correlated_muon_UP", "_FakerateClosure_correlated_muon_DOWN"),
    "FakerateClosure_uncorrelated_muon_2016preVFP": ("_FakerateClosure_uncorrelated_muon_2016preVFP_UP", "_FakerateClosure_uncorrelated_muon_2016preVFP_DOWN"),
    "FakerateClosure_uncorrelated_muon_2016":       ("_FakerateClosure_uncorrelated_muon_2016_UP", "_FakerateClosure_uncorrelated_muon_2016_DOWN"),
    "FakerateClosure_uncorrelated_muon_2017":       ("_FakerateClosure_uncorrelated_muon_2017_UP", "_FakerateClosure_uncorrelated_muon_2017_DOWN"),
    "FakerateClosure_uncorrelated_muon_2018":       ("_FakerateClosure_uncorrelated_muon_2018_UP", "_FakerateClosure_uncorrelated_muon_2018_DOWN"),
    "FakerateClosure_correlated_both":              ("_FakerateClosure_correlated_both_UP", "_FakerateClosure_correlated_both_DOWN"),
    "FakerateClosure_uncorrelated_both_2016preVFP": ("_FakerateClosure_uncorrelated_both_2016preVFP_UP", "_FakerateClosure_uncorrelated_both_2016preVFP_DOWN"),
    "FakerateClosure_uncorrelated_both_2016":       ("_FakerateClosure_uncorrelated_both_2016_UP", "_FakerateClosure_uncorrelated_both_2016_DOWN"),
    "FakerateClosure_uncorrelated_both_2017":       ("_FakerateClosure_uncorrelated_both_2017_UP", "_FakerateClosure_uncorrelated_both_2017_DOWN"),
    "FakerateClosure_uncorrelated_both_2018":       ("_FakerateClosure_uncorrelated_both_2018_UP", "_FakerateClosure_uncorrelated_both_2018_DOWN"),
    "Trigger_2016preVFP":             ("_Trigger_2016preVFP_UP", "_Trigger_2016preVFP_DOWN"),
    "Trigger_2016":                   ("_Trigger_2016_UP", "_Trigger_2016_DOWN"),
    "Trigger_2017":                   ("_Trigger_2017_UP", "_Trigger_2017_DOWN"),
    "Trigger_2018":                   ("_Trigger_2018_UP", "_Trigger_2018_DOWN"),
    "Prefire":                        ("_Prefire_UP", "_Prefire_DOWN"),
    "LepReco":                        ("_LepReco_UP", "_LepReco_DOWN"),
    "LepIDstat_elec_2016preVFP":      ("_LepIDstat_elec_2016preVFP_UP", "_LepIDstat_elec_2016preVFP_DOWN"),
    "LepIDstat_elec_2016":            ("_LepIDstat_elec_2016_UP", "_LepIDstat_elec_2016_DOWN"),
    "LepIDstat_elec_2017":            ("_LepIDstat_elec_2017_UP", "_LepIDstat_elec_2017_DOWN"),
    "LepIDstat_elec_2018":            ("_LepIDstat_elec_2018_UP", "_LepIDstat_elec_2018_DOWN"),
    "LepIDsys_elec":                  ("_LepIDsys_elec_UP", "_LepIDsys_elec_DOWN"),
    "LepIDstat_muon_2016preVFP":      ("_LepIDstat_muon_2016preVFP_UP", "_LepIDstat_muon_2016preVFP_DOWN"),
    "LepIDstat_muon_2016":            ("_LepIDstat_muon_2016_UP", "_LepIDstat_muon_2016_DOWN"),
    "LepIDstat_muon_2017":            ("_LepIDstat_muon_2017_UP", "_LepIDstat_muon_2017_DOWN"),
    "LepIDstat_muon_2018":            ("_LepIDstat_muon_2018_UP", "_LepIDstat_muon_2018_DOWN"),
    "LepIDsys_muon":                  ("_LepIDsys_muon_UP", "_LepIDsys_muon_DOWN"),
    "PU":                             ("_PU_UP", "_PU_DOWN"),
    # "JES":                            ("_JES_UP", "_JES_DOWN"),
    "JES_AbsoluteMPFBias":            ("_AbsoluteMPFBias_UP", "_AbsoluteMPFBias_DOWN"),
    "JES_AbsoluteScale":              ("_AbsoluteScale_UP", "_AbsoluteScale_DOWN"),
    "JES_AbsoluteStat_2016preVFP":    ("_AbsoluteStat_2016preVFP_UP", "_AbsoluteStat_2016preVFP_DOWN"),
    "JES_AbsoluteStat_2016":          ("_AbsoluteStat_2016_UP", "_AbsoluteStat_2016_DOWN"),
    "JES_AbsoluteStat_2017":          ("_AbsoluteStat_2017_UP", "_AbsoluteStat_2017_DOWN"),
    "JES_AbsoluteStat_2018":          ("_AbsoluteStat_2018_UP", "_AbsoluteStat_2018_DOWN"),
    "JES_RelativeBal":                ("_RelativeBal_UP", "_RelativeBal_DOWN"),
    "JES_RelativeFSR":                ("_RelativeFSR_UP", "_RelativeFSR_DOWN"),
    "JES_RelativeJEREC1_2016preVFP":  ("_RelativeJEREC1_2016preVFP_UP", "_RelativeJEREC1_2016preVFP_DOWN"),
    "JES_RelativeJEREC1_2016":        ("_RelativeJEREC1_2016_UP", "_RelativeJEREC1_2016_DOWN"),
    "JES_RelativeJEREC1_2017":        ("_RelativeJEREC1_2017_UP", "_RelativeJEREC1_2017_DOWN"),
    "JES_RelativeJEREC1_2018":        ("_RelativeJEREC1_2018_UP", "_RelativeJEREC1_2018_DOWN"),
    "JES_RelativeJEREC2_2016preVFP":  ("_RelativeJEREC2_2016preVFP_UP", "_RelativeJEREC2_2016preVFP_DOWN"),
    "JES_RelativeJEREC2_2016":        ("_RelativeJEREC2_2016_UP", "_RelativeJEREC2_2016_DOWN"),
    "JES_RelativeJEREC2_2017":        ("_RelativeJEREC2_2017_UP", "_RelativeJEREC2_2017_DOWN"),
    "JES_RelativeJEREC2_2018":        ("_RelativeJEREC2_2018_UP", "_RelativeJEREC2_2018_DOWN"),
    "JES_RelativeJERHF":              ("_RelativeJERHF_UP", "_RelativeJERHF_DOWN"),
    "JES_RelativePtBB":               ("_RelativePtBB_UP", "_RelativePtBB_DOWN"),
    "JES_RelativePtEC1_2016preVFP":   ("_RelativePtEC1_2016preVFP_UP", "_RelativePtEC1_2016preVFP_DOWN"),
    "JES_RelativePtEC1_2016":         ("_RelativePtEC1_2016_UP", "_RelativePtEC1_2016_DOWN"),
    "JES_RelativePtEC1_2017":         ("_RelativePtEC1_2017_UP", "_RelativePtEC1_2017_DOWN"),
    "JES_RelativePtEC1_2018":         ("_RelativePtEC1_2018_UP", "_RelativePtEC1_2018_DOWN"),
    "JES_RelativePtEC2_2016preVFP":   ("_RelativePtEC2_2016preVFP_UP", "_RelativePtEC2_2016preVFP_DOWN"),
    "JES_RelativePtEC2_2016":         ("_RelativePtEC2_2016_UP", "_RelativePtEC2_2016_DOWN"),
    "JES_RelativePtEC2_2017":         ("_RelativePtEC2_2017_UP", "_RelativePtEC2_2017_DOWN"),
    "JES_RelativePtEC2_2018":         ("_RelativePtEC2_2018_UP", "_RelativePtEC2_2018_DOWN"),
    "JES_RelativePtHF":               ("_RelativePtHF_UP", "_RelativePtHF_DOWN"),
    "JES_RelativeStatEC_2016preVFP":  ("_RelativeStatEC_2016preVFP_UP", "_RelativeStatEC_2016preVFP_DOWN"),
    "JES_RelativeStatEC_2016":        ("_RelativeStatEC_2016_UP", "_RelativeStatEC_2016_DOWN"),
    "JES_RelativeStatEC_2017":        ("_RelativeStatEC_2017_UP", "_RelativeStatEC_2017_DOWN"),
    "JES_RelativeStatEC_2018":        ("_RelativeStatEC_2018_UP", "_RelativeStatEC_2018_DOWN"),
    "JES_RelativeStatFSR_2016preVFP": ("_RelativeStatFSR_2016preVFP_UP", "_RelativeStatFSR_2016preVFP_DOWN"),
    "JES_RelativeStatFSR_2016":       ("_RelativeStatFSR_2016_UP", "_RelativeStatFSR_2016_DOWN"),
    "JES_RelativeStatFSR_2017":       ("_RelativeStatFSR_2017_UP", "_RelativeStatFSR_2017_DOWN"),
    "JES_RelativeStatFSR_2018":       ("_RelativeStatFSR_2018_UP", "_RelativeStatFSR_2018_DOWN"),
    "JES_RelativeStatHF_2016preVFP":  ("_RelativeStatHF_2016preVFP_UP", "_RelativeStatHF_2016preVFP_DOWN"),
    "JES_RelativeStatHF_2016":        ("_RelativeStatHF_2016_UP", "_RelativeStatHF_2016_DOWN"),
    "JES_RelativeStatHF_2017":        ("_RelativeStatHF_2017_UP", "_RelativeStatHF_2017_DOWN"),
    "JES_RelativeStatHF_2018":        ("_RelativeStatHF_2018_UP", "_RelativeStatHF_2018_DOWN"),
    "JES_RelativeSample_2016preVFP":  ("_RelativeSample_2016preVFP_UP", "_RelativeSample_2016preVFP_DOWN"),
    "JES_RelativeSample_2016":        ("_RelativeSample_2016_UP", "_RelativeSample_2016_DOWN"),
    "JES_RelativeSample_2017":        ("_RelativeSample_2017_UP", "_RelativeSample_2017_DOWN"),
    "JES_RelativeSample_2018":        ("_RelativeSample_2018_UP", "_RelativeSample_2018_DOWN"),
    "JES_PileUpDataMC":               ("_PileUpDataMC_UP", "_PileUpDataMC_DOWN"),
    "JES_PileUpPtBB":                 ("_PileUpPtBB_UP", "_PileUpPtBB_DOWN"),
    "JES_PileUpPtEC1":                ("_PileUpPtEC1_UP", "_PileUpPtEC1_DOWN"),
    "JES_PileUpPtEC2":                ("_PileUpPtEC2_UP", "_PileUpPtEC2_DOWN"),
    "JES_PileUpPtHF":                 ("_PileUpPtHF_UP", "_PileUpPtHF_DOWN"),
    "JES_PileUpPtRef":                ("_PileUpPtRef_UP", "_PileUpPtRef_DOWN"),
    "JES_FlavorQCD":                  ("_FlavorQCD_UP", "_FlavorQCD_DOWN"),
    "JES_Fragmentation":              ("_Fragmentation_UP", "_Fragmentation_DOWN"),
    "JES_SinglePionECAL":             ("_SinglePionECAL_UP", "_SinglePionECAL_DOWN"),
    "JES_SinglePionHCAL":             ("_SinglePionHCAL_UP", "_SinglePionHCAL_DOWN"),
    "JES_TimePtEta_2016preVFP":       ("_TimePtEta_2016preVFP_UP", "_TimePtEta_2016preVFP_DOWN"),
    "JES_TimePtEta_2016":             ("_TimePtEta_2016_UP", "_TimePtEta_2016_DOWN"),
    "JES_TimePtEta_2017":             ("_TimePtEta_2017_UP", "_TimePtEta_2017_DOWN"),
    "JES_TimePtEta_2018":             ("_TimePtEta_2018_UP", "_TimePtEta_2018_DOWN"),
    "JER_2016preVFP":                 ("_JER_2016preVFP_UP", "_JER_2016preVFP_DOWN"),
    "JER_2016":                       ("_JER_2016_UP", "_JER_2016_DOWN"),
    "JER_2017":                       ("_JER_2017_UP", "_JER_2017_DOWN"),
    "JER_2018":                       ("_JER_2018_UP", "_JER_2018_DOWN"),
    "Unclustered_2016preVFP":         ("_Unclustered_2016preVFP_UP", "_Unclustered_2016preVFP_DOWN"),
    "Unclustered_2016":               ("_Unclustered_2016_UP", "_Unclustered_2016_DOWN"),
    "Unclustered_2017":               ("_Unclustered_2017_UP", "_Unclustered_2017_DOWN"),
    "Unclustered_2018":               ("_Unclustered_2018_UP", "_Unclustered_2018_DOWN"),
    "Lumi_uncorrelated_2016":         ("_Lumi_uncorrelated_2016_UP", "_Lumi_uncorrelated_2016_DOWN"),
    "Lumi_uncorrelated_2017":         ("_Lumi_uncorrelated_2017_UP", "_Lumi_uncorrelated_2017_DOWN"),
    "Lumi_uncorrelated_2018":         ("_Lumi_uncorrelated_2018_UP", "_Lumi_uncorrelated_2018_DOWN"),
    "Lumi_correlated_161718":         ("_Lumi_correlated_161718_UP", "_Lumi_correlated_161718_DOWN"),
    "Lumi_correlated_1718":           ("_Lumi_correlated_1718_UP", "_Lumi_correlated_1718_DOWN"),
    "ISR_ttZ":                        ("_ISR_UP", "_ISR_DOWN"),
    "ISR_WZ":                         ("_ISR_UP", "_ISR_DOWN"),
    "ISR_ZZ":                         ("_ISR_UP", "_ISR_DOWN"),
    "ISR_tZq":                        ("_ISR_UP", "_ISR_DOWN"),
    "ISR_tWZ":                        ("_ISR_UP", "_ISR_DOWN"),
    "ISR_ttX":                        ("_ISR_UP", "_ISR_DOWN"),
    "ISR_triBoson":                   ("_ISR_UP", "_ISR_DOWN"),
    "ISR_ggToZZ":                     ("_ISR_UP", "_ISR_DOWN"),
    "FSR":                            ("_FSR_UP", "_FSR_DOWN"),
    # "FSR_ttZ":                        ("_FSR_UP", "_FSR_DOWN"),
    # "FSR_WZ":                         ("_FSR_UP", "_FSR_DOWN"),
    # "FSR_ZZ":                         ("_FSR_UP", "_FSR_DOWN"),
    # "FSR_tZq":                        ("_FSR_UP", "_FSR_DOWN"),
    # "FSR_tWZ":                        ("_FSR_UP", "_FSR_DOWN"),
    # "FSR_ttX":                        ("_FSR_UP", "_FSR_DOWN"),
    # "FSR_triBoson":                   ("_FSR_UP", "_FSR_DOWN"),
    # "FSR_ggToZZ":                     ("_FSR_UP", "_FSR_DOWN"),
    "muR_ttZ":                        ("_Scale_UPNONE", "_Scale_DOWNNONE"),
    "muR_WZ":                         ("_Scale_UPNONE", "_Scale_DOWNNONE"),
    "muR_ZZ":                         ("_Scale_UPNONE", "_Scale_DOWNNONE"),
    "muR_tZq":                        ("_Scale_UPNONE", "_Scale_DOWNNONE"),
    "muR_tWZ":                        ("_Scale_UPNONE", "_Scale_DOWNNONE"),
    "muR_ttX":                        ("_Scale_UPNONE", "_Scale_DOWNNONE"),
    "muR_triBoson":                   ("_Scale_UPNONE", "_Scale_DOWNNONE"),
    # "muR_ggToZZ":                     ("_Scale_UPNONE", "_Scale_DOWNNONE"),
    "muF_ttZ":                        ("_Scale_NONEUP", "_Scale_NONEDOWN"),
    "muF_WZ":                         ("_Scale_NONEUP", "_Scale_NONEDOWN"),
    "muF_ZZ":                         ("_Scale_NONEUP", "_Scale_NONEDOWN"),
    "muF_tZq":                        ("_Scale_NONEUP", "_Scale_NONEDOWN"),
    "muF_tWZ":                        ("_Scale_NONEUP", "_Scale_NONEDOWN"),
    "muF_ttX":                        ("_Scale_NONEUP", "_Scale_NONEDOWN"),
    "muF_triBoson":                   ("_Scale_NONEUP", "_Scale_NONEDOWN"),
    # "muF_ggToZZ":                     ("_Scale_NONEUP", "_Scale_NONEDOWN"),
    "rate_ttZ":                       (),
    "rate_WZ":                        (),
    "rate_ZZ":                        (),
    "WZ_Njet_reweight":               ("_WZnJet", ""),
    "WZ_heavyFlavour":                ("_WZheavy_UP", "_WZheavy_DOWN"),
    "EWK_mul_ZZ":                     ("_EWK_mul", ""),
    "EWK_mul_WZ":                     ("_EWK_mul", ""),
    "EWK_add_ZZ":                     ("_EWK_add", ""),
    "EWK_add_WZ":                     ("_EWK_add", ""),
}

for i in range(100):
    pdfstring = 'PDF_'+str(i+1)
    sysnames[pdfstring] = ('_'+pdfstring, "")


if args.scaleCorrelation:
    del sysnames['muR_WZ']
    del sysnames['muR_ZZ']
    del sysnames['muF_WZ']
    del sysnames['muF_ZZ']
    sysnames['muR_diboson'] = ("_Scale_UPNONE", "_Scale_DOWNNONE")
    sysnames['muF_diboson'] = ("_Scale_NONEUP", "_Scale_NONEDOWN")

# print sysnames


################################################################################
### Read Histograms and write to outfile
logger.info( "Collect hstograms" )

inname = 'Results.root'
logger.info( '--------------------------------------------------------' )
outname = outdir+'/CombineInput.root'
outfile = ROOT.TFile(outname, 'recreate')
outfile.cd()
for region in regions:
    outfile.mkdir(region+"__"+histname)
outfile.Close()
for region in regions:
    altbinning = True if "ZZ" in region else False
    logger.info( 'Filling region %s', region )
    p = Plotter(args.year+"__"+region+"__"+histname)
    p.plot_dir = plotdir
    p.lumi = lumi[args.year]
    p.drawRatio = True
    nominalHists = {}
    for process in processes:
        logger.info( '  %s', process )
        ########################################################################
        ## First get the nominal processes.
        ## Nonprompt needs special treatment because it is constructed from
        ## a control region
        if process == "nonprompt" and region in ["ttZ", "WZ", "ttZ_3jets", "ttZ_4jets"]:
            # Get prompt backgrounds in CR
            logger.info( '    (estimate from CR)')
            nominalHists[process] = getNonpromptFromCR(dirs[region+"_CR"]+inname, histname, altbinning, processes_CR)
            writeObjToDirInFile(outname, region+"__"+histname, nominalHists[process], "nonprompt", update=True)
            p.addBackground(nominalHists[process], processinfo[process][0], processinfo[process][1])
        else:
            logger.info( '    read nominal')
            # The SM also needs special treatment because we need to sum ttZ, WZ and ZZ
            # Also, we construct the lin and quad histograms for the EFT fit
            if process == "sm":
                # Get SM hist with SM samples
                nominalHists[process] = getCombinedSignal_SM(dirs[region]+inname, histname+"__"+process, altbinning)
                p.addBackground(nominalHists[process], processinfo[process][0], processinfo[process][1])
                writeObjToDirInFile(outname, region+"__"+histname, nominalHists[process], "sm", update=True)
                # Also get SM Hist from EFT samples
                hist_eft_sm = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process, altbinning)
                for WCname in WCnames:
                    # Get linear and quad terms from EFT samples
                    hist_plus = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+WCname+"=1.0000", altbinning)
                    hist_minus = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+WCname+"=-1.0000", altbinning)
                    hist_quad = getQuadratic(hist_eft_sm, hist_plus, hist_minus)
                    hist_lin = getLinear(hist_plus, hist_minus)
                    # And add to SM part of SM samples
                    nominalHists["sm_lin_quad_"+WCname] = nominalHists[process].Clone()
                    nominalHists["sm_lin_quad_"+WCname].Add(hist_lin)
                    nominalHists["sm_lin_quad_"+WCname].Add(hist_quad)
                    nominalHists["quad_"+WCname] = hist_quad.Clone()
                    writeObjToDirInFile(outname, region+"__"+histname, nominalHists["sm_lin_quad_"+WCname], "sm_lin_quad_"+WCname, update=True)
                    writeObjToDirInFile(outname, region+"__"+histname, nominalHists["quad_"+WCname], "quad_"+WCname, update=True)
                for WCmix in WCnames_mixed.keys():
                    # get mixed term from EFT samples
                    wc1 = WCnames_mixed[WCmix][0]
                    wc2 = WCnames_mixed[WCmix][1]
                    nominalHists["sm_lin_quad_mixed_"+wc1+"_"+wc2] = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+WCmix+"=1.0000", altbinning)
                    # Subtract SM part from EFT samples and add SM from SM samples
                    nominalHists["sm_lin_quad_mixed_"+wc1+"_"+wc2].Add(hist_eft_sm, -1)
                    nominalHists["sm_lin_quad_mixed_"+wc1+"_"+wc2].Add(nominalHists["sm"])
                    writeObjToDirInFile(outname, region+"__"+histname, nominalHists["sm_lin_quad_mixed_"+wc1+"_"+wc2], "sm_lin_quad_mixed_"+wc1+"_"+wc2, update=True)
            else:
                name = histname+"__"+process
                nominalHists[process] = getHist(dirs[region]+inname, name, altbinning)
                p.addBackground(nominalHists[process], processinfo[process][0], processinfo[process][1])
                writeObjToDirInFile(outname, region+"__"+histname, nominalHists[process], process, update=True)
        ########################################################################
        ## Now we run systematics. There are many things to take care of
        logger.info( '    Get systematic variations' )
        for sys in sysnames.keys():
            if sys == "Fakerate" or "FakerateClosure_" in sys:
                # The Fake rate uncertainty only exists for nonprompt, for all
                # other processes just Clone the nominal
                (upname, downname) = sysnames[sys]
                if "nonprompt" in process and region in ["ttZ", "WZ"]:
                    h_nonprompt_up = getNonpromptFromCR(dirs[region+"_CR"].replace('/Run', upname+'/Run').replace('/UL', upname+'/UL')+inname, histname, altbinning, processes_CR)
                    h_nonprompt_down = getNonpromptFromCR(dirs[region+"_CR"].replace('/Run', downname+'/Run').replace('/UL', downname+'/UL')+inname, histname, altbinning, processes_CR)
                    p.addSystematic(h_nonprompt_up, h_nonprompt_down, sys, processinfo[process][0])
                elif process == "sm":
                    # For all processes that are non prompt,
                    # there is no variation, so simply copy nominal
                    h_nonprompt_up = nominalHists[process].Clone()
                    h_nonprompt_down = nominalHists[process].Clone()
                    for WCname in WCnames:
                        h_nonprompt_up_lin_quad = nominalHists["sm_lin_quad_"+WCname].Clone()
                        h_nonprompt_down_lin_quad = nominalHists["sm_lin_quad_"+WCname].Clone()
                        h_nonprompt_up_quad = nominalHists["quad_"+WCname].Clone()
                        h_nonprompt_down_quad = nominalHists["quad_"+WCname].Clone()
                        writeObjToDirInFile(outname, region+"__"+histname, h_nonprompt_up_lin_quad, "sm_lin_quad_"+WCname+"__"+sys+"Up", update=True)
                        writeObjToDirInFile(outname, region+"__"+histname, h_nonprompt_down_lin_quad, "sm_lin_quad_"+WCname+"__"+sys+"Down", update=True)
                        writeObjToDirInFile(outname, region+"__"+histname, h_nonprompt_up_quad, "quad_"+WCname+"__"+sys+"Up", update=True)
                        writeObjToDirInFile(outname, region+"__"+histname, h_nonprompt_down_quad, "quad_"+WCname+"__"+sys+"Down", update=True)
                    for WCmix in WCnames_mixed.keys():
                        wc1 = WCnames_mixed[WCmix][0]
                        wc2 = WCnames_mixed[WCmix][1]
                        h_nonprompt_up_lin_quad_mix = nominalHists["sm_lin_quad_mixed_"+wc1+"_"+wc2].Clone()
                        h_nonprompt_down_lin_quad_mix = nominalHists["sm_lin_quad_mixed_"+wc1+"_"+wc2].Clone()
                        writeObjToDirInFile(outname, region+"__"+histname, h_nonprompt_up_lin_quad_mix, "sm_lin_quad_mixed_"+wc1+"_"+wc2+"__"+sys+"Up", update=True)
                        writeObjToDirInFile(outname, region+"__"+histname, h_nonprompt_down_lin_quad_mix, "sm_lin_quad_mixed_"+wc1+"_"+wc2+"__"+sys+"Down", update=True)

                else:
                    # For all processes that are non prompt,
                    # there is no variation, so simply copy nominal
                    h_nonprompt_up = nominalHists[process].Clone()
                    h_nonprompt_down = nominalHists[process].Clone()
                writeObjToDirInFile(outname, region+"__"+histname, h_nonprompt_up, process+"__"+sys+"Up", update=True)
                writeObjToDirInFile(outname, region+"__"+histname, h_nonprompt_down, process+"__"+sys+"Down", update=True)
            elif sys in ["rate_ttZ", "rate_WZ", "rate_ZZ"]:
                # The rate uncerts of ttZ, WZ, and ZZ have to be done here because
                # We sum those to a combined "sm" histogram for the EFT fit
                # There are special functions that only vary one of the processes when
                # summing over the three signals
                uncert = None
                rate_process = None
                if sys == "rate_ttZ":
                    uncert = 0.11
                    rate_process = "ttZ"
                elif sys == "rate_WZ":
                    uncert = 0.05
                    rate_process = "WZ"
                elif sys == "rate_ZZ":
                    uncert = 0.05
                    rate_process = "ZZ"

                if process == "sm":
                    histUP = getCombinedSignal_SM(dirs[region]+inname, histname+"__"+process, altbinning, rate=(1+uncert), rate_process=rate_process)
                    histDOWN = getCombinedSignal_SM(dirs[region]+inname, histname+"__"+process, altbinning, rate=(1-uncert), rate_process=rate_process)
                    histUP_eft_sm = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process, altbinning, rate=(1+uncert), rate_process=rate_process)
                    histDOWN_eft_sm = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process, altbinning, rate=(1-uncert), rate_process=rate_process)
                    for WCname in WCnames:
                        histUP_plus = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+WCname+"=1.0000", altbinning, rate=(1+uncert), rate_process=rate_process)
                        histUP_minus = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+WCname+"=-1.0000", altbinning, rate=(1+uncert), rate_process=rate_process)
                        histUP_lin = getLinear(histUP_plus, histUP_minus)
                        histUP_quad = getQuadratic(histUP_eft_sm, histUP_plus, histUP_minus)
                        histDOWN_plus = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+WCname+"=1.0000", altbinning, rate=(1-uncert), rate_process=rate_process)
                        histDOWN_minus = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+WCname+"=-1.0000", altbinning, rate=(1-uncert), rate_process=rate_process)
                        histDOWN_lin = getLinear(histDOWN_plus, histDOWN_minus)
                        histDOWN_quad = getQuadratic(histDOWN_eft_sm, histDOWN_plus, histDOWN_minus)
                        histUP_lin_quad = histUP.Clone()
                        histUP_lin_quad.Add(histUP_lin)
                        histUP_lin_quad.Add(histUP_quad)
                        histDOWN_lin_quad = histDOWN.Clone()
                        histDOWN_lin_quad.Add(histDOWN_lin)
                        histDOWN_lin_quad.Add(histDOWN_quad)
                        writeObjToDirInFile(outname, region+"__"+histname, histUP_lin_quad, "sm_lin_quad_"+WCname+"__"+sys+"Up", update=True)
                        writeObjToDirInFile(outname, region+"__"+histname, histDOWN_lin_quad, "sm_lin_quad_"+WCname+"__"+sys+"Down", update=True)
                        writeObjToDirInFile(outname, region+"__"+histname, histUP_quad, "quad_"+WCname+"__"+sys+"Up", update=True)
                        writeObjToDirInFile(outname, region+"__"+histname, histDOWN_quad, "quad_"+WCname+"__"+sys+"Down", update=True)
                    for WCmix in WCnames_mixed.keys():
                        wc1 = WCnames_mixed[WCmix][0]
                        wc2 = WCnames_mixed[WCmix][1]
                        histUP_mix = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+WCmix+"=1.0000", altbinning, rate=(1+uncert), rate_process=rate_process)
                        histDOWN_mix = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+WCmix+"=1.0000", altbinning, rate=(1-uncert), rate_process=rate_process)
                        histUP_mix.Add(histUP_eft_sm, -1)
                        histUP_mix.Add(histUP)
                        histDOWN_mix.Add(histDOWN_eft_sm, -1)
                        histDOWN_mix.Add(histDOWN)
                        writeObjToDirInFile(outname, region+"__"+histname, histUP_mix, "sm_lin_quad_mixed_"+wc1+"_"+wc2+"__"+sys+"Up", update=True)
                        writeObjToDirInFile(outname, region+"__"+histname, histDOWN_mix, "sm_lin_quad_mixed_"+wc1+"_"+wc2+"__"+sys+"Down", update=True)
                else:
                    histUP = nominalHists[process].Clone()
                    histDOWN = nominalHists[process].Clone()
                writeObjToDirInFile(outname, region+"__"+histname, histUP, process+"__"+sys+"Up", update=True)
                writeObjToDirInFile(outname, region+"__"+histname, histDOWN, process+"__"+sys+"Down", update=True)
            elif "muR_" in sys or "muF_" in sys or "ISR_" in sys or "EWK_add" is sys or "EWK_mul" in sys:
                # muR, muF, EWK, and ISR are divided by process, thus we have to do the variations
                # manually. For the "sm" histogram, the combination of signals is
                # built such that single processes can be read from a file that
                # contains the muR/muF variations while for other processes we use
                # the nominal.
                (upname, downname) = sysnames[sys]
                sysprocess = sys.split("_")[1]
                sysprocesses = []
                if sysprocess == "diboson":
                    sysprocesses = ["WZ", "ZZ"]
                else:
                    sysprocesses = [sys.split("_")[1]]
                sysdirUP = dirs[region]
                sysdirUP = sysdirUP.replace('/Run', upname+'/Run').replace('/UL', upname+'/UL')
                sysdirDOWN = dirs[region]
                sysdirDOWN = sysdirDOWN.replace('/Run', downname+'/Run').replace('/UL', downname+'/UL')
                if process == "nonprompt" and region in ["ttZ", "WZ"]:
                    # Nonprompt has no variations since it is estimated from data
                    # So, just copy the nominal
                    histUP = nominalHists[process].Clone()
                    histDOWN = nominalHists[process].Clone()
                elif process == "sm":
                    processesToVary = []
                    upFile = None
                    downFile = None
                    for p_vary in signals:
                        if p_vary in sysprocesses:
                            processesToVary.append(p_vary)
                            upFile = sysdirUP+inname
                            downFile = sysdirDOWN+inname
                    if len(processesToVary) > 0:
                        logger.info('      - for '+sys+' vary:')
                        for processToVary in processesToVary:
                            logger.info('          - '+processToVary)
                    histUP = getCombinedSignal_SM(dirs[region]+inname, histname+"__"+process, altbinning, rate=None, rate_process=None, sys_processes=processesToVary, fname_sys=upFile)
                    histDOWN = getCombinedSignal_SM(dirs[region]+inname, histname+"__"+process, altbinning, rate=None, rate_process=None, sys_processes=processesToVary, fname_sys=downFile)
                    histUP_eft_sm = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process, altbinning, rate=None, rate_process=None, sys_processes=processesToVary, fname_sys=upFile)
                    histDOWN_eft_sm = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process, altbinning, rate=None, rate_process=None, sys_processes=processesToVary, fname_sys=downFile)
                    for WCname in WCnames:
                        histUP_plus = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+WCname+"=1.0000", altbinning, rate=None, rate_process=None, sys_processes=processesToVary, fname_sys=upFile)
                        histUP_minus = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+WCname+"=-1.0000", altbinning, rate=None, rate_process=None, sys_processes=processesToVary, fname_sys=upFile)
                        histUP_lin = getLinear(histUP_plus, histUP_minus)
                        histUP_quad = getQuadratic(histUP_eft_sm, histUP_plus, histUP_minus)
                        histDOWN_plus = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+WCname+"=1.0000", altbinning, rate=None, rate_process=None, sys_processes=processesToVary, fname_sys=downFile)
                        histDOWN_minus = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+WCname+"=-1.0000", altbinning, rate=None, rate_process=None, sys_processes=processesToVary, fname_sys=downFile)
                        histDOWN_lin = getLinear(histDOWN_plus, histDOWN_minus)
                        histDOWN_quad = getQuadratic(histDOWN_eft_sm, histDOWN_plus, histDOWN_minus)
                        histUP_lin_quad = histUP.Clone()
                        histUP_lin_quad.Add(histUP_lin)
                        histUP_lin_quad.Add(histUP_quad)
                        histDOWN_lin_quad = histDOWN.Clone()
                        histDOWN_lin_quad.Add(histDOWN_lin)
                        histDOWN_lin_quad.Add(histDOWN_quad)
                        writeObjToDirInFile(outname, region+"__"+histname, histUP_lin_quad, "sm_lin_quad_"+WCname+"__"+sys+"Up", update=True)
                        writeObjToDirInFile(outname, region+"__"+histname, histDOWN_lin_quad, "sm_lin_quad_"+WCname+"__"+sys+"Down", update=True)
                        writeObjToDirInFile(outname, region+"__"+histname, histUP_quad, "quad_"+WCname+"__"+sys+"Up", update=True)
                        writeObjToDirInFile(outname, region+"__"+histname, histDOWN_quad, "quad_"+WCname+"__"+sys+"Down", update=True)
                    for WCmix in WCnames_mixed.keys():
                        wc1 = WCnames_mixed[WCmix][0]
                        wc2 = WCnames_mixed[WCmix][1]
                        histUP_mix = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+WCmix+"=1.0000", altbinning, rate=None, rate_process=None)
                        histDOWN_mix = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+WCmix+"=1.0000", altbinning, rate=None, rate_process=None)
                        histUP_mix.Add(histUP_eft_sm, -1)
                        histUP_mix.Add(histUP)
                        histDOWN_mix.Add(histDOWN_eft_sm, -1)
                        histDOWN_mix.Add(histDOWN)
                        writeObjToDirInFile(outname, region+"__"+histname, histUP_mix, "sm_lin_quad_mixed_"+wc1+"_"+wc2+"__"+sys+"Up", update=True)
                        writeObjToDirInFile(outname, region+"__"+histname, histDOWN_mix, "sm_lin_quad_mixed_"+wc1+"_"+wc2+"__"+sys+"Down", update=True)

                else:
                    if process in sysprocesses:
                        histUP   = getHist(sysdirUP+inname, name, altbinning)
                        histDOWN = getHist(sysdirDOWN+inname, name, altbinning)
                    else:
                        histUP = nominalHists[process].Clone()
                        histDOWN = nominalHists[process].Clone()
                writeObjToDirInFile(outname, region+"__"+histname, histUP, process+"__"+sys+"Up", update=True)
                writeObjToDirInFile(outname, region+"__"+histname, histDOWN, process+"__"+sys+"Down", update=True)
                p.addSystematic(histUP, histDOWN, sys, processinfo[process][0])
            else:
                # These are now all other uncertainties that do not need special
                # treatment.
                (upname, downname) = sysnames[sys]
                sysdirUP = dirs[region]
                sysdirUP = sysdirUP.replace('/Run', upname+'/Run').replace('/UL', upname+'/UL')
                sysdirDOWN = dirs[region]
                sysdirDOWN = sysdirDOWN.replace('/Run', downname+'/Run').replace('/UL', downname+'/UL')
                if process == "nonprompt" and region in ["ttZ", "WZ", "ttZ_3jets", "ttZ_4jets"]:
                    # Nonprompt has no variations since it is estimated from data
                    # So, just copy the nominal
                    histUP = nominalHists[process].Clone()
                    histDOWN = nominalHists[process].Clone()
                elif process == "sm":
                    histUP = getCombinedSignal_SM(sysdirUP+inname, histname+"__"+process, altbinning)
                    histDOWN = getCombinedSignal_SM(sysdirDOWN+inname, histname+"__"+process, altbinning)
                    histUP_eft_sm = getCombinedSignal_EFT(sysdirUP+inname, histname+"__"+process, altbinning)
                    histDOWN_eft_sm = getCombinedSignal_EFT(sysdirDOWN+inname, histname+"__"+process, altbinning)
                    for WCname in WCnames:
                        histUP_plus = getCombinedSignal_EFT(sysdirUP+inname, histname+"__"+process+"__"+WCname+"=1.0000", altbinning)
                        histUP_minus = getCombinedSignal_EFT(sysdirUP+inname, histname+"__"+process+"__"+WCname+"=-1.0000", altbinning)
                        histUP_lin = getLinear(histUP_plus, histUP_minus)
                        histUP_quad = getQuadratic(histUP_eft_sm, histUP_plus, histUP_minus)
                        histDOWN_plus = getCombinedSignal_EFT(sysdirDOWN+inname, histname+"__"+process+"__"+WCname+"=1.0000", altbinning)
                        histDOWN_minus = getCombinedSignal_EFT(sysdirDOWN+inname, histname+"__"+process+"__"+WCname+"=-1.0000", altbinning)
                        histDOWN_lin = getLinear(histDOWN_plus, histDOWN_minus)
                        histDOWN_quad = getQuadratic(histDOWN_eft_sm, histDOWN_plus, histDOWN_minus)
                        histUP_lin_quad = histUP.Clone()
                        histUP_lin_quad.Add(histUP_lin)
                        histUP_lin_quad.Add(histUP_quad)
                        histDOWN_lin_quad = histDOWN.Clone()
                        histDOWN_lin_quad.Add(histDOWN_lin)
                        histDOWN_lin_quad.Add(histDOWN_quad)
                        writeObjToDirInFile(outname, region+"__"+histname, histUP_lin_quad, "sm_lin_quad_"+WCname+"__"+sys+"Up", update=True)
                        writeObjToDirInFile(outname, region+"__"+histname, histDOWN_lin_quad, "sm_lin_quad_"+WCname+"__"+sys+"Down", update=True)
                        writeObjToDirInFile(outname, region+"__"+histname, histUP_quad, "quad_"+WCname+"__"+sys+"Up", update=True)
                        writeObjToDirInFile(outname, region+"__"+histname, histDOWN_quad, "quad_"+WCname+"__"+sys+"Down", update=True)
                    for WCmix in WCnames_mixed.keys():
                        wc1 = WCnames_mixed[WCmix][0]
                        wc2 = WCnames_mixed[WCmix][1]
                        histUP_mix = getCombinedSignal_EFT(sysdirUP+inname, histname+"__"+process+"__"+WCmix+"=1.0000", altbinning)
                        histDOWN_mix = getCombinedSignal_EFT(sysdirDOWN+inname, histname+"__"+process+"__"+WCmix+"=1.0000", altbinning)
                        histUP_mix.Add(histUP_eft_sm, -1)
                        histUP_mix.Add(histUP)
                        histDOWN_mix.Add(histDOWN_eft_sm, -1)
                        histDOWN_mix.Add(histDOWN)
                        writeObjToDirInFile(outname, region+"__"+histname, histUP_mix, "sm_lin_quad_mixed_"+wc1+"_"+wc2+"__"+sys+"Up", update=True)
                        writeObjToDirInFile(outname, region+"__"+histname, histDOWN_mix, "sm_lin_quad_mixed_"+wc1+"_"+wc2+"__"+sys+"Down", update=True)
                elif process == "ggToZZ" and "PDF_" in sys:
                    histUP = nominalHists[process].Clone()
                    histDOWN = nominalHists[process].Clone()
                else:
                    histUP   = getHist(sysdirUP+inname, name, altbinning)
                    histDOWN = getHist(sysdirDOWN+inname, name, altbinning)
                writeObjToDirInFile(outname, region+"__"+histname, histUP, process+"__"+sys+"Up", update=True)
                writeObjToDirInFile(outname, region+"__"+histname, histDOWN, process+"__"+sys+"Down", update=True)
                p.addSystematic(histUP, histDOWN, sys, processinfo[process][0])

    # Write observed
    # Add all relevant samples
    logger.info( '  DATA' )
    if args.noData:
        logger.info( '  (compose Asimov data from MC estimated)' )
        is_first = True
        observed = ROOT.TH1F()
        for process in processes:
            logger.info( '    adding up process %s', process)
            if process == "nonprompt" and region in ["ttZ", "WZ", "ttZ_3jets", "ttZ_4jets"]:
                # Get prompt backgrounds in CR
                logger.info( '    (estimate from CR)')
                h_obs_tmp = getNonpromptFromCR(dirs[region+"_CR"]+inname, histname, altbinning, processes_CR)
            elif process == "sm":
                if args.signalInjectionLight or args.signalInjectionHeavy:
                    h_obs_tmp = getCombinedSignal_SM(dirs[region]+inname, histname+"__"+process, altbinning)
                    h_eft_sm_tmp = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process, altbinning)
                    if args.signalInjectionLight:
                        WCvalue = 2.0
                        h_plus_tmp = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+"cHq1Re1122=1.0000", altbinning)
                        h_minus_tmp = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+"cHq1Re1122=-1.0000", altbinning)
                    elif args.signalInjectionHeavy:
                        WCvalue = 2.0
                        h_plus_tmp = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+"cHq1Re33=1.0000", altbinning)
                        h_minus_tmp = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+"cHq1Re33=-1.0000", altbinning)
                    h_lin_tmp = getLinear(h_plus_tmp, h_minus_tmp)
                    h_quad_tmp = getQuadratic(h_eft_sm_tmp, h_plus_tmp, h_minus_tmp)
                    h_obs_tmp.Add(h_lin_tmp, WCvalue)
                    h_obs_tmp.Add(h_quad_tmp, WCvalue*WCvalue)
                elif args.signalInjectionMixed:
                    h_obs_tmp = getCombinedSignal_SM(dirs[region]+inname, histname+"__"+process, altbinning)
                    h_eft_sm_tmp = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process, altbinning)
                    WCvalue1 = 2.0
                    h_plus1_tmp = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+"cHq1Re1122=1.0000", altbinning)
                    h_minus1_tmp = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+"cHq1Re1122=-1.0000", altbinning)
                    h_lin1_tmp = getLinear(h_plus1_tmp, h_minus1_tmp)
                    h_quad1_tmp = getQuadratic(h_eft_sm_tmp, h_plus1_tmp, h_minus1_tmp)
                    WCvalue2 = 2.0
                    h_plus2_tmp = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+"cHq1Re33=1.0000", altbinning)
                    h_minus2_tmp = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+"cHq1Re33=-1.0000", altbinning)
                    h_lin2_tmp = getLinear(h_plus2_tmp, h_minus2_tmp)
                    h_quad2_tmp = getQuadratic(h_eft_sm_tmp, h_plus2_tmp, h_minus2_tmp)
                    h_sm_lin_quad_mix_tmp = getCombinedSignal_EFT(dirs[region]+inname, histname+"__"+process+"__"+"cHq1Re112233=1.0000", altbinning)
                    # in order to get the mixed term only, one has to subtract all other contributions
                    # mixed = sm_lin_quad_mixed - sm - lin1 - quad1 - lin2 - quad2
                    h_mix_tmp = h_sm_lin_quad_mix_tmp.Clone()
                    h_mix_tmp.Add(h_eft_sm_tmp, -1)
                    h_mix_tmp.Add(h_lin1_tmp, -1)
                    h_mix_tmp.Add(h_quad1_tmp, -1)
                    h_mix_tmp.Add(h_lin2_tmp, -1)
                    h_mix_tmp.Add(h_quad2_tmp, -1)
                    # Now add everything to the SM
                    h_obs_tmp.Add(h_lin1_tmp, WCvalue1)
                    h_obs_tmp.Add(h_quad1_tmp, WCvalue1*WCvalue1)
                    h_obs_tmp.Add(h_lin2_tmp, WCvalue2)
                    h_obs_tmp.Add(h_quad2_tmp, WCvalue2*WCvalue2)
                    h_obs_tmp.Add(h_mix_tmp, WCvalue1*WCvalue2)
                elif args.signalInjectionWZjets:
                    sysdir = dirs[region]
                    sysdir = sysdir.replace('/Run', '_WZnJet'+'/Run').replace('/UL', '_WZnJet'+'/UL')
                    h_obs_tmp = getCombinedSignal_SM(sysdir+inname, histname+"__"+process, altbinning)
                else:
                    h_obs_tmp = getCombinedSignal_SM(dirs[region]+inname, histname+"__"+process, altbinning)
            else:
                h_obs_tmp = getHist(dirs[region]+inname, histname+"__"+process, altbinning)

            if is_first:
                observed = h_obs_tmp.Clone()
                is_first = False
            else:
                observed.Add(h_obs_tmp)
        # Now set sqrt(N) errors
        observed = setPseudoDataErrors(observed)
        if args.fluctuatePseudoData:
            observed = fluctuatePseudoData(observed)
    else:
        observed = getHist(dirs[region]+inname, histname+"__data", altbinning)
    writeObjToDirInFile(outname, region+"__"+histname, observed, "data_obs", update=True)
    if args.noData:
        p.addData(observed, "Pseudo data")
    else:
        p.addData(observed, "Data")
    p.draw()
# Write one file per EFT point
logger.info( 'Written file: %s' , outname)
