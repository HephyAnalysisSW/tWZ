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

def getHist(fname, hname, altbinning=False):
    bins  = [0, 60, 120, 180, 240, 300, 400, 1000]
    # bins  = [0, 40, 80, 120, 160, 200, 1000]
    if altbinning:
        bins  = [0, 60, 120, 180, 1000]
    hist = getObjFromFile(fname, hname)
    hist = hist.Rebin(len(bins)-1, hist.GetName()+"_rebin", array.array('d',bins))
    hist = removeNegative(hist)
    if hist.Integral() < 0.01:
        hist = removeZeros(hist)
    return hist

def getCombinedSignal(fname, hname, altbinning, rate=None, rate_process=None, sys_process=None, fname_sys=None):
    signals = ["ttZ", "WZ", "ZZ"]
    for i_sig, sig in enumerate(signals):
        # If one of the signals should be varied, use alternative file
        filename = fname
        if sig == sys_process:
            filename = fname_sys
        # If this is the first in the loop clone, otherwise Add to cloned
        if i_sig==0:
            hist = getHist(filename, hname.replace("sm", sig), altbinning)
            if sig == rate_process:
                hist.Scale(rate)
        else:
            tmp = getHist(filename, hname.replace("sm", sig), altbinning)
            if sig == rate_process:
                tmp.Scale(rate)
            hist.Add(tmp)
    return hist

def getNonpromptFromCR(fname, histname, altbinning):
    # Get prompt backgrounds in CR
    firstbkg = True
    backgrounds = ["ttZ", "WZ", "ZZ", "tWZ", "ttX", "tZq", "triBoson"]
    for bkg in backgrounds:
        h_bkg = getHist(fname, histname+"__"+bkg, altbinning)
        if firstbkg:
            h_bkg_CR = h_bkg.Clone()
            firstbkg = False
        else:
            h_bkg_CR.Add(h_bkg)
    # Get nonprompt = Data in CR * fakerate and subtract backgrounds
    h_nonprompt = getHist(fname, histname+"__data", altbinning)
    h_nonprompt.Add(h_bkg_CR, -1)
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
    "WZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint/"+args.year+"/all/trilepT-minDLmass12-onZ1-btag0-vetoMET60v2/",
    "ttZ":    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint/"+args.year+"/all/trilepT-minDLmass12-offZ1-njet3p-btag1p/",
    "WZ_CR":  "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint_FakeRateSF_useDataSF/"+args.year+"/all/trilepFOnoT-minDLmass12-onZ1-btag0-vetoMET60v2/",
    "ttZ_CR": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint_FakeRateSF_useDataSF/"+args.year+"/all/trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p/",
}

outdir = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_FakerateClosure/"+args.year+"/"

if not os.path.exists( outdir ): os.makedirs( outdir )


# Define backgrounds
processes = ["sm", "tWZ", "ttX", "tZq", "triBoson", "nonprompt"]
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
    # "BTag_b_correlated":              ("BTag_b_correlated_UP", "BTag_b_correlated_DOWN"),
    # "BTag_l_correlated":              ("BTag_l_correlated_UP", "BTag_l_correlated_DOWN"),
    # "BTag_b_uncorrelated_2016preVFP": ("BTag_b_uncorrelated_2016preVFP_UP", "BTag_b_uncorrelated_2016preVFP_DOWN"),
    # "BTag_l_uncorrelated_2016preVFP": ("BTag_l_uncorrelated_2016preVFP_UP", "BTag_l_uncorrelated_2016preVFP_DOWN"),
    # "BTag_b_uncorrelated_2016":       ("BTag_b_uncorrelated_2016_UP", "BTag_b_uncorrelated_2016_DOWN"),
    # "BTag_l_uncorrelated_2016":       ("BTag_l_uncorrelated_2016_UP", "BTag_l_uncorrelated_2016_DOWN"),
    # "BTag_b_uncorrelated_2017":       ("BTag_b_uncorrelated_2017_UP", "BTag_b_uncorrelated_2017_DOWN"),
    # "BTag_l_uncorrelated_2017":       ("BTag_l_uncorrelated_2017_UP", "BTag_l_uncorrelated_2017_DOWN"),
    # "BTag_b_uncorrelated_2018":       ("BTag_b_uncorrelated_2018_UP", "BTag_b_uncorrelated_2018_DOWN"),
    # "BTag_l_uncorrelated_2018":       ("BTag_l_uncorrelated_2018_UP", "BTag_l_uncorrelated_2018_DOWN"),
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
    # "Trigger":                        ("Trigger_UP", "Trigger_DOWN"),
    # "Prefire":                        ("Prefire_UP", "Prefire_DOWN"),
    # "LepReco":                        ("LepReco_UP", "LepReco_DOWN"),
    # "LepIDstat_2016preVFP":           ("LepIDstat_2016preVFP_UP", "LepIDstat_2016preVFP_DOWN"),
    # "LepIDstat_2016":                 ("LepIDstat_2016_UP", "LepIDstat_2016_DOWN"),
    # "LepIDstat_2017":                 ("LepIDstat_2017_UP", "LepIDstat_2017_DOWN"),
    # "LepIDstat_2018":                 ("LepIDstat_2018_UP", "LepIDstat_2018_DOWN"),
    # "LepIDsys":                       ("LepIDsys_UP", "LepIDsys_DOWN"),
    # "PU":                             ("PU_UP", "PU_DOWN"),
    # "JES":                            ("JES_UP", "JES_DOWN"),
    # "JER":                            ("JER_UP", "JER_DOWN"),
    # "Lumi_uncorrelated_2016":         ("Lumi_uncorrelated_2016_UP", "Lumi_uncorrelated_2016_DOWN"),
    # "Lumi_uncorrelated_2017":         ("Lumi_uncorrelated_2017_UP", "Lumi_uncorrelated_2017_DOWN"),
    # "Lumi_uncorrelated_2018":         ("Lumi_uncorrelated_2018_UP", "Lumi_uncorrelated_2018_DOWN"),
    # "Lumi_correlated_161718":         ("Lumi_correlated_161718_UP", "Lumi_correlated_161718_DOWN"),
    # "Lumi_correlated_1718":           ("Lumi_correlated_1718_UP", "Lumi_correlated_1718_DOWN"),
    # "ISR":                            ("ISR_UP", "ISR_DOWN"),
    # "FSR":                            ("FSR_UP", "FSR_DOWN"),
    # "muR_ttZ":                        ("Scale_UPNONE", "Scale_DOWNNONE"),
    # "muR_WZ":                         ("Scale_UPNONE", "Scale_DOWNNONE"),
    # "muR_ZZ":                         ("Scale_UPNONE", "Scale_DOWNNONE"),
    # "muR_tZq":                        ("Scale_UPNONE", "Scale_DOWNNONE"),
    # "muR_tWZ":                        ("Scale_UPNONE", "Scale_DOWNNONE"),
    # "muR_ttX":                        ("Scale_UPNONE", "Scale_DOWNNONE"),
    # "muR_triBoson":                   ("Scale_UPNONE", "Scale_DOWNNONE"),
    # "muF_ttZ":                        ("Scale_NONEUP", "Scale_NONEDOWN"),
    # "muF_WZ":                         ("Scale_NONEUP", "Scale_NONEDOWN"),
    # "muF_ZZ":                         ("Scale_NONEUP", "Scale_NONEDOWN"),
    # "muF_tZq":                        ("Scale_NONEUP", "Scale_NONEDOWN"),
    # "muF_tWZ":                        ("Scale_NONEUP", "Scale_NONEDOWN"),
    # "muF_ttX":                        ("Scale_NONEUP", "Scale_NONEDOWN"),
    # "muF_triBoson":                   ("Scale_NONEUP", "Scale_NONEDOWN"),
    # "PDF":                            (), # HAS 100 VARIATIONS, TREAT DIFFERENTLY
    # "rate_ttZ":                       (),
    # "rate_WZ":                        (),
    # "rate_ZZ":                        (),
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
    altbinning = True if "ZZ" in region else False
    logger.info( 'Filling region %s', region )
    p = Plotter(args.year+"__"+region+"__"+histname)
    p.plot_dir = plot_directory+"/PreFit_FakerateClosure/"
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
            nominalHists[process] = getNonpromptFromCR(dirs[region+"_CR"]+inname, histname, altbinning)
            writeObjToDirInFile(outname, region+"__"+histname, nominalHists[process], "nonprompt", update=True)
            p.addBackground(nominalHists[process], processinfo[process][0], processinfo[process][1])
        else:
            logger.info( '    read nominal')
            # The SM also needs special treatment because we need to sum ttZ, WZ and ZZ
            # Also, we construct the lin and quad histograms for the EFT fit
            if process == "sm":
                nominalHists[process] = getCombinedSignal(dirs[region]+inname, histname+"__"+process, altbinning)
                p.addBackground(nominalHists[process], processinfo[process][0], processinfo[process][1])
                writeObjToDirInFile(outname, region+"__"+histname, nominalHists[process], "sm", update=True)
            else:
                name = histname+"__"+process
                nominalHists[process] = getHist(dirs[region]+inname, name, altbinning)
                p.addBackground(nominalHists[process], processinfo[process][0], processinfo[process][1])
                writeObjToDirInFile(outname, region+"__"+histname, nominalHists[process], process, update=True)
        ########################################################################
        ## Now we run systematics. There are many things to take care of
        logger.info( '    Get systematic variations' )
        for sys in sysnames.keys():
            if sys == "PDF":
                # For PDF we do the RMS of the 100 variations
                # As for the nominal histograms, nonprompt and SM need to be
                # treated differently
                if process == "nonprompt" and region in ["ttZ", "WZ"]:
                    pdfUP = nominalHists[process].Clone()
                    pdfDOWN = nominalHists[process].Clone()
                elif process == "sm":
                    pdfvariations = []
                    for i in range(100):
                        pdfdir = dirs[region].replace('/Run', '_PDF_'+str(i+1)+'/Run').replace('/UL', '_PDF_'+str(i+1)+'/UL')
                        h_pdf = getCombinedSignal(pdfdir+inname, histname+"__"+process, altbinning)
                        pdfvariations.append(h_pdf)
                    pdfUP, pdfDOWN = getRMS(nominalHists[process], pdfvariations)
                else:
                    pdfvariations = []
                    for i in range(100):
                        pdfdir = dirs[region].replace('/Run', '_PDF_'+str(i+1)+'/Run').replace('/UL', '_PDF_'+str(i+1)+'/UL')
                        h_pdf = getHist(pdfdir+inname, name, altbinning)
                        pdfvariations.append(h_pdf)
                    pdfUP, pdfDOWN = getRMS(nominalHists[process], pdfvariations)
                writeObjToDirInFile(outname, region+"__"+histname, pdfUP, process+"__PDFUp", update=True)
                writeObjToDirInFile(outname, region+"__"+histname, pdfDOWN, process+"__PDFDown", update=True)
                p.addSystematic(pdfUP, pdfDOWN, sys, processinfo[process][0])
            elif sys == "Fakerate" or "FakerateClosure_" in sys:
                # The Fake rate uncertainty only exists for nonprompt, for all
                # other processes just Clone the nominal
                (upname, downname) = sysnames[sys]
                if "nonprompt" in process and region in ["ttZ", "WZ"]:
                    h_nonprompt_up = getNonpromptFromCR(dirs[region+"_CR"].replace('/Run', '_'+upname+'/Run').replace('/UL', '_'+upname+'/UL')+inname, histname, altbinning)
                    h_nonprompt_down = getNonpromptFromCR(dirs[region+"_CR"].replace('/Run', '_'+downname+'/Run').replace('/UL', '_'+downname+'/UL')+inname, histname, altbinning)
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
            elif sys in ["rate_ttZ", "rate_WZ", "rate_ZZ"]:
                # The rate uncerts of ttZ, WZ, and ZZ have to be done here because
                # We sum those to a combined "sm" histogram for the EFT fit
                # There are special functions that only vary one of the processes when
                # summing over the three signals
                uncert = None
                rate_process = None
                if sys == "rate_ttZ":
                    uncert = 0.11
                    rate_process = "ttZ"
                elif sys == "rate_WZ":
                    uncert = 0.025
                    rate_process = "WZ"
                elif sys == "rate_ZZ":
                    uncert = 0.025
                    rate_process = "ZZ"

                if process == "sm":
                    histUP = getCombinedSignal(dirs[region]+inname, histname+"__"+process, altbinning, rate=(1+uncert), rate_process=rate_process)
                    histDOWN = getCombinedSignal(dirs[region]+inname, histname+"__"+process, altbinning, rate=(1-uncert), rate_process=rate_process)
                else:
                    histUP = nominalHists[process].Clone()
                    histDOWN = nominalHists[process].Clone()
                writeObjToDirInFile(outname, region+"__"+histname, histUP, process+"__"+sys+"Up", update=True)
                writeObjToDirInFile(outname, region+"__"+histname, histDOWN, process+"__"+sys+"Down", update=True)
            elif "muR_" in sys or "muF" in sys:
                # muR and muF are divided by process, thus we have to do the variations
                # manually. For the "sm" histogram, the combination of signals is
                # built such that single processes can be read from a file that
                # contains the muR/muF variations while for other processes we use
                # the nominal.
                (upname, downname) = sysnames[sys]
                sysdirUP = dirs[region]
                sysdirUP = sysdirUP.replace('/Run', '_'+upname+'/Run').replace('/UL', '_'+upname+'/UL')
                sysdirDOWN = dirs[region]
                sysdirDOWN = sysdirDOWN.replace('/Run', '_'+downname+'/Run').replace('/UL', '_'+downname+'/UL')
                if process == "nonprompt" and region in ["ttZ", "WZ"]:
                    # Nonprompt has no variations since it is estimated from data
                    # So, just copy the nominal
                    histUP = nominalHists[process].Clone()
                    histDOWN = nominalHists[process].Clone()
                elif process == "sm":
                    processToVary = None
                    upFile = None
                    downFile = None
                    for p_vary in signals:
                        if p_vary == sys.split("_")[1]:
                            processToVary = p_vary
                            upFile = sysdirUP+inname
                            downFile = sysdirDOWN+inname
                            logger.info('      - only vary '+p_vary+" for "+sys)
                    histUP = getCombinedSignal(dirs[region]+inname, histname+"__"+process, altbinning, rate=None, rate_process=None, sys_process=processToVary, fname_sys=upFile)
                    histDOWN = getCombinedSignal(dirs[region]+inname, histname+"__"+process, altbinning, rate=None, rate_process=None, sys_process=processToVary, fname_sys=downFile)
                else:
                    histUP   = getHist(sysdirUP+inname, name, altbinning)
                    histDOWN = getHist(sysdirDOWN+inname, name, altbinning)
                writeObjToDirInFile(outname, region+"__"+histname, histUP, process+"__"+sys+"Up", update=True)
                writeObjToDirInFile(outname, region+"__"+histname, histDOWN, process+"__"+sys+"Down", update=True)
                p.addSystematic(histUP, histDOWN, sys, processinfo[process][0])
            else:
                # These are now all other uncertainties that do not need special
                # treatment.
                (upname, downname) = sysnames[sys]
                sysdirUP = dirs[region]
                sysdirUP = sysdirUP.replace('/Run', '_'+upname+'/Run').replace('/UL', '_'+upname+'/UL')
                sysdirDOWN = dirs[region]
                sysdirDOWN = sysdirDOWN.replace('/Run', '_'+downname+'/Run').replace('/UL', '_'+downname+'/UL')
                if process == "nonprompt" and region in ["ttZ", "WZ"]:
                    # Nonprompt has no variations since it is estimated from data
                    # So, just copy the nominal
                    histUP = nominalHists[process].Clone()
                    histDOWN = nominalHists[process].Clone()
                elif process == "sm":
                    histUP = getCombinedSignal(sysdirUP+inname, histname+"__"+process, altbinning)
                    histDOWN = getCombinedSignal(sysdirDOWN+inname, histname+"__"+process, altbinning)
                else:
                    histUP   = getHist(sysdirUP+inname, name, altbinning)
                    histDOWN = getHist(sysdirDOWN+inname, name, altbinning)
                writeObjToDirInFile(outname, region+"__"+histname, histUP, process+"__"+sys+"Up", update=True)
                writeObjToDirInFile(outname, region+"__"+histname, histDOWN, process+"__"+sys+"Down", update=True)
                p.addSystematic(histUP, histDOWN, sys, processinfo[process][0])

    # Write observed
    # Add all relevant samples
    logger.info( '  DATA' )
    observed = getHist(dirs[region]+inname, histname+"__data", altbinning)
    writeObjToDirInFile(outname, region+"__"+histname, observed, "data_obs", update=True)
    p.addData(observed, "Data")
    p.draw()
# Write one file per EFT point
logger.info( 'Written file: %s' , outname)
