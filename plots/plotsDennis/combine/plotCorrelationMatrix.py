#!/usr/bin/env python

import ROOT
import array
import os
import copy
import Analysis.Tools.syncer

from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.Tools.user                              import plot_directory
from tWZ.samples.color                           import color
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
argParser.add_argument('--light',            action='store_true', default=False)
argParser.add_argument('--wc',               action='store', type=str, default="cHq1Re11")
args = argParser.parse_args()

def getParameterMaps(mat, parameters):
    # Scan X axis
    parameterListX = copy.copy(parameters)
    NbinsX = mat.GetXaxis().GetNbins()
    mapX = {}
    for i in range(NbinsX):
        binX = i+1
        label = mat.GetXaxis().GetBinLabel(binX)
        if label in parameterListX:
            mapX[label] = binX
            parameterListX.remove(label)
    # Scan Y axis
    parameterListY = copy.copy(parameters)
    NbinsY = mat.GetYaxis().GetNbins()
    mapY = {}
    for i in range(NbinsY):
        binY = i+1
        label = mat.GetYaxis().GetBinLabel(binY)
        if label in parameterListY:
            mapY[label] = binY
            parameterListY.remove(label)
    # Check if all parameters were found
    if len(parameterListX) > 0:
        print "Could not find parameters on x-axis:", parameterListX
    if len(parameterListY) > 0:
        print "Could not find parameters on y-axis:", parameterListY
    return mapX, mapY

def truncateMatrix(mat, parameters):
    mapX, mapY = getParameterMaps(mat, parameters)
    Nparams = len(parameters)
    newmat = ROOT.TH2F("corr_trunc", "corr_trunc", Nparams, 0.5, Nparams+0.5, Nparams, 0.5, Nparams+0.5)
    for i, paramX in enumerate(parameters):
        binX = i+1
        oldBinX = mapX[paramX]
        for j, paramY in enumerate(parameters):
            binY = j+1
            oldBinY = mapY[paramY]
            content = mat.GetBinContent(oldBinX, oldBinY)
            newmat.SetBinContent(binX, binY, content)
            newmat.GetXaxis().SetBinLabel(binX, paramX)
            newmat.GetYaxis().SetBinLabel(binY, paramY)
    return newmat

def drawMatrix(mat, name):
    plotdir = plot_directory+"/CorrelationMatrix/"+args.year+"/"
    if not os.path.exists( plotdir ): os.makedirs( plotdir )
    c = ROOT.TCanvas("c", "c", 600, 600)
    ROOT.gStyle.SetPalette(ROOT.kSunset)
    ROOT.gPad.SetRightMargin(.2)
    ROOT.gPad.SetBottomMargin(.25)
    ROOT.gPad.SetLeftMargin(.26)
    mat.GetXaxis().LabelsOption("v")
    mat.GetXaxis().SetLabelSize(.018)
    mat.GetYaxis().SetLabelSize(.018)
    mat.GetZaxis().SetRangeUser(-1., 1.)
    mat.Draw("COLZ")
    c.Print(plotdir+name+".pdf")


light = "_light" if args.light else ""
region = "combined"
fname = "DataCards_threePoint"+light+"/"+args.year+"/fitDiagnostics.topEFT_ULRunII_"+region+"_13TeV_"+args.year+"_1D-"+args.wc+"_margin_SHAPES.root"

cor = getObjFromFile(fname, "covariance_fit_s")


parameters = ["k_"+args.wc]

processes = ["ttZ", "WZ", "ZZ", "tWZ", "tZq", "triBoson", "ttX"]
for u in ["rate", "muF", "muR", "ISR", "FSR"]:
    for p in processes:
        parameters.append(u+"_"+p)

parameters += [
    "BTag_b_correlated",
    "BTag_l_correlated",
    "BTag_b_uncorrelated_2016preVFP",
    "BTag_l_uncorrelated_2016preVFP",
    "BTag_b_uncorrelated_2016",
    "BTag_l_uncorrelated_2016",
    "BTag_b_uncorrelated_2017",
    "BTag_l_uncorrelated_2017",
    "BTag_b_uncorrelated_2018",
    "BTag_l_uncorrelated_2018",
    "Fakerate",
    "FakerateClosure_correlated_elec",
    "FakerateClosure_uncorrelated_elec_2016preVFP",
    "FakerateClosure_uncorrelated_elec_2016",
    "FakerateClosure_uncorrelated_elec_2017",
    "FakerateClosure_uncorrelated_elec_2018",
    "FakerateClosure_correlated_muon",
    "FakerateClosure_uncorrelated_muon_2016preVFP",
    "FakerateClosure_uncorrelated_muon_2016",
    "FakerateClosure_uncorrelated_muon_2017",
    "FakerateClosure_uncorrelated_muon_2018",
    "FakerateClosure_correlated_both",
    "FakerateClosure_uncorrelated_both_2016preVFP",
    "FakerateClosure_uncorrelated_both_2016",
    "FakerateClosure_uncorrelated_both_2017",
    "FakerateClosure_uncorrelated_both_2018",
    "Trigger",
    "Prefire",
    "LepReco",
    "LepIDstat_2016preVFP",
    "LepIDstat_2016",
    "LepIDstat_2017",
    "LepIDstat_2018",
    "LepIDsys",
    "PU",
    "JES",
    "JER",
    "Lumi_uncorrelated_2016",
    "Lumi_uncorrelated_2017",
    "Lumi_uncorrelated_2018",
    "Lumi_correlated_161718",
    "Lumi_correlated_1718",
    "WZ_Njet_reweight",
]


cor_trunc = truncateMatrix(cor, parameters)

drawMatrix(cor_trunc, "Correlation_"+args.wc+light)
