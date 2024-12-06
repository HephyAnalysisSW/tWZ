import ROOT
import os
import Analysis.Tools.syncer
import array

from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from MyRootTools.plotter.Plotter                 import Plotter
from tWZ.Tools.CMScolors                         import CMScolors
from math                                        import sqrt, pow

ROOT.gROOT.SetBatch(ROOT.kTRUE)

def getHist(fname, hname, bins):
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

def getCombinedSignal_EFT(fname, hname, bins, rate=None, rate_process=None, sys_processes=[], fname_sys=None):
    # logger.info( "  get EFT sample: "+hname)
    signals = ["ttZ", "WZ", "ZZ"]
    for i_sig, sig in enumerate(signals):
        # If one of the signals should be varied, use alternative file
        filename = fname
        if sig in sys_processes:
            # logger.info( "    - use variation for "+sig)
            filename = fname_sys
        # If this is the first in the loop clone, otherwise Add to cloned
        if i_sig==0:
            hist = getHist(filename, hname.replace("sm", sig), bins)
            if sig == rate_process:
                # logger.info( "    - scale rate for "+sig)
                hist.Scale(rate)
        else:
            tmp = getHist(filename, hname.replace("sm", sig), bins)
            if sig == rate_process:
                # logger.info( "    - scale rate for "+sig)
                tmp.Scale(rate)
            hist.Add(tmp)
    return hist

def uncertRatio(h1,h2,useRelative):
    h_ratio = h1.Clone(h1.GetName()+"_UncertRatio")
    h_ratio.Reset()
    Nbins = h1.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        if useRelative:
            rel1 = h1.GetBinError(bin)/h1.GetBinContent(bin)
            rel2 = h2.GetBinError(bin)/h2.GetBinContent(bin)
            ratio = rel1/rel2
        else:
            ratio = h1.GetBinError(bin)/h2.GetBinError(bin)
        h_ratio.SetBinContent(bin, ratio)
    return h_ratio



regions = ["ZZ__Z1_pt", "WZ__Z1_pt", "ttZ__Z1_pt"]
CombineInput = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_threePoint_light_minus_binning-A_noZero/ULRunII/CombineInput.root"
plotdir = plot_directory+"/MCstatDATAstat/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

dirs = {
    "ZZ__Z1_pt":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_threePoint_noData/ULRunII/all/qualepT-minDLmass12-onZ1-onZ2/",
    "WZ__Z1_pt":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_threePoint_noData/ULRunII/all/trilepT-minDLmass12-onZ1-btag0-met60/",
    "ttZ__Z1_pt":    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_threePoint_noData/ULRunII/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/",
}

bins_ttZ  = [40, 80, 120, 160, 200, 260, 340, 1000]
bins_WZ  = [40, 60, 80, 100, 120, 140, 180, 220, 260, 300, 340, 380, 420, 500, 1000]
bins_ZZ  = [40, 60, 80, 120, 200, 1000]

for region in regions:
    if "ZZ" in region:
        bins = bins_ZZ
    elif "WZ" in region:
        bins = bins_WZ
    else:
        bins = bins_ttZ

    h_sm_eft = getCombinedSignal_EFT(dirs[region]+"Results.root", "Z1_pt__sm", bins)
    h_sm_eft_point = getCombinedSignal_EFT(dirs[region]+"Results.root", "Z1_pt__sm__cHqMRe1122=1.0000", bins)
    h_sm = getObjFromFile(CombineInput, region+"/sm")
    h_data = getObjFromFile(CombineInput, region+"/data_obs")
    h_ratio = uncertRatio(h_data,h_sm,True)
    h_ratio_eft = uncertRatio(h_data,h_sm_eft,True)
    h_ratio_eft_point = uncertRatio(h_data,h_sm_eft_point,True)

    p = Plotter(region)
    p.plot_dir = plotdir
    p.lumi = "138"
    p.xtitle = "Z boson candidate #it{p}_{T} [GeV]"
    p.ytitle = "Ratio of stat. uncert"
    p.addBackground(h_ratio, "#sigma_{data}/#sigma_{SM MC}", 15)
    p.draw()

    p = Plotter(region+"_EFTsample")
    p.plot_dir = plotdir
    p.lumi = "138"
    p.xtitle = "Z boson candidate #it{p}_{T} [GeV]"
    p.ytitle = "Ratio of stat. uncert"
    p.addBackground(h_ratio_eft, "#sigma_{data}/#sigma_{EFT MC}", 15)
    p.draw()

    p = Plotter(region+"_EFTsample_point")
    p.plot_dir = plotdir
    p.lumi = "138"
    p.xtitle = "Z boson candidate #it{p}_{T} [GeV]"
    p.ytitle = "Ratio of stat. uncert"
    p.addBackground(h_ratio_eft_point, "#sigma_{data}/#sigma_{EFT MC}", 15)
    p.draw()
