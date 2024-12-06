import ROOT
import os
import Analysis.Tools.syncer

from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from MyRootTools.plotter.Plotter                 import Plotter
from tWZ.Tools.CMScolors                         import CMScolors
from math                                        import sqrt, pow

ROOT.gROOT.SetBatch(ROOT.kTRUE)

def getPrediction(sm, sm_lin_quad, quad, sm_lin_quad_mixed, values):
    newHist = sm.Clone(sm.GetName()+"_EFT")

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
    newHist.Scale(f_sm)
    # sm_lin_quad
    for i,WC1 in enumerate(WCnames):
        f_smlinquad = values[WC1]
        for j,WC2 in enumerate(WCnames):
            if i != j:
                f_smlinquad += -values[WC1]*values[WC2]
        newHist.Add(sm_lin_quad[WC1],f_smlinquad)
    # quad
    for i,WC in enumerate(WCnames):
        f_quad = values[WC]*values[WC] - values[WC]
        newHist.Add(quad[WC1],f_quad)

    # mixed
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
                    f_mixed = values[WC1]*values[WC2]
                    newHist.Add(sm_lin_quad_mixed[mixname],f_mixed)
    return newHist



backgrounds = ["ttX", "tZq", "triBoson", "tWZ", "nonprompt", "ggToZZ"]
plotdir = plot_directory+"/EFT_uncertainties/"
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

sm_lin_quad_up = {}
quad_up = {}
mixed_up = {}

sm_lin_quad_down = {}
quad_down = {}
mixed_down = {}

regions = ["ZZ__Z1_pt", "WZ__Z1_pt", "ttZ__Z1_pt"]

uncerts = [
    "ISR_WZ", "ISR_ttZ", "ISR_ZZ",
    "muR_WZ", "muR_ttZ", "muR_ZZ",
    "muF_WZ", "muF_ttZ", "muF_ZZ",
    "EWK_mul_ZZ" ,"EWK_mul_WZ","EWK_add_ZZ","EWK_add_WZ",
    # "WZ_Njet_reweight","WZ_heavyFlavour",
]

infile = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_threePoint_light_minus_binning-A_SMZero/ULRunII/CombineInput.root"
for uncert in uncerts:
    for region in regions:
        print "Region", region
        sm = getObjFromFile(infile, region+"/sm")
        sm_up = getObjFromFile(infile, region+"/sm__"+uncert+"Up")
        sm_down = getObjFromFile(infile, region+"/sm__"+uncert+"Down")

        p_smOnly = Plotter(region+"_smOnly_"+uncert)
        p_smOnly.plot_dir = plotdir
        p_smOnly.lumi = "138"
        p_smOnly.xtitle = "Z boson candidate #it{p}_{T} [GeV]"
        p_smOnly.drawRatio = True
        p_smOnly.ratiorange = (0.2, 1.8)
        p_smOnly.addBackground(sm, processinfo["total_signal"][0],  processinfo["total_signal"][1])
        p_smOnly.addSignal(sm_up, uncert+" up", ROOT.kRed)
        p_smOnly.addSignal(sm_down, uncert+" down", ROOT.kRed, 2)
        p_smOnly.addText(0.22, 0.7, "SM", font=43, size=16)
        p_smOnly.draw()

        for WCname in WCvalues.keys():
            sm_lin_quad[WCname] = getObjFromFile(infile, region+"/sm_lin_quad_"+WCname)
            sm_lin_quad_up[WCname] = getObjFromFile(infile, region+"/sm_lin_quad_"+WCname+"__"+uncert+"Up")
            sm_lin_quad_down[WCname] = getObjFromFile(infile, region+"/sm_lin_quad_"+WCname+"__"+uncert+"Down")
            quad[WCname] = getObjFromFile(infile, region+"/quad_"+WCname)
            quad_up[WCname] = getObjFromFile(infile, region+"/quad_"+WCname+"__"+uncert+"Up")
            quad_down[WCname] = getObjFromFile(infile, region+"/quad_"+WCname+"__"+uncert+"Down")

            p_smlinquad = Plotter(region+"_sm_lin_quad_"+WCname+"_"+uncert)
            p_smlinquad.plot_dir = plotdir
            p_smlinquad.lumi = "138"
            p_smlinquad.xtitle = "Z boson candidate #it{p}_{T} [GeV]"
            p_smlinquad.drawRatio = True
            p_smlinquad.ratiorange = (0.2, 1.8)
            p_smlinquad.addBackground(sm_lin_quad[WCname], processinfo["total_signal"][0],  processinfo["total_signal"][1])
            p_smlinquad.addSignal(sm_lin_quad_up[WCname], uncert+" up", ROOT.kRed)
            p_smlinquad.addSignal(sm_lin_quad_down[WCname], uncert+" down", ROOT.kRed, 2)
            p_smlinquad.addText(0.22, 0.7, "SM+Lin+Quad "+WCname, font=43, size=16)
            p_smlinquad.draw()

            p_quad = Plotter(region+"_quad_"+WCname+"_"+uncert)
            p_quad.plot_dir = plotdir
            p_quad.lumi = "138"
            p_quad.xtitle = "Z boson candidate #it{p}_{T} [GeV]"
            p_quad.drawRatio = True
            p_quad.ratiorange = (0.2, 1.8)
            p_quad.addBackground(quad[WCname], processinfo["total_signal"][0],  processinfo["total_signal"][1])
            p_quad.addSignal(quad_up[WCname], uncert+" up", ROOT.kRed)
            p_quad.addSignal(quad_down[WCname], uncert+" down", ROOT.kRed, 2)
            p_quad.addText(0.22, 0.7, "Quad "+WCname, font=43, size=16)
            p_quad.draw()

        for mixName in WCnames_mixed:
            mixed[mixName] = getObjFromFile(infile, region+"/sm_lin_quad_mixed_"+mixName)
            mixed_up[mixName] = getObjFromFile(infile, region+"/sm_lin_quad_mixed_"+mixName+"__"+uncert+"Up")
            mixed_down[mixName] = getObjFromFile(infile, region+"/sm_lin_quad_mixed_"+mixName+"__"+uncert+"Down")

            p_mixed = Plotter(region+"_mixed_"+mixName+"_"+uncert)
            p_mixed.plot_dir = plotdir
            p_mixed.lumi = "138"
            p_mixed.xtitle = "Z boson candidate #it{p}_{T} [GeV]"
            p_mixed.drawRatio = True
            p_mixed.ratiorange = (0.2, 1.8)
            p_mixed.addBackground(mixed[mixName], processinfo["total_signal"][0],  processinfo["total_signal"][1])
            p_mixed.addSignal(mixed_up[mixName], uncert+" up", ROOT.kRed)
            p_mixed.addSignal(mixed_down[mixName], uncert+" down", ROOT.kRed, 2)
            p_mixed.addText(0.22, 0.7, "Mixed "+mixName, font=43, size=16)
            p_mixed.draw()

        h_eft = getPrediction(sm, sm_lin_quad, quad, mixed, WCvalues)
        h_eft_up = getPrediction(sm_up, sm_lin_quad_up, quad_up, mixed_up, WCvalues)
        h_eft_down = getPrediction(sm_down, sm_lin_quad_down, quad_down, mixed_down, WCvalues)

        p_eftOnly = Plotter(region+"_eftOnly"+"_"+uncert)
        p_eftOnly.plot_dir = plotdir
        p_eftOnly.lumi = "138"
        p_eftOnly.xtitle = "Z boson candidate #it{p}_{T} [GeV]"
        p_eftOnly.drawRatio = True
        p_eftOnly.ratiorange = (0.2, 1.8)
        p_eftOnly.addBackground(h_eft, processinfo["total_signal"][0],  processinfo["total_signal"][1])
        p_eftOnly.addSignal(h_eft_up, uncert+" up", ROOT.kRed)
        p_eftOnly.addSignal(h_eft_down, uncert+" down", ROOT.kRed, 2)
        yPos = 0.7
        for WCname in ["cHqMRe1122","cHqMRe33","cHq3MRe1122","cHq3MRe33"]:
            text = WCname+"=%.2f"%(WCvalues[WCname])
            p_eftOnly.addText(0.22, yPos, text, font=43, size=16)
            yPos += -0.05
        p_eftOnly.draw()

        for SMEFT in ["SM", "EFT"]:
            p = Plotter(region+"_"+SMEFT+"_"+uncert)
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
                p.addSystematic(sm_up, sm_down, uncert, processinfo["total_signal"][0])
                sm_up_bkg = sm_up.Clone()
                sm_up_bkg.Add(h_bkg_all)
                sm_down_bkg = sm_down.Clone()
                sm_down_bkg.Add(h_bkg_all)
                p.addSignal(sm_up_bkg, uncert+" up", ROOT.kRed)
                p.addSignal(sm_down_bkg, uncert+" down", ROOT.kRed, 2)
                p.addText(0.22, 0.7, "SM", font=43, size=16)
            elif SMEFT == "EFT":
                p.addBackground(h_eft, processinfo["total_signal"][0],  processinfo["total_signal"][1])
                p.addSystematic(h_eft_up, h_eft_down, uncert, processinfo["total_signal"][0])
                h_eft_up_bkg = h_eft_up.Clone()
                h_eft_up_bkg.Add(h_bkg_all)
                h_eft_down_bkg = h_eft_down.Clone()
                h_eft_down_bkg.Add(h_bkg_all)
                p.addSignal(h_eft_up_bkg, uncert+" up", ROOT.kRed)
                p.addSignal(h_eft_down_bkg, uncert+" down", ROOT.kRed, 2)
                yPos = 0.7
                for WCname in ["cHqMRe1122","cHqMRe33","cHq3MRe1122","cHq3MRe33"]:
                    text = WCname+"=%.2f"%(WCvalues[WCname])
                    p.addText(0.22, yPos, text, font=43, size=16)
                    yPos += -0.05

            p.draw()
