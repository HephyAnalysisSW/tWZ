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


def getHist(fname, hname, altbinning=False):
    bins  = [0, 40, 80, 120, 160, 200, 260, 400, 1000]
    if altbinning:
        bins  = [0, 40, 80, 120, 1000]

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
    return hist


filePath = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_threePoint_noData/ULRunII/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/Results.root"
filePath_muR_up = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_threePoint_noData_Scale_UPNONE/ULRunII/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/Results.root"
filePath_muR_down = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_threePoint_noData_Scale_DOWNNONE/ULRunII/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/Results.root"
filePath_muF_up = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_threePoint_noData_Scale_NONEUP/ULRunII/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/Results.root"
filePath_muF_down = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_threePoint_noData_Scale_NONEDOWN/ULRunII/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/Results.root"

h_nom_sm = getHist(filePath, "Z1_pt__ttZ")
h_nom_plus = getHist(filePath, "Z1_pt__ttZ__cHqMRe1122=1.0000")
h_nom_minus = getHist(filePath, "Z1_pt__ttZ__cHqMRe1122=-1.0000")
h_nom_quad = h_nom_plus.Clone()
h_nom_quad.Add(h_nom_minus)
h_nom_quad.Add(h_nom_sm, -2)
h_nom_quad.Scale(0.5)

h_muRdown_sm = getHist(filePath_muR_down, "Z1_pt__ttZ")
h_muRdown_plus = getHist(filePath_muR_down, "Z1_pt__ttZ__cHqMRe1122=1.0000")
h_muRdown_minus = getHist(filePath_muR_down, "Z1_pt__ttZ__cHqMRe1122=-1.0000")
h_muRdown_quad = h_muRdown_plus.Clone()
h_muRdown_quad.Add(h_muRdown_minus)
h_muRdown_quad.Add(h_muRdown_sm, -2)
h_muRdown_quad.Scale(0.5)

c = ROOT.TCanvas()
h_nom_quad.Draw("HIST")
h_muRdown_quad.Draw("HIST SAME")
c.Print(plot_directory+"/scaleCheck.pdf")
