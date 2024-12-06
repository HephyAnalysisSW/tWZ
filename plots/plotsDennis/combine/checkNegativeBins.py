import ROOT
import os
import Analysis.Tools.syncer

from tWZ.Tools.helpers import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from MyRootTools.plotter.Plotter                 import Plotter
from tWZ.Tools.CMScolors                         import CMScolors

ROOT.gROOT.SetBatch(ROOT.kTRUE)


# infile = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_threePoint_light_minus_binning-A/ULRunII/CombineInput.root"
infile = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_threePoint_light_minus_binning-A_SMZero/ULRunII/CombineInput.root"
# infile = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_threePoint_light_minus_binning-A_noZero/ULRunII/CombineInput.root"

regions = ["ZZ__Z1_pt", "WZ__Z1_pt", "ttZ__Z1_pt"]
WCnames = ["cHqMRe1122", "cHqMRe33", "cHq3MRe1122", "cHq3MRe33"]

def getLin(sm, sm_lin_quad, quad, WCname):
    lin = sm_lin_quad.Clone("lin_"+WCname)
    lin.Add(sm, -1)
    lin.Add(quad, -1)
    return lin

def getMixed(sm, sm_lin_quad_mixed, lin1, lin2, quad1, quad2, WCname1, WCname2):
    mixed = sm_lin_quad_mixed.Clone("mixed_"+WCname1+"_"+WCname2)
    mixed.Add(sm, -1)
    mixed.Add(lin1, -1)
    mixed.Add(lin2, -1)
    mixed.Add(quad1, -1)
    mixed.Add(quad2, -1)
    return mixed

def getPredictionMixed(sm, lin1, lin2, quad1, quad2, mixed, value1, value2):
    newHist = sm.Clone("_"+str(value1)+"_"+str(value2))
    newHist.Add(lin1, value1)
    newHist.Add(lin2, value2)
    newHist.Add(quad1, value1*value1)
    newHist.Add(quad2, value2*value2)
    newHist.Add(mixed, value1*value2)
    return newHist

def getPredictionMixed_v2(sm, sm_lin_quad1, sm_lin_quad2, quad1, quad2, sm_lin_quad_mixed, value1, value2):
    binNr = 1
    print "-------------------"
    print sm.GetBinError(binNr)
    print sm_lin_quad1.GetBinError(binNr)
    print sm_lin_quad2.GetBinError(binNr)
    print quad1.GetBinError(binNr)
    print quad2.GetBinError(binNr)
    print sm_lin_quad_mixed.GetBinError(binNr)


    newHist = sm.Clone("_"+str(value1)+"_"+str(value2))
    newHist.Reset()
    newHist.Add(sm, 1-(value1+value2)+(value1*value2))
    newHist.Add(sm_lin_quad1, value1-value1*value2)
    newHist.Add(sm_lin_quad2, value2-value1*value2)
    newHist.Add(quad1, value1*value1-value1)
    newHist.Add(quad2, value2*value2-value2)
    newHist.Add(sm_lin_quad_mixed, value1*value2)
    return newHist

def getPrediction(sm, lin, quad, WCvalue):
    newHist = sm.Clone("_"+str(WCvalue))
    newHist.Add(lin, WCvalue)
    newHist.Add(quad, WCvalue*WCvalue)
    return newHist

def checkBins(hist):
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        content = hist.GetBinContent(i+1)
        if content < 0:
            print "ALERT! Bin", i+1, "has negative content", content
        # else:
        #     print content

def compareToSM(hist, sm):
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        percent = 100*(hist.GetBinContent(i+1)-sm.GetBinContent(i+1))/sm.GetBinContent(i+1)
        print "Bin", i+1, "EFT =", hist.GetBinContent(i+1), ", SM =", sm.GetBinContent(i+1), "(",percent," percent)"

for region in regions:
    print "Region", region
    sm = getObjFromFile(infile, region+"/sm")
    for WCname in WCnames:
        sm_lin_quad = getObjFromFile(infile, region+"/sm_lin_quad_"+WCname)
        quad = getObjFromFile(infile, region+"/quad_"+WCname)
        lin = getLin(sm, sm_lin_quad, quad, WCname)
        minVal = -10
        maxVal = 10
        steps = 20
        stepsize = (maxVal-minVal)/steps
        for i in range(steps):
            value = minVal + i*stepsize
            print "  - Scanning", WCname, "=", value, "..."
            hist = getPrediction(sm, lin, quad, value)
            checkBins(hist)


backgrounds = ["ttX", "tZq", "triBoson", "tWZ", "nonprompt", "ggToZZ"]
plotdir = plot_directory+"/EFTeval/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

processinfo = {
    "total_signal":("t#bar{t}Z + WZ + ZZ", CMScolors["sm"]),
    "tWZ":       ("tWZ", CMScolors["tWZ"]),
    "ttX":       ("t#bar{t}X", CMScolors["ttX"]),
    "tZq":       ("tZq", CMScolors["tZq"]),
    "triBoson":  ("Triboson", CMScolors["triboson"]),
    "nonprompt": ("Nonprompt", CMScolors["nonprompt"]),
    "ggToZZ":    ("gg #rightarrow ZZ", CMScolors["ggZZ"]),
}



for region in regions:
    print "Region", region
    sm = getObjFromFile(infile, region+"/sm")
    # (WCname1, WCname2) = ("cHqMRe1122", "cHqMRe33")
    # value1, value2 = -3.4, 9.9
    WCname1, WCname2 = "cHq3MRe1122", "cHq3MRe33"
    value1, value2 = 0.0, 12.0
    sm_lin_quad1 = getObjFromFile(infile, region+"/sm_lin_quad_"+WCname1)
    sm_lin_quad2 = getObjFromFile(infile, region+"/sm_lin_quad_"+WCname2)
    quad1 = getObjFromFile(infile, region+"/quad_"+WCname1)
    quad2 = getObjFromFile(infile, region+"/quad_"+WCname2)
    lin1 = getLin(sm, sm_lin_quad1, quad1, WCname1)
    lin2 = getLin(sm, sm_lin_quad2, quad2, WCname2)
    sm_lin_quad_mixed = getObjFromFile(infile, region+"/sm_lin_quad_mixed_"+WCname1+"_"+WCname2)
    mixed = getMixed(sm, sm_lin_quad_mixed, lin1, lin2, quad1, quad2, WCname1, WCname2)
    hist = getPredictionMixed(sm, lin1, lin2, quad1, quad2, mixed, value1, value2)
    hist_v2 = getPredictionMixed_v2(sm, sm_lin_quad1, sm_lin_quad2, quad1, quad2, sm_lin_quad_mixed, value1, value2)
    compareToSM(hist, sm)
    print "--------------------------"
    compareToSM(hist, hist_v2)


    p_contribs = Plotter(region+"__"+WCname1+"_"+str(value1)+"__"+WCname2+"_"+str(value2)+"__CONTRIBUTIONS")
    p_contribs.plot_dir = plotdir
    p_contribs.lumi = "138"
    p_contribs.xtitle = "Z boson candidate #it{p}_{T} [GeV]"
    p_contribs.drawRatio = True
    p_contribs.ratiorange = (0.2, 1.8)
    # p_contribs.addBackground(sm, "SM",  15)
    p_contribs.addSignal(lin1, "lin1", ROOT.kBlue)
    p_contribs.addSignal(lin2, "lin2", ROOT.kRed)
    p_contribs.addSignal(quad1, "quad1", ROOT.kBlue, 2)
    p_contribs.addSignal(quad2, "quad2", ROOT.kRed, 2)
    p_contribs.addSignal(mixed, "mixed", ROOT.kGreen)
    p_contribs.draw()

    p = Plotter(region+"__"+WCname1+"_"+str(value1)+"__"+WCname2+"_"+str(value2))
    p.plot_dir = plotdir
    p.lumi = "138"
    p.xtitle = "Z boson candidate #it{p}_{T} [GeV]"
    p.drawRatio = True
    p.ratiorange = (0.2, 1.8)
    p.addBackground(hist_v2, processinfo["total_signal"][0],  processinfo["total_signal"][1])
    h_all_SM = sm.Clone("allSM")
    for bkg in backgrounds:
        h_bkg = getObjFromFile(infile, region+"/"+bkg)
        p.addBackground(h_bkg, processinfo[bkg][0],  processinfo[bkg][1])
        h_all_SM.Add(h_bkg)
    p.addSignal(h_all_SM, "SM", 1)
    h_data = getObjFromFile(infile, region+"/data_obs")
    p.addData(h_data)
    p.draw()
