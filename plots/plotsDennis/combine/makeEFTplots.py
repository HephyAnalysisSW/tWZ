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
colors = {
    "cHqMRe1122": ROOT.kRed,
    "cHqMRe33":   ROOT.kOrange-3,
    "cHq3MRe1122":ROOT.kBlue,
    "cHq3MRe33":  ROOT.kAzure+7
}

def getPrediction(sm, sm_lin_quad1, quad1, value1, sm_lin_quad2=None, quad2=None, value2=None, sm_lin_quad_mixed=None):
    doOneDonly = False
    none_count = ([sm_lin_quad2, quad2, value2, sm_lin_quad_mixed]).count(None)
    if none_count == 4:
        print "Only 1 WC provided"
        value2 = 0
        doOneDonly = True
    elif none_count == 0:
        print "2 WCs provided"
    else:
        print "Check inputs to getPrediction again"

    newHist = sm.Clone("_"+str(value1)+"_"+str(value2))
    newHist.Reset()
    newHist.Add(sm, 1-(value1+value2)+(value1*value2))
    newHist.Add(sm_lin_quad1, value1-value1*value2)
    newHist.Add(quad1, value1*value1-value1)
    if not doOneDonly:
        newHist.Add(sm_lin_quad2, value2-value1*value2)
        newHist.Add(quad2, value2*value2-value2)
        newHist.Add(sm_lin_quad_mixed, value1*value2)
    return newHist


backgrounds = ["ttX", "tZq", "triBoson", "tWZ", "nonprompt", "ggToZZ"]
plotdir = plot_directory+"/EFTplots_new/"
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
    h_sm = getObjFromFile(infile, region+"/sm")
    p = Plotter(region)
    p.plot_dir = plotdir
    p.lumi = "138"
    p.xtitle = "Z boson candidate #it{p}_{T} [GeV]"
    p.drawRatio = True
    p.ratiorange = (0.2, 1.8)
    p.addBackground(h_sm, processinfo["total_signal"][0],  processinfo["total_signal"][1])
    h_all_bkgs = ROOT.TH1F()
    first_bkg = True
    for bkg in backgrounds:
        h_bkg = getObjFromFile(infile, region+"/"+bkg)
        p.addBackground(h_bkg, processinfo[bkg][0],  processinfo[bkg][1])
        if first_bkg:
            first_bkg = False
            h_all_bkgs = h_bkg.Clone("allBKG_"+region)
        else:
            h_all_bkgs.Add(h_bkg)

    for wc in WCnames:
        values = [-1, 1]
        for val in values:
            sm_lin_quad1 = getObjFromFile(infile, region+"/sm_lin_quad_"+wc)
            quad1 = getObjFromFile(infile, region+"/quad_"+wc)
            h_eft = getPrediction(h_sm, sm_lin_quad1, quad1, val)
            h_eft.Add(h_all_bkgs)
            linestyle = 1 if val > 0 else 2
            p.addSignal(h_eft, wc+"=%i"%(val), colors[wc], linestyle)
    h_data = getObjFromFile(infile, region+"/data_obs")
    p.addData(h_data)
    p.draw()
