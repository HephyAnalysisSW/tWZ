#!/usr/bin/env python

import ROOT
import Analysis.Tools.syncer
import os

from math                                        import sqrt
from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from tWZ.samples.color                           import color
from tWZ.Tools.histogramHelper                   import WClatexNames
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import tWZ.Tools.logger as logger

logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--noData',           action='store_true', default=False)
args = argParser.parse_args()


dataTag = "_noData" if args.noData else ""
dirname_suffix = "_light"
combineInput = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_threePoint"+dataTag+dirname_suffix+"/ULRunII/CombineInput.root"

plotdir = plot_directory+"/PaperPlots/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

regions = ["WZ", "ZZ", "ttZ"]
histname = "Z1_pt"
signals = ["sm"]
backgrounds = ["tWZ", "ttX", "tZq", "triBoson", "nonprompt"]
WCs = {
    "WZ" : "cHq3Re1122",
    "ZZ" : "cHq1Re1122",
    "ttZ": "cHq3Re33",
}

processinfo = {
    "sm":        ("t#bar{t}Z + WZ + ZZ", ROOT.kAzure+7),
    "ttZ":       ("t#bar{t}Z", color.TTZ),
    "WZ":        ("WZ",  color.WZ),
    "ZZ":        ("ZZ", color.ZZ),
    "tWZ":       ("tWZ", color.TWZ),
    "ttX":       ("t#bar{t}X", color.TTX_rare),
    "tZq":       ("tZq", color.TZQ),
    "triBoson":  ("Triboson", color.triBoson),
    "nonprompt": ("Nonprompt", color.nonprompt),
}


sys = [
    'BTag_b_correlated', 'BTag_b_uncorrelated_2016', 'BTag_b_uncorrelated_2016preVFP', 'BTag_b_uncorrelated_2017', 'BTag_b_uncorrelated_2018', 'BTag_l_correlated', 'BTag_l_uncorrelated_2016', 'BTag_l_uncorrelated_2016preVFP', 'BTag_l_uncorrelated_2017', 'BTag_l_uncorrelated_2018',
    'FSR_WZ', 'FSR_ZZ', 'FSR_tWZ', 'FSR_tZq', 'FSR_triBoson', 'FSR_ttX', 'FSR_ttZ',
    'Fakerate', 'FakerateClosure_correlated_both', 'FakerateClosure_correlated_elec', 'FakerateClosure_correlated_muon',
    'FakerateClosure_uncorrelated_both_2016', 'FakerateClosure_uncorrelated_both_2016preVFP', 'FakerateClosure_uncorrelated_both_2017', 'FakerateClosure_uncorrelated_both_2018',
    'FakerateClosure_uncorrelated_elec_2016', 'FakerateClosure_uncorrelated_elec_2016preVFP', 'FakerateClosure_uncorrelated_elec_2017', 'FakerateClosure_uncorrelated_elec_2018',
    'FakerateClosure_uncorrelated_muon_2016', 'FakerateClosure_uncorrelated_muon_2016preVFP', 'FakerateClosure_uncorrelated_muon_2017', 'FakerateClosure_uncorrelated_muon_2018',
    'ISR_WZ', 'ISR_ZZ', 'ISR_tWZ', 'ISR_tZq', 'ISR_triBoson', 'ISR_ttX', 'ISR_ttZ',
    'JER', 'JES',
    'LepIDstat_2016', 'LepIDstat_2016preVFP', 'LepIDstat_2017', 'LepIDstat_2018', 'LepIDsys', 'LepReco',
    'Lumi_correlated_161718', 'Lumi_correlated_1718',
    'Lumi_uncorrelated_2016', 'Lumi_uncorrelated_2017', 'Lumi_uncorrelated_2018',
    'PU', 'Prefire', 'Trigger', 'WZ_Njet_reweight', 'WZ_heavyFlavour',
    'muF_WZ', 'muF_ZZ', 'muF_tWZ', 'muF_tZq', 'muF_triBoson', 'muF_ttX', 'muF_ttZ',
    'muR_WZ', 'muR_ZZ', 'muR_tWZ', 'muR_tZq', 'muR_triBoson', 'muR_ttX', 'muR_ttZ',
    'rate_WZ', 'rate_ZZ', 'rate_ttZ'
]

rates_bkg = {
    "tWZ": 0.2,
    "ttX": 0.2,
    "tZq": 0.1,
    "triBoson": 0.2,
}

for region in regions:
    p = Plotter("PreFit_ULRunII__"+region+"__"+histname)
    p.plot_dir = plotdir
    p.lumi = "138"
    p.xtitle = "Z #it{p}_{T} [GeV]"
    p.drawRatio = True
    p.ratiotitle = "#splitline{Ratio}{to SM}"
    p.subtext = "Preliminary"
    p.legshift = (-0.1, -0.1, 0.0, 0.0)
    regiontext = "SR"
    if region == "ttZ":
        regiontext+="_{t#bar{t}Z}"
    elif region == "WZ":
        regiontext+="_{WZ}"
    elif region == "ZZ":
        regiontext+="_{ZZ}"
    regiontext+=", PreFit"
    p.addText(0.22, 0.7, regiontext, font=43, size=16)
    if region == "WZ":
        p.ratiorange = 0.1, 2.4
    isFirstProcess = True
    hist_bkg = ROOT.TH1F()
    for process in signals+backgrounds:
        hist = getObjFromFile(combineInput, region+"__"+histname+"/"+process)
        if process in backgrounds:
            if isFirstProcess:
                hist_bkg = hist.Clone("allBKGs")
                isFirstProcess = False
            else:
                hist_bkg.Add(hist)
        p.addBackground(hist, processinfo[process][0], processinfo[process][1])
        for sname in sys:
            hist_up = getObjFromFile(combineInput, region+"__"+histname+"/"+process+"__"+sname+"Up")
            hist_down = getObjFromFile(combineInput, region+"__"+histname+"/"+process+"__"+sname+"Down")
            p.addSystematic(hist_up, hist_down, sname, processinfo[process][0])
        if process in backgrounds and process != "nonprompt":
            p.addNormSystematic(processinfo[process][0], rates_bkg[process])
    hist_signal = getObjFromFile(combineInput, region+"__"+histname+"/"+"sm_lin_quad_"+WCs[region])
    hist_signal.Add(hist_bkg)
    p.addSignal(hist_signal, WClatexNames[WCs[region]].replace("[TeV^{-2}]", "")+" = 1 TeV^{-2}", ROOT.kRed)
    p.draw()
