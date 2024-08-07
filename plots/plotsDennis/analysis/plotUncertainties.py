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
    return (up, down)


# histname
histname = "Z1_pt"

version = "v14"
logger.info( "Version = %s", version )

# Directories
dirs = {
    "ZZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint_noData/"+args.year+"/all/qualepT-minDLmass12-onZ1-onZ2/",
    "WZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint_noData/"+args.year+"/all/trilepT-minDLmass12-onZ1-btag0-met60/",
    "ttZ":    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint_noData/"+args.year+"/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/",
    "WZ_CR":  "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_FakeRateSF_useDataSF/"+args.year+"/all/trilepFOnoT-minDLmass12-onZ1-btag0-met60/",
    "ttZ_CR": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_FakeRateSF_useDataSF/"+args.year+"/all/trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p/",
}

regions = ["ttZ", "WZ", "ZZ"]
processes = {
    "ttZ": "ttZ_sm",
    "WZ": "WZTo3LNu", #WZTo3LNu_powheg
    "ZZ": "ZZ_powheg"
}

# processes = {
#     "ttZ": "ttZ",
#     "WZ": "WZ",
#     "ZZ": "ZZ"
# }

lumi = {
    "UL2016preVFP": "19.5",
    "UL2016":       "16.5",
    "UL2017":       "41.5",
    "UL2018":       "60",
    "ULRunII":      "138",
}

colors = {
    "ttZ": ROOT.kAzure+4,
    "ttZ_sm": ROOT.kAzure+4,
    "WZ": ROOT.kAzure+6,
    "WZTo3LNu_powheg": ROOT.kAzure+6,
    "WZTo3LNu": ROOT.kAzure+6,
    "ZZ": ROOT.kGreen+3,
    "ZZ_powheg": ROOT.kGreen+3,
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
    "Trigger_2016preVFP":             ("Trigger_2016preVFP_UP", "Trigger_2016preVFP_DOWN"),
    "Trigger_2016":                   ("Trigger_2016_UP", "Trigger_2016_DOWN"),
    "Trigger_2017":                   ("Trigger_2017_UP", "Trigger_2017_DOWN"),
    "Trigger_2018":                   ("Trigger_2018_UP", "Trigger_2018_DOWN"),
    "Prefire":                        ("Prefire_UP", "Prefire_DOWN"),
    "LepReco":                        ("LepReco_UP", "LepReco_DOWN"),
    "LepIDstat_elec_2016preVFP":      ("LepIDstat_elec_2016preVFP_UP", "LepIDstat_elec_2016preVFP_DOWN"),
    "LepIDstat_elec_2016":            ("LepIDstat_elec_2016_UP", "LepIDstat_elec_2016_DOWN"),
    "LepIDstat_elec_2017":            ("LepIDstat_elec_2017_UP", "LepIDstat_elec_2017_DOWN"),
    "LepIDstat_elec_2018":            ("LepIDstat_elec_2018_UP", "LepIDstat_elec_2018_DOWN"),
    "LepIDsys_elec":                  ("LepIDsys_elec_UP", "LepIDsys_elec_DOWN"),
    "LepIDstat_muon_2016preVFP":      ("LepIDstat_muon_2016preVFP_UP", "LepIDstat_muon_2016preVFP_DOWN"),
    "LepIDstat_muon_2016":            ("LepIDstat_muon_2016_UP", "LepIDstat_muon_2016_DOWN"),
    "LepIDstat_muon_2017":            ("LepIDstat_muon_2017_UP", "LepIDstat_muon_2017_DOWN"),
    "LepIDstat_muon_2018":            ("LepIDstat_muon_2018_UP", "LepIDstat_muon_2018_DOWN"),
    "LepIDsys_muon":                  ("LepIDsys_muon_UP", "LepIDsys_muon_DOWN"),
    "PU":                             ("PU_UP", "PU_DOWN"),
    # "JES":                            ("JES_UP", "JES_DOWN"),
    "JES_AbsoluteMPFBias":            ("AbsoluteMPFBias_UP", "AbsoluteMPFBias_DOWN"),
    "JES_AbsoluteScale":              ("AbsoluteScale_UP", "AbsoluteScale_DOWN"),
    "JES_AbsoluteStat_2016preVFP":    ("AbsoluteStat_2016preVFP_UP", "AbsoluteStat_2016preVFP_DOWN"),
    "JES_AbsoluteStat_2016":          ("AbsoluteStat_2016_UP", "AbsoluteStat_2016_DOWN"),
    "JES_AbsoluteStat_2017":          ("AbsoluteStat_2017_UP", "AbsoluteStat_2017_DOWN"),
    "JES_AbsoluteStat_2018":          ("AbsoluteStat_2018_UP", "AbsoluteStat_2018_DOWN"),
    "JES_RelativeBal":                ("RelativeBal_UP", "RelativeBal_DOWN"),
    "JES_RelativeFSR":                ("RelativeFSR_UP", "RelativeFSR_DOWN"),
    "JES_RelativeJEREC1_2016preVFP":  ("RelativeJEREC1_2016preVFP_UP", "RelativeJEREC1_2016preVFP_DOWN"),
    "JES_RelativeJEREC1_2016":        ("RelativeJEREC1_2016_UP", "RelativeJEREC1_2016_DOWN"),
    "JES_RelativeJEREC1_2017":        ("RelativeJEREC1_2017_UP", "RelativeJEREC1_2017_DOWN"),
    "JES_RelativeJEREC1_2018":        ("RelativeJEREC1_2018_UP", "RelativeJEREC1_2018_DOWN"),
    "JES_RelativeJEREC2_2016preVFP":  ("RelativeJEREC2_2016preVFP_UP", "RelativeJEREC2_2016preVFP_DOWN"),
    "JES_RelativeJEREC2_2016":        ("RelativeJEREC2_2016_UP", "RelativeJEREC2_2016_DOWN"),
    "JES_RelativeJEREC2_2017":        ("RelativeJEREC2_2017_UP", "RelativeJEREC2_2017_DOWN"),
    "JES_RelativeJEREC2_2018":        ("RelativeJEREC2_2018_UP", "RelativeJEREC2_2018_DOWN"),
    "JES_RelativeJERHF":              ("RelativeJERHF_UP", "RelativeJERHF_DOWN"),
    "JES_RelativePtBB":               ("RelativePtBB_UP", "RelativePtBB_DOWN"),
    "JES_RelativePtEC1_2016preVFP":   ("RelativePtEC1_2016preVFP_UP", "RelativePtEC1_2016preVFP_DOWN"),
    "JES_RelativePtEC1_2016":         ("RelativePtEC1_2016_UP", "RelativePtEC1_2016_DOWN"),
    "JES_RelativePtEC1_2017":         ("RelativePtEC1_2017_UP", "RelativePtEC1_2017_DOWN"),
    "JES_RelativePtEC1_2018":         ("RelativePtEC1_2018_UP", "RelativePtEC1_2018_DOWN"),
    "JES_RelativePtEC2_2016preVFP":   ("RelativePtEC2_2016preVFP_UP", "RelativePtEC2_2016preVFP_DOWN"),
    "JES_RelativePtEC2_2016":         ("RelativePtEC2_2016_UP", "RelativePtEC2_2016_DOWN"),
    "JES_RelativePtEC2_2017":         ("RelativePtEC2_2017_UP", "RelativePtEC2_2017_DOWN"),
    "JES_RelativePtEC2_2018":         ("RelativePtEC2_2018_UP", "RelativePtEC2_2018_DOWN"),
    "JES_RelativePtHF":               ("RelativePtHF_UP", "RelativePtHF_DOWN"),
    "JES_RelativeStatEC_2016preVFP":  ("RelativeStatEC_2016preVFP_UP", "RelativeStatEC_2016preVFP_DOWN"),
    "JES_RelativeStatEC_2016":        ("RelativeStatEC_2016_UP", "RelativeStatEC_2016_DOWN"),
    "JES_RelativeStatEC_2017":        ("RelativeStatEC_2017_UP", "RelativeStatEC_2017_DOWN"),
    "JES_RelativeStatEC_2018":        ("RelativeStatEC_2018_UP", "RelativeStatEC_2018_DOWN"),
    "JES_RelativeStatFSR_2016preVFP": ("RelativeStatFSR_2016preVFP_UP", "RelativeStatFSR_2016preVFP_DOWN"),
    "JES_RelativeStatFSR_2016":       ("RelativeStatFSR_2016_UP", "RelativeStatFSR_2016_DOWN"),
    "JES_RelativeStatFSR_2017":       ("RelativeStatFSR_2017_UP", "RelativeStatFSR_2017_DOWN"),
    "JES_RelativeStatFSR_2018":       ("RelativeStatFSR_2018_UP", "RelativeStatFSR_2018_DOWN"),
    "JES_RelativeStatHF_2016preVFP":  ("RelativeStatHF_2016preVFP_UP", "RelativeStatHF_2016preVFP_DOWN"),
    "JES_RelativeStatHF_2016":        ("RelativeStatHF_2016_UP", "RelativeStatHF_2016_DOWN"),
    "JES_RelativeStatHF_2017":        ("RelativeStatHF_2017_UP", "RelativeStatHF_2017_DOWN"),
    "JES_RelativeStatHF_2018":        ("RelativeStatHF_2018_UP", "RelativeStatHF_2018_DOWN"),
    "JES_RelativeSample_2016preVFP":  ("RelativeSample_2016preVFP_UP", "RelativeSample_2016preVFP_DOWN"),
    "JES_RelativeSample_2016":        ("RelativeSample_2016_UP", "RelativeSample_2016_DOWN"),
    "JES_RelativeSample_2017":        ("RelativeSample_2017_UP", "RelativeSample_2017_DOWN"),
    "JES_RelativeSample_2018":        ("RelativeSample_2018_UP", "RelativeSample_2018_DOWN"),
    "JES_PileUpDataMC":               ("PileUpDataMC_UP", "PileUpDataMC_DOWN"),
    "JES_PileUpPtBB":                 ("PileUpPtBB_UP", "PileUpPtBB_DOWN"),
    "JES_PileUpPtEC1":                ("PileUpPtEC1_UP", "PileUpPtEC1_DOWN"),
    "JES_PileUpPtEC2":                ("PileUpPtEC2_UP", "PileUpPtEC2_DOWN"),
    "JES_PileUpPtHF":                 ("PileUpPtHF_UP", "PileUpPtHF_DOWN"),
    "JES_PileUpPtRef":                ("PileUpPtRef_UP", "PileUpPtRef_DOWN"),
    "JES_FlavorQCD":                  ("FlavorQCD_UP", "FlavorQCD_DOWN"),
    "JES_Fragmentation":              ("Fragmentation_UP", "Fragmentation_DOWN"),
    "JES_SinglePionECAL":             ("SinglePionECAL_UP", "SinglePionECAL_DOWN"),
    "JES_SinglePionHCAL":             ("SinglePionHCAL_UP", "SinglePionHCAL_DOWN"),
    "JES_TimePtEta_2016preVFP":       ("TimePtEta_2016preVFP_UP", "TimePtEta_2016preVFP_DOWN"),
    "JES_TimePtEta_2016":             ("TimePtEta_2016_UP", "TimePtEta_2016_DOWN"),
    "JES_TimePtEta_2017":             ("TimePtEta_2017_UP", "TimePtEta_2017_DOWN"),
    "JES_TimePtEta_2018":             ("TimePtEta_2018_UP", "TimePtEta_2018_DOWN"),
    "JER_2016preVFP":                 ("JER_2016preVFP_UP", "JER_2016preVFP_DOWN"),
    "JER_2016":                       ("JER_2016_UP", "JER_2016_DOWN"),
    "JER_2017":                       ("JER_2017_UP", "JER_2017_DOWN"),
    "JER_2018":                       ("JER_2018_UP", "JER_2018_DOWN"),
    "Unclustered_2016preVFP":         ("Unclustered_2016preVFP_UP", "Unclustered_2016preVFP_DOWN"),
    "Unclustered_2016":               ("Unclustered_2016_UP", "Unclustered_2016_DOWN"),
    "Unclustered_2017":               ("Unclustered_2017_UP", "Unclustered_2017_DOWN"),
    "Unclustered_2018":               ("Unclustered_2018_UP", "Unclustered_2018_DOWN"),
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
    process = processes[region] # only plot ttZ in ttZ region, WZ in WZ region and ZZ in ZZ region
    for sys in sysnames.keys():
        # if sys in ["muR", "muF"]:
        #     print "SKIPPING", sys, region
        #     continue

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
