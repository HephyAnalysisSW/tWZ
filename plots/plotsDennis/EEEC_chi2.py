#!/usr/bin/env python

import os
import ROOT
import array
import numpy as np
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from MyRootTools.plotter.Plotter                 import Plotter
from math                                        import sqrt

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--nowidth',      action='store_true')
argParser.add_argument('--scaleSYS',     action='store', default=1.0)
argParser.add_argument('--scaleSTAT',    action='store', default=1.0)
args = argParser.parse_args()

normWidth = True
if args.nowidth:
    normWidth = False

ROOT.gROOT.SetBatch(ROOT.kTRUE)
# binning = [1.8, 2.0, 2.2]
# binning = [0.0, 1.0, 1.4, 1.8, 2.2]
binning = [0.0, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 3.0]

# binning = [0.0, 0.6, 1.4, 1.8, 2.4]
# binning = []
# Nbins = 30 
# min = 0.0
# max = 3.0
# stepsize = (max-min)/Nbins
# for i in range(Nbins):
#     binning.append(min+i*stepsize)
# binning.append(max)


def rebinhist(hist):
    h_new = hist.Rebin(len(binning)-1, hist.GetName()+"_rebin", array.array('d', binning) )
    return h_new

def getDelta(nominal, variation):
    h_delta = ROOT.TH1D(variation.GetName()+"_delta", "3 zeta", len(binning)-1, array.array('d', binning))
    Nbins = len(binning)-1
    for i in range(Nbins):
        bin = i+1
        diff = variation.GetBinContent(bin)-nominal.GetBinContent(bin)
        h_delta.SetBinContent(bin, diff)
    return h_delta
    
def averageDelta(down, up, nominal):
    h_delta = ROOT.TH1D(up.GetName()+down.GetName()+"_average", "3 zeta", len(binning)-1, array.array('d', binning))
    Nbins = len(binning)-1
    mean = nominal.GetMean()
    mean_up = up.GetMean()
    mean_down = down.GetMean()
    shift_up = abs(mean-mean_up)
    shift_down = abs(mean-mean_down)
    for i in range(Nbins):
        bin = i+1
        diff_up = up.GetBinContent(bin)-nominal.GetBinContent(bin)
        diff_down = down.GetBinContent(bin)-nominal.GetBinContent(bin)
        sign = diff_up/abs(diff_up) if shift_up > shift_down else diff_down/abs(diff_down)
        average = sign * (abs(diff_up)+abs(diff_down))/2
        h_delta.SetBinContent(bin, average)
    return h_delta    
    
def getCovFromDelta(delta):
    cov = ROOT.TH2D(delta.GetName()+"_cov", "cov", len(binning)-1, array.array('d', binning), len(binning)-1, array.array('d', binning))
    Nbins = len(binning)-1
    for i in range(Nbins):
        for j in range(Nbins):
            bini = i+1
            binj = j+1
            SF = float(args.scaleSYS)
            entry = (SF*SF)*delta.GetBinContent(bini) * delta.GetBinContent(binj)
            cov.SetBinContent(bini, binj, entry)    
    return cov

def getCovFromStat(hist):
    cov = ROOT.TH2D(hist.GetName()+"_stat_cov", "cov", len(binning)-1, array.array('d', binning), len(binning)-1, array.array('d', binning))
    Nbins = len(binning)-1
    for i in range(Nbins):
        bin = i+1
        SF = float(args.scaleSTAT)
        err = hist.GetBinError(bin)*SF
        cov.SetBinContent(bin, bin, err*err)
    return cov

def getCovDummy(hist):
    cov = ROOT.TH2D("DummyCov", "cov", len(binning)-1, array.array('d', binning), len(binning)-1, array.array('d', binning))
    Nbins = len(binning)-1
    for i in range(Nbins):
        for j in range(Nbins):
            bini = i+1
            binj = j+1
            erri = 0.3*hist.GetBinContent(bini)
            errj = 0.3*hist.GetBinContent(binj)
            cov.SetBinContent(bini, binj, erri*errj)
    return cov

def normalizeCov(cov, nominal, width):
    cov_norm = ROOT.TH2D(cov.GetName()+"_norm", "cov norm", len(binning)-1, array.array('d', binning), len(binning)-1, array.array('d', binning))
    Nbins = len(binning)-1
    integral = nominal.Integral()
    for i in range(Nbins):
        for j in range(Nbins):
            bini = i+1
            binj = j+1
            sum = 0;
            derivation_i = 0;
            derivation_j = 0;
            for k in range(Nbins):
                for l in range(Nbins):
                    bink = k+1
                    binl = l+1
                    old_entry = cov.GetBinContent(bink,binl)
                    binwidth_i = nominal.GetBinWidth(bini)
                    binwidth_j = nominal.GetBinWidth(binj)
                    if not width:
                        binwidth_i = 1.0
                        binwidth_j = 1.0

                    if bini==bink: 
                        derivation_i = (integral - nominal.GetBinContent(bini)) / (integral*integral) * (1/binwidth_i)
                    else:          
                        derivation_i = - (nominal.GetBinContent(bini))          / (integral*integral) * (1/binwidth_i)
                    if binj==binl: 
                        derivation_j = (integral - nominal.GetBinContent(binj)) / (integral*integral) * (1/binwidth_j)
                    else:     
                        derivation_j = - (nominal.GetBinContent(binj))          / (integral*integral) * (1/binwidth_j)
                    sum += derivation_i * derivation_j * old_entry
            cov_norm.SetBinContent(bini, binj, sum)
    return cov_norm

def drawDelta(delta, plotname, dir):
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetOptStat(0)
    c = ROOT.TCanvas("c", "c", 600, 600)
    ROOT.gPad.SetRightMargin(0.19)
    ROOT.gPad.SetLeftMargin(0.19)
    ROOT.gPad.SetBottomMargin(0.12)
    delta.SetTitle(" ")
    delta.GetXaxis().SetTitle("3 #zeta")
    delta.GetYaxis().SetTitle("variation-nominal")
    delta.SetLineColor(ROOT.kRed)
    delta.SetFillColor(ROOT.kRed)
    delta.Draw("HIST")
    c.Print(dir+plotname+".pdf")

        
def drawCov(cov, plotname, dir):
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPalette(ROOT.kSunset)
    c = ROOT.TCanvas("c", "c", 600, 600)
    ROOT.gPad.SetRightMargin(0.19)
    ROOT.gPad.SetLeftMargin(0.19)
    ROOT.gPad.SetBottomMargin(0.12)
    cov.SetTitle(" ")
    cov.GetXaxis().SetTitle("3 #zeta")
    cov.GetYaxis().SetTitle("3 #zeta")
    cov.Draw("COLZ")
    cov.Draw("BOX SAME")    
    c.Print(dir+plotname+".pdf")


def reduceCondition(mat, diag, step, condition_threshold):
    done = False
    counter = 0
    while not done:
        condition = np.linalg.cond(mat)
        if condition < condition_threshold:
            done = True 
        else:
            mat += step*diag
            counter += 1
    print "needed %i steps and added diagonal values of %.5f" %(counter, counter*step) 
    return mat


def svdsolve(A):
    u, s, v = np.linalg.svd(A)
    Ainv = np.dot(v.transpose(), np.dot(np.diag(s**-1), u.transpose()))
    return Ainv
    
def compute_chi2(template_hist, data_hist, cov):
    # type: (Any, Any, np.ndarray) -> float
    Nbins = len(binning)-1
    template_hist_cont = np.zeros((Nbins), dtype=np.float64)
    data_hist_cont = np.zeros((Nbins), dtype=np.float64)
    bin_list = list(range(Nbins))
    for idx, bin_nbr in enumerate(bin_list):
        template_hist_cont[idx] = template_hist.GetBinContent(bin_nbr+1)
        data_hist_cont[idx] = data_hist.GetBinContent(bin_nbr+1)
    d_vec = data_hist_cont - template_hist_cont

    # Create diagonal matrix
    diag = np.zeros((Nbins, Nbins), dtype=np.float64)
    for i in range(Nbins):
        diag[i,i] = 1.0
        
    # remove a bin 
    d_vec = np.delete(d_vec, 0)
    cov = np.delete(np.delete(cov, 0, 0), 0, 1)
    diag = np.delete(np.delete(diag, 0, 0), 0, 1)
    ###
    
    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    # newcov = reduceCondition(cov, diag, 0.0000001, 10)
    newcov = cov
    print "condition number =", np.linalg.cond(newcov)
    print "determinant =", np.linalg.det(newcov)
    # print newcov
    
    # cov_inv = svdsolve(newcov)
    cov_inv = np.linalg.inv(newcov)
    # cov_inv = np.linalg.inv(np.linalg.cholesky(newcov))
    print np.dot(cov_inv, newcov)
    # print np.dot(cov_inv2, newcov)
    chi2 = np.linalg.multi_dot([d_vec, cov_inv, d_vec])
    
    return chi2
    
def compute_chi2_test(template_hist, data_hist, cov):
    Nbins = len(binning)-1
    bins = []
    for i in range(Nbins):
        bin = i+1
        if bin != 1:
            bins.append(bin)

            
    vDiff = ROOT.TVectorD(len(bins))
    
    mat = ROOT.TMatrixDSym(len(bins))
    
    for i, bini in enumerate(bins):
        vDiff[i] = data_hist.GetBinContent(bini)-template_hist.GetBinContent(bini)
        for j, binj in enumerate(bins):
            mat[i][j] = cov.GetBinContent(bini, binj)
        
    # mat.SetTol(1.e-20)
    # mat.Invert()
    matinv = ROOT.TDecompChol(mat).Invert()
    

    # chi2 = vDiff * imat * vDiff
    # First do right part imat*vDiff
    vRight = ROOT.TVectorD(len(bins))
    for i in range(len(bins)):
        for j in range(len(bins)):
            vRight[i] = vRight[i] + matinv[i][j] * vDiff[j]

    # Now left part chi2 = vDiff * right
    chi2 = 0 
    for i in range(len(bins)):
        chi2 += vDiff[i]*vRight[i]
        
    # print "chi2 =",  chi2 

    return chi2


def TH2toNP(cov):
    Nbins = len(binning)-1
    matrix = np.zeros((Nbins, Nbins), dtype=np.float64)
    for i in range(Nbins):
        for j in range(Nbins):
            bini = i+1
            binj = j+1
            matrix[i,j] = cov.GetBinContent(bini,binj)
    return matrix
    
def measureMtop(graph):
    fit_func = ROOT.TF1('pol2_fit', 'pol2', 170, 175)
    graph.Fit(fit_func, 'QR')
    fit = graph.GetFunction('pol2_fit')
    
    minY = fit.GetMinimum()
    mtop = fit.GetX(minY, 170, 175)
    sigmaUp = fit.GetX(minY+1, mtop, 175) - mtop
    sigmaDown = mtop - fit.GetX(minY+1, 170, mtop)
    
    return (mtop, sigmaUp, sigmaDown)
    
def getBinGraphs(histdict, factors):
    (hist, _) = histdict[factors[0]]
    Nbins = hist.GetSize()-2
    graphs = {}
    for i in range(Nbins):
        bin = i+1
        content = []
        error = []
        xerror = []
        for f in factors:
            (hist, _) = histdict[f]
            content.append(hist.GetBinContent(bin))
            error.append(hist.GetBinError(bin))
            xerror.append(0)
        g = ROOT.TGraphErrors(len(factors), array.array('d', factors), array.array('d', content), array.array('d', xerror), array.array('d', error)  )
        graphs[bin] = g    
    return graphs

def drawBinGraph(graph, name):
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetOptStat(0)
    c = ROOT.TCanvas("c", "c", 600, 600)
    ROOT.gPad.SetLeftMargin(0.19)
    ROOT.gPad.SetBottomMargin(0.12)
    leg = ROOT.TLegend(.3, .5, .7, .8)
    graph.SetTitle(" ")
    graph.GetXaxis().SetTitle("f")
    graph.GetYaxis().SetTitle("bin content")
    graph.SetLineColor(1)
    graph.SetMarkerColor(1)
    graph.SetMarkerStyle(20)
    graph.Draw("AP")
    line_func = ROOT.TF1('pol1_fit', 'pol1')
    graph.Fit(line_func)
    fit = graph.GetFunction('pol1_fit')
    fit.SetLineColor(ROOT.kRed)
    fit.Draw("SAME")
    plotdir = plot_directory+"/EEECplots/"
    if not os.path.exists( plotdir ): os.makedirs( plotdir )
    c.Print(plotdir+name+".pdf")
################################################################################    
    
plotdir = plot_directory+"/EEECplots/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

filename = "/users/dennis.schwarz/correlator_hist_trip_28.root" 
histdir = "Top-Quark/Gen-Level/weighted/"

histname = "correlator_hist_Gen_None_450_500"

colors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen-2, 798, ROOT.kAzure+7, ROOT.kMagenta, ROOT.kRed+3, ROOT.kGreen+3]
masses = [171.5, 171.75, 172.0, 172.25, 172.75, 173.0, 173.25, 173.5]
# masses = [171.5, 172.0, 173.0, 173.5]
# ptfactors = [0.9, 0.95, 0.98, 0.99, 1.01, 1.02, 1.05, 1.1]
ptfactors = [0.95, 0.98, 0.99, 1.01, 1.02, 1.05]

h_central = rebinhist(getObjFromFile(filename, histdir+histname))
h_masses = {}
h_ptvars = {}

for i,m in enumerate(masses):
    hname = histdir+histname.replace("None", str(m))
    h_masses[m] = (rebinhist(getObjFromFile(filename, hname)), colors[i] )
    
p = Plotter("EEEC_masses")
p.plot_dir = plotdir
p.drawRatio = True
p.ratiorange = (0.7, 1.3)
p.xtitle = "3#zeta"
# p.legshift = (0.15, 0., 0.15, 0.)
p.yfactor = 1.3
p.addBackground(h_central, "172.5", 15)
for m in masses:
    (hist, color) = h_masses[m]
    p.addSignal(hist, str(m), color)
p.draw()

for i,f in enumerate(ptfactors):
    hname = histdir+histname.replace("correlator_hist", "correlator_hist_varied_jet_"+str(f))
    if f == 0.9 or f == 1.1:
        hname = hname.replace("0.9", "0.90")
        hname = hname.replace("1.1", "1.10")
    h_ptvars[f] = (rebinhist(getObjFromFile(filename, hname)),  colors[i] )

p = Plotter("EEEC_jetPt")
p.plot_dir = plotdir
p.drawRatio = True
p.ratiorange = (0.7, 1.3)
p.xtitle = "3#zeta"
p.yfactor = 1.3
# p.legshift = (0.15, 0., 0.15, 0.)
p.addBackground(h_central, "Nominal", 15)
for f in ptfactors:
    (hist, color) = h_ptvars[f]
    p.addSignal(hist, str(f), color)
p.draw()       



bingraphs_masses = getBinGraphs(h_masses, masses)
for bin in bingraphs_masses.keys():
    name = "BinHist_masses_"+str(bin)
    drawBinGraph(bingraphs_masses[bin], name) 
    
bingraphs_ptvar = getBinGraphs(h_ptvars, ptfactors)
for bin in bingraphs_ptvar.keys():
    name = "BinHist_ptvar_"+str(bin)
    drawBinGraph(bingraphs_ptvar[bin], name) 

################################################################################
##### COV Stat 
cov_stat = getCovFromStat(h_central)
drawCov(cov_stat, "COV_stat", plotdir)

################################################################################
##### Get Deltas 
h_ptvar_deltas = {}
h_ptvar_covs = {}
for f in ptfactors:
    (hist, color) = h_ptvars[f]
    delta = getDelta(h_central, hist)
    cov = getCovFromDelta(delta)
    h_ptvar_deltas[f] = delta
    h_ptvar_covs[f] = cov
    drawCov(cov, "COV_jetPt_"+str(f), plotdir)
    drawDelta(delta, "DELTA_jetPt_"+str(f), plotdir)

average_deltas = {
    1: averageDelta(h_ptvars[0.99][0], h_ptvars[1.01][0], h_central),
    2: averageDelta(h_ptvars[0.98][0], h_ptvars[1.02][0], h_central),
    5: averageDelta(h_ptvars[0.95][0], h_ptvars[1.05][0], h_central),
}

average_covs = {}
for f in average_deltas.keys():
    average_covs[f] = getCovFromDelta(average_deltas[f])
    drawCov(average_covs[f], "COV_jetPt_AVERAGE_"+str(f), plotdir)
    drawDelta(average_deltas[f], "DELTA_jetPt_AVERAGE_"+str(f), plotdir)

################################################################################
##### Normalize
h_central_norm = h_central.Clone(h_central.GetName()+"_norm")
if normWidth:
    h_central_norm.Scale(1/h_central.Integral(), "width")
else:
    h_central_norm.Scale(1/h_central.Integral())
cov_stat_norm = normalizeCov(cov_stat, h_central, normWidth)
drawCov(cov_stat_norm, "COV_stat_norm", plotdir)


h_masses_norm = {}
for m in masses:
    (hist, color) = h_masses[m]
    hnorm = hist.Clone(hist.GetName()+"_norm")
    if normWidth:
        hnorm.Scale(1/hist.Integral(), "width")
    else:
        hnorm.Scale(1/hist.Integral())
        
    h_masses_norm[m] = hnorm, color

p = Plotter("EEEC_masses_norm")
p.plot_dir = plotdir
p.drawRatio = True
p.ratiorange = (0.7, 1.3)
p.xtitle = "3#zeta"
# p.legshift = (0.15, 0., 0.15, 0.)
p.yfactor = 1.3
p.addBackground(h_central_norm, "172.5", 15)
for m in masses:
    (hist, color) = h_masses_norm[m]
    p.addSignal(hist, str(m), color)
p.draw()

h_ptvars_norm = {}
h_ptvar_covs_norm = {}
for f in ptfactors:
    (hist, color) = h_ptvars[f]
    hnorm = hist.Clone(hist.GetName()+"_norm")
    if normWidth:
        hnorm.Scale(1/hist.Integral(), "width")
    else:
        hnorm.Scale(1/hist.Integral())
    h_ptvars_norm[f] = hnorm, color
    cov_norm = normalizeCov(h_ptvar_covs[f], h_central, normWidth)
    drawCov(cov_norm, "COV_jetPt_"+str(f)+"_norm", plotdir)
    h_ptvar_covs_norm[f] = cov_norm
    
p = Plotter("EEEC_jetPt_norm")
p.plot_dir = plotdir
p.drawRatio = True
p.ratiorange = (0.7, 1.3)
p.xtitle = "3#zeta"
p.yfactor = 1.3
# p.legshift = (0.15, 0., 0.15, 0.)
p.addBackground(h_central_norm, "Nominal", 15)
for f in ptfactors:
    (hist, color) = h_ptvars_norm[f]
    p.addSignal(hist, str(f), color)
p.draw() 

bingraphs_masses_norm = getBinGraphs(h_masses_norm, masses)
for bin in bingraphs_masses_norm.keys():
    name = "BinHist_masses_norm_"+str(bin)
    drawBinGraph(bingraphs_masses_norm[bin], name) 

bingraphs_ptvar_norm = getBinGraphs(h_ptvars_norm, ptfactors)
for bin in bingraphs_ptvar_norm.keys():
    name = "BinHist_ptvar_norm_"+str(bin)
    drawBinGraph(bingraphs_ptvar_norm[bin], name)

# Normalize Matrix
average_covs_norm = {}
for f in average_covs.keys():
    cov_norm = normalizeCov(average_covs[f], h_central, normWidth)
    average_covs_norm[f] = cov_norm
    drawCov(cov_norm, "COV_jetPt_AVERAGE_"+str(f)+"_norm", plotdir)


covDummy = getCovDummy(h_central)
covDummy_norm = normalizeCov(covDummy, h_central, normWidth)
drawCov(covDummy, "COV_DUMMY", plotdir)
drawCov(covDummy_norm, "COV_DUMMY_NORM", plotdir)

################################################################################
#### Write output
outfile = ROOT.TFile("EEEC.root", "RECREATE")
outfile.cd()
h_central_norm.Write("data")
cov_stat_norm.Write("cov_stat")
for m in masses:
    (hist, color) = h_masses_norm[m]
    hist.Write("mtop_"+str(m))
for f in average_covs.keys():
    average_covs_norm[f].Write("cov_jetPt"+str(f))
outfile.Close()    

################################################################################    
#### Calculate chi2

chi2_values_stat = []
chi2_values_ptvars = {}
chi2_values_ptvars_average = {}

for m in masses:
    template, color = h_masses_norm[m]
    chi2 = compute_chi2(template, h_central_norm, TH2toNP(cov_stat_norm))
    # chi2 = compute_chi2_test(template, h_central_norm, cov_stat_norm)
    chi2_values_stat.append(chi2)
    
for f in ptfactors:
    chi2_values_ptvars[f] = []
    cov_norm_tot = h_ptvar_covs_norm[f].Clone()
    cov_norm_tot.Add(cov_stat_norm)
    for m in masses:
        template, color = h_masses_norm[m]
        chi2 = compute_chi2(template, h_central_norm, TH2toNP(cov_norm_tot))
        # chi2 = compute_chi2_test(template, h_central_norm, cov_norm_tot)
        chi2_values_ptvars[f].append(chi2)

for f in average_covs_norm.keys():
    chi2_values_ptvars_average[f] = []
    cov_norm_tot = average_covs_norm[f].Clone()
    cov_norm_tot.Add(cov_stat_norm)
    for m in masses:
        template, color = h_masses_norm[m]
        chi2 = compute_chi2(template, h_central_norm, TH2toNP(cov_norm_tot))
        # chi2 = compute_chi2_test(template, h_central_norm, cov_norm_tot)
        chi2_values_ptvars_average[f].append(chi2)

chi2_graph_stat = ROOT.TGraph(len(masses), array.array('d', masses), array.array('d', chi2_values_stat)  )

chi2_graph_ptvars = {}
for f in ptfactors:
    g = ROOT.TGraph(len(masses), array.array('d', masses), array.array('d', chi2_values_ptvars[f])  )
    chi2_graph_ptvars[f] = g

chi2_graph_ptvars_average = {}
for f in average_covs_norm.keys():
    g = ROOT.TGraph(len(masses), array.array('d', masses), array.array('d', chi2_values_ptvars_average[f])  )
    chi2_graph_ptvars_average[f] = g

################################################################################
### DRAW CHI2 

ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetOptStat(0)
c = ROOT.TCanvas("c", "c", 600, 600)
ROOT.gPad.SetLeftMargin(0.19)
ROOT.gPad.SetBottomMargin(0.12)
leg = ROOT.TLegend(.3, .5, .7, .8)
chi2_graph_stat.SetTitle(" ")
ymax = max(chi2_graph_stat.Eval(171.5), chi2_graph_stat.Eval(173.5))
chi2_graph_stat.GetYaxis().SetRangeUser(0, ymax*1.4)
chi2_graph_stat.GetXaxis().SetTitle("m_{t} [GeV]")
chi2_graph_stat.GetYaxis().SetTitle("#chi^{2}")
chi2_graph_stat.SetLineColor(1)
chi2_graph_stat.SetMarkerColor(1)
chi2_graph_stat.SetMarkerStyle(20)
chi2_graph_stat.Draw("AP")
fit_func = ROOT.TF1('pol2_fit', 'pol2', 170, 175)
chi2_graph_stat.Fit(fit_func, 'R')
fit = chi2_graph_stat.GetFunction('pol2_fit')
fit.SetLineColor(1)
fit.Draw("SAME")
leg.AddEntry(chi2_graph_stat, "Stat only", "pl")
for f in ptfactors:
    (hist, color) = h_ptvars_norm[f]
    chi2_graph_ptvars[f].SetLineColor(color)
    chi2_graph_ptvars[f].SetMarkerColor(color)
    chi2_graph_ptvars[f].SetMarkerStyle(20)
    chi2_graph_ptvars[f].Draw("P SAME")
    fit_func = ROOT.TF1('pol2_fit', 'pol2', 170, 175)
    chi2_graph_ptvars[f].Fit(fit_func, 'R')
    fit = chi2_graph_ptvars[f].GetFunction('pol2_fit')
    fit.SetLineColor(color)
    fit.Draw("SAME")    
    leg.AddEntry(chi2_graph_ptvars[f], str((f-1.0)*100)+"% jet p_{T} uncert", "pl")
    
leg.Draw()
c.Print(plotdir+"Chi2.pdf")


ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetOptStat(0)
c = ROOT.TCanvas("c", "c", 600, 600)
ROOT.gPad.SetLeftMargin(0.19)
ROOT.gPad.SetBottomMargin(0.12)
leg = ROOT.TLegend(.3, .5, .7, .8)
chi2_graph_stat.SetTitle(" ")
ymax = max(chi2_graph_stat.Eval(171.5), chi2_graph_stat.Eval(173.5))
chi2_graph_stat.GetYaxis().SetRangeUser(0, ymax*1.4)
chi2_graph_stat.GetXaxis().SetTitle("m_{t} [GeV]")
chi2_graph_stat.GetYaxis().SetTitle("#chi^{2}")
chi2_graph_stat.SetLineColor(1)
chi2_graph_stat.SetMarkerColor(1)
chi2_graph_stat.SetMarkerStyle(20)
chi2_graph_stat.Draw("AP")
fit_func = ROOT.TF1('pol2_fit', 'pol2', 170, 175)
chi2_graph_stat.Fit(fit_func, 'R')
fit = chi2_graph_stat.GetFunction('pol2_fit')
fit.SetLineColor(1)
fit.Draw("SAME")
leg.AddEntry(chi2_graph_stat, "Stat only", "pl")
for i,f in enumerate(average_covs.keys()):
    color = colors[i]
    chi2_graph_ptvars_average[f].SetLineColor(color)
    chi2_graph_ptvars_average[f].SetMarkerColor(color)
    chi2_graph_ptvars_average[f].SetMarkerStyle(20)
    chi2_graph_ptvars_average[f].Draw("P SAME")
    fit_func = ROOT.TF1('pol2_fit', 'pol2', 170, 175)
    chi2_graph_ptvars_average[f].Fit(fit_func, 'R')
    fit = chi2_graph_ptvars_average[f].GetFunction('pol2_fit')
    fit.SetLineColor(color)
    fit.Draw("SAME")    
    leg.AddEntry(chi2_graph_ptvars_average[f], str(f)+"% jet p_{T} uncert (average)", "pl")
    
leg.Draw()
c.Print(plotdir+"Chi2_average.pdf")
        
mt, up, down = measureMtop(chi2_graph_stat)
uncert = (up+down)/2
print "m_t =", mt, "+", up, "-", down
        
print "-------------"
measurements_ptvar = {}
for f in ptfactors:    
    print "f =", f    
    measurements_ptvar[f] = measureMtop(chi2_graph_ptvars[f])
    average = (measurements_ptvar[f][1]+measurements_ptvar[f][2])/2
    sysonly = sqrt(average*average - uncert*uncert)
    print "   m_t =", measurements_ptvar[f][0], "+", measurements_ptvar[f][1], "-", measurements_ptvar[f][2], "(+-", sysonly, "sys only)"


print "-------------"
measurements_ptvar_average = {}

for f in average_covs.keys():    
    print "f =", f    
    measurements_ptvar_average[f] = measureMtop(chi2_graph_ptvars_average[f])
    average = (measurements_ptvar_average[f][1]+measurements_ptvar_average[f][2])/2
    sysonly = sqrt(average*average - uncert*uncert)
    print "   m_t =", measurements_ptvar_average[f][0], "+", measurements_ptvar_average[f][1], "-", measurements_ptvar_average[f][2], "(+-", sysonly, "sys only)"
