#!/usr/bin/env python
import os, ROOT, pickle
from tWZ.Tools.user                      import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.samples.color import color
from MyRootTools.plotter.Plotter                 import Plotter

import Analysis.Tools.syncer


import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

ROOT.gROOT.SetBatch(ROOT.kTRUE)

# path = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/FakeRate_v5_noPreScale/"
path = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/FakeRate_v5_noPreScale_reduce/"
years = ["UL2017", "UL2018"]
channels = ["elec", "muon"]
# channels = ["elec"]
selection = "singlelepT-vetoAddLepFO-met40"
triggerlist = {
    "elec" : ["HLT_Ele8_CaloIdM_TrackIdM_PFJet30","HLT_Ele17_CaloIdM_TrackIdM_PFJet30"],
    "muon" : ["HLT_Mu3_PFJet40","HLT_Mu8","HLT_Mu17","HLT_Mu20","HLT_Mu27"],
}

QCDsamples = {
    "elec": ["QCD_EMEnriched", "QCD_bcToE"],
    "muon": ["QCD_MuEnriched"]
}

MTmin = 90
MTmax = 130

colors = {
    "Wjets": color.WJets,
    "WZ": color.WZ, 
    "ZZ": color.ZZ, 
    "WW": color.WW, 
    "TTbar": color.TTJets, 
    "DY": color.DY, 
    "QCD_EMEnriched": color.QCD+5, 
    "QCD_bcToE": color.QCD-5,
    "QCD_MuEnriched": color.QCD+10,
}


for year in years:
    prescales = {}
    logger.info("Running year %s", year)
    for channel in channels:
        logger.info("Running channel %s", channel)
        for trigger in triggerlist[channel]:
            logger.info("Running trigger %s", trigger)
            backgrounds = ["Wjets","WZ", "ZZ", "WW", "TTbar", "DY"]+QCDsamples[channel]
            filename = path+year+"/"+channel+"/"+selection+"/Results.root"
            hist_prefix = "T_MTfix__TRIGGER_"
            h_data = getObjFromFile(filename, hist_prefix+trigger+"__data")
            h_background = {}
            for bkg in backgrounds:
                h_background[bkg] = getObjFromFile(filename, hist_prefix+trigger+"__"+bkg)
            
            bin_lo = h_data.FindBin(MTmin)
            bin_hi = h_data.FindBin(MTmax)
            
            Nevents = {}
            Nevents["data"] = h_data.Integral(bin_lo, bin_hi)
            bkgsum = 0
            for bkg in backgrounds:
                Nevents[bkg] =  h_background[bkg].Integral(bin_lo,bin_hi)
                bkgsum += h_background[bkg].Integral(bin_lo,bin_hi)
            Nevents["MC"] = bkgsum
            prescales[trigger] = Nevents["MC"]/Nevents["data"]
            
            plotdir = plot_directory+"/FakeRate_prescales/"
            if not os.path.exists( plotdir ): os.makedirs( plotdir )
            p = Plotter(year+"__"+channel+"__"+trigger)
            p.plot_dir = plotdir
            p.drawRatio = True
            p.xtitle = "m_{T}^{fix}"
            p.yfactor = 2.0
            p.lumi = "60"
            p.legshift = (-0.35, +0.02, -0.4, -0.14) 
            p.addData(h_data, "Data")
            for bkg in backgrounds:
                h_background[bkg].Scale(1.0/prescales[trigger]) 
                p.addBackground(h_background[bkg], bkg, colors[bkg])
            p.draw()
            print trigger, prescales[trigger]
        
    with open(year+'_prescales.pkl', 'wb') as handle:
        pickle.dump(prescales, handle)
