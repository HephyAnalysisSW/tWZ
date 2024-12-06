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
from tWZ.Tools.CMScolors import CMScolors

import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)



def checkDifference(h_nom, h_var, threshold):
    binsOverThreshold = []
    Nbins = h_nom.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        diff = h_var.GetBinContent(bin) - h_nom.GetBinContent(bin)
        percent = 100.*abs(diff)/h_nom.GetBinContent(bin)
        if percent > threshold:
            binsOverThreshold.append(bin)
    return binsOverThreshold

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--file',             action='store', type=str, default=None)
args = argParser.parse_args()

categories = ["topEFT_ULRunII_1_13TeV","topEFT_ULRunII_2_13TeV","topEFT_ULRunII_3_13TeV"]
processes = ["sm", "ttX", "tWZ", "tZq", "triBoson", "ggToZZ", "nonprompt"]

uncerts = []
uncerts += ["ISR_ttZ","ISR_WZ","ISR_ZZ","ISR_tZq","ISR_tWZ","ISR_ttX","ISR_triBoson","ISR_ggToZZ","FSR"]
uncerts += ["muR_ttZ","muR_WZ","muR_ZZ","muF_ttZ","muF_WZ","muF_ZZ"]
uncerts += ["muR_tZq","muR_tWZ","muR_ttX","muR_triBoson","muF_tZq","muF_tWZ","muF_ttX","muF_triBoson"]
uncerts += ["WZ_Njet_reweight", "WZ_heavyFlavour"]
uncerts += ["EWK_mul_WZ", "EWK_mul_ZZ", "EWK_add_WZ", "EWK_add_ZZ"]
uncerts += ["PDF_"+str(i) for i in range(1,101)]
uncerts += ["rate_ttZ", "rate_WZ", "rate_ZZ"]
# uncerts += ["rate_ttX", "rate_triBoson", "rate_tWZ", "rate_tZq", "rate_ggToZZ"]
uncerts += ["Fakerate", "FakerateClosure_correlated_elec", "FakerateClosure_uncorrelated_elec_2016preVFP", "FakerateClosure_uncorrelated_elec_2016", "FakerateClosure_uncorrelated_elec_2017", "FakerateClosure_uncorrelated_elec_2018", "FakerateClosure_correlated_muon", "FakerateClosure_uncorrelated_muon_2016preVFP", "FakerateClosure_uncorrelated_muon_2016", "FakerateClosure_uncorrelated_muon_2017", "FakerateClosure_uncorrelated_muon_2018", "FakerateClosure_correlated_both", "FakerateClosure_uncorrelated_both_2016preVFP", "FakerateClosure_uncorrelated_both_2016", "FakerateClosure_uncorrelated_both_2017", "FakerateClosure_uncorrelated_both_2018"]
uncerts += ["Lumi_uncorrelated_2016","Lumi_uncorrelated_2017","Lumi_uncorrelated_2018","Lumi_correlated_161718","Lumi_correlated_1718"]
uncerts += ["BTag_b_correlated","BTag_l_correlated","BTag_b_uncorrelated_2016preVFP","BTag_l_uncorrelated_2016preVFP","BTag_b_uncorrelated_2016","BTag_l_uncorrelated_2016","BTag_b_uncorrelated_2017","BTag_l_uncorrelated_2017","BTag_b_uncorrelated_2018","BTag_l_uncorrelated_2018"]
uncerts += ["LepReco", "LepIDsys_muon","LepIDstat_muon_2016preVFP","LepIDstat_muon_2016","LepIDstat_muon_2017","LepIDstat_muon_2018", "LepIDsys_elec","LepIDstat_elec_2016preVFP","LepIDstat_elec_2016","LepIDstat_elec_2017","LepIDstat_elec_2018"]
uncerts += ["Trigger_2016preVFP", "Trigger_2016", "Trigger_2017", "Trigger_2018", "PU", "Prefire"]
uncerts += ["JER_2016preVFP", "JER_2016", "JER_2017", "JER_2018", "Unclustered_2016preVFP", "Unclustered_2016", "Unclustered_2017", "Unclustered_2018", "JES_AbsoluteMPFBias",    "JES_AbsoluteScale",  "JES_AbsoluteStat_2016preVFP",  "JES_AbsoluteStat_2016",  "JES_AbsoluteStat_2017",  "JES_AbsoluteStat_2018",  "JES_RelativeBal",  "JES_RelativeFSR",  "JES_RelativeJEREC1_2016preVFP",  "JES_RelativeJEREC1_2016",  "JES_RelativeJEREC1_2017",  "JES_RelativeJEREC1_2018",  "JES_RelativeJEREC2_2016preVFP",  "JES_RelativeJEREC2_2016",  "JES_RelativeJEREC2_2017",  "JES_RelativeJEREC2_2018",  "JES_RelativeJERHF",  "JES_RelativePtBB",  "JES_RelativePtEC1_2016preVFP",  "JES_RelativePtEC1_2016",  "JES_RelativePtEC1_2017",  "JES_RelativePtEC1_2018",  "JES_RelativePtEC2_2016preVFP",  "JES_RelativePtEC2_2016",  "JES_RelativePtEC2_2017",  "JES_RelativePtEC2_2018",  "JES_RelativePtHF",  "JES_RelativeStatEC_2016preVFP",  "JES_RelativeStatEC_2016",  "JES_RelativeStatEC_2017",  "JES_RelativeStatEC_2018",  "JES_RelativeStatFSR_2016preVFP",  "JES_RelativeStatFSR_2016",  "JES_RelativeStatFSR_2017",  "JES_RelativeStatFSR_2018",  "JES_RelativeStatHF_2016preVFP",  "JES_RelativeStatHF_2016",  "JES_RelativeStatHF_2017",  "JES_RelativeStatHF_2018",  "JES_RelativeSample_2016preVFP",  "JES_RelativeSample_2016",  "JES_RelativeSample_2017",  "JES_RelativeSample_2018", "JES_PileUpDataMC",  "JES_PileUpPtBB",  "JES_PileUpPtEC1",  "JES_PileUpPtEC2",  "JES_PileUpPtHF",  "JES_PileUpPtRef",  "JES_FlavorQCD",  "JES_Fragmentation",  "JES_SinglePionECAL","JES_SinglePionHCAL","JES_TimePtEta_2016preVFP","JES_TimePtEta_2016","JES_TimePtEta_2017","JES_TimePtEta_2018"]

if not os.path.isfile(args.file):
    raise RuntimeError( "File %s does not exist", args.file)

plotdir = plot_directory+"/DataCardCheck/ULRunII/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

Ncolums = 3
Nlines = 4

for cat in categories:
    for process in processes:
        plotList = []
        plotsOnOnePage = []
        nom_name = cat+"/"+process
        h_nominal = getObjFromFile(args.file, nom_name)
        for uncert in uncerts:
            # check if it a variation per process
            if uncert.split("_")[-1] in ["ttZ", "WZ", "ZZ"]:
                if process != "sm":
                    continue
            if uncert.split("_")[-1] in processes:
                if uncert.split("_")[-1] != process:
                    continue
            # Fakerate only on nonprompt
            if "Fakerate" in uncert:
                if process != "nonprompt":
                    continue
            if process == "nonprompt" and not "Fakerate" in uncert:
                continue
            # WZ uncerts
            if uncert in ["WZ_Njet_reweight", "WZ_heavyFlavour"]:
                if process != "sm":
                    continue
            # print uncert, process
            var_name = cat+"/"+process+"_"+uncert
            h_up = getObjFromFile(args.file, var_name+"Up")
            h_down = getObjFromFile(args.file, var_name+"Down")
            threshold = 0.01
            binsOverThreshold_up = checkDifference(h_nominal, h_up, threshold)
            binsOverThreshold_down = checkDifference(h_nominal, h_down, threshold)

            if len(binsOverThreshold_up)+len(binsOverThreshold_down) < 1:
                print "No bins with large variation found for "+var_name

            plotname = cat+"__"+process+"__"+uncert

            if len(plotsOnOnePage) == Ncolums*Nlines:
                plotList.append(plotsOnOnePage)
                plotsOnOnePage = []
            plotsOnOnePage.append(plotname)

            p = Plotter(plotname)
            p.plot_dir = plotdir
            p.lumi = "138"
            p.addText(0.4, 0.5, uncert, size=16)
            p.xtitle = "Z p_{T} [GeV]"
            p.drawRatio = True
            p.ratiorange = (0.85, 1.15)
            p.addBackground(h_nominal, process, 15)
            p.addSignal(h_up, "up", ROOT.kAzure+7)
            p.addSignal(h_down, "down", ROOT.kRed-4)
            p.draw()

        ## Create Latex File
        file = open(plotdir+"/"+cat+"__"+process+".tex", 'w')
        file.write("\\documentclass[11pt,a4paper,roman]{article} \n")
        file.write("\\usepackage{graphicx} \n")
        file.write("\\begin{document} \n")
        width = "%.2f" %(1.0/Ncolums-0.01)
        for plotsOnOnePage in plotList:
            file.write("\\begin{figure} \n")
            for i, plotname in enumerate(plotsOnOnePage):
                file.write("\\includegraphics[width="+width+"\\textwidth]{"+plotname+"}")
                if i > 0 and (i+1)%Ncolums == 0:
                    file.write("\\\\")
                file.write(" \n")
            file.write("\\end{figure} \n")
            file.write("\\clearpage \n")
        file.write("\\end{document} \n")
        file.close()
