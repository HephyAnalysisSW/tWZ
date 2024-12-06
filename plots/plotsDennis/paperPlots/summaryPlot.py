import ROOT
import os
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.histogramHelper import WClatexNames

################################################################################
################################################################################
################################################################################
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--noQuad', action='store_true', default=False)
argParser.add_argument('--both', action='store_true', default=False)
argParser.add_argument('--addExpected', action='store_true', default=False)
argParser.add_argument('--addHalf', action='store_true', default=False)
# argParser.add_argument('--addHalf', action='store_true', default=False)
args = argParser.parse_args()

################################################################################
################################################################################
################################################################################
def getValues(path, wcname, floatingOtherWCs, factor):
    path = path.replace("WCNAME", WCname)
    if floatingOtherWCs:
        path = path.replace("FLOATMARGIN", "float")
    else:
        path = path.replace("FLOATMARGIN", "margin")
    print "Reading", path, "..."

    bestfit, sigma1, sigma2 = readDataFromFile(path,factor)
    return bestfit, sigma1, sigma2

def makeGraph(values, WCnames, offset, color, markerstyle, asimov=False):
    # per WC make multiple graphs:
    # - the first with only the best fit point
    # - one for each 1sigma interval
    # - one for each 2sigma interval
    g_best = ROOT.TGraphAsymmErrors(len(WCnames))
    N1SD = 0
    N2SD = 0
    for WCname in WCnames:
        bestfit, sigma1intervals, sigma2intervals = values[WCname]
        N1SD += len(sigma1intervals)
        N2SD += len(sigma2intervals)
    g_1SD = ROOT.TGraphAsymmErrors(N1SD)
    g_2SD = ROOT.TGraphAsymmErrors(N2SD)

    counter_1SD = 0
    counter_2SD = 0
    for i,WCname in enumerate(WCnames):
        ypos = len(WCnames)-i
        bestfit, sigma1intervals, sigma2intervals = values[WCname]
        xerr = 0.0
        if asimov:
            xerr = 0.05

        # First fill best fit
        g_best.SetPoint(i, bestfit, ypos+offset)
        g_best.SetPointError(i, 0.0, 0.0, 0.0, 0.0)
        # Iterate through 1 sigma intervals
        for (down, up) in sigma1intervals:
            center = down+(up-down)/2
            g_1SD.SetPoint(counter_1SD, center, ypos+offset)
            g_1SD.SetPointError(counter_1SD, center-down, up-center, xerr, xerr)
            counter_1SD += 1
        # Iterate through 2 sigma intervals
        for (down, up) in sigma2intervals:
            center = down+(up-down)/2
            g_2SD.SetPoint(counter_2SD, center, ypos+offset)
            g_2SD.SetPointError(counter_2SD, center-down, up-center, xerr, xerr)
            counter_2SD += 1

    if asimov:
        setStyle_asimov(g_best, 15)
        setStyle_asimov(g_1SD, 15)
        setStyle_asimov(g_2SD, 17)
    else:
        setStyle(g_best, color, markerstyle, 1.0, color, 5, 1)
        setStyle(g_1SD, color, markerstyle, 0.0, color, 5, 1)
        setStyle(g_2SD, color, markerstyle, 0.0, color, 3, 2)
    return g_best,g_1SD, g_2SD

def readDataFromFile(filename, factor=1.0):
    bestfit = None
    sigma1 = []
    sigma2 = []
    with open(filename, 'r') as file:
        for i,line in enumerate(file):
            line = line.replace("\n", "")
            if i == 0 and "None" not in line:
                bestfit = factor*float(line)
            elif i == 1 and "None" not in line:
                for interval in line.split(";"):
                    if not "," in interval:
                        continue
                    down = interval.split(",")[0]
                    up = interval.split(",")[1]
                    sigma1.append( (factor*float(down),factor*float(up)) )
            elif i == 2 and "None" not in line:
                for interval in line.split(";"):
                    if not "," in interval:
                        continue
                    down = interval.split(",")[0]
                    up = interval.split(",")[1]
                    sigma2.append( (factor*float(down),factor*float(up)) )
    return bestfit, sigma1, sigma2

def setStyle(g, markercol, markerstyle, markersize, linecol, linewidth, linestyle):
    g.SetMarkerStyle(markerstyle)
    g.SetMarkerColor(markercol)
    g.SetMarkerSize(markersize)
    g.SetLineColor(linecol)
    g.SetLineWidth(linewidth)
    g.SetLineStyle(linestyle)

def setStyle_asimov(g, col):
    g.SetFillColor(col)
    g.SetLineColor(col)


def getCMS(factor=1.0):
    cmstext = ROOT.TLatex(3.5, 24, "CMS")
    cmstext.SetNDC()
    cmstext.SetTextAlign(13)
    cmstext.SetTextFont(62)
    cmstext.SetTextSize(0.08*factor)
    cmstext.SetX(0.01)
    cmstext.SetY(0.99)
    return cmstext

def getPrelim():
    prelim = ROOT.TLatex(3.5, 24, "Preliminary")
    prelim.SetNDC()
    prelim.SetTextAlign(13)
    prelim.SetTextFont(52)
    prelim.SetTextSize(0.05)
    prelim.SetX(0.01)
    prelim.SetY(0.92)
    return prelim

def addText(x, y, text, font=43, size=12, color=1):
    latex = ROOT.TLatex(3.5, 24, text)
    latex.SetNDC()
    latex.SetTextAlign(12)
    latex.SetTextFont(font)
    latex.SetTextSize(size)
    latex.SetTextColor(color)
    latex.SetX(x)
    latex.SetY(y)
    return latex

################################################################################
################################################################################
################################################################################

WCnames = ["cHqMRe1122", "cHqMRe33", "cHq3MRe1122", "cHq3MRe33", "cHuRe1122", "cHuRe33", "cHdRe1122", "cHdRe33","cW", "cWtil"]
path_data = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/Limits_UL_threePoint_light_minus_UNBLINDED_binning-A_SMZero/ULRunII/1D__ULRunII__WCNAME__combined__FLOATMARGIN.txt"
path_data_noQuad = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/Limits_UL_threePoint_light_minus_UNBLINDED_noQuad_binning-A_SMZero/ULRunII/1D__ULRunII__WCNAME__combined__FLOATMARGIN.txt"
path_asimov = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/Limits_UL_threePoint_light_minus_binning-A_SMZero/ULRunII/1D__ULRunII__WCNAME__combined__FLOATMARGIN.txt"
path_asimov_noQuad = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/Limits_UL_threePoint_light_minus_noQuad_binning-A_SMZero/ULRunII/1D__ULRunII__WCNAME__combined__FLOATMARGIN.txt"
path_data_half = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/Limits_UL_threePoint_light_minus_UNBLINDED_binning-A_SMZero_HALF/ULRunII/1D__ULRunII__WCNAME__combined__FLOATMARGIN.txt"

factors = {
    "cHqMRe1122" :   1.0,
    "cHqMRe33" :     0.1,
    "cHq3MRe1122" : 10.0,
    "cHq3MRe33" :    0.5,
    "cHuRe1122" :    1.0,
    "cHuRe33" :      0.1,
    "cHdRe1122" :    1.0,
    "cHdRe33" :      0.1,
    "cW" :          10.0,
    "cWtil" :       10.0,
}

if args.noQuad:
    factors["cWtil"] = 0.5
    factors["cHq3MRe33"] = 0.1

if args.both:
    factors["cWtil"] = 0.5
    factors["cHq3MRe33"] = 0.1

values_data = {}
values_data_float = {}
values_data_noQuad = {}
values_data_float_noQuad = {}
values_asimov = {}
values_asimov_float = {}
values_asimov_noQuad = {}
values_asimov_float_noQuad = {}

for WCname in WCnames:
    values_data_float[WCname] = getValues(path_data, WCname, True, factors[WCname])
    values_data[WCname] = getValues(path_data, WCname, False, factors[WCname])
    if args.both or args.noQuad:
        values_data_float_noQuad[WCname] = getValues(path_data_noQuad, WCname, True, factors[WCname])
        values_data_noQuad[WCname] = getValues(path_data_noQuad, WCname, False, factors[WCname])

    if args.addExpected:
        values_asimov_float[WCname] = getValues(path_asimov, WCname, True, factors[WCname])
        values_asimov[WCname] = getValues(path_asimov, WCname, False, factors[WCname])
        if args.both or args.noQuad:
            values_asimov_float_noQuad[WCname] = getValues(path_asimov_noQuad, WCname, True, factors[WCname])
            values_asimov_noQuad[WCname] = getValues(path_asimov_noQuad, WCname, False, factors[WCname])

    if args.addHalf:
        values_asimov_float[WCname] = getValues(path_data_half, WCname, True, factors[WCname])
        values_asimov[WCname] = getValues(path_data_half, WCname, False, factors[WCname])
        if args.both or args.noQuad:
            values_asimov_float_noQuad[WCname] = getValues(path_asimov_noQuad, WCname, True, factors[WCname])
            values_asimov_noQuad[WCname] = getValues(path_asimov_noQuad, WCname, False, factors[WCname])

plotdir = plot_directory+"/PaperPlots/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

xmin,xmax = -6.3, 6.7
ymin, ymax = 0.4, 12.8 # 0.4, 5.2
if args.both:
    xmin,xmax = -6.3, 6.7
    ymin, ymax = 0.4, 9.0
if args.addExpected or args.addHalf:
    ymin, ymax = 0.4, 9.0, # 0.4, 6.0
margin_top = 0.01
margin_left = 0.29
margin_right = 0.02
margin_bottom = 0.1
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetEndErrorSize(0.0)
ROOT.gStyle.SetLegendBorderSize(0)
# canvas = ROOT.TCanvas("","",600,600)
canvas = ROOT.TCanvas("","",600,800)
ROOT.gPad.SetTopMargin(margin_top)
ROOT.gPad.SetLeftMargin(margin_left)
ROOT.gPad.SetRightMargin(margin_right)
ROOT.gPad.SetBottomMargin(margin_bottom)

dummy = ROOT.TGraph(2)
dummy.SetPoint(0,xmin,ymin)
dummy.SetPoint(1,xmax,ymax)
dummy.SetMarkerSize(0.0)
dummy.Draw("AP")
dummy.SetTitle("")
dummy.GetXaxis().SetTitle("Wilson coefficient value")
dummy.GetYaxis().SetTitle("")
dummy.GetYaxis().SetTitleSize(0.0)
dummy.GetYaxis().SetLabelSize(0.0)
dummy.GetYaxis().SetLabelSize(0.0)
dummy.GetYaxis().SetTickLength(0.0)
dummy.GetXaxis().SetRangeUser(xmin,xmax)
dummy.GetYaxis().SetRangeUser(ymin,ymax)


line_SM = ROOT.TLine(0., ymin, 0., 11.3)# ROOT.TLine(0., ymin, 0., 4.25)
line_SM.SetLineColor(15)
line_SM.SetLineWidth(2)
line_SM.SetLineStyle(2)
line_SM.Draw("SAME")

if args.both:
    if args.addExpected:
        g_asimov_best_float, g_asimov_1SD_float, g_asimov_2SD_float = makeGraph(values_asimov_float, WCnames, 0.225, 1, 1, asimov=True)
        g_asimov_best, g_asimov_1SD, g_asimov_2SD = makeGraph(values_asimov, WCnames, 0.075, 1, 1, asimov=True)
        g_asimov_best_float_noQuad, g_asimov_1SD_float_noQuad, g_asimov_2SD_float_noQuad = makeGraph(values_asimov_float_noQuad, WCnames, -0.075, 1, 1, asimov=True)
        g_asimov_best_noQuad, g_asimov_1SD_noQuad, g_asimov_2SD_noQuad = makeGraph(values_asimov_noQuad, WCnames, -0.225,  1, 1, asimov=True)
        # g_asimov_best_float.Draw("E2 SAME")
        # g_asimov_best.Draw("E2 SAME")
        # g_asimov_best_float_noQuad.Draw("E2 SAME")
        # g_asimov_best_noQuad.Draw("E2 SAME")
        g_asimov_2SD.Draw("E2 SAME")
        g_asimov_1SD.Draw("E2 SAME")
        g_asimov_2SD_float.Draw("E2 SAME")
        g_asimov_1SD_float.Draw("E2 SAME")
        g_asimov_2SD_noQuad.Draw("E2 SAME")
        g_asimov_1SD_noQuad.Draw("E2 SAME")
        g_asimov_2SD_float_noQuad.Draw("E2 SAME")
        g_asimov_1SD_float_noQuad.Draw("E2 SAME")
    graph_best_float, graph_1SD_float, graph_2SD_float = makeGraph(values_data_float, WCnames, 0.225, ROOT.kBlack, 20)
    graph_best, graph_1SD, graph_2SD = makeGraph(values_data, WCnames, 0.075, ROOT.kAzure+7, 20)
    graph_best_float_noQuad, graph_1SD_float_noQuad, graph_2SD_float_noQuad = makeGraph(values_data_float_noQuad, WCnames, -0.075, ROOT.kGreen-3, 21)
    graph_best_noQuad, graph_1SD_noQuad, graph_2SD_noQuad = makeGraph(values_data_noQuad, WCnames, -0.225, ROOT.kOrange-3, 21)
    graph_best_float.Draw("PE SAME")
    graph_best.Draw("PE SAME")
    graph_best_float_noQuad.Draw("PE SAME")
    graph_best_noQuad.Draw("PE SAME")
    graph_2SD.Draw("PE SAME")
    graph_1SD.Draw("PE SAME")
    graph_2SD_float.Draw("PE SAME")
    graph_1SD_float.Draw("PE SAME")
    graph_2SD_noQuad.Draw("PE SAME")
    graph_1SD_noQuad.Draw("PE SAME")
    graph_2SD_float_noQuad.Draw("PE SAME")
    graph_1SD_float_noQuad.Draw("PE SAME")
else:
    if args.addExpected or args.addHalf:
        g_asimov_best_float, g_asimov_1SD_float, g_asimov_2SD_float = makeGraph(values_asimov_float, WCnames, 0.1, 1, 1, asimov=True)
        g_asimov_best, g_asimov_1SD, g_asimov_2SD = makeGraph(values_asimov, WCnames, -0.1, 1, 1, asimov=True)
        # g_asimov_best_float.Draw("E2 SAME")
        # g_asimov_best.Draw("E2 SAME")
        g_asimov_2SD.Draw("E2 SAME")
        g_asimov_1SD.Draw("E2 SAME")
        g_asimov_2SD_float.Draw("E2 SAME")
        g_asimov_1SD_float.Draw("E2 SAME")
    graph_best, graph_1SD, graph_2SD = makeGraph(values_data, WCnames, -0.1, ROOT.kAzure+7, 20)
    graph_best_float, graph_1SD_float, graph_2SD_float = makeGraph(values_data_float, WCnames, 0.1, ROOT.kBlack, 20)
    graph_best.Draw("PE SAME")
    graph_best_float.Draw("PE SAME")
    graph_2SD.Draw("PE SAME")
    graph_1SD.Draw("PE SAME")
    graph_2SD_float.Draw("PE SAME")
    graph_1SD_float.Draw("PE SAME")

labels = []
for i,WCname in enumerate(WCnames):
    ypos = len(WCnames)-i
    ypos_canvas = margin_bottom + (ypos-ymin)*(1-margin_top-margin_bottom)/(ymax-ymin)
    labels.append(addText(0.01, ypos_canvas, WClatexNames[WCname].replace("/#Lambda^{2} [TeV^{-2}]",""), font=43, size=30, color=1))
    if abs(factors[WCname]-1.0) > 0.000001:
        labels.append(addText(0.185, ypos_canvas, "[#times %.1f]"%(factors[WCname]), font=43, size=15, color=12))



for l in labels:
    l.Draw()

l_cms=getCMS()
l_prelim=getPrelim()
l_cms.Draw()
l_prelim.Draw()

leg_left = margin_left-0.035
leg_right = 1-margin_right-0.05
leg_top = 0.95
leg_bottom1 = 0.85
leg_bottom2 = 0.85
leg_split = 0.65
if args.both:
    leg_bottom1 = 0.75

if args.addExpected or args.addHalf:
    leg_bottom2 = 0.75

if args.addHalf:
    leg_split = 0.58

leg1 = ROOT.TLegend(leg_left, leg_bottom1, leg_split, leg_top)
leg1.AddEntry(graph_best_float, "Best fit (profiled)", "p")
leg1.AddEntry(graph_best, "Best fit (fixed)", "p")
if args.both:
    leg1.AddEntry(graph_best_float_noQuad, "Best fit (linear, profiled)", "p")
    leg1.AddEntry(graph_best_noQuad, "Best fit (linear, fixed)", "p")
leg1.SetTextSize(0.0375)
leg1.Draw()

leg2 = ROOT.TLegend(leg_split, leg_bottom2, leg_right, leg_top)
leg2.AddEntry(graph_1SD_float, "-2 #Delta ln L < 1.0", "l")
leg2.AddEntry(graph_2SD_float, "-2 #Delta ln L < 3.84", "l")
leg2.SetTextSize(0.0375)
if args.addExpected:
    leg2.AddEntry(g_asimov_1SD, "-2 #Delta ln L < 1.0 (exp.)", "f")
    leg2.AddEntry(g_asimov_2SD, "-2 #Delta ln L < 3.84 (exp.)", "f")
    leg2.SetTextSize(0.03)
if args.addHalf:
    leg2.AddEntry(g_asimov_1SD, "-2 #Delta ln L < 1.0 (half stats)", "f")
    leg2.AddEntry(g_asimov_2SD, "-2 #Delta ln L < 3.84 (half stats)", "f")
    leg2.SetTextSize(0.03)
leg2.Draw()

ROOT.gPad.RedrawAxis()
outname = plotdir+"Summary.pdf"
if args.noQuad:
    outname = plotdir+"Summary_noQuad.pdf"
elif args.both:
    outname = plotdir+"Summary_both.pdf"

if args.addExpected:
    outname = outname.replace(".pdf", "_addExp.pdf")
if args.addHalf:
    outname = outname.replace(".pdf", "_addHalf.pdf")
canvas.Print(outname)
