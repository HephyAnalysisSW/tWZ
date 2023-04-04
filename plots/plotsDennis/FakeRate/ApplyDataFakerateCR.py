#!/usr/bin/env python

import os
import ROOT
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--ttW',      action='store_true')
argParser.add_argument('--bril',     action='store_true')
argParser.add_argument('--tunePtCone',      action='store_true')
argParser.add_argument('--SR',      action='store_true')

args = argParser.parse_args()

logger.info("Apply fake rate to control region and compare with signal region")
    
################################################################################
# Some functions

################################################################################    
ROOT.gROOT.SetBatch(ROOT.kTRUE)

version = "v7"

path_SR = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"/"
path_CR = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_FakeRateSF_useDataSF/"

if args.ttW:
    path_SR = path_SR.replace("EFT_UL_"+version, "EFT_UL_"+version+"_splitTTX")
    path_CR = path_CR.replace("EFT_UL_"+version, "EFT_UL_"+version+"_splitTTX")

if args.bril:
    path_CR = path_CR.replace("useDataSF", "useBRILSF")

if args.tunePtCone:
    path_CR = path_CR.replace("useDataSF", "useDataSF_tunePtCone")
    

prefix_SR = "trilepT-"
prefix_CR = "trilepFOnoT-"

selections = [
    "minDLmass12-offZ1/",
    "minDLmass12-offZ1-njet3p-btag1p/",
    "minDLmass12-offZ1-btag0-met60/",
]


years = ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]

if args.tunePtCone:
    years = ["ULRunII"]

if args.SR:
    selections = [
    "minDLmass12-onZ1-njet3p-btag1p/",
    "minDLmass12-onZ1-btag0-met60/",
    ]
    years = ["ULRunII"]
    
    
channels = ["all", "eee", "mumumu"]
# channels = ["all"]

histnames = ["N_jets", "Z1_pt", "l1_pt", "l2_pt", "l3_pt"]
# histnames = ["Z1_pt"]
object = {
    "N_jets": "Number of jets",
    "Z1_pt": "Z", 
    "l1_pt": "Leading lepton", 
    "l2_pt": "Sub-leading lepton", 
    "l3_pt": "Trailing lepton",
}

rebin = {
    "N_jets": 1,
    "Z1_pt": 2, 
    "l1_pt": 4, 
    "l2_pt": 4, 
    "l3_pt": 4,
}

xmax = {
    "N_jets": 10.5, 
    "Z1_pt": 300, 
    "l1_pt": 200, 
    "l2_pt": 150, 
    "l3_pt": 100,
}

prompt_processes = [
    ("tWZ", "tWZ", color.TWZ),
    ("ttZ", "ttZ", color.TTZ),
    ("ttX", "ttX", color.TTX_rare),
    ("tZq", "tZq", color.TZQ),
    ("WZ",  "WZ",  color.WZ),
    ("triBoson", "Triboson", color.triBoson),
    ("ZZ", "ZZ", color.ZZ),
]

if args.ttW:
    prompt_processes = [
        ("tWZ", "tWZ", color.TWZ),
        ("ttZ", "ttZ", color.TTZ),
        ("ttW", "ttW", color.TTW),
        ("ttX_noTTW", "ttX (no ttW)", color.TTX_rare),
        ("tZq", "tZq", color.TZQ),
        ("WZ",  "WZ",  color.WZ),
        ("triBoson", "Triboson", color.triBoson),
        ("ZZ", "ZZ", color.ZZ),
    ]
    years = ["ULRunII"]
    channels = ["all"]
    
for year in years:
    logger.info("Running year %s", year)
    for selection in selections:
        logger.info("Selection = %s", selection)
        for channel in channels:
            for histname in histnames:
                plotdir = plot_directory+"/FakeRate/ClosureTest_data/"+selection
                if args.ttW:
                    plotdir = plotdir.replace("ClosureTest_data", "ClosureTest_data_ttW")
                if args.bril:
                    plotdir = plotdir.replace("ClosureTest_data", "ClosureTest_BRIL")
                if args.tunePtCone:
                    plotdir = plotdir.replace("ClosureTest_data", "ClosureTest_tunePtCone")
                
                if not os.path.exists( plotdir ): os.makedirs( plotdir )
                p = Plotter(year+"__"+channel+"__"+histname)
                p.plot_dir = plotdir
                p.drawRatio = True
                p.ratiorange = (0.2, 1.8)
                p.rebin = rebin[histname]
                p.setCustomXRange(0, xmax[histname])
                p.xtitle = object[histname]+" p_{T} [GeV]"
                if "N_jets" in histname: p.xtitle = object[histname]
                # Get File names
                filename_SR = path_SR+year+"/"+channel+"/"+prefix_SR+selection+"/Results.root"
                filename_CR = path_CR+year+"/"+channel+"/"+prefix_CR+selection+"/Results.root"
                # Get Data in SR
                h_data_SR = getObjFromFile(filename_SR, histname+"__data") 
                p.addData(h_data_SR, "Data")
                # Get prompt backgrounds in CR
                firstbkg = True
                for (process,legname,color) in prompt_processes:
                    h_bkg = getObjFromFile(filename_CR, histname+"__"+process)
                    if firstbkg:
                        h_bkg_CR = h_bkg.Clone()
                        firstbkg = False 
                    else:
                        h_bkg_CR.Add(h_bkg)
                # Get nonpromt = Data in CR * fakerate and subtract backgrounds
                h_nonpromt = getObjFromFile(filename_CR, histname+"__data")
                h_nonpromt.Add(h_bkg_CR, -1)
                p.addBackground(h_nonpromt, "Nonprompt", 15)
                # Get uncertainty 
                filename_UP   = path_CR[:-1]+"_Fakerate_UP/"+year+"/"+channel+"/"+prefix_CR+selection+"/Results.root"
                h_nonpromt_up = getObjFromFile(filename_UP, histname+"__data")
                h_nonpromt_up.Add(h_bkg_CR, -1)
                filename_DOWN = path_CR[:-1]+"_Fakerate_DOWN/"+year+"/"+channel+"/"+prefix_CR+selection+"/Results.root"
                h_nonpromt_down = getObjFromFile(filename_DOWN, histname+"__data")
                h_nonpromt_down.Add(h_bkg_CR, -1)
                p.addSystematic(h_nonpromt_up, h_nonpromt_down, "Fakerate", "Nonprompt")
                p.addNormSystematic("Nonprompt", 0.3)
                # Get all prompt backgrounds
                for (process,legname,color) in prompt_processes:
                    h_bkg = getObjFromFile(filename_SR, histname+"__"+process) 
                    if args.ttW and process == "ttW":
                        h_bkg.Scale(1.4)
                    p.addBackground(h_bkg, legname, color)
                p.draw()
