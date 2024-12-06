import ROOT
import os
import Analysis.Tools.syncer

from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from MyRootTools.plotter.Plotter                 import Plotter
from tWZ.Tools.CMScolors                         import CMScolors
from math                                        import sqrt, pow

ROOT.gROOT.SetBatch(ROOT.kTRUE)

def getPrediction(sm, sm_lin_quad, quad, sm_lin_quad_mixed, values, correlation=False):
    WCnames_mixed = {
        "cHqMRe1122_cHqMRe33"    :["cHqMRe1122", "cHqMRe33"],
        "cHqMRe1122_cHq3MRe1122" :["cHqMRe1122", "cHq3MRe1122"],
        "cHqMRe1122_cHq3MRe33"   :["cHqMRe1122", "cHq3MRe33"],
        "cHqMRe33_cHq3MRe1122"   :["cHqMRe33", "cHq3MRe1122"],
        "cHqMRe33_cHq3MRe33"     :["cHqMRe33", "cHq3MRe33"],
        "cHq3MRe1122_cHq3MRe33"  :["cHq3MRe1122", "cHq3MRe33"],
    }

    WCnames = values.keys()

    # print "--------------"

    # SM factor
    f_sm = 1.
    for WC in WCnames:
        f_sm += -values[WC]
    for i,WC1 in enumerate(WCnames):
        for j,WC2 in enumerate(WCnames):
            if i<j:
                f_sm += values[WC1]*values[WC2]
    # sm_lin_quad
    f_smlinquad = {}
    for i,WC1 in enumerate(WCnames):
        f_smlinquad[WC1] = values[WC1]
        for j,WC2 in enumerate(WCnames):
            if i != j:
                f_smlinquad[WC1] += -values[WC1]*values[WC2]
    # quad
    f_quad = {}
    for i,WC in enumerate(WCnames):
        f_quad[WC] = values[WC]*values[WC] - values[WC]
    # mixed
    f_mixed = {}
    for i,WC1 in enumerate(WCnames):
        for j,WC2 in enumerate(WCnames):
            if i != j:
                foundMixed = False
                mixname = ""
                for mixedTerms in WCnames_mixed.keys():
                    if WC1 == WCnames_mixed[mixedTerms][0] and WC2 == WCnames_mixed[mixedTerms][1]:
                        foundMixed = True
                        mixname = mixedTerms
                if foundMixed:
                    f_mixed[mixname] = values[WC1]*values[WC2]


    newHist = sm.Clone(sm.GetName()+"_EFT")
    newHist.Reset()
    Nbins = sm.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        content = f_sm*sm.GetBinContent(bin)
        for WC in WCnames:
            content += f_smlinquad[WC]*sm_lin_quad[WC].GetBinContent(bin)
            content += f_quad[WC]*quad[WC].GetBinContent(bin)
        for mixname in WCnames_mixed.keys():
            content += f_mixed[mixname]*sm_lin_quad_mixed[mixname].GetBinContent(bin)
        newHist.SetBinContent(bin, content)
        error = 0
        if correlation:
            # print "Fully correlated"
            error = f_sm*sm.GetBinError(bin)
            for WC in WCnames:
                error += f_smlinquad[WC]*sm_lin_quad[WC].GetBinError(bin)
                error += f_quad[WC]*quad[WC].GetBinError(bin)
            for mixname in WCnames_mixed.keys():
                error += f_mixed[mixname]*sm_lin_quad_mixed[mixname].GetBinError(bin)
            error = abs(error)
        else:
            # print "Not correlated"
            err2 = pow(f_sm*sm.GetBinError(bin), 2)
            for WC in WCnames:
                err2 += pow(f_smlinquad[WC]*sm_lin_quad[WC].GetBinError(bin), 2)
                err2 += pow(f_quad[WC]*quad[WC].GetBinError(bin), 2)
            for mixname in WCnames_mixed.keys():
                err2 += pow(f_mixed[mixname]*sm_lin_quad_mixed[mixname].GetBinError(bin), 2)
            error = sqrt(err2)
        newHist.SetBinError(bin, error)
    return newHist



backgrounds = ["ttX", "tZq", "triBoson", "tWZ", "nonprompt", "ggToZZ"]
plotdir = plot_directory+"/EFT_correlationTest/"
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



WCvalues = {
    "cHqMRe1122": -1.0,
    "cHqMRe33": 10.0,
    "cHq3MRe1122": 0.0,
    "cHq3MRe33": 0.0,
}

WCnames_mixed = {
    "cHqMRe1122_cHqMRe33"    :["cHqMRe1122", "cHqMRe33"],
    "cHqMRe1122_cHq3MRe1122" :["cHqMRe1122", "cHq3MRe1122"],
    "cHqMRe1122_cHq3MRe33"   :["cHqMRe1122", "cHq3MRe33"],
    "cHqMRe33_cHq3MRe1122"   :["cHqMRe33", "cHq3MRe1122"],
    "cHqMRe33_cHq3MRe33"     :["cHqMRe33", "cHq3MRe33"],
    "cHq3MRe1122_cHq3MRe33"  :["cHq3MRe1122", "cHq3MRe33"],
}

sm_lin_quad = {}
quad = {}
mixed = {}

regions = ["ZZ__Z1_pt", "WZ__Z1_pt", "ttZ__Z1_pt"]


for mode in ["noErr", "correlated", "noCorrelation"]:
    if mode == "noErr":
        infile = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_threePoint_light_minus_binning-A_SMZero/ULRunII/CombineInput.root"
    else:
        infile = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_threePoint_light_minus_binning-A_noZero/ULRunII/CombineInput.root"
    correlation = True if mode=="correlated" else False

    for region in regions:
        print "Region", region
        sm = getObjFromFile(infile, region+"/sm")

        for WCname in WCvalues.keys():
            sm_lin_quad[WCname] = getObjFromFile(infile, region+"/sm_lin_quad_"+WCname)
            quad[WCname] = getObjFromFile(infile, region+"/quad_"+WCname)

        for mixName in WCnames_mixed:
            mixed[mixName] = getObjFromFile(infile, region+"/sm_lin_quad_mixed_"+mixName)


        h_eft = getPrediction(sm, sm_lin_quad, quad, mixed, WCvalues, correlation=correlation)

        for SMEFT in ["SM", "EFT"]:
            p = Plotter(region+"_"+SMEFT+"_"+mode)
            p.plot_dir = plotdir
            p.lumi = "138"
            p.xtitle = "Z boson candidate #it{p}_{T} [GeV]"
            p.drawRatio = True
            p.ratiorange = (0.2, 1.8)
            h_bkg_all = ROOT.TH1F()
            firstbkg = True
            for bkg in backgrounds:
                h_bkg = getObjFromFile(infile, region+"/"+bkg)
                p.addBackground(h_bkg, processinfo[bkg][0],  processinfo[bkg][1])
                if firstbkg:
                    firstbkg = False
                    h_bkg_all = h_bkg.Clone()
                else:
                    h_bkg_all.Add(h_bkg)

            if SMEFT == "SM":
                p.addBackground(sm, processinfo["total_signal"][0],  processinfo["total_signal"][1])
                p.addText(0.22, 0.7, "SM", font=43, size=16)
            elif SMEFT == "EFT":
                p.addBackground(h_eft, processinfo["total_signal"][0],  processinfo["total_signal"][1])
                yPos = 0.7
                for WCname in ["cHqMRe1122","cHqMRe33","cHq3MRe1122","cHq3MRe33"]:
                    text = WCname+"=%.2f"%(WCvalues[WCname])
                    p.addText(0.22, yPos, text, font=43, size=16)
                    yPos += -0.05
            h_data = getObjFromFile(infile, region+"/data_obs")
            p.addData(h_data)
            p.draw()
