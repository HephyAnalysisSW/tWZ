#!/usr/bin/env python

import ROOT
import Analysis.Tools.syncer
import os

from math                                        import sqrt
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.histogramHelper                   import WClatexNames
from Plotter_custom                              import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import tWZ.Tools.logger as logger

def getEFTatWCpoint(file, region, histname, wcname, wcvalue):
    sm = getObjFromFile(file, region+"__"+histname+"/sm")
    sm_lin_quad = getObjFromFile(file, region+"__"+histname+"/sm_lin_quad_"+wcname)
    quad = getObjFromFile(file, region+"__"+histname+"/quad_"+wcname)
    # This is the formula:
    # signal = (1 - k)* sm + k* sm_lin_quad + (k^2 - k) quad
    h_eft = sm.Clone(region+"__"+histname+"__"+wcname+"__"+str(wcvalue))
    h_eft.Add(sm, -wcvalue)
    h_eft.Add(sm_lin_quad, wcvalue)
    h_eft.Add(quad, wcvalue*wcvalue-wcvalue)
    return h_eft


logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--noData',           action='store_true', default=False)
args = argParser.parse_args()


dataTag = "_noData" if args.noData else ""
dirname_suffix = "_light_minus_binning-A_SMZero"
combineInput = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_threePoint"+dataTag+dirname_suffix+"/ULRunII/CombineInput.root"

plotdir = plot_directory+"/PaperPlots/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

sys = [
    "muF_ttZ", "muF_WZ", "muF_ZZ",
    "muR_ttZ", "muR_WZ", "muR_ZZ",
]
histname = "Z1_pt"

allWCs = ["cHqMRe1122", "cHqMRe33", "cHq3MRe1122", "cHq3MRe33", "cHuRe1122", "cHuRe33", "cHdRe1122", "cHdRe33", "cW", "cWtil"]
allWCs = []
for region in ["ttZ", "WZ", "ZZ"]:
    signalName = region.replace("ttZ", "t#bar{t}Z")+" (SM)"
    for wc in allWCs+["special"]:
        h_sm = getObjFromFile(combineInput, region+"__"+histname+"/sm")
        wcvalueUp = 1
        wcvalueDown = -1
        if region == "WZ" and wc in ["cHq3Re1122","cHq3MRe1122", "cW", "cWtil"]:
            wcvalueUp = 0.1
            wcvalueDown = -0.1

        eftLines = []
        if wc == "special":
            eftLines.append( (getEFTatWCpoint(combineInput, region, histname, "cHqMRe1122", 1.0), WClatexNames["cHqMRe1122"].replace("/#Lambda^{2} [TeV^{-2}]", "")+" = 1", ROOT.kRed, 1, 2, 3) )
            eftLines.append( (getEFTatWCpoint(combineInput, region, histname, "cHq3MRe1122", 0.1), WClatexNames["cHq3MRe1122"].replace("/#Lambda^{2} [TeV^{-2}]", "")+" = 0.1", ROOT.kGreen+2, 2, 2, 3) )
            eftLines.append( (getEFTatWCpoint(combineInput, region, histname, "cHuRe1122", 1.0), WClatexNames["cHuRe1122"].replace("/#Lambda^{2} [TeV^{-2}]", "")+" = 1", ROOT.kBlack, 7, 2, 3) )
            eftLines.append( (getEFTatWCpoint(combineInput, region, histname, "cHdRe1122", 1.0), WClatexNames["cHdRe1122"].replace("/#Lambda^{2} [TeV^{-2}]", "")+" = 1", ROOT.kPink+6, 5, 2, 3) )
            eftLines.append( (getEFTatWCpoint(combineInput, region, histname, "cHqMRe33", 1.0), WClatexNames["cHqMRe33"].replace("/#Lambda^{2} [TeV^{-2}]", "")+" = 1", ROOT.kBlue, 1, 2, 2) )
            eftLines.append( (getEFTatWCpoint(combineInput, region, histname, "cHq3MRe33", 1.0), WClatexNames["cHq3MRe33"].replace("/#Lambda^{2} [TeV^{-2}]", "")+" = 1", ROOT.kMagenta, 2, 2, 2) )
            eftLines.append( (getEFTatWCpoint(combineInput, region, histname, "cHuRe33", 1.0), WClatexNames["cHuRe33"].replace("/#Lambda^{2} [TeV^{-2}]", "")+" = 1", ROOT.kCyan+2, 7, 2, 2) )
            eftLines.append( (getEFTatWCpoint(combineInput, region, histname, "cHdRe33", 1.0), WClatexNames["cHdRe33"].replace("/#Lambda^{2} [TeV^{-2}]", "")+" = 1", ROOT.kAzure+7, 5, 2, 2) )
            eftLines.append( (getEFTatWCpoint(combineInput, region, histname, "cW", 0.1), WClatexNames["cW"].replace("/#Lambda^{2} [TeV^{-2}]", "")+" = 0.1", ROOT.kViolet+5, 1, 2, 1) )
            eftLines.append( (getEFTatWCpoint(combineInput, region, histname, "cWtil", 0.1), WClatexNames["cWtil"].replace("/#Lambda^{2} [TeV^{-2}]", "")+" = 0.1", ROOT.kOrange+7, 2, 2, 1) )

        else:
            eftLines.append( (getEFTatWCpoint(combineInput, region, histname, wc, wcvalueUp), WClatexNames[wc].replace("/#Lambda^{2} [TeV^{-2}]", "")+" = "+str(wcvalueUp)+"", ROOT.kRed, 2, 2) )
            eftLines.append( (getEFTatWCpoint(combineInput, region, histname, wc, wcvalueDown),  WClatexNames[wc].replace("/#Lambda^{2} [TeV^{-2}]", "")+" = "+str(wcvalueDown)+"", ROOT.kAzure+7, 1, 2) )
        for log in [False, True]:
            suffix = ""
            if log:
                suffix+="_log"
            p = Plotter("EFT_ULRunII__"+region+"__"+histname+"__"+wc+suffix)
            p.plot_dir = plotdir
            p.lumi = "138"
            p.xtitle = "Z boson candidate #it{p}_{T} [GeV]"
            p.ytitle = "Events / GeV"
            p.divideByWidth = True
            p.drawRatio = True
            p.ratiotitle = "#splitline{Ratio}{to SM}"
            p.simtext = "Simulation"
            p.subtext = ""
            p.logoAbovePlot = True
            p.legshift = (-0.05, -0.3, 0.05, 0.0)
            p.legtextsize = 0.05 #0.045
            p.ratiorange = 0.7, 1.7
            p.ratiodivision = 503
            # if region == "ZZ":
            #     p.ratiorange = 0.85, 1.15
            # elif region == "WZ":
            #     p.ratiorange = 0.7, 1.7
            #     p.ratiodivision = 503

            p.NcolumnsLegend = 2
            p.totalUncText = "#mu_{R}/#mu_{F} uncertainties"
            regiontext = "SR"
            if region == "ttZ":
                regiontext+="_{t#bar{t}Z}"
            elif region == "WZ":
                regiontext+="_{WZ}"
            elif region == "ZZ":
                regiontext+="_{ZZ}"
            p.addText(0.25, 0.8, regiontext, font=43, size=20)
            if wc == "special":
                p.addText(0.25, 0.84, "light quark", font=43, size=18, pad=4)
                p.addText(0.25, 0.84, "heavy quark", font=43, size=18, pad=3)
                p.addText(0.25, 0.91, "EW", font=43, size=18, pad=2)

            if log:
                p.log = True
                if region == "WZ":
                    p.setCustomYRange(0.02, 20000)
                elif region == "ZZ":
                    p.setCustomYRange(0.02, 900)
                elif region == "ttZ":
                    p.setCustomYRange(0.02, 300)
            else:
                p.yfactor = 1.4
            p.addBackground(h_sm, signalName, 17)
            for s in sys:
                h_up = getObjFromFile(combineInput, region+"__"+histname+"/sm__"+s+"Up")
                h_down = getObjFromFile(combineInput, region+"__"+histname+"/sm__"+s+"Down")
                p.addSystematic(h_up, h_down, s, signalName)

            for (hist, legtext, col, linestyle, linewidth, ratioPad) in eftLines:
                p.addSignal(hist, legtext, col, lineStyle=linestyle, lineWidth=linewidth, ratioPad=ratioPad)
            # p.addSignal(h_eftUp,   signalName.replace("(SM)", "")+"("+WClatexNames[wc].replace("/#Lambda^{2} [TeV^{-2}]", "")+" = "+str(wcvalueUp)+")", ROOT.kRed, lineStyle=2, lineWidth=2)
            # p.addSignal(h_eftDown, signalName.replace("(SM)", "")+"("+WClatexNames[wc].replace("/#Lambda^{2} [TeV^{-2}]", "")+" = "+str(wcvalueDown)+")", ROOT.kAzure+7, lineWidth=2)
            p.draw()
