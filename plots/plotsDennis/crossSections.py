#!/usr/bin/env python

import os
import ROOT
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter

# ttZ = ["ttZ", "ttZToLL", "ttZToLLNunu"]
# WZ = ["WZ", "WZTo3LNu"]
# ZZ = ["ZZ", "ZZTo4L"]
#
# analysis
#
# ttZtZq = {}
# ttZtZq["ttZToLLNunu"] = 0.28136
# ttZtZq["WZTo3LNu"] = 5.052
# ttZtZq["ZZ"] = 16.523
#
# ghent = {}
# ghent["ttZToLLNunu"] = 0.281
# ghent["WZTo3LNu"] = 4.9173
# ghent["ZZTo4L"] = 1.256
#
# multilep = {}
# multilep["ttZToLLNunu"] = 0.281
# multilep["WZTo3LNu"] = 5.2843
# multilep["ZZTo4L"] = 1.256


import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--ttZ',              action='store', type=str, default="ttZ")
argParser.add_argument('--WZ',               action='store', type=str, default="WZ")
argParser.add_argument('--ZZ',               action='store', type=str, default="ZZ")
args = argParser.parse_args()



ROOT.gROOT.SetBatch(ROOT.kTRUE)

files = {
    "ZZ":  "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint/YEAR/all/qualepT-minDLmass12-onZ1-onZ2/Results.root",
    "WZ":  "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint/YEAR/all/trilepT-minDLmass12-onZ1-btag0-met60/Results.root",
    "ttZ": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint/YEAR/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/Results.root",
}

years = ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]
# all_processes = ["ttZ", "WZ", "ZZ", "tWZ", "ttX", "tZq", "triBoson", "nonprompt"]
all_processes = ["ttZ_sm", "WZTo3LNu_powheg", "ZZ_pythia", "tWZ", "ttX", "tZq", "triBoson", "nonprompt"]

SF_ttZ = 0.281/0.2728
SF_WZ = 5.2843/4.42965
SF_ZZ = 16.91/16.523

processSettings = {
    "tWZ": ("tWZ", color.TWZ),
    "ttZ": ("ttZ", color.TTZ),
    "ttZ_sm": ("ttZ", color.TTZ),
    "ttX": ("ttX", color.TTX_rare),
    "tZq": ("tZq", color.TZQ),
    "WZ": ( "WZ",  color.WZ),
    "WZTo3LNu_powheg": ( "WZ",  color.WZ),
    "WZTo3LNu": ( "WZ",  color.WZ),
    "WZ_pythia": ( "WZ",  color.WZ),
    "triBoson": ("Triboson", color.triBoson),
    "ZZ": ("ZZ", color.ZZ),
    "ZZ_pythia": ("ZZ", color.ZZ),
    "nonprompt": ("Nonprompt", color.nonprompt),
}

plotdir = plot_directory+"/EFTvsSM/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

histname = "Z1_pt"

for year in years:
    for region in ["ttZ", "WZ", "ZZ"]:
        p = Plotter(year+"__"+region+"__"+histname)
        p.plot_dir = plotdir
        p.lumi = ""
        p.xtitle = "Z p_{T} [GeV]"
        file = files[region].replace("YEAR", year)
        # print file
        N_mc = 0
        for proc in all_processes:
            legname, col = processSettings[proc]
            hist = getObjFromFile(file, histname+"__"+proc)
            if proc in ["WZTo3LNu_powheg", "WZTo3LNu"]:
                hist.Scale(SF_WZ)
            elif proc in ["ttZ_sm"]:
                hist.Scale(SF_ttZ)
            elif proc in ["ZZ", "ZZ_pythia"]:
                hist.Scale(SF_ZZ)
            N_mc += hist.Integral()
            p.addBackground(hist, legname, col)
        h_data = getObjFromFile(file, histname+"__data")
        N_data = h_data.Integral()
        p.addData(h_data)
        p.draw()

        p_compare = Plotter(year+"__"+region+"__"+histname+"__comparison")
        p_compare.plot_dir = plotdir
        p_compare.lumi = ""
        p_compare.xtitle = "Z p_{T} [GeV]"
        sm_file = "ttZ_sm"
        eft_file = "ttZ__cHq1Re11=0.0000"
        SM_SF = SF_ttZ
        if region == "WZ":
            sm_file = "WZTo3LNu_powheg"
            eft_file = "WZ__cHq1Re11=0.0000"
            SM_SF = SF_WZ
        elif region == "ZZ":
            sm_file = "ZZ_pythia"
            eft_file = "ZZ__cHq1Re11=0.0000"
            SM_SF = SF_ZZ
        h_sm = getObjFromFile(file, histname+"__"+sm_file)
        h_sm.Scale(SM_SF)
        h_eft = getObjFromFile(file, histname+"__"+eft_file)
        p_compare.addBackground(h_sm, "SM sample", 13)
        p_compare.addSignal(h_eft, "EFT sample", ROOT.kRed)
        p_compare.draw()

        print "MC/data = ", N_mc/N_data
        print "EFT/SM = ", h_eft.Integral()/h_sm.Integral()
        print "EFT SF = ", 1 / (h_eft.Integral()/h_sm.Integral())
