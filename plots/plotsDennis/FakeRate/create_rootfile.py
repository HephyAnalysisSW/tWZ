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
argParser.add_argument('--plotOnly',         action='store_true', default=False, help='only plot without re-creating root file?')
argParser.add_argument('--noPlots',          action='store_true', default=False, help='No plots?')
argParser.add_argument('--noTWZ',            action='store_true', default=False, help='Keep tWZ at SM point?')
# argParser.add_argument('--channel',          action='store', default='muon')
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
    

################################################################################
### Setup
ROOT.gROOT.SetBatch(ROOT.kTRUE)


boundaries_pt = [0, 20, 30, 45, 65, 120]
boundaries_eta = [0, 1.2, 2.1, 2.4]

channels = ["muon", "elec"]
# channels = ["muon"]

years = ["UL2018"]
outdir = "/groups/hephy/cms/dennis.schwarz/www/tWZ/Fakerate/CombineInput/"

prompt = ["Wjets", "WZ", "ZZ", "WW", "TTbar", "DY"]
nonprompt = {
    "muon" : ["QCD_MuEnriched"],
    "elec" : ["QCD_EMEnriched", "QCD_bcToE"],
}

selection = "singlelepL-vetoAddLepL-vetoMET"
list_of_rootfiles = []

for year in years:
    logger.info("Running year %s", year)
    for channel in channels:
        logger.info("Running channel %s", channel)
        filename = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/FakeRate_v3/%s/%s/%s/Results.root" %(year, channel, selection)
        logger.info("Reading %s", filename)
        for i in range(len(boundaries_pt)):
            for j in range(len(boundaries_eta)):
                ptbin = i+1
                etabin = j+1
                if ptbin >= 6 or etabin >= 4:
                    continue
                outname = outdir+"FakeRate_%s_%s_PT%s_ETA%s" %(year,channel,ptbin,etabin)
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
                # Write loose
                outnameL = outname+"_LOOSE.root"
                outfile_L = ROOT.TFile(outnameL, "RECREATE")
                outfile_L.cd()
                outfile_L.mkdir("singlelep")
                outfile_L.cd("singlelep")
                hist_prompt_L.Write("prompt") 
                hist_nonprompt_L.Write("nonprompt")  
                hist_data_L.Write("data_obs")  
                outfile_L.Close()
                list_of_rootfiles.append(outnameL)
                # Write tight
                outnameT = outname+"_TIGHT.root"
                outfile_T = ROOT.TFile(outnameT, "RECREATE")
                outfile_T.cd()
                outfile_T.mkdir("singlelep")
                outfile_T.cd("singlelep")
                hist_prompt_T.Write("prompt")  
                hist_nonprompt_T.Write("nonprompt")  
                hist_data_T.Write("data_obs")  
                outfile_T.Close()
                list_of_rootfiles.append(outnameT)
                
                
# for f in list_of_rootfiles:
#     h_prompt = getObjFromFile(f, "singlelep/rompt")
#     h_nonprompt = getObjFromFile(f, "singlelep/nonprompt")
#     h_data = getObjFromFile(f, "singlelep/data_obs")
#     splits = f.split("/")
#     name = splits[len(splits)-1].replace(".root", "")
#     p = Plotter(name)
#     p.plot_dir = plot_directory+"/FakeRate/CombineInput/"
#     p.drawRatio = True
#     p.xtitle = "M_{T}^{fix} [GeV]"
#     p.addBackground(h_prompt, "prompt", ROOT.kRed)
#     p.addBackground(h_nonprompt, "nonprompt", ROOT.kBlue)
#     p.addData(h_data)
#     p.draw()
