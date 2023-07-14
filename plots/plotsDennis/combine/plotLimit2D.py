import ROOT
import os
import array
import ctypes
import Analysis.Tools.syncer
from math                                import sqrt
from tWZ.Tools.helpers                   import getObjFromFile
from tWZ.Tools.user                      import plot_directory
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

def scanGraph(g):
    minval = -3.
    maxval = 3.
    Nsteps = 20
    stepsize = (maxval-minval)/Nsteps
    print "---------------------------------------------------------------------"
    for i in range(Nsteps):
        # x = 0
        # y = minval+i*stepsize
        x = minval+i*stepsize
        y = 0
        print x, y, g.Interpolate(x, y)

def getHist2DFromTree(filename, wcname1, wcname2):
    wc1values, wc2values, twodeltaNLLs = array.array( 'd' ), array.array( 'd' ), array.array( 'd' )
    branchname1 = "k_"+wcname1
    branchname2 = "k_"+wcname2
    rf = ROOT.TFile.Open(filename)
    tree = getattr(rf, "limit")
    if tree.GetEntry(0)<=0:
        raise RuntimeError( "Tree of file %s is empty", filename)
    for point in tree:
        if point.deltaNLL > 0.000000001:
            # first value is the best fit with deltaNLL=0, jump this one
            wc1values.append(eval("point."+branchname1))
            wc2values.append(eval("point."+branchname2))
            twodeltaNLLs.append(2*point.deltaNLL)
        else:
            bestFit_wc1 = eval("point."+branchname1)
            bestFit_wc2 = eval("point."+branchname2)
    rf.Close()
    graph = ROOT.TGraph2D( len(twodeltaNLLs), wc1values, wc2values, twodeltaNLLs)
    NpointsOneAxis = int(sqrt(len(twodeltaNLLs)))
    # scanGraph(graph)
    graph.SetNpx(NpointsOneAxis)
    graph.SetNpy(NpointsOneAxis)
    hist = graph.GetHistogram().Clone()
    # hist.Smooth()
    hist = setDrawStyle(hist, wcname1, wcname2)
    return hist, bestFit_wc1, bestFit_wc2

def setDrawStyle(h, wcname1, wcname2):
    h.SetTitle('')
    h.GetXaxis().SetTitle(wcname1)
    h.GetYaxis().SetTitle(wcname2)
    h.GetZaxis().SetTitle('-2 #Delta ln L')
    h.GetZaxis().SetTitleOffset(1.3)
    h.GetXaxis().SetNdivisions(505)
    h.GetYaxis().SetNdivisions(505)
    return h

def plot2Dlimit(h, legname, name, xmin, xmax, ymin, ymax, bestFit_wc1, bestFit_wc2):
    c = ROOT.TCanvas(name, "", 700, 600)
    ROOT.gPad.SetTopMargin(0.02)
    ROOT.gPad.SetRightMargin(0.2)
    ROOT.gStyle.SetPalette(ROOT.kSunset)

    h.GetXaxis().SetRangeUser(xmin, xmax)
    h.GetYaxis().SetRangeUser(ymin, ymax)
    # h.GetZaxis().SetRangeUser(0.01, 100)
    ROOT.gPad.SetLogz()

    # Contours
    contours = [2.28, 5.99]# (68%, 95%) for 2D
    histsForCont = h.Clone()
    c_contlist = ((ctypes.c_double)*(len(contours)))(*contours)
    histsForCont.SetContour(len(c_contlist),c_contlist)
    histsForCont.Draw("contzlist")
    c.Update()
    conts = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
    cont_p1 = conts.At(0).Clone()
    cont_p2 = conts.At(1).Clone()

    # Draw 2D hist
    h.Draw("COLZ")

    # Draw contours
    for conts in [cont_p2]:
        for cont in conts:
            cont.SetLineColor(ROOT.kAzure+7)
            cont.SetLineWidth(3)
            cont.Draw("same")
    for conts in [cont_p1]:
        for cont in conts:
            cont.SetLineColor(ROOT.kSpring-1)
            cont.SetLineWidth(3)
            cont.Draw("same")

    # SM point
    SMpoint = ROOT.TGraph(1)
    SMpoint.SetName("SMpoint")
    SMpoint.SetPoint(0, 0, 0)
    SMpoint.SetMarkerStyle(20)
    SMpoint.SetMarkerSize(2)
    SMpoint.SetMarkerColor(ROOT.kOrange+1)
    SMpoint.Draw("p same")
    # Best fit point
    BFpoint = ROOT.TGraph(1)
    BFpoint.SetName("BFpoint")
    BFpoint.SetPoint(0, bestFit_wc1, bestFit_wc2)
    BFpoint.SetMarkerStyle(29)
    BFpoint.SetMarkerSize(3)
    BFpoint.SetMarkerColor(ROOT.kCyan-3)
    BFpoint.Draw("p same")
    # legend
    leg = ROOT.TLegend(.6, .7, .75, .85)
    leg.SetHeader(legname)
    leg.AddEntry( BFpoint, "Best fit","p")
    leg.AddEntry( SMpoint, "SM","p")
    leg.AddEntry( cont_p1.At(0), "68%s CL"%"%", "l")
    leg.AddEntry( cont_p2.At(0), "95%s CL"%"%", "l")
    leg.Draw()
    # Draw
    ROOT.gPad.RedrawAxis()
    c.Print(name)

################################################################################
################################################################################
################################################################################
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
argParser.add_argument('--wc',               action='store', type=str, default="cHq1Re11-cHq1Re33")
argParser.add_argument('--float',            action='store_true', default=False)
argParser.add_argument('--freeze',           action='store', type=str, default=None)
argParser.add_argument('--statOnly',         action='store_true', default=False)
argParser.add_argument('--light',            action='store_true', default=False)
args = argParser.parse_args()

logger.info( "Make 2D limit plot")

WCnames = ["cHq1Re11", "cHq1Re22", "cHq1Re33", "cHq3Re11", "cHq3Re22", "cHq3Re33"]
if args.light:
    WCnames = ["cHq1Re1122", "cHq1Re33", "cHq3Re1122", "cHq3Re33"]

if args.year not in ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]:
    raise RuntimeError( "Year %s is not knwon", args.year)
logger.info( "Year = %s", args.year )

if not "-" in args.wc:
    raise RuntimeError( "Argument for --wc has wrong format. Should be --wc=wc1-wc2" )
if len(args.wc.split("-")) != 2:
    raise RuntimeError( "Argument for --wc has wrong format. Should be --wc=wc1-wc2" )

wcname1 = args.wc.split("-")[0]
wcname2 = args.wc.split("-")[1]


if wcname1 not in WCnames:
    raise RuntimeError( "Wilson coefficient %s is not knwon", wcname1)
if wcname2 not in WCnames:
    raise RuntimeError( "Wilson coefficient %s is not knwon", wcname2)
logger.info( "Wilson coefficients = %s and %s", wcname1, wcname2 )

uncertaintyGroups = ["btag","jet","lepton","lumi","nonprompt","other_exp","rate_bkg","rate_sig","theory"]
if args.freeze is not None:
    if args.statOnly:
        raise RuntimeError( "Cannot run statOnly AND freeze nuisance groups" )
    for group in args.freeze.split("-"):
        if group not in uncertaintyGroups:
            raise RuntimeError( "Uncertainty group %s not known. You also might have used a wrong format: --freeze=btag-jec", group )

nRegions = 3
logger.info( "Number of regions: %s", nRegions)

this_dir = os.getcwd()
if args.light:
    dataCard_dir = this_dir+"/DataCards_threePoint_light/"+args.year+"/"


plotdir = plot_directory+"/Limits_UL_threePoint/"+args.year+"/"
if args.light:
    plotdir = plot_directory+"/Limits_UL_threePoint_light/"+args.year+"/"

if not os.path.exists( plotdir ): os.makedirs( plotdir )

plotstyle = {
    1: ("ZZ region", ROOT.kGreen+3),
    2: ("WZ region", ROOT.kRed-2),
    3: ("ttZ region", ROOT.kAzure+4),
    "combined": ("Combination", 1),
}

for r in range(nRegions)+["combined"]:
    region = r+1 if isinstance(r, int) else r
    marginfloat = "float" if args.float else "margin"
    filename = "higgsCombine.topEFT_%s_%s_13TeV_%s_2D-%s_%s.MultiDimFit.mH125.123456.root"%(args.year, str(region), args.year, args.wc, marginfloat)
    if args.freeze is not None:
        filename = filename.replace(".MultiDimFit", "_freeze-"+args.freeze+".MultiDimFit")
    if args.statOnly:
        filename = filename.replace(".MultiDimFit", "_statOnly.MultiDimFit")
    hist, bestFit_wc1, bestFit_wc2 = getHist2DFromTree(dataCard_dir+filename, wcname1, wcname2)
    outname = "2D__"+args.year+"__"+args.wc+"__"+str(region)+"__"+marginfloat+".pdf"
    if args.freeze is not None:
        outname = outname.replace(".pdf", "_freeze-"+args.freeze+".pdf")
    if args.statOnly:
        outname = outname.replace(".pdf", "_statOnly.pdf")
    xmin, xmax = -4.5, 4.5
    if wcname1 in ["cHq3Re11","cHq3Re1122"]:
        xmin, xmax = -0.5, 0.5
        if region == "combined" or region == 2:
            xmin, xmax = -0.2, 0.2
    ymin, ymax = -4.5, 4.5
    if wcname2 in ["cHq3Re11","cHq3Re1122"]:
        ymin, ymax = -0.5, 0.5
        if region == "combined" or region == 2:
            ymin, ymax = -0.2, 0.2
    plot2Dlimit(hist, plotstyle[region][0], plotdir+outname, xmin, xmax, ymin, ymax, bestFit_wc1, bestFit_wc2)
