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

def getCMS(x,y,x2,y2,prelim=False):
    labels = []
    cmstext = ROOT.TLatex(3.5, 24, "CMS")
    cmstext.SetNDC()
    cmstext.SetTextAlign(11)
    cmstext.SetTextFont(62)
    cmstext.SetTextSize(0.06)
    cmstext.SetX(x)
    cmstext.SetY(y)
    labels.append(cmstext)
    if prelim:
        prelimtext = ROOT.TLatex(3.5, 24, "Preliminary")
        prelimtext.SetNDC()
        prelimtext.SetTextAlign(11)
        prelimtext.SetTextFont(52)
        prelimtext.SetTextSize(0.04)
        prelimtext.SetX(x+0.12)
        prelimtext.SetY(y)
        labels.append(prelimtext)
    lumitext = ROOT.TLatex(3.5, 24, "138 fb^{-1} (13 TeV)")
    lumitext.SetNDC()
    lumitext.SetTextAlign(31)
    lumitext.SetTextFont(42)
    lumitext.SetTextSize(0.045)
    lumitext.SetX(x2)
    lumitext.SetY(y2)
    labels.append(lumitext)
    return labels

# def scanGraph(g):
#     minval = -3.
#     maxval = 3.
#     Nsteps = 20
#     stepsize = (maxval-minval)/Nsteps
#     print "---------------------------------------------------------------------"
#     for i in range(Nsteps):
#         # x = 0
#         # y = minval+i*stepsize
#         x = minval+i*stepsize
#         y = 0
#         print x, y, g.Interpolate(x, y)

def getHist2DFromTree(filenames, wcname1, wcname2):
    wc1values, wc2values, twodeltaNLLs = array.array( 'd' ), array.array( 'd' ), array.array( 'd' )
    branchname1 = "k_"+wcname1
    branchname2 = "k_"+wcname2
    bestFit_wc1 = 0
    bestFit_wc2 = 0
    minDeltaNLL = 10000000000000000
    for filename in filenames:
        logger.info( "Reading file = %s", filename )
        if not os.path.exists(filename):
            print("File %s Does not exist! Skipping..."%(filename))
            continue
        rf = ROOT.TFile.Open(filename)
        tree = getattr(rf, "limit")
        if tree.GetEntry(0)<=0:
            raise RuntimeError( "Tree of file %s is empty", filename)
        # First find minimum
        for point in tree:
            wc1values.append(eval("point."+branchname1))
            wc2values.append(eval("point."+branchname2))
            twodeltaNLLs.append(2*(point.deltaNLL-minDeltaNLL))
            if args.ignoreNegative and point.deltaNLL < 0:
                continue
            if point.deltaNLL < minDeltaNLL:
                minDeltaNLL = point.deltaNLL
                bestFit_wc1 = eval("point."+branchname1)
                bestFit_wc2 = eval("point."+branchname2)
        rf.Close()

    print "min(deltaNLL) = %.3f"%(minDeltaNLL)
    graph = ROOT.TGraph2D( len(twodeltaNLLs), wc1values, wc2values, twodeltaNLLs)
    NpointsOneAxis = int(sqrt(len(twodeltaNLLs)))
    # scanGraph(graph)
    graph.SetNpx(NpointsOneAxis)
    graph.SetNpy(NpointsOneAxis)
    hist = graph.GetHistogram().Clone()
    hist.Smooth()
    hist = setDrawStyle(hist, wcname1, wcname2)
    print "Best fit:", wcname1, "=", bestFit_wc1, "---" , wcname2, "=", bestFit_wc2
    return hist, bestFit_wc1, bestFit_wc2

def setDrawStyle(h, wcname1, wcname2):
    from tWZ.Tools.histogramHelper import WClatexNames
    h.SetTitle('')
    h.GetXaxis().SetTitle(WClatexNames[wcname1])
    h.GetYaxis().SetTitle(WClatexNames[wcname2])
    h.GetZaxis().SetTitle('#minus 2 #Delta ln L')
    h.GetXaxis().SetTitleOffset(1.1)
    h.GetYaxis().SetTitleOffset(0.9)
    h.GetZaxis().SetTitleOffset(1.1)
    h.GetXaxis().SetNdivisions(505)
    h.GetYaxis().SetNdivisions(505)
    return h

def plot2Dlimit(h, legname, name, xmin, xmax, ymin, ymax, bestFit_wc1, bestFit_wc2, addText=None):
    c = ROOT.TCanvas(name, "", 700, 600)
    topmargin = 0.08
    rightmargin = 0.18
    leftmargin = 0.12
    bottommargin = 0.15

    ROOT.gPad.SetTopMargin(topmargin)
    ROOT.gPad.SetRightMargin(rightmargin)
    ROOT.gPad.SetLeftMargin(leftmargin)
    ROOT.gPad.SetBottomMargin(bottommargin)
    ROOT.gStyle.SetPalette(ROOT.kSunset)

    h.GetXaxis().SetRangeUser(xmin, xmax)
    h.GetYaxis().SetRangeUser(ymin, ymax)
    zmax = h.GetMaximum()
    h.GetZaxis().SetRangeUser(0.01, zmax)
    if not args.unblind:
        h.GetZaxis().SetRangeUser(0.01, zmax)

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
    # leg = ROOT.TLegend(.15, .77, 1.0-rightmargin-0.03, 1.0-topmargin-0.02)
    leg = ROOT.TLegend(.25, .77, 0.7, 1.0-topmargin-0.02)
    leg.SetTextSize(.035)
    leg.SetNColumns(2)
    if legname is not None:
        leg.SetHeader(legname)
    leg.AddEntry( BFpoint, "Best fit","p")
    leg.AddEntry( cont_p1.At(0), "#minus 2 #Delta ln L < 2.28", "l")
    leg.AddEntry( SMpoint, "SM","p")
    leg.AddEntry( cont_p2.At(0), "#minus 2 #Delta ln L < 5.99", "l")
    leg.Draw()
    # CMSlabel
    x_CMS = leftmargin
    y_CMS = 1.0-topmargin+0.01
    x_lumi = 1.0-rightmargin
    y_lumi = 1.0-topmargin+0.01
    labels = getCMS(x_CMS, y_CMS, x_lumi, y_lumi, False)
    for l in labels:
        l.Draw()

    # add text
    texts = []
    if addText is not None:
        latex = ROOT.TLatex(3.5, 24, addText)
        latex.SetNDC()
        latex.SetTextAlign(13)
        latex.SetTextFont(63)
        latex.SetTextSize(24)
        latex.SetX(0.15)
        latex.SetY(0.22)
        texts.append(latex)
    for t in texts:
        t.Draw()



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
argParser.add_argument('--minus',            action='store_true', default=False)
argParser.add_argument('--NjetSplit',        action='store_true', default=False)
argParser.add_argument('--scaleCorrelation', action='store_true', default=False)
argParser.add_argument('--signalInjectionLight',  action='store_true', default=False)
argParser.add_argument('--signalInjectionHeavy',  action='store_true', default=False)
argParser.add_argument('--signalInjectionMixed',  action='store_true', default=False)
argParser.add_argument('--signalInjectionWZjets',  action='store_true', default=False)
argParser.add_argument('--unblind',          action='store_true', default=False)
argParser.add_argument('--BBmode',         action='store', default="default")
argParser.add_argument('--noQuad',               action='store_true', default=False)
argParser.add_argument('--fluctuatePseudoData',  action='store_true', default=False)
argParser.add_argument('--onlyCombined',  action='store_true', default=False)
argParser.add_argument('--binning',          action='store', default="default")
argParser.add_argument('--sysMode',          action='store', default="default")
argParser.add_argument('--onlyRegion',          action='store', default=None)
argParser.add_argument('--ignoreNegative',  action='store_true', default=False)
argParser.add_argument('--noZero', action='store_true', default=False)
argParser.add_argument('--SMZero', action='store_true', default=False)
argParser.add_argument('--split', action='store', type=int, default=None)
args = argParser.parse_args()

logger.info( "Make 2D limit plot")
ranges = {
    "cHqMRe1122":  (-2.5, 2.5),
    "cHqMRe33":    (-5.5,5.5),
    "cHq3MRe1122": (-0.28,0.28),
    "cHq3MRe33":   (-14.5,14.5),
    "cHuRe1122":   (-6.9,6.9),
    "cHuRe33":     (-9.9,9.9),
    "cHdRe1122":   (-5.9,5.9),
    "cHdRe33":     (-34,49),
    "cW":          (-0.26,0.26),
    "cWtil":       (-0.26,0.26),
}

if args.float:
    ranges["cHqMRe33"] = (-9.0, 39)
    ranges["cHuRe33"] = (-29, 33)

if "cHuRe33" in args.wc and "cHqMRe33" in args.wc:
    ranges["cHqMRe33"] = (-45, 45)
    ranges["cHuRe33"] = (-45, 45)

WCnames = ["cHq1Re11", "cHq1Re22", "cHq1Re33", "cHq3Re11", "cHq3Re22", "cHq3Re33"]
if args.light:
    WCnames = ["cHq1Re1122", "cHq1Re33", "cHq3Re1122", "cHq3Re33"]
    if args.minus:
        WCnames = ["cHqMRe1122", "cHqMRe33", "cHq3MRe1122", "cHq3MRe33", "cHuRe1122", "cHuRe33", "cHdRe1122", "cHdRe33", "cW", "cWtil"]

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

uncertaintyGroups = ["autoMCStats","btag","ewk","jet","lepton","lumi","nonprompt","other_exp","pdf","ps","rate_bkg","rate_sig","scale_bkg","scale_sig","wz"]
if args.freeze is not None:
    if args.statOnly:
        raise RuntimeError( "Cannot run statOnly AND freeze nuisance groups" )
    for group in args.freeze.split("-"):
        if group not in uncertaintyGroups:
            raise RuntimeError( "Uncertainty group %s not known. You also might have used a wrong format: --freeze=btag-jec", group )

nRegions = 4 if args.NjetSplit else 3

if args.onlyCombined:
    nRegions = 0 # combined region is added later
    logger.info( "Only plot combined region")
    extraRegion = ["combined"]
elif args.onlyRegion is not None:
    nRegions = 0 # combined region is added later
    logger.info( "Only plot %s region", args.onlyRegion)
    extraRegion = [args.onlyRegion]
else:
    logger.info( "Number of regions: %s", nRegions)
    extraRegion = ["combined"]

dirname_suffix = ""
if args.light:               dirname_suffix+="_light"
if args.minus:               dirname_suffix+="_minus"
if args.NjetSplit:           dirname_suffix+="_NjetSplit"
if args.scaleCorrelation:    dirname_suffix+="_scaleCorrelation"
if args.signalInjectionLight:     dirname_suffix+="_signalInjectionLight"
if args.signalInjectionHeavy:     dirname_suffix+="_signalInjectionHeavy"
if args.signalInjectionMixed:     dirname_suffix+="_signalInjectionMixed"
if args.signalInjectionWZjets:    dirname_suffix+="_signalInjectionWZjets"
if args.fluctuatePseudoData:      dirname_suffix+="_fluctuatePseudoData"
if args.unblind:                  dirname_suffix+="_UNBLINDED"
if args.noQuad:                  dirname_suffix+="_noQuad"
if args.BBmode != "default":
    dirname_suffix+="_"+args.BBmode
if args.binning != "default":    dirname_suffix+="_binning-"+args.binning
if args.sysMode != "default":    dirname_suffix+="_"+args.sysMode
if args.noZero:                  dirname_suffix+="_noZero"
if args.SMZero:                  dirname_suffix+="_SMZero"

this_dir = os.getcwd()
dataCard_dir = this_dir+"/DataCards_threePoint"+dirname_suffix+"/"+args.year+"/"
plotdir = plot_directory+"/Limits_UL_threePoint"+dirname_suffix+"/"+args.year+"/"

if not os.path.exists( plotdir ): os.makedirs( plotdir )

plotstyle = {
    1: ("ZZ region", ROOT.kGreen+3),
    2: ("WZ region", ROOT.kRed-2),
    3: ("ttZ region", ROOT.kAzure+4),
    "combined": ("", 1),
    "ZZ-WZ": ("ZZ+WZ regions", 1),
    "ZZ-ttZ": ("ZZ+ttZ regions", 1),
    "WZ-ttZ": ("WZ+ttZ regions", 1),
}
if args.NjetSplit:
    plotstyle = {
        1: ("ZZ region", ROOT.kGreen+3),
        2: ("WZ region", ROOT.kRed-2),
        3: ("ttZ (3j) region", ROOT.kAzure+4),
        4: ("ttZ (4+j) region", ROOT.kBlue),
        "combined": ("Combination", 1),
    }

for r in range(nRegions)+extraRegion:
    region = r+1 if isinstance(r, int) else r
    marginfloat = "float" if args.float else "margin"
    filename = "higgsCombine.topEFT_%s_%s_13TeV_%s_2D-%s_%s.MultiDimFit.mH125.123456.root"%(args.year, str(region), args.year, args.wc, marginfloat)
    if args.freeze is not None:
        filename = filename.replace(".MultiDimFit", "_freeze-"+args.freeze+".MultiDimFit")
    if args.statOnly:
        filename = filename.replace(".MultiDimFit", "_statOnly.MultiDimFit")

    if args.split is not None:
        filenames = [dataCard_dir+filename.replace(".MultiDimFit", "_SPLIT_%i.MultiDimFit"%(i)) for i in range(args.split)]
    else:
        filenames = [dataCard_dir+filename]

    hist, bestFit_wc1, bestFit_wc2 = getHist2DFromTree(filenames, wcname1, wcname2)
    outname = "2D__"+args.year+"__"+args.wc+"__"+str(region)+"__"+marginfloat+".pdf"
    if args.freeze is not None:
        outname = outname.replace(".pdf", "_freeze-"+args.freeze+".pdf")
    if args.statOnly:
        outname = outname.replace(".pdf", "_statOnly.pdf")
    if args.ignoreNegative:
        outname = outname.replace(".pdf", "_ignoreNegative.pdf")
    xmin, xmax = ranges[wcname1]
    ymin, ymax = ranges[wcname2]
    legheader =  plotstyle[region][0]+" (profiled)" if args.float else plotstyle[region][0]+" (fixed)"
    addText = None
    if region == "combined":
        legheader = None
        addText = "Profiled" if args.float else "Fixed"

    plot2Dlimit(hist, legheader, plotdir+outname, xmin, xmax, ymin, ymax, bestFit_wc1, bestFit_wc2, addText)
    resultfile = plotdir+outname.replace(".pdf", ".root")
    f_out = ROOT.TFile(resultfile, "RECREATE")
    f_out.cd()
    hist.Write("scan")
    f_out.Close()
