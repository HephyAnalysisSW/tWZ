#!/usr/bin/env python

import ROOT
from math                                import sqrt
import array
import Analysis.Tools.syncer
from tWZ.Tools.helpers                           import getObjFromFile
from MyRootTools.plotter.Plotter                 import Plotter
from tWZ.Tools.user                              import plot_directory

import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)
################################################################################
### Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--channel',        action='store',      default='muon')
argParser.add_argument('--year',           action='store',      default='UL2018')
argParser.add_argument('--prescalemode',   action='store', type=str, default="mine")
args = argParser.parse_args()

################################################################################
### Functions

def getSumOfHistograms(filename, names):
    if len(names) < 1:
        raise Exception("Legth of names is 0")
    hist = getObjFromFile(filename, names[0])
    for i, name in enumerate(names):
        if i==0:
            continue
        else:
            hist_tmp = getObjFromFile(filename, name)
            hist.Add(hist_tmp)
    return hist
    
def getPlotter(name, dir, h_prompt, h_nonprompt, h_data):
    p = Plotter(name)
    p.plot_dir = dir
    p.drawRatio = True
    p.xtitle = "M_{T}^{fix} [GeV]"
    p.addBackground(h_prompt, "prompt", ROOT.kRed)
    p.addBackground(h_nonprompt, "nonprompt", ROOT.kBlue)
    p.addData(h_data)
    return p 
    
def prepareHist(hist):
    newhist = hist.Clone()
    newhist.GetXaxis().SetRangeUser(0., 56.)
    return newhist
################################################################################
### Setup
ROOT.gROOT.SetBatch(ROOT.kTRUE)


boundaries_pt = [0, 20, 30, 45, 120]
boundaries_eta = [0, 1.2, 2.1, 2.4]
if args.channel == "elec":
    boundaries_eta = [0, 0.8, 1.44, 2.4]
    
channel = args.channel
year = args.year

outdir = "/groups/hephy/cms/dennis.schwarz/www/tWZ/Fakerate/CombineInput/"
outdir_plots = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/CombineInput/"

if args.prescalemode == "bril": 
    outdir = outdir.replace("CombineInput", "CombineInput_BRIL")
    outdir_plots = outdir_plots.replace("CombineInput", "CombineInput_BRIL")

prompt = ["Wjets", "WZ", "ZZ", "WW", "TTbar", "DY"]
nonprompt = {
    "muon" : ["QCD_MuEnriched"],
    "elec" : ["QCD_EMEnriched", "QCD_bcToE"],
}

selection = "singlelepFOconept-vetoAddLepFOconept-vetoMET"
plotters = {}

logger.info("Running year %s", year)
logger.info("Running channel %s", channel)
filename = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/FakeRate_v10/%s/%s/%s/Results.root" %(year, channel, selection)
if args.prescalemode == "bril": 
    filename = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/FakeRate_v10_BRILprescale/%s/%s/%s/Results.root" %(year, channel, selection)


logger.info("Reading %s", filename)
for i in range(len(boundaries_pt)):
    for j in range(len(boundaries_eta)):
        ptbin = i+1
        etabin = j+1
        if ptbin >= 5 or etabin >= 4:
            continue
        suffix = "__BIN_pt%s_eta%s" %(ptbin, etabin)
        histnameL = "L_MTfix"+suffix
        histnameT = "T_MTfix"+suffix
        promptlistL = []
        promptlistT = []
        for process in prompt:
            promptlistL.append(histnameL+"__"+process) 
            promptlistT.append(histnameT+"__"+process) 
        nonpromptlistL = []
        nonpromptlistT = []
        for process in nonprompt[channel]:
            nonpromptlistL.append(histnameL+"__"+process) 
            nonpromptlistT.append(histnameT+"__"+process)    
        hist_prompt_L = getSumOfHistograms(filename, promptlistL)
        hist_prompt_T = getSumOfHistograms(filename, promptlistT)
        hist_nonprompt_L = getSumOfHistograms(filename, nonpromptlistL)
        hist_nonprompt_T = getSumOfHistograms(filename, nonpromptlistT)
        hist_data_L = getObjFromFile(filename, histnameL+"__data")             
        hist_data_T = getObjFromFile(filename, histnameT+"__data")
                
        hist_prompt_L = prepareHist(hist_prompt_L)
        hist_prompt_T = prepareHist(hist_prompt_T)
        hist_nonprompt_L = prepareHist(hist_nonprompt_L)
        hist_nonprompt_T = prepareHist(hist_nonprompt_T)
        hist_data_L = prepareHist(hist_data_L)
        hist_data_T = prepareHist(hist_data_T)
        
        # Write loose
        plotname_L = "FakeRate_%s_%s_PT%s_ETA%s_LOOSE" %(year,channel,ptbin,etabin)
        outfile_L = ROOT.TFile(outdir+plotname_L+".root", "RECREATE")
        outfile_L.cd()
        outfile_L.mkdir("singlelep")
        outfile_L.cd("singlelep")
        hist_prompt_L.Write("prompt") 
        hist_nonprompt_L.Write("nonprompt")  
        hist_data_L.Write("data_obs")  
        outfile_L.Close()
        # Write tight
        plotname_T = "FakeRate_%s_%s_PT%s_ETA%s_TIGHT" %(year,channel,ptbin,etabin)
        outfile_T = ROOT.TFile(outdir+plotname_T+".root", "RECREATE")
        outfile_T.cd()
        outfile_T.mkdir("singlelep")
        outfile_T.cd("singlelep")
        hist_prompt_T.Write("prompt")  
        hist_nonprompt_T.Write("nonprompt")  
        hist_data_T.Write("data_obs")  
        outfile_T.Close()
        # Prepare plotters
        plotters[plotname_L] = getPlotter(plotname_L, outdir_plots, hist_prompt_L, hist_nonprompt_L, hist_data_L)
        plotters[plotname_T] = getPlotter(plotname_T, outdir_plots, hist_prompt_T, hist_nonprompt_T, hist_data_T)
        
                
for name in plotters:
    plotters[name].draw()
