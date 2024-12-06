#!/usr/bin/env python

import ROOT
import Analysis.Tools.syncer
import os

from math                                        import sqrt
from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.CMScolors import CMScolors

from tWZ.samples.color                           import color
from tWZ.Tools.histogramHelper                   import WClatexNames
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import tWZ.Tools.logger as logger

logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--noData',           action='store_true', default=False)
argParser.add_argument('--addSignal',           action='store_true', default=False)
args = argParser.parse_args()


# dataTag = "_noData" if args.noData else ""
# dirname_suffix = "_light"
# combineInput = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_threePoint"+dataTag+dirname_suffix+"/ULRunII/CombineInput.root"

combineInput = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_threePoint_light_minus_binning-A_SMZero/ULRunII/CombineInput.root"

plotdir = plot_directory+"/PaperPlots/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

regions = ["WZ", "ZZ", "ttZ"]
histname = "Z1_pt"
signals = ["sm"]
backgrounds = ["tWZ", "ttX", "tZq", "triBoson", "ggToZZ", "nonprompt"]
WCs = {
    "WZ" : "cHq3Re1122",
    "ZZ" : "cHq1Re1122",
    "ttZ": "cHq3Re33",
}

processinfo = {
    "sm":        ("t#bar{t}Z + WZ + ZZ", CMScolors["sm"]),
    "ttZ"  :    ("t#bar{t}Z", CMScolors["ttZ"]),
    "WZ":        ("WZ",  CMScolors["WZ"]),
    "ZZ":        ("ZZ", CMScolors["ZZ"]),
    "tWZ":       ("tWZ", CMScolors["tWZ"]),
    "ttX":       ("t#bar{t}X", CMScolors["ttX"]),
    "tZq":       ("tZq", CMScolors["tZq"]),
    "triBoson":  ("Triboson", CMScolors["triboson"]),
    "nonprompt": ("Nonprompt", CMScolors["nonprompt"]),
    "ggToZZ":    ("gg #rightarrow ZZ", CMScolors["ggZZ"]),
}


sys = [
    'BTag_b_correlated', 'BTag_b_uncorrelated_2016', 'BTag_b_uncorrelated_2016preVFP', 'BTag_b_uncorrelated_2017', 'BTag_b_uncorrelated_2018', 'BTag_l_correlated', 'BTag_l_uncorrelated_2016', 'BTag_l_uncorrelated_2016preVFP', 'BTag_l_uncorrelated_2017', 'BTag_l_uncorrelated_2018',
    'Fakerate', 'FakerateClosure_correlated_both', 'FakerateClosure_correlated_elec', 'FakerateClosure_correlated_muon',
    'FakerateClosure_uncorrelated_both_2016', 'FakerateClosure_uncorrelated_both_2016preVFP', 'FakerateClosure_uncorrelated_both_2017', 'FakerateClosure_uncorrelated_both_2018',
    'FakerateClosure_uncorrelated_elec_2016', 'FakerateClosure_uncorrelated_elec_2016preVFP', 'FakerateClosure_uncorrelated_elec_2017', 'FakerateClosure_uncorrelated_elec_2018',
    'FakerateClosure_uncorrelated_muon_2016', 'FakerateClosure_uncorrelated_muon_2016preVFP', 'FakerateClosure_uncorrelated_muon_2017', 'FakerateClosure_uncorrelated_muon_2018',
    'ISR_WZ', 'ISR_ZZ', 'ISR_tWZ', 'ISR_tZq', 'ISR_triBoson', 'ISR_ttX', 'ISR_ttZ', 'ISR_ggToZZ',
    'FSR',
    "JES_AbsoluteMPFBias","JES_AbsoluteScale","JES_AbsoluteStat_2016preVFP","JES_AbsoluteStat_2016","JES_AbsoluteStat_2017","JES_AbsoluteStat_2018",
    "JES_RelativeBal","JES_RelativeFSR","JES_RelativeJEREC1_2016preVFP","JES_RelativeJEREC1_2016","JES_RelativeJEREC1_2017","JES_RelativeJEREC1_2018",
    "JES_RelativeJEREC2_2016preVFP","JES_RelativeJEREC2_2016","JES_RelativeJEREC2_2017","JES_RelativeJEREC2_2018","JES_RelativeJERHF",
    "JES_RelativePtBB","JES_RelativePtEC1_2016preVFP","JES_RelativePtEC1_2016","JES_RelativePtEC1_2017","JES_RelativePtEC1_2018",
    "JES_RelativePtEC2_2016preVFP","JES_RelativePtEC2_2016","JES_RelativePtEC2_2017","JES_RelativePtEC2_2018","JES_RelativePtHF",
    "JES_RelativeStatEC_2016preVFP","JES_RelativeStatEC_2016","JES_RelativeStatEC_2017","JES_RelativeStatEC_2018",
    "JES_RelativeStatFSR_2016preVFP","JES_RelativeStatFSR_2016","JES_RelativeStatFSR_2017","JES_RelativeStatFSR_2018",
    "JES_RelativeStatHF_2016preVFP","JES_RelativeStatHF_2016","JES_RelativeStatHF_2017","JES_RelativeStatHF_2018",
    "JES_RelativeSample_2016preVFP","JES_RelativeSample_2016","JES_RelativeSample_2017","JES_RelativeSample_2018",
    "JES_PileUpDataMC","JES_PileUpPtBB","JES_PileUpPtEC1","JES_PileUpPtEC2","JES_PileUpPtHF","JES_PileUpPtRef","JES_FlavorQCD","JES_Fragmentation",
    "JES_SinglePionECAL","JES_SinglePionHCAL","JES_TimePtEta_2016preVFP","JES_TimePtEta_2016","JES_TimePtEta_2017","JES_TimePtEta_2018",
    'JER_2016preVFP', 'JER_2016',  'JER_2017', 'JER_2018',
    'Unclustered_2016preVFP', 'Unclustered_2016',  'Unclustered_2017', 'Unclustered_2018',
    'LepReco',
    'LepIDsys_elec',
    'LepIDstat_elec_2016', 'LepIDstat_elec_2016preVFP', 'LepIDstat_elec_2017', 'LepIDstat_elec_2018',
    'LepIDsys_muon',
    'LepIDstat_muon_2016', 'LepIDstat_muon_2016preVFP', 'LepIDstat_muon_2017', 'LepIDstat_muon_2018',
    'Lumi_correlated_161718', 'Lumi_correlated_1718',
    'Lumi_uncorrelated_2016', 'Lumi_uncorrelated_2017', 'Lumi_uncorrelated_2018',
    'Trigger_2016preVFP', 'Trigger_2016', 'Trigger_2017', 'Trigger_2018',
    'PU', 'Prefire', 'WZ_Njet_reweight', 'WZ_heavyFlavour',
    'muF_WZ', 'muF_ZZ', 'muF_tWZ', 'muF_tZq', 'muF_triBoson', 'muF_ttX', 'muF_ttZ', #'muF_ggToZZ',
    'muR_WZ', 'muR_ZZ', 'muR_tWZ', 'muR_tZq', 'muR_triBoson', 'muR_ttX', 'muR_ttZ', #'muR_ggToZZ',
    'rate_WZ', 'rate_ZZ', 'rate_ttZ',
    'EWK_add_WZ', 'EWK_add_ZZ','EWK_mul_WZ', 'EWK_mul_ZZ',
]

rates_bkg = {
    "tWZ": 0.2,
    "ttX": 0.2,
    "tZq": 0.1,
    "triBoson": 0.2,
    "ggToZZ": 0.2,
}

for region in regions:
    for log in [False, True]:
        suffix = "__EFTsignal" if args.addSignal else ""
        if log:
            suffix+="_log"
        p = Plotter("PreFit_ULRunII__"+region+"__"+histname+suffix)
        p.plot_dir = plotdir
        p.lumi = "138"
        p.xtitle = "Z boson candidate #it{p}_{T} [GeV]"
        p.ytitle = "Events / GeV [ GeV^{-1} ]"
        p.divideByWidth = True
        p.drawRatio = True
        p.ratiotitle = "#splitline{Ratio}{to SM}"
        p.subtext = "Preliminary"
        p.legshift = (-0.1, -0.1, 0.0, 0.0)
        if log:
            p.log = True
            if region == "WZ":
                p.setCustomYRange(0.001, 10000)
            elif region == "ZZ":
                p.setCustomYRange(0.001, 1000)
            elif region == "ttZ":
                p.setCustomYRange(0.001, 1000)

        regiontext = "SR"
        if region == "ttZ":
            regiontext+="_{t#bar{t}Z}"
        elif region == "WZ":
            regiontext+="_{WZ}"
        elif region == "ZZ":
            regiontext+="_{ZZ}"
        regiontext+=", PreFit"
        p.addText(0.22, 0.7, regiontext, font=43, size=16)
        # if region == "WZ":
        #     p.ratiorange = 0.1, 2.4
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
                # print sname
                hist_up = getObjFromFile(combineInput, region+"__"+histname+"/"+process+"__"+sname+"Up")
                hist_down = getObjFromFile(combineInput, region+"__"+histname+"/"+process+"__"+sname+"Down")
                p.addSystematic(hist_up, hist_down, sname, processinfo[process][0])
            if process in backgrounds and process != "nonprompt":
                p.addNormSystematic(processinfo[process][0], rates_bkg[process])
        h_data = getObjFromFile(combineInput, region+"__"+histname+"/data_obs")
        p.addData(h_data)
        if args.addSignal:
            hist_signal = getObjFromFile(combineInput, region+"__"+histname+"/"+"sm_lin_quad_"+WCs[region])
            hist_signal.Add(hist_bkg)
            p.addSignal(hist_signal, WClatexNames[WCs[region]].replace("[TeV^{-2}]", "")+" = 1 TeV^{-2}", ROOT.kRed)
        p.draw()
