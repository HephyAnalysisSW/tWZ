#!/usr/bin/env python

import ROOT
import os
import Analysis.Tools.syncer
from math                                        import sqrt
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from MyRootTools.plotter.Plotter                 import Plotter

ROOT.gROOT.SetBatch(ROOT.kTRUE)


outdir = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_TEST/"
plotdir = plot_directory+"/PreFit_TEST/"

if not os.path.exists( outdir ): os.makedirs( outdir )
if not os.path.exists( plotdir ): os.makedirs( plotdir )

outname = outdir+'/CombineInput.root'
outfile = ROOT.TFile(outname, 'recreate')
outfile.cd()
outfile.mkdir("A__Zpt")
outfile.Close()


signal = ROOT.TH1F("sig", "sig", 5, 0, 500)
bkg1 = ROOT.TH1F("bkg1", "bkg1", 5, 0, 500)
bkg2 = ROOT.TH1F("bkg2", "bkg2", 5, 0, 500)
data = ROOT.TH1F("data", "data", 5, 0, 500)



for i, content in enumerate([5, 10, 10, 10, 70]):
    signal.SetBinContent(i+1, content)
    signal.SetBinError(i+1, 0.01)

for i, content in enumerate([50, 30, 20, 10, 5]):
    bkg1.SetBinContent(i+1, content)
    bkg1.SetBinError(i+1, 0.01)

for i, content in enumerate([10, 10, 10, 10, 10]):
    bkg2.SetBinContent(i+1, content)
    bkg2.SetBinError(i+1, 0.01)

for i, content in enumerate([65, 50, 40, 30, 20]):
    data.SetBinContent(i+1, content)
    data.SetBinError(i+1, sqrt(content))

writeObjToDirInFile(outname, "A__Zpt", signal, "signal", update=True)
writeObjToDirInFile(outname, "A__Zpt", bkg1, "bkg1", update=True)
writeObjToDirInFile(outname, "A__Zpt", bkg2, "bkg2", update=True)
writeObjToDirInFile(outname, "A__Zpt", data, "data_obs", update=True)





sigPlusBkg = signal.Clone()
sigPlusBkg.Add(bkg1)
sigPlusBkg.Add(bkg2)

p = Plotter("PreFit_TEST")
p.plot_dir = plotdir
p.lumi = "138"
p.drawRatio = True
p.addBackground(bkg1, "bkg1", ROOT.kAzure+7)
p.addBackground(bkg2, "bkg2", ROOT.kGreen-2)
p.addSignal(sigPlusBkg, "sig+bkg", ROOT.kRed)
p.addData(data)
p.draw()
