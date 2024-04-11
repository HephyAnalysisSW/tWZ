#!/usr/bin/env python

import ROOT
import Analysis.Tools.syncer
import os
import array

from math                                        import sqrt, pow
from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from tWZ.samples.color                           import color
from tWZ.Tools.histogramHelper                   import WClatexNames
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

from ctypes import c_double

def checkBins(h1, h2):
    nbinsx = h1.GetNbinsX();
    for i in range(nbinsx+2):
        if h1.GetBinContent(i) > h2.GetBinContent(i):
            h1.SetBinContent(i, h2.GetBinContent(i))

def makeEffiPlot(effiplots, xtitle, plotname):
    xmin = 0.
    xmax = 1000.
    ymin = 0.0
    ymax = 1.2
    if "lepton" in xtitle:
        xmax = 400.
    elif "Inclusive" in xtitle:
        xmax = 1.
        ymin = 0.9
        ymax = 1.05


    dummy = ROOT.TGraph(2)
    dummy.SetPoint(0, xmin, ymin)
    dummy.SetPoint(1, xmax, ymax)
    dummy.SetMarkerSize(0.)
    dummy.SetTitle(" ;"+xtitle+"; Trigger Efficiency")

    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetErrorX(.5)

    canvas = ROOT.TCanvas(plotname, "", 600, 600)
    leg = ROOT.TLegend(.2, .2, .5, .35)
    dummy.Draw("AP")
    for (h_effi, legname, color) in effiplots:
        h_effi.SetTitle(" ;"+xtitle+"; Trigger Efficiency")
        h_effi.Draw("P SAME")
        h_effi.SetLineColor(color)
        h_effi.SetMarkerColor(color)
        # h_effi.GetYaxis().SetRangeUser(0., 1.2)
        leg.AddEntry(h_effi, legname, "pel")
    leg.Draw()
    canvas.Print(plotname+".pdf")

selections = [
    "trilepFO-minDLmass12",
    "trilepT-minDLmass12",
    # "trilepT-minDLmass12-onZ1",
    # "trilepT-minDLmass12-onZ1-btag0-met60",
    # "trilepT-minDLmass12-onZ1-njet3p-btag1p",
    # "trilepFOnoT-minDLmass12",
    # "trilepFOnoT-minDLmass12-onZ1",
    # "trilepFOnoT-minDLmass12-onZ1-btag0-met60",
    # "trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p",
    # "qualepT-minDLmass12",
    # "qualepT-minDLmass12-onZ1",
    # "qualepT-minDLmass12-onZ1-onZ2",
    ]
years = ["UL2016preVFP","UL2016","UL2017","UL2018"]
# years = ["UL2018"]

histnames = [
    ("l1_pt", "Leading lepton p_{T} [GeV]", 4),
    ("l2_pt", "Sub-leading lepton p_{T} [GeV]", 4),
    ("l3_pt", "Trailing lepton p_{T} [GeV]", 4),
    ("Z1_pt", "Z boson candidate p_{T} [GeV]", 5),
    ("INCLUSIVE", "Inclusive", 0),

]

processInfo = {
    "ttZ_sm":            ("t#bar{t}Z", ROOT.kRed),
    "WZTo3LNu_powheg":   ("WZ", ROOT.kBlue),
    "WZTo3LNu":          ("WZ", ROOT.kGreen),
    "ZZ_powheg":         ("ZZ", ROOT.kGreen),
}


processes = {
    "trilepFO-minDLmass12": ["ttZ_sm", "WZTo3LNu_powheg", "ZZ_powheg"],
    "trilepT-minDLmass12": ["ttZ_sm", "WZTo3LNu_powheg", "ZZ_powheg"],
    "trilepT-minDLmass12-onZ1": ["ttZ_sm", "WZTo3LNu_powheg"],
    "trilepT-minDLmass12-onZ1-btag0-met60": ["WZTo3LNu_powheg"],
    "trilepT-minDLmass12-onZ1-njet3p-btag1p": ["ttZ_sm"],
    "trilepFOnoT-minDLmass12": ["ttZ_sm", "WZTo3LNu_powheg"],
    "trilepFOnoT-minDLmass12-onZ1": ["ttZ_sm", "WZTo3LNu_powheg"],
    "trilepFOnoT-minDLmass12-onZ1-btag0-met60": ["WZTo3LNu_powheg"],
    "trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p": ["ttZ_sm"],
    "qualepT-minDLmass12": ["ZZ_powheg"],
    "qualepT-minDLmass12-onZ1": ["ZZ_powheg"],
    "qualepT-minDLmass12-onZ1-onZ2": ["ZZ_powheg"],
}

for selection in selections:
    print("=====================================================================")
    print("Selection:", selection)
    plotdir = plot_directory+"/TriggerSF/"+selection+"/"
    if not os.path.exists( plotdir ): os.makedirs( plotdir )
    for year in years:
        print("  Year:", year)
        file = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/TriggerSF_v1/"+year+"/all/"+selection+"/Results.root"
        print file
        for (histname, xtitle, rebin) in histnames:
            print("    Hist:", histname)
            effiplots = []
            if histname == "INCLUSIVE":
                # Select one of the histograms
                h_pass_tmp = getObjFromFile(file, "Z1_pt_passTrigger__data")
                h_total_tmp = getObjFromFile(file, "Z1_pt__data")
                Nbins = h_pass_tmp.GetSize()-2
                # Get Integral and error
                err_pass = c_double(0.)
                N_pass = h_pass_tmp.IntegralAndError(0, Nbins, err_pass)
                err_total = c_double(0.)
                N_total = h_total_tmp.IntegralAndError(0, Nbins, err_total)
                # Fill in new hists
                h_pass_data = ROOT.TH1F("pass_inclusive_data", "pass_inclusive", 1, 0, 1)
                h_pass_data.SetBinContent(1, N_pass)
                h_pass_data.SetBinError(1, err_pass.value)
                h_total_data = ROOT.TH1F("total_inclusive_data", "total_inclusive", 1, 0, 1)
                h_total_data.SetBinContent(1, N_total)
                h_total_data.SetBinError(1, err_total.value)
            else:
                h_pass_data = getObjFromFile(file, histname+"_passTrigger__data")
                h_total_data = getObjFromFile(file, histname+"__data")
                h_pass_data.Rebin(rebin)
                h_total_data.Rebin(rebin)
            checkBins(h_pass_data, h_total_data)
            h_effi_data = ROOT.TEfficiency(h_pass_data, h_total_data)
            effiplots.append( (h_effi_data, "Data", ROOT.kBlack) )

            g_efficiency = ROOT.TGraphAsymmErrors()
            g_efficiency.Divide(h_pass_data, h_total_data, "cl=0.683 b(1,1) mode")
            # effiplots.append( (g_efficiency, "Data TEST", 15) )


            for process in processes[selection]:
                if histname == "INCLUSIVE":
                    # Select one of the histograms
                    h_pass_tmp = getObjFromFile(file, "Z1_pt_passTrigger__"+process)
                    h_total_tmp = getObjFromFile(file, "Z1_pt__"+process)
                    Nbins = h_pass_tmp.GetSize()-2
                    # Get Integral and error
                    err_pass = c_double(0.)
                    N_pass = h_pass_tmp.IntegralAndError(0, Nbins, err_pass)
                    err_total = c_double(0.)
                    N_total = h_total_tmp.IntegralAndError(0, Nbins, err_total)
                    # Fill in new hists
                    h_pass = ROOT.TH1F("pass_inclusive_"+process, "pass_inclusive", 1, 0, 1)
                    h_pass.SetBinContent(1, N_pass)
                    h_pass.SetBinError(1, err_pass.value)
                    h_total = ROOT.TH1F("total_inclusive_"+process, "total_inclusive", 1, 0, 1)
                    h_total.SetBinContent(1, N_total)
                    h_total.SetBinError(1, err_total.value)
                else:
                    h_pass = getObjFromFile(file, histname+"__"+process)
                    h_total = getObjFromFile(file, histname+"_passTrigger"+"__"+process)
                    h_pass.Rebin(rebin)
                    h_total.Rebin(rebin)
                checkBins(h_pass, h_total)
                h_effi = ROOT.TEfficiency(h_pass, h_total)
                effiplots.append( (h_effi, processInfo[process][0], processInfo[process][1]) )

            plotname = plotdir+"TriggerSF__"+year+"__"+histname
            makeEffiPlot(effiplots, xtitle, plotname)
