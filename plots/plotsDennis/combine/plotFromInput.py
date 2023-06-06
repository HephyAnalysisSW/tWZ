#!/usr/bin/env python

import ROOT
import array
import os
import Analysis.Tools.syncer

from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.Tools.user                              import plot_directory
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--file',               action='store', type=str, default="nodef")
args = argParser.parse_args()

if not os.path.exists(args.file):
    raise RuntimeError( "File %s does not exist", args.file)

processinfo = {
    "ttZ":       ("ttZ", color.TTZ),
    "WZ":        ("WZ",  color.WZ),
    "ZZ":        ("ZZ", color.ZZ),
    "tWZ":       ("tWZ", color.TWZ),
    "ttX":       ("ttX", color.TTX_rare),
    "tZq":       ("tZq", color.TZQ),
    "triBoson":  ("Triboson", color.triBoson),
    "nonprompt": ("Nonprompt", color.nonprompt),
}

lumi = {
    "UL2016preVFP": "19.5",
    "UL2016":       "16.5",
    "UL2017":       "41.5",
    "UL2018":       "60",
    "ULRunII":      "138",
}

sysnames = {
    "BTag_b_correlated":              ("BTag_b_correlated_UP", "BTag_b_correlated_DOWN"),
    "BTag_l_correlated":              ("BTag_l_correlated_UP", "BTag_l_correlated_DOWN"),
    "BTag_b_uncorrelated_2016preVFP": ("BTag_b_uncorrelated_2016preVFP_UP", "BTag_b_uncorrelated_2016preVFP_DOWN"),
    "BTag_l_uncorrelated_2016preVFP": ("BTag_l_uncorrelated_2016preVFP_UP", "BTag_l_uncorrelated_2016preVFP_DOWN"),
    "BTag_b_uncorrelated_2016":       ("BTag_b_uncorrelated_2016_UP", "BTag_b_uncorrelated_2016_DOWN"),
    "BTag_l_uncorrelated_2016":       ("BTag_l_uncorrelated_2016_UP", "BTag_l_uncorrelated_2016_DOWN"),
    "BTag_b_uncorrelated_2017":       ("BTag_b_uncorrelated_2017_UP", "BTag_b_uncorrelated_2017_DOWN"),
    "BTag_l_uncorrelated_2017":       ("BTag_l_uncorrelated_2017_UP", "BTag_l_uncorrelated_2017_DOWN"),
    "BTag_b_uncorrelated_2018":       ("BTag_b_uncorrelated_2018_UP", "BTag_b_uncorrelated_2018_DOWN"),
    "BTag_l_uncorrelated_2018":       ("BTag_l_uncorrelated_2018_UP", "BTag_l_uncorrelated_2018_DOWN"),
    "Fakerate":                       ("Fakerate_UP", "Fakerate_DOWN"), # TREAT DIFFERENTLY
    "Trigger":                        ("Trigger_UP", "Trigger_DOWN"),
    "Prefire":                        ("Prefire_UP", "Prefire_DOWN"),
    "LepReco":                        ("LepReco_UP", "LepReco_DOWN"),
    "LepIDstat_2016preVFP":           ("LepIDstat_2016preVFP_UP", "LepIDstat_2016preVFP_DOWN"),
    "LepIDstat_2016":                 ("LepIDstat_2016_UP", "LepIDstat_2016_DOWN"),
    "LepIDstat_2017":                 ("LepIDstat_2017_UP", "LepIDstat_2017_DOWN"),
    "LepIDstat_2018":                 ("LepIDstat_2018_UP", "LepIDstat_2018_DOWN"),
    "LepIDsys":                       ("LepIDsys_UP", "LepIDsys_DOWN"),
    "PU":                             ("PU_UP", "PU_DOWN"),
    # "JES":                            ("JES_UP", "JES_DOWN"),
    # "JER":                            ("JER_UP", "JER_DOWN"),
    "Lumi_uncorrelated_2016":         ("Lumi_uncorrelated_2016_UP", "Lumi_uncorrelated_2016_DOWN"),
    "Lumi_uncorrelated_2017":         ("Lumi_uncorrelated_2017_UP", "Lumi_uncorrelated_2017_DOWN"),
    "Lumi_uncorrelated_2018":         ("Lumi_uncorrelated_2018_UP", "Lumi_uncorrelated_2018_DOWN"),
    "Lumi_correlated_161718":         ("Lumi_correlated_161718_UP", "Lumi_correlated_161718_DOWN"),
    "Lumi_correlated_1718":           ("Lumi_correlated_1718_UP", "Lumi_correlated_1718_DOWN"),
    "ISR":                            ("ISR_UP", "ISR_DOWN"),
    "FSR":                            ("FSR_UP", "FSR_DOWN"),
    "muR":                            ("Scale_UPNONE", "Scale_DOWNNONE"), # muR
    "muF":                            ("Scale_NONEUP", "Scale_NONEDOWN"), # muF
    "PDF":                            (), # TREAT DIFFERENTLY
}

year = ""
if   "UL2016preVFP" in args.file: year = "UL2016preVFP"
elif "UL2016"       in args.file: year = "UL2016"
elif "UL2017"       in args.file: year = "UL2017"
elif "UL2018"       in args.file: year = "UL2018"

rootname = args.file.split("/")[-1]

file = ROOT.TFile(args.file)

regions = ["ttZ__Z1_pt", "WZ__Z1_pt", "ZZ__Z1_pt"]

for region in regions:
    p = Plotter(rootname.replace(".root","")+"__"+region)
    p.plot_dir = outdir = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL/"+year+"/plots/"
    p.lumi = lumi[year]
    p.xtitle = "Z p_{T} [GeV]"
    p.drawRatio = True
    p.ratiorange = (0.2, 1.8)
    for process in processinfo.keys():
        legname, color = processinfo[process]
        hist = getObjFromFile(args.file, region+"/"+process)
        p.addBackground(hist, legname, color)
        for sys in sysnames.keys():
            histUP   = getObjFromFile(args.file, region+"/"+process+"__"+sys+"Up")
            histDOWN = getObjFromFile(args.file, region+"/"+process+"__"+sys+"Down")
            p.addSystematic(histUP, histDOWN, sys, legname)
    histData = hist = getObjFromFile(args.file, region+"/data_obs")
    p.addData(histData, "Asimov data")
    p.draw()
