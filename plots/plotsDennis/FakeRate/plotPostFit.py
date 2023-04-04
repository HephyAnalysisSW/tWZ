#!/usr/bin/env python

import os, sys
import ROOT
import Analysis.Tools.syncer
import array as arr
from math                                        import sqrt
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile
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
argParser.add_argument('--tunePtCone',     action='store_true')
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
    
def ConvertBinning(h_post, dummy, name):
    # Get Binning from pre fit
    Nbins = dummy.GetSize()-2
    binning = []
    for i in range(Nbins):
        bin = i+1
        binning.append(dummy.GetXaxis().GetBinLowEdge(bin))
        if bin == Nbins:
            binning.append(dummy.GetXaxis().GetBinUpEdge(bin))
    h_new = ROOT.TH1F(name, name, Nbins, arr.array('d',binning))
    if Nbins != dummy.GetSize()-2:
        print "Bin number does not match!"
    for i in range(Nbins):
        bin = i+1
        h_new.SetBinContent(bin, h_post.GetBinContent(bin))
        h_new.SetBinError(bin, h_post.GetBinError(bin))
    return h_new
    
def createMap(boundaries_pt, boundaries_eta, name):
    array_pt = arr.array('d',boundaries_pt)
    array_eta = arr.array('d',boundaries_eta)
    map = ROOT.TH2F(name, name, len(array_pt)-1, array_pt, len(array_eta)-1, array_eta)
    return map

def drawMap(map, plotname, dir):
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPalette(ROOT.kSunset)
    c = ROOT.TCanvas("c", "c", 600, 600)
    ROOT.gPad.SetRightMargin(0.23)
    ROOT.gPad.SetLeftMargin(0.19)
    ROOT.gPad.SetBottomMargin(0.12)
    map.SetTitle(" ")
    map.GetXaxis().SetTitle("Lepton p_{T}^{cone}")
    map.GetYaxis().SetTitle("Lepton |#eta|")
    ztitle = "Fake rate"
    if "stat" in plotname: ztitle = "Stat. uncertainty"
    if "statrel" in plotname: ztitle = "Relative stat. uncertainty"
    map.GetZaxis().SetTitle(ztitle)
    map.GetZaxis().SetTitleOffset(1.3)
    # print plotname, map.GetMaximum()
    # map.GetZaxis().SetRangeUser(0., 1.)
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
    
def combinePDFs(names, outname, dir):
    cmd = "gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER -sOutputFile="+outname+".pdf "
    for name in names:
        cmd += name+".pdf "
    cmd += " >/dev/null 2>&1"
        
    current_dir = os.getcwd()
    os.chdir(dir)
    os.system(cmd)
    os.chdir(current_dir)
    # print cmd

def make1Dprojection(map, map_uncert, name, boundaries_pt):
    histograms = {}
    NbinsX = map.GetXaxis().GetNbins()
    NbinsY = map.GetYaxis().GetNbins()
    for j in range(NbinsY):
        etabin = j+1
        hname = name+"_ETA"+str(etabin)
        hist = ROOT.TH1F(hname, hname, len(boundaries_pt)-1, arr.array('d',boundaries_pt) )
        for i in range(NbinsX):
            ptbin = i+1
            content = map.GetBinContent(ptbin, etabin)
            error = map_uncert.GetBinContent(ptbin, etabin)
            hist.SetBinContent(ptbin, content)
            hist.SetBinError(ptbin, error)
        histograms["ETA"+str(etabin)] = hist
    return histograms

# various methods to get fake rate:
# - from postfit nonprompt only 
# - from prefit (data-prompt)
# - from postfit (data-prompt)
################################################################################    
ROOT.gROOT.SetBatch(ROOT.kTRUE)
year = args.year
channel = args.channel

prefitpath = "/groups/hephy/cms/dennis.schwarz/www/tWZ/Fakerate/CombineInput/"
postfitpath = "/groups/hephy/cms/dennis.schwarz/www/tWZ/Fakerate/Fits/"
plotdir = plot_directory+"/FakeRate/PostFit/"
plotdir_maps = plot_directory+"/FakeRate/Maps_data/"
outname = year+"_"+channel

if args.prescalemode == "bril":
    prefitpath = "/groups/hephy/cms/dennis.schwarz/www/tWZ/Fakerate/CombineInput_BRIL/"
    postfitpath = "/groups/hephy/cms/dennis.schwarz/www/tWZ/Fakerate/Fits_BRIL/"
    plotdir = plot_directory+"/FakeRate/PostFit_BRIL/"
    plotdir_maps = plot_directory+"/FakeRate/Maps_data_BRIL/"
    
if args.tunePtCone:
    prefitpath = "/groups/hephy/cms/dennis.schwarz/www/tWZ/Fakerate/CombineInput_tunePtCone/"
    postfitpath = "/groups/hephy/cms/dennis.schwarz/www/tWZ/Fakerate/Fits_tunePtCone/"
    plotdir = plot_directory+"/FakeRate/PostFit_tunePtCone/"
    plotdir_maps = plot_directory+"/FakeRate/Maps_data_tunePtCone/"
    
if args.plotPrefit:
    plotdir = plotdir.replace("PostFit", "PreFit")
    
if not os.path.exists( plotdir ): os.makedirs( plotdir )
if not os.path.exists( plotdir_maps ): os.makedirs( plotdir_maps )


boundaries_pt = [0, 20, 30, 45, 120]
boundaries_eta = [0, 1.2, 2.1, 2.4]
if args.channel == "elec":
    boundaries_eta = [0, 0.8, 1.44, 2.4]
    
FakerateMap_v1 = createMap(boundaries_pt, boundaries_eta, "FakerateMap_v1")
FakerateMap_v1_stat = createMap(boundaries_pt, boundaries_eta, "FakerateMap_v1_stat")
FakerateMap_v1_statrel = createMap(boundaries_pt, boundaries_eta, "FakerateMap_v1_statrel")
FakerateMap_v2 = createMap(boundaries_pt, boundaries_eta, "FakerateMap_v2")
FakerateMap_v2_stat = createMap(boundaries_pt, boundaries_eta, "FakerateMap_v2_stat")
FakerateMap_v2_statrel = createMap(boundaries_pt, boundaries_eta, "FakerateMap_v2_statrel")
FakerateMap_v3 = createMap(boundaries_pt, boundaries_eta, "FakerateMap_v3")
FakerateMap_v3_stat = createMap(boundaries_pt, boundaries_eta, "FakerateMap_v3_stat")
FakerateMap_v3_statrel = createMap(boundaries_pt, boundaries_eta, "FakerateMap_v3_statrel")

allnames = []

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
        h_post_prompt_L = ConvertBinning(h_post_prompt_L, dummy_pre, plotname+"_prompt_LOOSE")
        h_post_prompt_T = ConvertBinning(h_post_prompt_T, dummy_pre, plotname+"_prompt_TIGHT")
        h_post_nonprompt_L = ConvertBinning(h_post_nonprompt_L, dummy_pre, plotname+"_nonprompt_LOOSE")
        h_post_nonprompt_T = ConvertBinning(h_post_nonprompt_T, dummy_pre, plotname+"_nonprompt_TIGHT")
        
        ptstring = "%i < p_{T} < %i GeV" %(boundaries_pt[i], boundaries_pt[i+1])
        etastring = "%.1f < |#eta| < %.1f" %(boundaries_eta[j], boundaries_eta[j+1])
        
        # Loose plots
        allnames.append(plotname+"_LOOSE")
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
        p_L.addText(0.24, 0.7, ptstring, size=14)
        p_L.addText(0.24, 0.65, etastring, size=14)
        p_L.addText(0.24, 0.6, "Loose", size=14)
        p_L.draw()

        # Tight plots 
        allnames.append(plotname+"_TIGHT")
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
        p_T.addText(0.24, 0.7, ptstring, size=14)
        p_T.addText(0.24, 0.65, etastring, size=14)
        p_T.addText(0.24, 0.6, "Tight", size=14)
        p_T.draw()

        # Fakerate maps 
        # Version 1: nonprompt = data - prompt_postfit
        h_nonprompt_data_L = h_pre_data_L.Clone()
        h_nonprompt_data_L.Add(h_post_prompt_L, -1)
        h_nonprompt_data_T = h_pre_data_T.Clone()
        h_nonprompt_data_T.Add(h_post_prompt_T, -1)
        fakerate_v1, fakerate_v1_stat = getRateAndError(h_nonprompt_data_T, h_nonprompt_data_L)
        FakerateMap_v1.SetBinContent(ptbin, etabin, fakerate_v1)
        FakerateMap_v1_stat.SetBinContent(ptbin, etabin, fakerate_v1_stat)
        FakerateMap_v1_statrel.SetBinContent(ptbin, etabin, fakerate_v1_stat/fakerate_v1)

        # Version 2: nonprompt = data - prompt_prefit
        h_nonprompt_data_pre_L = h_pre_data_L.Clone()
        h_nonprompt_data_pre_L.Add(h_pre_prompt_L, -1)
        h_nonprompt_data_pre_T = h_pre_data_T.Clone()
        h_nonprompt_data_pre_T.Add(h_pre_prompt_T, -1)
        fakerate_v2, fakerate_v2_stat = getRateAndError(h_nonprompt_data_pre_T, h_nonprompt_data_pre_L)
        FakerateMap_v2.SetBinContent(ptbin, etabin, fakerate_v2)
        FakerateMap_v2_stat.SetBinContent(ptbin, etabin, fakerate_v2_stat)        
        FakerateMap_v2_statrel.SetBinContent(ptbin, etabin, fakerate_v2_stat/fakerate_v2)
        
        # Version 3: nonprompt = nonprompt_postfit
        h_nonprompt_fit_L = h_post_nonprompt_L.Clone()
        h_nonprompt_fit_T = h_post_nonprompt_T.Clone()
        fakerate_v3, fakerate_v3_stat = getRateAndError(h_nonprompt_fit_T, h_nonprompt_fit_L)
        FakerateMap_v3.SetBinContent(ptbin, etabin, fakerate_v3)
        FakerateMap_v3_stat.SetBinContent(ptbin, etabin, fakerate_v3_stat)     
        FakerateMap_v3_statrel.SetBinContent(ptbin, etabin, fakerate_v3_stat/fakerate_v3)
        
        # Check compatibility of various methods
        d12 = fakerate_v1 - fakerate_v2
        d13 = fakerate_v1 - fakerate_v3
        d23 = fakerate_v2 - fakerate_v3
        if d12 > 0.4 or d13 > 0.4 or d23 > 0.4:
            logger.info("PT%s ETA%s, v1 and v2 not compatible: v1=%s, v2=%s, v3=%s", ptbin, etabin, fakerate_v1, fakerate_v2, fakerate_v3)
                            

        
if not args.plotPrefit:
    drawMap(FakerateMap_v1, year+"__"+channel+"__Map_DATA_v1", plotdir_maps)
    drawMap(FakerateMap_v2, year+"__"+channel+"__Map_DATA_v2", plotdir_maps)
    drawMap(FakerateMap_v3, year+"__"+channel+"__Map_DATA_v3", plotdir_maps)
    drawMap(FakerateMap_v1_stat, year+"__"+channel+"__Map_DATA_v1_stat", plotdir_maps)
    drawMap(FakerateMap_v2_stat, year+"__"+channel+"__Map_DATA_v2_stat", plotdir_maps)
    drawMap(FakerateMap_v3_stat, year+"__"+channel+"__Map_DATA_v3_stat", plotdir_maps)
    drawMap(FakerateMap_v1_statrel, year+"__"+channel+"__Map_DATA_v1_statrel", plotdir_maps)
    drawMap(FakerateMap_v2_statrel, year+"__"+channel+"__Map_DATA_v2_statrel", plotdir_maps)
    drawMap(FakerateMap_v3_statrel, year+"__"+channel+"__Map_DATA_v3_statrel", plotdir_maps)
        
    # 1D projection of the maps
    hists_1D_v3 = make1Dprojection(FakerateMap_v3, FakerateMap_v3_stat, year+"__"+channel+"__Map_DATA_v3", boundaries_pt)
    for etabin in hists_1D_v3:
        etabinint = int(etabin.replace("ETA", ""))-1
        etastring = "%.1f < |#eta| < %.1f" %(boundaries_eta[etabinint], boundaries_eta[etabinint+1])
        p = Plotter(year+"__"+channel+"__Map_DATA_v3_1D_"+etabin)
        p.plot_dir = plotdir_maps
        p.xtitle = "p_{T}^{cone} [GeV]"
        p.ytitle = "Fake rate"
        p.setCustomYRange(0.0, 1.0)
        p.addData(hists_1D_v3[etabin])
        p.addText(0.24, 0.7, etastring, size=14)
        p.draw()
    
    # Store maps in file
    suffix = ""
    if args.prescalemode == "bril":
        suffix = "__BRIL"
    if args.tunePtCone:
        suffix = "__tunePtCone"
    mapfilename = "LeptonFakerate__"+year+"__"+channel+suffix+".root"
    writeObjToFile(mapfilename, FakerateMap_v1, "Fakerate_v1")
    writeObjToFile(mapfilename, FakerateMap_v2, "Fakerate_v2", update=True)
    writeObjToFile(mapfilename, FakerateMap_v3, "Fakerate_v3", update=True)
    writeObjToFile(mapfilename, FakerateMap_v1_stat, "Fakerate_v1_stat", update=True)
    writeObjToFile(mapfilename, FakerateMap_v2_stat, "Fakerate_v2_stat", update=True)
    writeObjToFile(mapfilename, FakerateMap_v3_stat, "Fakerate_v3_stat", update=True)


combinePDFs(allnames, outname, plotdir)
