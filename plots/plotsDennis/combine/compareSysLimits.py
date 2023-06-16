#!/usr/bin/env python

import ROOT, os
ROOT.gROOT.SetBatch(ROOT.kTRUE)
import array
import Analysis.Tools.syncer
from tWZ.Tools.user                      import plot_directory
from tWZ.Tools.helpers                   import getObjFromFile

import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
argParser.add_argument('--wc',               action='store', type=str, default="cHq1Re11")
args = argParser.parse_args()

if args.year not in ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]:
    raise RuntimeError( "Year %s is not knwon", args.year)
logger.info( "Year = %s", args.year )

if args.wc not in ["cHq1Re11", "cHq1Re22", "cHq1Re33", "cHq3Re11", "cHq3Re22", "cHq3Re33"]:
    raise RuntimeError( "WC %s is not knwon", args.wc)
logger.info( "WC = %s", args.wc )

sysVersions = ["default", "statOnly", "noScales", "noRates", "noBtag", "noJEC", "noLepton", "noLumi", "noPS", "noFakerate"]
colors = {
    "default":    ROOT.kBlack,
    "statOnly":   15,
    "noScales":   ROOT.kRed,
    "noRates":    ROOT.kBlue,
    "noBtag":     ROOT.kGreen,
    "noJEC":      798,
    "noLepton":   ROOT.kAzure+7,
    "noLumi":     ROOT.kGreen-4 ,
    "noPS":       ROOT.kMagenta,
    "noFakerate": ROOT.kRed-3,
}

for region in ["ZZ", "WZ", "ttZ", "combined"]:
    likelihoods = {}
    for sys in sysVersions:
        filename = plot_directory+"/Limits_UL_"+sys+"/"+args.year+"/"+"Likelihoods_"+args.wc+".root"
        if sys == "default":
            filename = plot_directory+"/Limits_UL/"+args.year+"/"+"Likelihoods_"+args.wc+".root"
        graphname = "Likelihood__"+region+"__"+args.wc
        likelihoods[sys] = getObjFromFile(filename,graphname)
    c = ROOT.TCanvas("c_"+region, "c_"+region, 600, 600)
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetOptStat(0)
    likelihoods["default"].SetLineColor(colors["default"])
    likelihoods["default"].SetLineWidth(3)
    likelihoods["default"].Draw("AC")
    leg = ROOT.TLegend(.4, .6, .7, .9)
    leg.AddEntry(likelihoods["default"], "All uncert.", "l")

    for sys in sysVersions:
        if "default" not in sys:
            likelihoods[sys].SetLineColor(colors[sys])
            likelihoods[sys].Draw("C SAME")
            leg.AddEntry(likelihoods[sys], sys, "l")
    leg.Draw()
    c.Print(plot_directory+"/Limits_UL_SYScomparison/"+args.year+"__"+region+"__"+args.wc+".pdf")
