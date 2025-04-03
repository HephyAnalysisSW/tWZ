import ROOT
import os
import array
import Analysis.Tools.syncer
from tWZ.Tools.helpers                   import getObjFromFile
from tWZ.Tools.user                      import plot_directory
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

def getMinimum(graphs, xmin, xmax, stepsize):
    Npoints = int((xmax-xmin)/stepsize)
    g_min = ROOT.TGraph(Npoints)
    inRange = True
    x = xmin
    i = 0
    while inRange:
        minimum = 100000000
        for rand in graphs.keys():
            if graphs[rand].Eval(x) < minimum:
                minimum = graphs[rand].Eval(x)
        g_min.SetPoint(i, x, minimum)
        i += 1
        x += stepsize
        if x >= xmax or i >= Npoints:
            inRange = False
    return g_min




def getGraphFromTree(filename, wcname):
    wcvalues, twodeltaNLLs = array.array( 'd' ), array.array( 'd' )
    branchname = "k_"+wcname
    rf = ROOT.TFile.Open(filename)
    tree = getattr(rf, "limit")
    if not tree.GetEntry(0)<=0:
        for point in tree:
            if point.deltaNLL > 0.000000001:
                # first value is the best fit with deltaNLL=0, jump this one
                wcvalues.append(eval("point."+branchname))
                twodeltaNLLs.append(2*point.deltaNLL)
        rf.Close()
    # print len(wcvalues)
    if len(wcvalues) == 0:
        wcvalues.append(0)
        twodeltaNLLs.append(0)
    graph = ROOT.TGraph(len(wcvalues), wcvalues, twodeltaNLLs)
    graph = setDrawStyle(graph, wcname)
    return graph

def setDrawStyle(g, wcname):
    from tWZ.Tools.histogramHelper import WClatexNames
    g.GetYaxis().SetRangeUser(0, 8)
    g.SetTitle('')
    g.GetXaxis().SetTitle(WClatexNames[wcname])
    g.GetYaxis().SetTitle('-2 #Delta ln L')
    g.SetLineWidth(2)
    return g

def plotGraph(g, legname, name, xmin, xmax, g_stat=None):
    c = ROOT.TCanvas(name, "", 600, 600)
    ROOT.gPad.SetTopMargin(0.02)
    g.GetXaxis().SetLimits(xmin, xmax)
    g.Draw("AL")
    if g_stat is not None:
        g_stat.SetLineStyle(2)
        g_stat.Draw("L SAME")
    leg = ROOT.TLegend(.6, .25, .9, .4)
    leg.AddEntry(g, legname, "l")
    if g_stat is not None:
        leg.AddEntry(g_stat, legname+" (stat. only)", "l")
    leg.Draw()
    l1, l2 = getLines(xmin, xmax)
    l1.Draw("SAME")
    l2.Draw("SAME")
    g.Draw("L SAME")
    ROOT.gPad.RedrawAxis()
    c.Print(name)

def plotGraphComparison(graphs, name, xmin, xmax):
    c = ROOT.TCanvas(name, "", 600, 600)
    ROOT.gPad.SetTopMargin(0.02)
    leg = ROOT.TLegend(.65, .25, .9, .5)
    isFirst = True
    for rand in graphs.keys():
        color = int(rand)+1
        style = 1
        if color > 9:
            style = color / 9 # for numbers larger 9 choose different style
            color = color % 9 # set color to rest of division: 10 -> 1, 11->2, ...
        graphs[rand].GetXaxis().SetLimits(xmin, xmax)
        graphs[rand].SetLineColor(color)
        graphs[rand].SetLineStyle(style)
        leg.AddEntry(graphs[rand], str(rand), "l")
        if isFirst:
            graphs[rand].Draw("AL")
            isFirst = False
        else:
            graphs[rand].Draw("L SAME")
    leg.Draw()
    l1, l2 = getLines(xmin, xmax)
    l1.Draw("SAME")
    l2.Draw("SAME")
    ROOT.gPad.RedrawAxis()
    c.Print(name)

def getLines(xmin, xmax):
    y_1sigma = 1.00
    y_2sigma = 3.84
    line_1sigma = ROOT.TLine(xmin, y_1sigma, xmax, y_1sigma)
    line_2sigma = ROOT.TLine(xmin, y_2sigma, xmax, y_2sigma)
    line_1sigma.SetLineWidth(2)
    line_2sigma.SetLineWidth(2)
    line_1sigma.SetLineStyle(2)
    line_2sigma.SetLineStyle(2)
    return line_1sigma, line_2sigma

def getInterval(graph, xmin, xmax):
    bestFit = None
    minimum = 1000
    stepsize = 0.001
    x = xmin
    lower68 = []
    upper68 = []
    lower95 = []
    upper95 = []
    print "------------"
    while x < xmax:
        value_before = graph.Eval(x-stepsize)
        value = graph.Eval(x)
        value_after = graph.Eval(x+stepsize)

        if value < minimum:
            minimum = value
            bestFit = x

        if value_before > 1.00 and value_after < 1.00:
            lower68.append(x)
        elif value_before < 1.00 and value_after > 1.00:
            upper68.append(x)

        if value_before > 3.84 and value_after < 3.84:
            lower95.append(x)
        elif value_before < 3.84 and value_after > 3.84:
            upper95.append(x)
        x += stepsize

    for l in [lower68,upper68,lower95,upper95]:
        if len(l) > 1:
            if abs(max(l)-min(l)) < 0.1:
                average = float(sum(l) / len(l))
                l[:] = [average] # this modifies the original list and not just the new object l

    l68, u68, l95, u95 = None, None, None, None
    if len(lower68) == 1:
        l68 = lower68[0]
    if len(upper68) == 1:
        u68 = upper68[0]
    if len(lower95) == 1:
        l95 = lower95[0]
    if len(upper95) == 1:
        u95 = upper95[0]

    print "Best fit =", bestFit, "| 68%: (",l68,",",u68,")", "95%: (",l95,",",u95,")"
    return bestFit, l68, u68, l95, u95


################################################################################
################################################################################
################################################################################
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
argParser.add_argument('--wc',               action='store', type=str, default="cHq1Re11")
argParser.add_argument('--float',            action='store_true', default=False)
argParser.add_argument('--freeze',           action='store', type=str, default=None)
argParser.add_argument('--statOnly',         action='store_true', default=False)
argParser.add_argument('--addStatOnly',      action='store_true', default=False)
argParser.add_argument('--light',            action='store_true', default=False)
argParser.add_argument('--minus',            action='store_true', default=False)
argParser.add_argument('--excludeTriplet',   action='store_true', default=False)
argParser.add_argument('--NjetSplit',        action='store_true', default=False)
argParser.add_argument('--scaleCorrelation', action='store_true', default=False)
argParser.add_argument('--signalInjectionLight',  action='store_true', default=False)
argParser.add_argument('--signalInjectionHeavy',  action='store_true', default=False)
argParser.add_argument('--signalInjectionMixed',  action='store_true', default=False)
argParser.add_argument('--signalInjectionWZjets',  action='store_true', default=False)
argParser.add_argument('--unblind',          action='store_true', default=False)
argParser.add_argument('--noBB',          action='store_true', default=False)
argParser.add_argument('--fluctuatePseudoData',  action='store_true', default=False)
argParser.add_argument('--binning',          action='store', default="default")
argParser.add_argument('--sysMode',          action='store', default="default")
argParser.add_argument('--noZero', action='store_true', default=False)
argParser.add_argument('--SMZero', action='store_true', default=False)
argParser.add_argument('--randomMin', action='store', default=None)
argParser.add_argument('--randomMax', action='store', default=None)

args = argParser.parse_args()

logger.info( "Make 1D limit plot")

WCnames = ["cHq1Re11", "cHq1Re22", "cHq1Re33", "cHq3Re11", "cHq3Re22", "cHq3Re33"]
if args.light:
    WCnames = ["cHq1Re1122", "cHq1Re33", "cHq3Re1122", "cHq3Re33"]
    if args.minus:
        WCnames = ["cHqMRe1122", "cHqMRe33", "cHq3MRe1122", "cHq3MRe33", "cHuRe1122", "cHuRe33","cHdRe1122", "cHdRe33",]
        if args.excludeTriplet:
            WCnames = ["cHqMRe1122", "cHqMRe33", "cHq3MRe1122"]


if args.year not in ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]:
    raise RuntimeError( "Year %s is not knwon", args.year)
logger.info( "Year = %s", args.year )

if args.wc not in WCnames:
    raise RuntimeError( "Wilson coefficient "+args.wc+" is not knwon. Did you run with light option?")
logger.info( "Wilson coefficient = %s", args.wc )

uncertaintyGroups = ["autoMCStats","btag","ewk","jet","lepton","lumi","nonprompt","other_exp","pdf","ps","rate_bkg","rate_sig","scale_bkg","scale_sig","wz"]
if args.freeze is not None:
    if args.statOnly:
        raise RuntimeError( "Cannot run statOnly AND freeze nuisance groups" )
    for group in args.freeze.split("-"):
        if group not in uncertaintyGroups:
            raise RuntimeError( "Uncertainty group %s not known. You also might have used a wrong format: --freeze=btag-jec", group )

if args.addStatOnly:
    if args.statOnly:
        raise RuntimeError( "Cannot run statOnly AND addStatOnly" )
    logger.info( "Adding also statOnly lines" )



nRegions = 4 if args.NjetSplit else 3
logger.info( "Number of regions: %s", nRegions)

dirname_suffix = ""
if args.light:               dirname_suffix+="_light"
if args.minus:               dirname_suffix+="_minus"
if args.excludeTriplet:      dirname_suffix+="_excludeTriplet"
if args.NjetSplit:           dirname_suffix+="_NjetSplit"
if args.scaleCorrelation:    dirname_suffix+="_scaleCorrelation"
if args.signalInjectionLight:     dirname_suffix+="_signalInjectionLight"
if args.signalInjectionHeavy:     dirname_suffix+="_signalInjectionHeavy"
if args.signalInjectionMixed:     dirname_suffix+="_signalInjectionMixed"
if args.signalInjectionWZjets:    dirname_suffix+="_signalInjectionWZjets"
if args.fluctuatePseudoData:      dirname_suffix+="_fluctuatePseudoData"
if args.unblind:                  dirname_suffix+="_UNBLINDED"
if args.noBB:                  dirname_suffix+="_noBB"
if args.binning != "default":  dirname_suffix+="_binning-"+args.binning
if args.sysMode != "default":    dirname_suffix+="_"+args.sysMode
if args.noZero:                  dirname_suffix+="_noZero"
if args.SMZero:                  dirname_suffix+="_SMZero"

this_dir = os.getcwd()
dataCard_dir = this_dir+"/DataCards_threePoint"+dirname_suffix+"/"+args.year+"/"
plotdir = plot_directory+"/Limits_UL_threePoint"+dirname_suffix+"/"+args.year+"/"

if not os.path.exists( plotdir ): os.makedirs( plotdir )

graphs = {}


#################################
for i in range( int(args.randomMin), int(args.randomMax)+1):
    r = "combined"
    region = r+1 if isinstance(r, int) else r
    marginfloat = "float" if args.float else "margin"
    filename = "higgsCombine.topEFT_%s_%s_13TeV_%s_1D-%s_%s_random_%i.MultiDimFit.mH125.123456.root"%(args.year, str(region), args.year, args.wc, marginfloat, i)
    if args.freeze is not None:
        filename = filename.replace(".MultiDimFit", "_freeze-"+args.freeze+".MultiDimFit")
    if args.statOnly:
        filename = filename.replace(".MultiDimFit", "_statOnly.MultiDimFit")
    graphs[i] = getGraphFromTree(dataCard_dir+filename, args.wc)


outname = "1D__"+args.year+"__"+args.wc+"__combined__"+marginfloat+"_random.pdf"
if args.freeze is not None:
    outname = outname.replace(".pdf", "_freeze-"+args.freeze+".pdf")
if args.statOnly:
    outname = outname.replace(".pdf", "_statOnly.pdf")
xmin, xmax = -5, 7
if args.wc in ["cHq3Re11", "cHq3Re1122", "cHq3MRe11", "cHq3MRe1122"]:
    xmin, xmax = -1, 2
if args.wc in ["cHq3MRe33"]:
    xmin, xmax = -8, 7
    if args.float:
        xmin, xmax = -9.9, 9.9
plotGraphComparison(graphs, plotdir+outname, xmin, xmax)

outname_min = outname.replace(".pdf", "_random_minimum.pdf")
stepsize = 0.05
gMin = getMinimum(graphs, xmin, xmax, stepsize)
plotGraph(gMin, "Minimum", plotdir+outname_min, xmin, xmax)
