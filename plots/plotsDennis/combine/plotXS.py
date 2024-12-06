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


def getGraphFromTree(filename, param):
    values, twodeltaNLLs = array.array( 'd' ), array.array( 'd' )
    branchname = param
    rf = ROOT.TFile.Open(filename)
    tree = getattr(rf, "limit")
    if tree.GetEntry(0)<=0:
        raise RuntimeError( "Tree of file %s is empty", filename)
    for point in tree:
        if point.deltaNLL > 0.000000001:
            # first value is the best fit with deltaNLL=0, jump this one
            values.append(eval("point."+branchname))
            twodeltaNLLs.append(2*point.deltaNLL)
    rf.Close()
    if len(values) == 0:
        values.append(0)
        twodeltaNLLs.append(0)
    graph = ROOT.TGraph(len(values), values, twodeltaNLLs)
    graph = setDrawStyle(graph, param)
    return graph

def setDrawStyle(g, param):
    g.GetYaxis().SetRangeUser(0, 8)
    g.SetTitle('')
    g.GetXaxis().SetTitle(param)
    g.GetYaxis().SetTitle('-2 #Delta ln L')
    g.SetLineWidth(2)
    return g

def plotGraph(g, legname, name, xmin, xmax):
    c = ROOT.TCanvas(name, "", 600, 600)
    ROOT.gPad.SetTopMargin(0.02)
    g.GetXaxis().SetLimits(xmin, xmax)
    g.Draw("AL")
    leg = ROOT.TLegend(.6, .25, .9, .4)
    leg.AddEntry(g, legname, "l")
    leg.Draw()
    l1, l2 = getLines(xmin, xmax)
    l1.Draw("SAME")
    l2.Draw("SAME")
    g.Draw("L SAME")
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

plotdir = plot_directory+"/XS_scans/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

path = "/users/dennis.schwarz/CMSSW_10_6_28/src/tWZ/plots/plotsDennis/combine/DataCards_threePoint_light_minus_UNBLINDED_binning-A_SMZero/ULRunII/"


files = {
    "ttZ": "higgsCombine.topEFT_ULRunII_combined_13TeV_ULRunII_TTZ_margin.MultiDimFit.mH125.123456.root",
    "WZ": "higgsCombine.topEFT_ULRunII_combined_13TeV_ULRunII_WZ_margin.MultiDimFit.mH125.123456.root",
    "ZZ": "higgsCombine.topEFT_ULRunII_combined_13TeV_ULRunII_ZZ_margin.MultiDimFit.mH125.123456.root",
}


for process in ["ttZ", "WZ", "ZZ"]:
    for freeze in [True,False]:
        xmin, xmax = -3.5, 3.5
        if process == "ZZ":
            xmax = 8.5
        # Get scan with other rates frozen at 0
        plotname = plotdir+"/XS_"+process+".pdf" if freeze else plotdir+"/XS_"+process+"_float.pdf"
        filename = path+files[process]
        if freeze:
            filename = filename.replace("margin", "float")

        graph = getGraphFromTree(filename=filename, param="rate_"+process)
        plotGraph(graph, "rate_"+process, plotname, xmin, xmax)

        bestFit,lower68,upper68,lower95,upper95 = getInterval(graph, xmin, xmax)
        txtfilename = plotname.replace(".pdf", ".txt")
        with open(txtfilename, "w") as file:
            if None in [bestFit,lower68,upper68,lower95,upper95]:
                print "Not all intervals defined, do not store txt file."
            else:
                file.write("%.2f\n"%(bestFit))
                file.write("%.2f,%.2f \n"%(lower68,upper68))
                file.write("%.2f,%.2f \n"%(lower95,upper95))
        print "Wrote values to %s"%(txtfilename)
