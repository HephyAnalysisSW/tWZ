import ROOT
from tWZ.Tools.dibosonEWKcorrection import getNNLOtoNLO,getEWKtoQCD
from tWZ.Tools.user                              import plot_directory
import Analysis.Tools.syncer

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

xmin = 100.
xmax = 2000.
steps = 1000
stepsize = (xmax-xmin)/steps


g_NNLO_ZZ = ROOT.TGraph(steps)
g_NNLO_ZZ_norm = ROOT.TGraph(steps)
g_EWK_add_ZZ = ROOT.TGraph(steps)
g_EWK_mul_ZZ = ROOT.TGraph(steps)
g_NNLO_WZ = ROOT.TGraph(steps)
g_NNLO_WZ_norm = ROOT.TGraph(steps)
g_EWK_add_WZ = ROOT.TGraph(steps)
g_EWK_mul_WZ = ROOT.TGraph(steps)

for i in range(steps):
    pt = xmin + i*stepsize
    g_NNLO_ZZ.SetPoint(i+1, pt, getNNLOtoNLO(pt, "ZZ", False))
    g_NNLO_WZ.SetPoint(i+1, pt, getNNLOtoNLO(pt, "WZ", False))
    g_NNLO_ZZ_norm.SetPoint(i+1, pt, getNNLOtoNLO(pt, "ZZ", True))
    g_NNLO_WZ_norm.SetPoint(i+1, pt, getNNLOtoNLO(pt, "WZ", True))
    g_EWK_add_ZZ.SetPoint(i+1, pt, getEWKtoQCD(pt, "ZZ", "add"))
    g_EWK_add_WZ.SetPoint(i+1, pt, getEWKtoQCD(pt, "WZ", "add"))
    g_EWK_mul_ZZ.SetPoint(i+1, pt, getEWKtoQCD(pt, "ZZ", "mul"))
    g_EWK_mul_WZ.SetPoint(i+1, pt, getEWKtoQCD(pt, "WZ", "mul"))


c_NNLO_ZZ = ROOT.TCanvas("c_NNLO_ZZ", "c_NNLO_ZZ", 600, 600)
ROOT.gPad.SetLogx(1)
ROOT.gPad.SetLogy(1)
g_NNLO_ZZ.Draw("AC")
g_NNLO_ZZ.SetTitle("ZZ")
g_NNLO_ZZ.GetXaxis().SetRangeUser(xmin, xmax)
g_NNLO_ZZ.GetYaxis().SetRangeUser(0.007, 30)
c_NNLO_ZZ.Print(plot_directory+"/EWKcorrections/NNLO_ZZ.pdf")

c_NNLO_WZ = ROOT.TCanvas("c_NNLO_WZ", "c_NNLO_WZ", 600, 600)
ROOT.gPad.SetLogx(1)
ROOT.gPad.SetLogy(1)
g_NNLO_WZ.Draw("AC")
g_NNLO_WZ.SetTitle("WZ")
g_NNLO_WZ.GetXaxis().SetRangeUser(xmin, xmax)
g_NNLO_WZ.GetYaxis().SetRangeUser(0.007, 30)
c_NNLO_WZ.Print(plot_directory+"/EWKcorrections/NNLO_WZ.pdf")

c_NNLO_ZZ_norm = ROOT.TCanvas("c_NNLO_ZZ_norm", "c_NNLO_ZZ_norm", 600, 600)
ROOT.gPad.SetLogx(1)
ROOT.gPad.SetLogy(1)
g_NNLO_ZZ_norm.Draw("AC")
g_NNLO_ZZ_norm.SetTitle("ZZ normalized")
g_NNLO_ZZ_norm.GetXaxis().SetRangeUser(xmin, xmax)
g_NNLO_ZZ_norm.GetYaxis().SetRangeUser(0.007, 30)
c_NNLO_ZZ_norm.Print(plot_directory+"/EWKcorrections/NNLO_ZZ_norm.pdf")

c_NNLO_WZ_norm = ROOT.TCanvas("c_NNLO_WZ_norm", "c_NNLO_WZ_norm", 600, 600)
ROOT.gPad.SetLogx(1)
ROOT.gPad.SetLogy(1)
g_NNLO_WZ_norm.Draw("AC")
g_NNLO_WZ_norm.SetTitle("WZ normalized")
g_NNLO_WZ_norm.GetXaxis().SetRangeUser(xmin, xmax)
g_NNLO_WZ_norm.GetYaxis().SetRangeUser(0.007, 30)
c_NNLO_WZ_norm.Print(plot_directory+"/EWKcorrections/NNLO_WZ_norm.pdf")

c_EWK_ZZ = ROOT.TCanvas("c_EWK_ZZ", "c_EWK_ZZ", 600, 600)
ROOT.gPad.SetLogx(1)
ROOT.gPad.SetLogy(0)
g_EWK_add_ZZ.SetLineColor(ROOT.kGreen)
g_EWK_mul_ZZ.SetLineColor(ROOT.kMagenta)
g_EWK_add_ZZ.Draw("AC")
g_EWK_add_ZZ.SetTitle("ZZ")
g_EWK_add_ZZ.GetXaxis().SetRangeUser(xmin, xmax)
g_EWK_add_ZZ.GetYaxis().SetRangeUser(0., 1.5)
g_EWK_mul_ZZ.Draw("C SAME")
c_EWK_ZZ.Print(plot_directory+"/EWKcorrections/EWK_ZZ.pdf")

c_EWK_WZ = ROOT.TCanvas("c_EWK_WZ", "c_EWK_WZ", 600, 600)
ROOT.gPad.SetLogx(1)
ROOT.gPad.SetLogy(0)
g_EWK_add_WZ.SetLineColor(ROOT.kGreen)
g_EWK_mul_WZ.SetLineColor(ROOT.kMagenta)
g_EWK_add_WZ.Draw("AC")
g_EWK_add_WZ.SetTitle("WZ")
g_EWK_add_WZ.GetXaxis().SetRangeUser(xmin, xmax)
g_EWK_add_WZ.GetYaxis().SetRangeUser(0., 1.5)
g_EWK_mul_WZ.Draw("C SAME")
c_EWK_WZ.Print(plot_directory+"/EWKcorrections/EWK_WZ.pdf")
