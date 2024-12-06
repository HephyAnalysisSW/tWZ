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

    # l68, u68, l95, u95 = None, None, None, None
    # if len(lower68) == 1:
    #     l68 = lower68[0]
    # if len(upper68) == 1:
    #     u68 = upper68[0]
    # if len(lower95) == 1:
    #     l95 = lower95[0]
    # if len(upper95) == 1:
    #     u95 = upper95[0]
    #
    # print "Best fit =", bestFit, "| 68%: (",l68,",",u68,")", "95%: (",l95,",",u95,")"
    # return bestFit, l68, u68, l95, u95
    print "Best fit =", bestFit
    if len(lower68) != len(upper68):
        print("[ERROR] Found %i lower bounds but %i upper bounds for 68CL"%(len(lower68),len(upper68)))
        lower68 = None
        upper68 = None
    else:
        for i,l68 in enumerate(lower68):
            print "68CL: (",lower68[i],",", upper68[i],")"
    if len(lower95) != len(upper95):
        print("[ERROR] Found %i lower bounds but %i upper bounds for 95CL"%(len(lower95),len(upper95)))
        lower95 = None
        upper95 = None
    else:
        for i,l95 in enumerate(lower95):
            print "95CL: (",lower95[i],",", upper95[i],")"
    return bestFit, lower68, upper68, lower95, upper95

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
argParser.add_argument('--half', action='store_true', default=False)
argParser.add_argument('--noQuad',               action='store_true', default=False)

args = argParser.parse_args()

logger.info( "Make 1D limit plot")

WCnames = ["cHq1Re11", "cHq1Re22", "cHq1Re33", "cHq3Re11", "cHq3Re22", "cHq3Re33"]
if args.light:
    WCnames = ["cHq1Re1122", "cHq1Re33", "cHq3Re1122", "cHq3Re33"]
    if args.minus:
        WCnames = ["cHqMRe1122", "cHqMRe33", "cHq3MRe1122", "cHq3MRe33", "cHuRe1122", "cHuRe33", "cHdRe1122", "cHdRe33", "cW", "cWtil"]
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
if args.noQuad:                  dirname_suffix+="_noQuad"
if args.noBB:                  dirname_suffix+="_noBB"
if args.binning != "default":  dirname_suffix+="_binning-"+args.binning
if args.sysMode != "default":    dirname_suffix+="_"+args.sysMode
if args.noZero:                  dirname_suffix+="_noZero"
if args.SMZero:                  dirname_suffix+="_SMZero"
if args.half:                  dirname_suffix+="_HALF"

this_dir = os.getcwd()
dataCard_dir = this_dir+"/DataCards_threePoint"+dirname_suffix+"/"+args.year+"/"
plotdir = plot_directory+"/Limits_UL_threePoint"+dirname_suffix+"/"+args.year+"/"

if not os.path.exists( plotdir ): os.makedirs( plotdir )

graphs = {}
graphs_statonly = {}
plotstyle = {
    1: ("ZZ region", ROOT.kGreen+3),
    2: ("WZ region", ROOT.kRed-2),
    3: ("ttZ region", ROOT.kAzure+4),
    "combined": ("Combination", 1),
}
if args.NjetSplit:
    plotstyle = {
        1: ("ZZ region", ROOT.kGreen+3),
        2: ("WZ region", ROOT.kRed-2),
        3: ("ttZ (3j) region", ROOT.kAzure+4),
        4: ("ttZ (4+j) region", ROOT.kBlue),
        "combined": ("Combination", 1),
    }

for r in range(nRegions)+["combined"]:
    # for r in [2]:
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
    if args.wc in ["cHq3Re11", "cHq3Re1122", "cHq3MRe11", "cHq3MRe1122", "cW", "cWtil"]:
        xmin, xmax = -1, 2
        if args.wc in ["cW", "cWtil"] and args.noQuad:
            xmin, xmax = -4.8, 10.0
    if args.wc in ["cHq3MRe33"]:
        xmin, xmax = -8, 7
        if args.float:
            xmin, xmax = -13.9, 13.9
        if args.noQuad:
            xmin, xmax = -15, 24
    if args.wc in ["cHdRe33"]:
        xmin, xmax = -39.9, 39.9
    if args.wc in ["cHqMRe33"] and args.float:
        xmin, xmax = -9.9, 29.9
    if args.wc in ["cHuRe33"] and args.float:
        xmin, xmax = -29.9, 29.9


    bestFit,lower68,upper68,lower95,upper95 = getInterval(graphs[region], xmin, xmax)
    txtfilename = plotdir+outname.replace(".pdf", ".txt")
    with open(txtfilename, "w") as file:
        if None in [bestFit,lower68,upper68,lower95,upper95]:
            print "Not all intervals defined, do not store txt file."
        else:
            file.write("%.2f\n"%(bestFit))
            if lower68 is not None:
                for i, l68 in enumerate(lower68):
                    file.write("%.2f,%.2f;"%(lower68[i],upper68[i]))
                file.write("\n")
            if lower95 is not None:
                for i, l95 in enumerate(lower95):
                    file.write("%.2f,%.2f;"%(lower95[i],upper95[i]))
                file.write("\n")
    print "Wrote values to %s"%(txtfilename)
    if args.addStatOnly:
        filename_stat = filename.replace(".MultiDimFit", "_statOnly.MultiDimFit")
        if args.freeze is not None:
            filename_stat = filename_stat.replace("_freeze-"+args.freeze, "")
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
