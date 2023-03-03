#!/usr/bin/env python

import os
import ROOT
import Analysis.Tools.syncer
import array as arr
from math                                        import sqrt
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--channel',        action='store',      default='muon')
argParser.add_argument('--year',           action='store',      default='UL2018')
argParser.add_argument('--plotPrefit',     action='store_true', default=False)
argParser.add_argument('--prescalemode',   action='store', type=str, default="mine")
args = argParser.parse_args()

logger.info("Plot post fit distributions")

    
################################################################################
# Some functions
def getPrefit(plotname, process, path):
    filename_L = path+"FakeRate_"+plotname+"_LOOSE.root"
    filename_T = path+"FakeRate_"+plotname+"_TIGHT.root"
    
    hist_L = getObjFromFile(filename_L, "singlelep/"+process) 
    hist_T = getObjFromFile(filename_T, "singlelep/"+process) 
    return hist_L, hist_T
    
def getPostfit(plotname, process, path):
    prefix = "fitDiagnostics."
    histdir_L = "shapes_fit_s/Fakerate_"+plotname+"_LOOSE_1_13TeV/"
    histdir_T = "shapes_fit_s/Fakerate_"+plotname+"_TIGHT_1_13TeV/"
    filename_L = path+prefix+plotname+"_LOOSE_1_13TeV_0.root"
    filename_T = path+prefix+plotname+"_TIGHT_1_13TeV_0.root"
    hist_L = getObjFromFile(filename_L, histdir_L+process) 
    hist_T = getObjFromFile(filename_T, histdir_T+process) 
    return hist_L, hist_T
    
def ConvertBinning(h_post, dummy):
    h_new = dummy.Clone()
    Nbins = h_post.GetSize()-2
    if Nbins != dummy.GetSize()-2:
        print "Bin number does not match!"
    for i in range(Nbins):
        bin = i+1
        h_new.SetBinContent(bin, h_post.GetBinContent(bin))
        h_new.SetBinError(bin, h_post.GetBinError(bin))
    return h_new
    
def createMap(boundaries_pt, boundaries_eta):
    array_pt = arr.array('d',boundaries_pt)
    array_eta = arr.array('d',boundaries_eta)
    map = ROOT.TH2F("hist", "hist", len(array_pt)-1, array_pt, len(array_eta)-1, array_eta)
    return map

def drawMap(map, plotname, dir):
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetOptStat(0)
    c = ROOT.TCanvas("c", "c", 600, 600)
    ROOT.gPad.SetRightMargin(0.19)
    ROOT.gPad.SetLeftMargin(0.19)
    ROOT.gPad.SetBottomMargin(0.12)
    map.SetTitle(" ")
    map.GetXaxis().SetTitle("Lepton p_{T}^{cone}")
    map.GetYaxis().SetTitle("Lepton |#eta|")
    map.Draw("COLZ")
    map.GetXaxis().SetRangeUser(0, 100)
    c.Print(dir+plotname+".pdf")
        
def getRateAndError(h1, h2):
    N1 = 0
    N2 = 0
    e1sq = 0
    e2sq = 0
    Nbins = h1.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        N1 += h1.GetBinContent(bin)
        e1sq += pow(h1.GetBinError(bin),2)
        N2 += h2.GetBinContent(bin)
        e2sq += pow(h2.GetBinError(bin),2)
    e1 = sqrt(e1sq)
    e2 = sqrt(e2sq)
    if N1 == 0 or N2 == 0:
        return (0., 0.)
    ratio = N1/N2 if N2 !=0 else 0
    error = sqrt( pow((e1/N2),2) + pow((-N1*e2/(N2*N2)),2) )
    return (ratio, error)
    
# various methods to get fake rate:
# - from postfit nonprompt only 
# - from prefit (data-prompt)
# - from postfit (data-prompt)
################################################################################    
ROOT.gROOT.SetBatch(ROOT.kTRUE)

prefitpath = "/groups/hephy/cms/dennis.schwarz/www/tWZ/Fakerate/CombineInput/"
postfitpath = "/groups/hephy/cms/dennis.schwarz/www/tWZ/Fakerate/Fits/"
plotdir = plot_directory+"/FakeRate/Maps_data/"

if args.prescalemode == "bril":
    prefitpath = "/groups/hephy/cms/dennis.schwarz/www/tWZ/Fakerate/CombineInput_BRIL/"
    postfitpath = "/groups/hephy/cms/dennis.schwarz/www/tWZ/Fakerate/Fits_BRIL/"
    plotdir = plot_directory+"/FakeRate/Maps_data_BRIL/"


year = args.year
channel = args.channel
boundaries_pt = [0, 20, 30, 45, 120]
boundaries_eta = [0, 1.2, 2.1, 2.4]
if args.channel == "elec":
    boundaries_eta = [0, 0.8, 1.44, 2.4]
    
plotters = {}

FakerateMap_v1 = createMap(boundaries_pt, boundaries_eta)
FakerateMap_v1_stat = createMap(boundaries_pt, boundaries_eta)
FakerateMap_v2 = createMap(boundaries_pt, boundaries_eta)
FakerateMap_v2_stat = createMap(boundaries_pt, boundaries_eta)
FakerateMap_v3 = createMap(boundaries_pt, boundaries_eta)
FakerateMap_v3_stat = createMap(boundaries_pt, boundaries_eta)

for i in range(len(boundaries_pt)):
    for j in range(len(boundaries_eta)):
        ptbin = i+1
        etabin = j+1
        if ptbin >= 5 or etabin >= 4:
            continue
        plotname = year+"_"+channel+"_PT"+str(ptbin)+"_ETA"+str(etabin)
        # Get prefit histograms
        h_pre_prompt_L, h_pre_prompt_T = getPrefit(plotname, "prompt", prefitpath)
        h_pre_nonprompt_L, h_pre_nonprompt_T = getPrefit(plotname, "nonprompt", prefitpath)
        h_pre_data_L, h_pre_data_T = getPrefit(plotname, "data_obs", prefitpath)
        
        # Create a dummy histogram that has correct binning
        dummy_pre = h_pre_data_L.Clone()
        dummy_pre.Reset()
        
        # Get postfit histograms
        h_post_prompt_L, h_post_prompt_T = getPostfit(plotname, "prompt", postfitpath)
        h_post_nonprompt_L, h_post_nonprompt_T = getPostfit(plotname, "nonprompt", postfitpath)


        # Convert postfit since they have different binning scheme than prefit 
        h_post_prompt_L = ConvertBinning(h_post_prompt_L, dummy_pre)
        h_post_prompt_T = ConvertBinning(h_post_prompt_T, dummy_pre)
        h_post_nonprompt_L = ConvertBinning(h_post_nonprompt_L, dummy_pre)
        h_post_nonprompt_T = ConvertBinning(h_post_nonprompt_T, dummy_pre)
        
        plotdir = plot_directory+"/FakeRate/PostFit/"
        if args.prescalemode == "bril":
            plotdir = plot_directory+"/FakeRate/PostFit_BRIL/"
        
        if args.plotPrefit:
            plotdir = plotdir.replace("PostFit", "PreFit")
                
            
        if not os.path.exists( plotdir ): os.makedirs( plotdir )
        
        # Loose plots
        p_L = Plotter(plotname+"_LOOSE")
        p_L.plot_dir = plotdir
        p_L.drawRatio = True
        p_L.ratiorange = (0.2, 1.8)
        p_L.xtitle = "M_{T}^{fix} [GeV]"
        if args.plotPrefit:
            p_L.addBackground(h_pre_prompt_L, "prompt", ROOT.kRed)
            p_L.addBackground(h_pre_nonprompt_L, "nonprompt", ROOT.kBlue)
        else:            
            p_L.addBackground(h_post_prompt_L, "prompt", ROOT.kRed)
            p_L.addBackground(h_post_nonprompt_L, "nonprompt", ROOT.kBlue)
        p_L.addData(h_pre_data_L)
        plotters[plotname+"_LOOSE"] = p_L

        # Tight plots 
        p_T = Plotter(plotname+"_TIGHT")
        p_T.plot_dir = plotdir
        p_T.drawRatio = True
        p_T.ratiorange = (0.2, 1.8)
        p_T.xtitle = "M_{T}^{fix} [GeV]"
        if args.plotPrefit:
            p_T.addBackground(h_pre_prompt_T, "prompt", ROOT.kRed)
            p_T.addBackground(h_pre_nonprompt_T, "nonprompt", ROOT.kBlue)
        else:            
            p_T.addBackground(h_post_prompt_T, "prompt", ROOT.kRed)
            p_T.addBackground(h_post_nonprompt_T, "nonprompt", ROOT.kBlue)
        p_T.addData(h_pre_data_T)
        plotters[plotname+"_TIGHT"] = p_T
        
        # Fakerate maps 
        # Version 1: nonprompt = data - prompt_postfit
        h_nonprompt_data_L = h_pre_data_L.Clone()
        h_nonprompt_data_L.Add(h_post_prompt_L, -1)
        h_nonprompt_data_T = h_pre_data_T.Clone()
        h_nonprompt_data_T.Add(h_post_prompt_T, -1)
        fakerate_v1, fakerate_v1_stat = getRateAndError(h_nonprompt_data_T, h_nonprompt_data_L)
        FakerateMap_v1.SetBinContent(ptbin, etabin, fakerate_v1)
        FakerateMap_v1_stat.SetBinContent(ptbin, etabin, fakerate_v1_stat)

        # Version 2: nonprompt = data - prompt_prefit
        h_nonprompt_data_pre_L = h_pre_data_L.Clone()
        h_nonprompt_data_pre_L.Add(h_pre_prompt_L, -1)
        h_nonprompt_data_pre_T = h_pre_data_T.Clone()
        h_nonprompt_data_pre_T.Add(h_pre_prompt_T, -1)
        fakerate_v2, fakerate_v2_stat = getRateAndError(h_nonprompt_data_pre_T, h_nonprompt_data_pre_L)
        FakerateMap_v2.SetBinContent(ptbin, etabin, fakerate_v2)
        FakerateMap_v2_stat.SetBinContent(ptbin, etabin, fakerate_v2_stat)        
        
        # Version 3: nonprompt = nonprompt_postfit
        h_nonprompt_fit_L = h_post_nonprompt_L.Clone()
        h_nonprompt_fit_T = h_post_nonprompt_T.Clone()
        fakerate_v3, fakerate_v3_stat = getRateAndError(h_nonprompt_fit_T, h_nonprompt_fit_L)
        FakerateMap_v3.SetBinContent(ptbin, etabin, fakerate_v3)
        FakerateMap_v3_stat.SetBinContent(ptbin, etabin, fakerate_v3_stat)     
        
        # Check compatibility of various methods
        d12 = fakerate_v1 - fakerate_v2
        d13 = fakerate_v1 - fakerate_v3
        d23 = fakerate_v2 - fakerate_v3
        if d12 > 0.4 or d13 > 0.4 or d23 > 0.4:
            logger.info("PT%s ETA%s, v1 and v2 not compatible: v1=%s, v2=%s, v3=%s", ptbin, etabin, fakerate_v1, fakerate_v2, fakerate_v3)
                                        

if not args.plotPrefit:
    drawMap(FakerateMap_v1, year+"__"+channel+"__Map_DATA_v1", plotdir)
    drawMap(FakerateMap_v2, year+"__"+channel+"__Map_DATA_v2", plotdir)
    drawMap(FakerateMap_v3, year+"__"+channel+"__Map_DATA_v3", plotdir)
    drawMap(FakerateMap_v1_stat, year+"__"+channel+"__Map_DATA_v1_stat", plotdir)
    drawMap(FakerateMap_v2_stat, year+"__"+channel+"__Map_DATA_v2_stat", plotdir)
    drawMap(FakerateMap_v3_stat, year+"__"+channel+"__Map_DATA_v3_stat", plotdir)


for name in plotters:
    plotters[name].draw()

# del plotters

# Store maps in file
if not args.plotPrefit:
    suffix = ""
    if args.prescalemode == "bril":
        suffix = "__BRIL"
    outfile = ROOT.TFile("LeptonFakerate__"+year+"__"+channel+suffix+".root", "RECREATE")
    outfile.cd()
    FakerateMap_v1.Write("Fakerate_v1")
    FakerateMap_v2.Write("Fakerate_v2")
    FakerateMap_v3.Write("Fakerate_v3")
    FakerateMap_v1_stat.Write("Fakerate_v1_stat")
    FakerateMap_v2_stat.Write("Fakerate_v2_stat")
    FakerateMap_v3_stat.Write("Fakerate_v3_stat")
    outfile.Close()
####
