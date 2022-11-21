#!/usr/bin/env python

import os
import ROOT
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory

import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
args = argParser.parse_args()

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetOptStat(0)

ROOT.gStyle.SetPalette(ROOT.kLightTemperature)

regions = ROOT.TH2F("regions", "regions", 2, 0, 2, 2, 0, 2)
regions.SetBinContent(1,1, 4)
regions.SetBinContent(1,2, 1)
regions.SetBinContent(2,1, 3.5)
regions.SetBinContent(2,2, 2)

regions.SetTitle("")
regions.GetXaxis().SetTitle("")
regions.GetYaxis().SetTitle("")
regions.GetXaxis().SetLabelSize(0)
regions.GetYaxis().SetLabelSize(0)
regions.GetXaxis().SetTickLength(0)
regions.GetYaxis().SetTickLength(0)
regions.GetZaxis().SetRangeUser(1, 4.5)



c = ROOT.TCanvas("c", "c", 600, 600)
ROOT.gPad.SetLeftMargin(0)
ROOT.gPad.SetRightMargin(0)
ROOT.gPad.SetTopMargin(0)
ROOT.gPad.SetBottomMargin(0)
regions.Draw("COL")
labeldata = [
    ("#splitline{QCDT}{1 tight lepton}", 0.2, 0.75), 
    ("#splitline{QCDL}{1 loose lepton}", 0.2, 0.25), 
    ("#splitline{CR}{3 loose leptons, max 2 tight}", 0.65, 0.25), 
    ("#splitline{SR}{3 tight leptons}", 0.7, 0.75), 
]

labels = []
for (text, x, y) in labeldata:
    label = ROOT.TLatex(3.5, 24, text)
    label.SetNDC()
    label.SetTextAlign(12)
    label.SetTextFont(42)
    label.SetTextSize(0.025)
    label.SetX(x)
    label.SetY(y)
    labels.append(label)

for l in labels: l.Draw()

c.Print(plot_directory+'/FakeRate/FakerateRegions.pdf')
