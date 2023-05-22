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
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--nowidth',      action='store_true')
argParser.add_argument('--scaleSYS',     action='store', default=1.0)
argParser.add_argument('--scaleSTAT',    action='store', default=1.0)
args = argParser.parse_args()


plotdir = plot_directory+"/EEECplots/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

filename = "/users/dennis.schwarz/correlator_hist_trip_28.root"
histdir = "Top-Quark/Gen-Level/weighted/"
histdir_W = "W-Boson/Gen-Level/weighted/"

histname = "correlator_hist_Gen_None_450_500"
histname_W = "correlator_hist_W_Gen_None_450_500"

colors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen-2, 798, ROOT.kAzure+7, ROOT.kMagenta, ROOT.kRed+3, ROOT.kGreen+3]
masses = [171.5, 171.75, 172.0, 172.25, 172.75, 173.0, 173.25, 173.5]
# masses = [171.5, 172.0, 173.0, 173.5]
# ptfactors = [0.9, 0.95, 0.98, 0.99, 1.01, 1.02, 1.05, 1.1]
ptfactors = [0.95, 0.98, 0.99, 1.01, 1.02, 1.05]

h_central = getObjFromFile(filename, histdir+histname)
h_central_W = getObjFromFile(filename, histdir_W+histname_W)

h_masses = {}
for i,m in enumerate(masses):
    hname = histdir+histname.replace("None", str(m))
    h_masses[m] = ( getObjFromFile(filename, hname), colors[i] )

yfactor = 1.5

p = Plotter("EEEC_fine")
p.plot_dir = plotdir
p.drawRatio = False
# p.ratiorange = (0.85, 1.15)
p.xtitle = "3#zeta"
p.ytitle = "Weighted triplets"
p.rebin = 10
p.yfactor = yfactor
p.addBackground(h_central, "172.5", 15)
p.draw()

p = Plotter("EEEC_W_fine")
p.plot_dir = plotdir
p.drawRatio = False
# p.ratiorange = (0.85, 1.15)
p.xtitle = "3#zeta"
p.ytitle = "Weighted triplets"
p.rebin = 10
p.yfactor = yfactor
p.addBackground(h_central_W, "172.5", 15)
p.draw()
