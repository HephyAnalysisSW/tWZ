#!/usr/bin/env python

import ROOT
import array
import Analysis.Tools.syncer

from math                                        import sqrt
from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
args = argParser.parse_args()


def getRMS(nominal, variations):
    up   = nominal.Clone()
    down = nominal.Clone()
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        diff_sum2_up = 0
        diff_sum2_down = 0
        Nvars_up = 0
        Nvars_down = 0
        for var in variations:
            diff = var.GetBinContent(bin)-nominal.GetBinContent(bin)
            if diff > 0:
                diff_sum2_up += diff*diff
                # diff_sum2_up += var.GetBinContent(bin)*var.GetBinContent(bin)
                Nvars_up += 1
            else:
                diff_sum2_down += diff*diff
                # diff_sum2_down += var.GetBinContent(bin)*var.GetBinContent(bin)
                Nvars_down += 1
        rmsup = sqrt(diff_sum2_up/Nvars_up) if Nvars_up > 0 else 0
        rmsdown = sqrt(diff_sum2_down/Nvars_down) if Nvars_down > 0 else 0
        up.SetBinContent(bin, nominal.GetBinContent(bin)+rmsup)
        down.SetBinContent(bin, nominal.GetBinContent(bin)-rmsdown)
        # up.SetBinContent(bin, rmsup)
        # down.SetBinContent(bin, rmsdown)
    return (up, down)


# histname
histname = "Z1_pt"

version = "v9"
logger.info( "Version = %s", version )

# Directories
dirs = {
    "ZZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_noData/"+args.year+"/all/qualepT-minDLmass12-onZ1-onZ2/",
    "WZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_noData/"+args.year+"/all/trilepT-minDLmass12-onZ1-btag0-met60/",
    "ttZ":    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_noData/"+args.year+"/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/",
    "WZ_CR":  "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_FakeRateSF_useDataSF/"+args.year+"/all/trilepFOnoT-minDLmass12-onZ1-btag0-met60/",
    "ttZ_CR": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_FakeRateSF_useDataSF/"+args.year+"/all/trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p/",
}

regions = ["ttZ", "WZ", "ZZ"]
lumi = {
    "UL2016preVFP": "19.5",
    "UL2016":       "16.5",
    "UL2017":       "41.5",
    "UL2018":       "60",
    "ULRunII":      "138",
}

colors = {
    "ttZ": ROOT.kAzure+4,
    "WZ": ROOT.kAzure+6,
    "ZZ": ROOT.kGreen+3,
}

sysnames = {
    "BTag_b_correlated":              ("BTag_b_correlated_UP", "BTag_b_correlated_DOWN"),
    "BTag_l_correlated":              ("BTag_l_correlated_UP", "BTag_l_correlated_DOWN"),
    "BTag_b_uncorrelated_2016preVFP": ("BTag_b_uncorrelated_2016preVFP_UP", "BTag_b_uncorrelated_2016preVFP_DOWN"),
    "BTag_l_uncorrelated_2016preVFP": ("BTag_l_uncorrelated_2016preVFP_UP", "BTag_l_uncorrelated_2016preVFP_DOWN"),
    "BTag_b_uncorrelated_2016":       ("BTag_b_uncorrelated_2016_UP", "BTag_b_uncorrelated_2016_DOWN"),
    "BTag_l_uncorrelated_2016":       ("BTag_l_uncorrelated_2016_UP", "BTag_l_uncorrelated_2016_DOWN"),
    "BTag_b_uncorrelated_2017":       ("BTag_b_uncorrelated_2017_UP", "BTag_b_uncorrelated_2017_DOWN"),
    "BTag_l_uncorrelated_2017":       ("BTag_l_uncorrelated_2017_UP", "BTag_l_uncorrelated_2017_DOWN"),
    "BTag_b_uncorrelated_2018":       ("BTag_b_uncorrelated_2018_UP", "BTag_b_uncorrelated_2018_DOWN"),
    "BTag_l_uncorrelated_2018":       ("BTag_l_uncorrelated_2018_UP", "BTag_l_uncorrelated_2018_DOWN"),
    # "Fakerate":                       ("Fakerate_UP", "Fakerate_DOWN"), # TREAT DIFFERENTLY
    "Trigger":                        ("Trigger_UP", "Trigger_DOWN"),
    "Prefire":                        ("Prefire_UP", "Prefire_DOWN"),
    "LepReco":                        ("LepReco_UP", "LepReco_DOWN"),
    "LepIDstat_2016preVFP":           ("LepIDstat_2016preVFP_UP", "LepIDstat_2016preVFP_DOWN"),
    "LepIDstat_2016":                 ("LepIDstat_2016_UP", "LepIDstat_2016_DOWN"),
    "LepIDstat_2017":                 ("LepIDstat_2017_UP", "LepIDstat_2017_DOWN"),
    "LepIDstat_2018":                 ("LepIDstat_2018_UP", "LepIDstat_2018_DOWN"),
    "LepIDsys":                       ("LepIDsys_UP", "LepIDsys_DOWN"),
    "PU":                             ("PU_UP", "PU_DOWN"),
    "JES":                            ("JES_UP", "JES_DOWN"),
    "JER":                            ("JER_UP", "JER_DOWN"),
    "Lumi_uncorrelated_2016":         ("Lumi_uncorrelated_2016_UP", "Lumi_uncorrelated_2016_DOWN"),
    "Lumi_uncorrelated_2017":         ("Lumi_uncorrelated_2017_UP", "Lumi_uncorrelated_2017_DOWN"),
    "Lumi_uncorrelated_2018":         ("Lumi_uncorrelated_2018_UP", "Lumi_uncorrelated_2018_DOWN"),
    "Lumi_correlated_161718":         ("Lumi_correlated_161718_UP", "Lumi_correlated_161718_DOWN"),
    "Lumi_correlated_1718":           ("Lumi_correlated_1718_UP", "Lumi_correlated_1718_DOWN"),
    "ISR":                            ("ISR_UP", "ISR_DOWN"),
    "FSR":                            ("FSR_UP", "FSR_DOWN"),
    "muR":                            ("Scale_UPNONE", "Scale_DOWNNONE"), # muR
    "muF":                            ("Scale_NONEUP", "Scale_NONEDOWN"), # muF
    "PDF":                            (), # TREAT DIFFERENTLY
}

for region in regions:
    process = region # only plot ttZ in ttZ region, WZ in WZ region and ZZ in ZZ region
    for sys in sysnames.keys():
        p = Plotter(region+"__"+process+"__"+sys)
        p.plot_dir = plot_directory+"/Uncertainties/"+args.year+"/"
        p.lumi = lumi[args.year]
        p.addText(0.4, 0.55, args.year, size=16)
        p.addText(0.4, 0.5, sys, size=16)
        p.xtitle = "Z p_{T} [GeV]"
        p.drawRatio = True
        p.ratiorange = (0.85, 1.15)
        hist = getObjFromFile(dirs[region]+"Results.root", histname+"__"+process)
        p.addBackground(hist, process, colors[process])
        if sys == "PDF":
            pdfvariations = []
            for i in range(100):
                pdfdir = dirs[region].replace('/Run', '_PDF_'+str(i+1)+'/Run').replace('/UL', '_PDF_'+str(i+1)+'/UL')
                h_pdf = getObjFromFile(pdfdir+"Results.root", histname+"__"+process)
                pdfvariations.append(h_pdf)
            histUP, histDOWN = getRMS(hist, pdfvariations)
            p_pdf = Plotter(region+"__"+process+"__"+sys+"__allVariations")
            p_pdf.plot_dir = plot_directory+"/Uncertainties/"+args.year+"/"
            p_pdf.lumi = lumi[args.year]
            p_pdf.xtitle = "Z p_{T} [GeV]"
            p_pdf.drawRatio = True
            p_pdf.ratiorange = (0.85, 1.15)
            p_pdf.addBackground(hist, process, colors[process])
            for i, h in enumerate(pdfvariations):
                p_pdf.addSignal(h, "pdf"+str(i), 29+i)
            p_pdf.draw()
        else:
            upname, downname = sysnames[sys]
            sysdirUP = dirs[region].replace('/Run', '_'+upname+'/Run').replace('/UL', '_'+upname+'/UL')
            sysdirDOWN = dirs[region].replace('/Run', '_'+downname+'/Run').replace('/UL', '_'+downname+'/UL')
            histUP   = getObjFromFile(sysdirUP+"Results.root", histname+"__"+process)
            histDOWN = getObjFromFile(sysdirDOWN+"Results.root", histname+"__"+process)
        p.addSignal(histUP, "up", ROOT.kAzure+7)
        p.addSignal(histDOWN, "down", ROOT.kRed-4)
        p.draw()
