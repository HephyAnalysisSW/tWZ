#!/usr/bin/env python

import ROOT
import array
import Analysis.Tools.syncer
import os

from math                                        import sqrt
from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
args = argParser.parse_args()

################################################################################
### Functions
def getRMS(nominal, variations):
    up   = nominal.Clone()
    down = nominal.Clone()
    Nbins = nominal.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        diff_sum2_up = 0
        diff_sum2_down = 0
        Nvars_up = 0
        Nvars_down = 0
        for var in variations:
            diff = var.GetBinContent(bin)-nominal.GetBinContent(bin)
            if diff > 0:
                diff_sum2_up += diff*diff
                Nvars_up += 1
            else:
                diff_sum2_down += diff*diff
                Nvars_down += 1
        rmsup = sqrt(diff_sum2_up/Nvars_up) if Nvars_up > 0 else 0
        rmsdown = sqrt(diff_sum2_down/Nvars_down) if Nvars_down > 0 else 0
        up.SetBinContent(bin, nominal.GetBinContent(bin)+rmsup)
        down.SetBinContent(bin, nominal.GetBinContent(bin)-rmsdown)
    return (up, down)

def setPseudoDataErrors(hist):
    newhist = hist.Clone()
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        content = hist.GetBinContent(bin)
        newhist.SetBinError(bin, sqrt(content))
    return newhist

def removeNegative(hist):
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        content = hist.GetBinContent(bin)
        if content < 0:
            hist.SetBinContent(bin, 0.01)
    return hist

def removeZeros(hist):
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        content = hist.GetBinContent(bin)
        if content < 0.01:
            hist.SetBinContent(bin, 0.01)
    return hist

def makeIntegers(hist):
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        contentInt = int(hist.GetBinContent(bin))
        if contentInt == 0:
            hist.SetBinContent(bin, 1.)
        else:
            hist.SetBinContent(bin, contentInt)
    return hist

def getHist(fname, hname, integer=False):
    # print fname, hname
    # bins  = [0, 60, 120, 180, 1000]
    bins  = [0, 40, 100, 180, 1000]

    if "ULRunII" in fname:
        # Get histograms from each era
        hist_18 = getObjFromFile(fname.replace("/ULRunII/", "/UL2018/"), hname)
        hist_17 = getObjFromFile(fname.replace("/ULRunII/", "/UL2017/"), hname)
        hist_16 = getObjFromFile(fname.replace("/ULRunII/", "/UL2016/"), hname)
        hist_16preVFP = getObjFromFile(fname.replace("/ULRunII/", "/UL2016preVFP/"), hname)
        # add them
        hist = hist_18.Clone(hist_18.GetName()+"_RunIIcombination")
        hist.Add(hist_17)
        hist.Add(hist_16)
        hist.Add(hist_16preVFP)
    else:
        hist = getObjFromFile(fname, hname)
    hist = hist.Rebin(len(bins)-1, hist.GetName()+"_rebin", array.array('d',bins))
    hist = removeNegative(hist)
    if integer:
        hist = makeIntegers(hist)
    return hist

def getNonpromptFromCR_MC(fname, histname):
    h_nonprompt = getHist(fname, histname+"__nonprompt")
    h_nonprompt = removeNegative(h_nonprompt) # make sure there are no negative bins
    return h_nonprompt

################################################################################
### Setup
logger.info( "Prepare input file for combine.")

if args.year not in ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]:
    raise RuntimeError( "Year %s is not knwon", args.year)
logger.info( "Year = %s", args.year )

# regions
regions = ["WZ", "ttZ"]
# regions = ["WZ"]

# histname
histname = "Z1_pt"

version = "v11"
logger.info( "Version = %s", version )


# Directories
dirs = {
    "WZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint/"+args.year+"/all/trilepT-minDLmass12-onZ1-btag0-met60/",
    "ttZ":    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint/"+args.year+"/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/",
    "WZ_CR":  "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_threePoint_FakeRateSF/"+args.year+"/all/trilepFOnoT-minDLmass12-onZ1-btag0-met60/",
    "ttZ_CR": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_threePoint_FakeRateSF/"+args.year+"/all/trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p/",
}

outdir = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_FakerateClosureMConly/"+args.year+"/"

if not os.path.exists( outdir ): os.makedirs( outdir )


# Define backgrounds
processes = ["nonprompt"]
signals = ["WZ", "ZZ", "ttZ"]

processinfo = {
    "sm":        ("ttZ+WZ+ZZ", ROOT.kAzure+7),
    "ttZ":       ("ttZ", color.TTZ),
    "WZ":        ("WZ",  color.WZ),
    "ZZ":        ("ZZ", color.ZZ),
    "tWZ":       ("tWZ", color.TWZ),
    "ttX":       ("ttX", color.TTX_rare),
    "tZq":       ("tZq", color.TZQ),
    "triBoson":  ("Triboson", color.triBoson),
    "nonprompt": ("Nonprompt", color.nonprompt),
}

lumi = {
    "UL2016preVFP": "19.5",
    "UL2016":       "16.5",
    "UL2017":       "41.5",
    "UL2018":       "60",
    "ULRunII":      "138",
}

# Define Systematics
sysnames = {
    "Fakerate":                       ("Fakerate_UP", "Fakerate_DOWN"), # THIS IS ONLY IN NONPROMPT
    "FakerateClosure_correlated_elec":              ("FakerateClosure_correlated_elec_UP", "FakerateClosure_correlated_elec_DOWN"),
    "FakerateClosure_uncorrelated_elec_2016preVFP": ("FakerateClosure_uncorrelated_elec_2016preVFP_UP", "FakerateClosure_uncorrelated_elec_2016preVFP_DOWN"),
    "FakerateClosure_uncorrelated_elec_2016":       ("FakerateClosure_uncorrelated_elec_2016_UP", "FakerateClosure_uncorrelated_elec_2016_DOWN"),
    "FakerateClosure_uncorrelated_elec_2017":       ("FakerateClosure_uncorrelated_elec_2017_UP", "FakerateClosure_uncorrelated_elec_2017_DOWN"),
    "FakerateClosure_uncorrelated_elec_2018":       ("FakerateClosure_uncorrelated_elec_2018_UP", "FakerateClosure_uncorrelated_elec_2018_DOWN"),
    "FakerateClosure_correlated_muon":              ("FakerateClosure_correlated_muon_UP", "FakerateClosure_correlated_muon_DOWN"),
    "FakerateClosure_uncorrelated_muon_2016preVFP": ("FakerateClosure_uncorrelated_muon_2016preVFP_UP", "FakerateClosure_uncorrelated_muon_2016preVFP_DOWN"),
    "FakerateClosure_uncorrelated_muon_2016":       ("FakerateClosure_uncorrelated_muon_2016_UP", "FakerateClosure_uncorrelated_muon_2016_DOWN"),
    "FakerateClosure_uncorrelated_muon_2017":       ("FakerateClosure_uncorrelated_muon_2017_UP", "FakerateClosure_uncorrelated_muon_2017_DOWN"),
    "FakerateClosure_uncorrelated_muon_2018":       ("FakerateClosure_uncorrelated_muon_2018_UP", "FakerateClosure_uncorrelated_muon_2018_DOWN"),
    "FakerateClosure_correlated_both":              ("FakerateClosure_correlated_both_UP", "FakerateClosure_correlated_both_DOWN"),
    "FakerateClosure_uncorrelated_both_2016preVFP": ("FakerateClosure_uncorrelated_both_2016preVFP_UP", "FakerateClosure_uncorrelated_both_2016preVFP_DOWN"),
    "FakerateClosure_uncorrelated_both_2016":       ("FakerateClosure_uncorrelated_both_2016_UP", "FakerateClosure_uncorrelated_both_2016_DOWN"),
    "FakerateClosure_uncorrelated_both_2017":       ("FakerateClosure_uncorrelated_both_2017_UP", "FakerateClosure_uncorrelated_both_2017_DOWN"),
    "FakerateClosure_uncorrelated_both_2018":       ("FakerateClosure_uncorrelated_both_2018_UP", "FakerateClosure_uncorrelated_both_2018_DOWN"),

}



################################################################################
### Read Histograms and write to outfile
logger.info( "Collect hstograms" )

inname = 'Results.root'
logger.info( '--------------------------------------------------------' )
outname = outdir+'/CombineInput.root'
outfile = ROOT.TFile(outname, 'recreate')
outfile.cd()
for region in regions:
    outfile.mkdir(region+"__"+histname)
outfile.Close()
for region in regions:
    logger.info( 'Filling region %s', region )
    p = Plotter(args.year+"__"+region+"__"+histname)
    p.plot_dir = plot_directory+"/PreFit_FakerateClosureMConly/"
    p.lumi = lumi[args.year]
    p.drawRatio = True
    nominalHists = {}
    for process in processes:
        logger.info( '  %s', process )
        ########################################################################
        ## First get the nominal processes.
        ## Nonprompt needs special treatment because it is constructed from
        ## a control region
        if process == "nonprompt" and region in ["ttZ", "WZ"]:
            # Get prompt backgrounds in CR
            logger.info( '    (estimate from CR)')
            nominalHists[process] = getNonpromptFromCR_MC(dirs[region+"_CR"]+inname, histname)
            writeObjToDirInFile(outname, region+"__"+histname, nominalHists[process], "nonprompt", update=True)
            p.addBackground(nominalHists[process], processinfo[process][0], processinfo[process][1])
        else:
            raise RuntimeError( "Process %s is not defined", process)
        ########################################################################
        ## Now we run systematics. There are many things to take care of
        logger.info( '    Get systematic variations' )
        for sys in sysnames.keys():
            if sys == "Fakerate" or "FakerateClosure_" in sys:
                # The Fake rate uncertainty only exists for nonprompt, for all
                # other processes just Clone the nominal
                (upname, downname) = sysnames[sys]
                if "nonprompt" in process and region in ["ttZ", "WZ"]:
                    h_nonprompt_up = getNonpromptFromCR_MC(dirs[region+"_CR"].replace('/Run', '_'+upname+'/Run').replace('/UL', '_'+upname+'/UL')+inname, histname)
                    h_nonprompt_down = getNonpromptFromCR_MC(dirs[region+"_CR"].replace('/Run', '_'+downname+'/Run').replace('/UL', '_'+downname+'/UL')+inname, histname)
                    p.addSystematic(h_nonprompt_up, h_nonprompt_down, sys, processinfo[process][0])
                elif process == "sm":
                    # For all processes that are non prompt,
                    # there is no variation, so simply copy nominal
                    h_nonprompt_up = nominalHists[process].Clone()
                    h_nonprompt_down = nominalHists[process].Clone()
                else:
                    # For all processes that are non prompt,
                    # there is no variation, so simply copy nominal
                    h_nonprompt_up = nominalHists[process].Clone()
                    h_nonprompt_down = nominalHists[process].Clone()
                writeObjToDirInFile(outname, region+"__"+histname, h_nonprompt_up, process+"__"+sys+"Up", update=True)
                writeObjToDirInFile(outname, region+"__"+histname, h_nonprompt_down, process+"__"+sys+"Down", update=True)
            else:
                raise RuntimeError( "Systematic %s is not defined", sys)

    # Write observed
    # Add all relevant samples
    logger.info( '  DATA (nonprompt MC)' )
    observed = getHist(dirs[region]+inname, histname+"__nonprompt", integer=True)
    writeObjToDirInFile(outname, region+"__"+histname, observed, "data_obs", update=True)
    p.addData(observed, "Nonprompt MC in SR")
    p.draw()
# Write one file per EFT point
logger.info( 'Written file: %s' , outname)
