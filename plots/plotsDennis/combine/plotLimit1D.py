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

def getGraphFromTree(filename, wcname):
    wcvalues, twodeltaNLLs = array.array( 'd' ), array.array( 'd' )
    branchname = "k_"+wcname
    rf = ROOT.TFile.Open(filename)
    tree = getattr(rf, "limit")
    if tree.GetEntry(0)<=0:
        raise RuntimeError( "Tree of file %s is empty", filename)
    for point in tree:
        if point.deltaNLL > 0.000000001:
            # first value is the best fit with deltaNLL=0, jump this one
            wcvalues.append(eval("point."+branchname))
            twodeltaNLLs.append(2*point.deltaNLL)
    rf.Close()
    graph = ROOT.TGraph(len(wcvalues), wcvalues, twodeltaNLLs)
    graph = setDrawStyle(graph, wcname)
    return graph

def setDrawStyle(g, wcname):
    g.GetYaxis().SetRangeUser(0, 8)
    g.SetTitle('')
    g.GetXaxis().SetTitle(wcname)
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

def plotGraphComparison(graphs, plotstyle, name, xmin, xmax, graphs_statonly=None):
    c = ROOT.TCanvas(name, "", 600, 600)
    ROOT.gPad.SetTopMargin(0.02)
    leg = ROOT.TLegend(.65, .25, .9, .5)
    isFirst = True
    for region in graphs.keys():
        graphs[region].GetXaxis().SetLimits(xmin, xmax)
        graphs[region].SetLineColor(plotstyle[region][1])
        leg.AddEntry(graphs[region], plotstyle[region][0], "l")
        if isFirst:
            graphs[region].Draw("AL")
            isFirst = False
        else:
            graphs[region].Draw("L SAME")
    if graphs_statonly is not None:
        for region in graphs_statonly.keys():
            if region == "combined":
                graphs_statonly[region].SetLineColor(plotstyle[region][1])
                graphs_statonly[region].SetLineStyle(2)
                leg.AddEntry(graphs_statonly[region], plotstyle[region][0]+" (stat. only)", "l")
                graphs_statonly[region].Draw("L SAME")
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
argParser.add_argument('--scaleCorrelation', action='store_true', default=False)
args = argParser.parse_args()

logger.info( "Make 1D limit plot")

WCnames = ["cHq1Re11", "cHq1Re22", "cHq1Re33", "cHq3Re11", "cHq3Re22", "cHq3Re33"]
if args.light:
    WCnames = ["cHq1Re1122", "cHq1Re33", "cHq3Re1122", "cHq3Re33"]

if args.year not in ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]:
    raise RuntimeError( "Year %s is not knwon", args.year)
logger.info( "Year = %s", args.year )

if args.wc not in WCnames:
    raise RuntimeError( "Wilson coefficient "+args.wc+" is not knwon. Did you run with light option?")
logger.info( "Wilson coefficient = %s", args.wc )

uncertaintyGroups = ["btag","jet","lepton","lumi","nonprompt","other_exp","rate_bkg","rate_sig","theory"]
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



nRegions = 3
logger.info( "Number of regions: %s", nRegions)

this_dir = os.getcwd()
dataCard_dir = this_dir+"/DataCards_threePoint/"+args.year+"/"
if args.scaleCorrelation:
    dataCard_dir = this_dir+"/DataCards_threePoint_scaleCorr/"+args.year+"/"
if args.light:
    dataCard_dir = dataCard_dir.replace("threePoint", "threePoint_light")


plotdir = plot_directory+"/Limits_UL_threePoint/"+args.year+"/"
if args.scaleCorrelation:
    plotdir = plot_directory+"/Limits_UL_threePoint_scaleCorr/"+args.year+"/"
if args.light:
    plotdir = plotdir.replace("threePoint", "threePoint_light")

if not os.path.exists( plotdir ): os.makedirs( plotdir )

graphs = {}
graphs_statonly = {}
plotstyle = {
    1: ("ZZ region", ROOT.kGreen+3),
    2: ("WZ region", ROOT.kRed-2),
    3: ("ttZ region", ROOT.kAzure+4),
    "combined": ("Combination", 1),
}

for r in range(nRegions)+["combined"]:
    region = r+1 if isinstance(r, int) else r
    marginfloat = "float" if args.float else "margin"
    filename = "higgsCombine.topEFT_%s_%s_13TeV_%s_1D-%s_%s.MultiDimFit.mH125.123456.root"%(args.year, str(region), args.year, args.wc, marginfloat)
    if args.freeze is not None:
        filename = filename.replace(".MultiDimFit", "_freeze-"+args.freeze+".MultiDimFit")
    if args.statOnly:
        filename = filename.replace(".MultiDimFit", "_statOnly.MultiDimFit")
    graphs[region] = getGraphFromTree(dataCard_dir+filename, args.wc)
    outname = "1D__"+args.year+"__"+args.wc+"__"+str(region)+"__"+marginfloat+".pdf"
    if args.freeze is not None:
        outname = outname.replace(".pdf", "_freeze-"+args.freeze+".pdf")
    if args.statOnly:
        outname = outname.replace(".pdf", "_statOnly.pdf")
    xmin, xmax = -5, 7
    if args.wc in ["cHq3Re11", "cHq3Re1122"]:
        xmin, xmax = -1, 2
    if args.addStatOnly:
        filename_stat = filename.replace(".MultiDimFit", "_statOnly.MultiDimFit")
        graphs_statonly[region] = getGraphFromTree(dataCard_dir+filename_stat, args.wc)
        plotGraph(graphs[region], plotstyle[region][0], plotdir+outname, xmin, xmax, graphs_statonly[region])
    else:
        plotGraph(graphs[region], plotstyle[region][0], plotdir+outname, xmin, xmax)

outname_comp = "1D__"+args.year+"__"+args.wc+"__comparison__"+marginfloat+".pdf"
if args.freeze is not None:
    outname_comp = outname_comp.replace(".pdf", "_freeze-"+args.freeze+".pdf")
if args.statOnly:
    outname_comp = outname_comp.replace(".pdf", "_statOnly.pdf")

if args.addStatOnly:
    plotGraphComparison(graphs, plotstyle, plotdir+outname_comp, xmin, xmax, graphs_statonly)
else:
    plotGraphComparison(graphs, plotstyle, plotdir+outname_comp, xmin, xmax)
