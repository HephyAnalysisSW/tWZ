#!/usr/bin/env python

import ROOT
import Analysis.Tools.syncer
import os
import array

from math                                        import sqrt
from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from tWZ.samples.color                           import color
from tWZ.Tools.histogramHelper                   import WClatexNames
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
args = argParser.parse_args()




def getQuadratic(hist_sm, hist_plus, hist_minus):
    # Since the quadratic term does not change sign, we can get it from the
    # histograms where c = +1, c = 0, and c = -1
    # (1) c = +1 is SM + LIN + QUAD
    # (2) c = -1 is SM - LIN + QUAD
    # (3) c =  0 is SM

    # Thus, we can get the quad from
    # (1)+(2) = SM + SM + QUAD + QUAD | -2*(3)
    # (1)+(2)-2*(3) = QUAD + QUAD     | /2
    # 0.5*[(1)+(2)-2*(3)] = QUAD
    hist_quad = hist_plus.Clone(hist_plus.GetName()+"_quad")
    hist_quad.Add(hist_minus)
    hist_quad.Add(hist_sm, -2)
    hist_quad.Scale(0.5)
    return hist_quad

def getHist(fname, hname, altbinning=False):
    bins  = [0, 60, 120, 180, 240, 300, 400, 1000]
    if altbinning:
        bins  = [0, 60, 120, 180, 1000]
    if "ULRunII" in fname:
        # Get histograms from each era
        hist_18 = getObjFromFile(fname.replace("/ULRunII/", "/UL2018/"), hname)
        hist_17 = getObjFromFile(fname.replace("/ULRunII/", "/UL2017/"), hname)
        hist_16 = getObjFromFile(fname.replace("/ULRunII/", "/UL2016/"), hname)
        hist_16preVFP = getObjFromFile(fname.replace("/ULRunII/", "/UL2016preVFP/"), hname)
        # add them
        hist = hist_18.Clone(hist_18.GetName()+"_RunIIcombination")
        hist.Add(hist_17)
        hist.Add(hist_16)
        hist.Add(hist_16preVFP)
    else:
        hist = getObjFromFile(fname, hname)
    hist = hist.Rebin(len(bins)-1, hist.GetName()+"_rebin", array.array('d',bins))
    return hist

# file = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v12_reduceEFT_threePoint_noData/UL2018/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/Results.root"
# hist_sm_comp = getHist(file, "Z1_pt__ttZ", False)

ctZ_file = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_ctZ_v2_threePoint_noData/UL2018/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/Results.root"
hist_sm = getHist(ctZ_file, "Z1_pt__ttZ_ctZ", False)

WCs = [
    "cHq1Re33",
    "cHq3Re33",
    # "cuWRe33",
    # "cuWIm33",
    # "cuBRe33",
    # "cuBIm33",
    "ctZ",
    "ctZI",
    # "ctW",
    # "ctWI",
]

hists_sm_lin_quad = {}
hists_quad = {}


for WC in WCs:
    h_plus = getHist(ctZ_file, "Z1_pt__ttZ_ctZ__"+WC+"=1.0000", False)
    h_minus = getHist(ctZ_file, "Z1_pt__ttZ_ctZ__"+WC+"=-1.0000", False)
    h_quad = getQuadratic(hist_sm, h_plus, h_minus)
    hists_sm_lin_quad[WC] = h_plus.Clone("sm_lin_quad_"+WC)
    hists_quad[WC] = h_quad.Clone("quad_"+WC)

plotdir = plot_directory+"/ctZ/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

# ctZ = -ctWRe cos(theta) + ctBRe sin(theta)
# sin^2(theta) = 0.223
# theta = 0.492
# sin(theta) = 0.472
# cos(theta) = 0.88
costheta = 0.88
sintheta = 0.472


# at cuBRe = 0 -> ctZ = -ctWRe cos(theta) -> 0.3 = ctZ is ctWRe = - 0.34
WCsettings = {
    "cHq1Re33": (-1 , 1, ROOT.kAzure+7),
    "cHq3Re33": (-1 , 1, ROOT.kRed),
    "cuWRe33": (-1 , 1, ROOT.kGreen),
    "cuWIm33": (-1 , 1, ROOT.kBlue),
    "cuBRe33": (-1 , 1, ROOT.kOrange-5),
    "cuBIm33": (-1 , 1, ROOT.kMagenta),
    "ctZ": (-0.3 , 0.3, ROOT.kOrange-3),
    "ctZI": (-0.3 , 0.3, ROOT.kGreen+3),
    "ctW": (-1 , 1, ROOT.kYellow),
    "ctWI": (-1 , 1, ROOT.kMagenta-3),
}

p = Plotter("UL2018__ttZ_ctZ")
p.plot_dir = plotdir
p.lumi = "60"
p.xtitle = "Z #it{p}_{T} [GeV]"
p.drawRatio = True
p.subtext = "Preliminary"
p.legshift = (-0.1, -0.1, 0.0, 0.0)
p.addBackground(hist_sm, "ttZ SM", 13)
for WC in WCs:
    (down, up, color) = WCsettings[WC]
    # N = (1-k)SM + k*(SM+Li+QU) + (k**2 - k)Quad
    h_up = hist_sm.Clone("up")
    h_up.Add(hist_sm, -up)
    h_up.Add(hists_sm_lin_quad[WC], up)
    h_up.Add(hists_quad[WC], up*up - up)
    p.addSignal(h_up, WC+"="+str(up), color)

    h_down = hist_sm.Clone("down")
    h_down.Add(hist_sm, -down)
    h_down.Add(hists_sm_lin_quad[WC], down)
    h_down.Add(hists_quad[WC], (down*down-down) )
    p.addSignal(h_down, WC+"="+str(down), color, 2)

# p.addSignal(hist_sm_comp, "ttZ SM (full)", 1, 2)
p.draw()
