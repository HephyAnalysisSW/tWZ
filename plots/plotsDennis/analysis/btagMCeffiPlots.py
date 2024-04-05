#!/usr/bin/env python

import ROOT
import Analysis.Tools.syncer
import os
import array

from Analysis.Tools.BTagEfficiencyUL import BTagEfficiency
from tWZ.Tools.user                  import plot_directory

import tWZ.Tools.logger as logger

ROOT.gROOT.SetBatch(ROOT.kTRUE)

def makePlot(hist, outname):
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetOptStat(0)
    c = ROOT.TCanvas("c"+outname, "c"+outname, 600, 600)
    ROOT.gPad.SetRightMargin(.15)
    hist.GetXaxis().SetTitle("p_{T}")
    hist.GetYaxis().SetTitle("#eta")
    hist.GetZaxis().SetRangeUser(0.5, 1.0)
    if "_c_" in outname or "_other_" in outname:
        hist.GetZaxis().SetRangeUser(0., 0.5)
    hist.Draw("COLZ")
    c.Print(outname)




ptBorders = [20, 30, 50, 70, 100, 140, 200, 300, 600, 1000]
etaBorders2016 = [0, 2.4]
etaBorders2017 = [0, 2.4]
etaBorders2018 = [0, 2.5]


for year in ["UL2016_preVFP", "UL2016", "UL2017", "UL2018"]:

    print("============================================================")
    print(year)

    plotdir = plot_directory+"/BTagMCeffi/"
    if not os.path.exists( plotdir ): os.makedirs( plotdir )

    if year in ["UL2016_preVFP", "UL2016"]:
        etaBorders = etaBorders2016
    elif year in ["UL2017"]:
        etaBorders = etaBorders2017
    elif year in ["UL2018"]:
        etaBorders = etaBorders2018

    b_tagger = "DeepJet"
    btagEff = BTagEfficiency( fastSim = False, year=year, tagger=b_tagger )

    hist_b = ROOT.TH2F("MCeffi_b_"+year, "Efficiency b "+year, len(ptBorders)-1, array.array('d',ptBorders), len(etaBorders)-1, array.array('d',etaBorders))
    hist_c = ROOT.TH2F("MCeffi_c_"+year, "Efficiency c "+year, len(ptBorders)-1, array.array('d',ptBorders), len(etaBorders)-1, array.array('d',etaBorders))
    hist_other = ROOT.TH2F("MCeffi_other_"+year, "Efficiency other "+year, len(ptBorders)-1, array.array('d',ptBorders), len(etaBorders)-1, array.array('d',etaBorders))

    for i, ptlow in enumerate(ptBorders):
        for j, etalow in enumerate(etaBorders):
            if i == len(ptBorders)-1 or j == len(etaBorders)-1:
                continue
            pthigh = ptBorders[i+1]
            etahigh = etaBorders[j+1]
            pt = ptlow+0.5*(pthigh-ptlow)
            eta = etalow+0.5*(etahigh-etalow)

            effi_b = btagEff.getMCEff(5, pt, eta)
            effi_c = btagEff.getMCEff(4, pt, eta)
            effi_other = btagEff.getMCEff(0, pt, eta)

            print(pt, eta, effi_b)

            hist_b.SetBinContent(i+1, j+1, effi_b)
            hist_c.SetBinContent(i+1, j+1, effi_c)
            hist_other.SetBinContent(i+1, j+1, effi_other)

    makePlot(hist_b, plotdir+year+"__b_effi.pdf")
    makePlot(hist_c, plotdir+year+"__c_effi.pdf")
    makePlot(hist_other, plotdir+year+"__other_effi.pdf")
