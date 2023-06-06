#!/usr/bin/env python

import ROOT
import array
import Analysis.Tools.syncer

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
argParser.add_argument('--twoD',             action='store_true', default=False, help='2D limits?')
argParser.add_argument('--triplet',          action='store_true', default=False)
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
argParser.add_argument('--wc',               action='store', type=str, default="cHq1Re11")
args = argParser.parse_args()

################################################################################
### Functions
def getRMS(nominal, variations):
    up   = nominal.Clone()
    down = nominal.Clone()
    Nbins = hist.GetSize()-2
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
            hist.SetBinContent(bin, 0.0)
    return hist

def getHist(fname, hname):
    hist = getObjFromFile(fname, hname)
    hist = hist.Rebin(len(bins)-1, hist.GetName()+"_rebin", array.array('d',bins))
    hist = removeNegative(hist)
    return hist

################################################################################
### Setup
logger.info( "Prepare input file for combine.")

if args.year not in ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]:
    raise RuntimeError( "Year %s is not knwon", args.year)
logger.info( "Year = %s", args.year )

if not args.twoD and args.wc not in ["cHq1Re11", "cHq1Re22", "cHq1Re33", "cHq3Re11", "cHq3Re22", "cHq3Re33"]:
    raise RuntimeError( "Wilson coefficient %s is not knwon", args.wc)
logger.info( "WC = %s", args.wc )

# regions
regions = ["WZ", "ZZ", "ttZ"]

# binning
bins  = [0, 60, 120, 180, 240, 300, 400, 1000]

# histname
histname = "Z1_pt"

version = "v9"
logger.info( "Version = %s", version )

# Directories
dirs = {
    "ZZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_noData/"+args.year+"/all/qualepT-minDLmass12-onZ1-onZ2/",
    "WZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_noData/"+args.year+"/all/trilepT-minDLmass12-onZ1-btag0-met60/",
    "ttZ":    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_noData/"+args.year+"/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/",
    "WZ_CR":  "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_FakeRateSF_useDataSF/"+args.year+"/all/trilepFOnoT-minDLmass12-onZ1-btag0-met60/",
    "ttZ_CR": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_FakeRateSF_useDataSF/"+args.year+"/all/trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p/",
}

outdir = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL/"+args.year+"/"

if args.twoD:
    outdir = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_twoD"
    if args.triplet:
        outdir = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_twoD_triplet"

# Define backgrounds
processes = ["ttZ", "WZ", "ZZ", "tWZ", "ttX", "tZq", "triBoson", "nonprompt"]
backgrounds = ["ttX", "tZq", "triBoson", "tWZ", "nonprompt"]
signals = ["ttZ", "WZ", "ZZ"]

processinfo = {
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

# Define Signal points
logger.info( "Make list of points in EFT space" )
signalnames = []
Npoints = 21
SMpointName = ""
goodnames = {}
value_to_number = {}
if not args.twoD:
    WCname = args.wc
    minval = -10.0
    maxval = 10.0
    if "cHq3Re11" in WCname:
        minval = -0.2
        maxval = 0.2
    vtn = {}
    for i in range(Npoints):
        value = round(minval + ((maxval-minval)/(Npoints-1))*i,4)
        signalname='%s=%3.4f'%(WCname, value)
        if abs(value) < 0.001:
            print 'Found SM point for', WCname
            SMpointName = signalname
        signalnames.append(signalname)
        goodnames[signalname]="%s_%s"%(WCname,i)
        vtn[value] = i
    value_to_number[WCname] = vtn
elif args.twoD:
    minval1  = -4.0
    maxval1  = 4.0
    minval2  = -4.0
    maxval2  = 4.0
    Npoints1 = 21
    Npoints2 = 21
    WC1 = 'cHq1Re1122'
    WC2 = 'cHq1Re33'
    if args.triplet:
        WC1 = 'cHq3Re1122'
        WC2 = 'cHq3Re33'
        minval1 = -0.2
        maxval1 = 0.2
    for i in range(Npoints1):
        value1 = minval1 + ((maxval1-minval1)/(Npoints1-1))*i
        for j in range(Npoints2):
            value2 = minval2 + ((maxval2-minval2)/(Npoints2-1))*j
            signalname='%s=%3.4f, %s=%3.4f'%(WC1,value1,WC2,value2)
            if abs(value1)<0.001 and abs(value2)<0.001:
                print 'Found SM point'
                SMpointName = signalname
            signalnames.append(signalname)
            goodnames[signalname]="%s_%i_%s_%i"%(WC1,i,WC2,j)

# Define Systematics
sysnames = {
    "BTag_b_correlated":              ("BTag_b_correlated_UP", "BTag_b_correlated_DOWN"),
    "BTag_l_correlated":              ("BTag_l_correlated_UP", "BTag_l_correlated_DOWN"),
    "BTag_b_uncorrelated_2016preVFP": ("BTag_b_uncorrelated_2016preVFP_UP", "BTag_b_uncorrelated_2016preVFP_DOWN"),
    "BTag_l_uncorrelated_2016preVFP": ("BTag_l_uncorrelated_2016preVFP_UP", "BTag_l_uncorrelated_2016preVFP_DOWN"),
    "BTag_b_uncorrelated_2016":       ("BTag_b_uncorrelated_2016_UP", "BTag_b_uncorrelated_2016_DOWN"),
    "BTag_l_uncorrelated_2016":       ("BTag_l_uncorrelated_2016_UP", "BTag_l_uncorrelated_2016_DOWN"),
    "BTag_b_uncorrelated_2017":       ("BTag_b_uncorrelated_2017_UP", "BTag_b_uncorrelated_2017_DOWN"),
    "BTag_l_uncorrelated_2017":       ("BTag_l_uncorrelated_2017_UP", "BTag_l_uncorrelated_2017_DOWN"),
    "BTag_b_uncorrelated_2018":       ("BTag_b_uncorrelated_2018_UP", "BTag_b_uncorrelated_2018_DOWN"),
    "BTag_l_uncorrelated_2018":       ("BTag_l_uncorrelated_2018_UP", "BTag_l_uncorrelated_2018_DOWN"),
    "Fakerate":                       ("Fakerate_UP", "Fakerate_DOWN"), # TREAT DIFFERENTLY
    "Trigger":                        ("Trigger_UP", "Trigger_DOWN"),
    "Prefire":                        ("Prefire_UP", "Prefire_DOWN"),
    "LepReco":                        ("LepReco_UP", "LepReco_DOWN"),
    "LepIDstat_2016preVFP":           ("LepIDstat_2016preVFP_UP", "LepIDstat_2016preVFP_DOWN"),
    "LepIDstat_2016":                 ("LepIDstat_2016_UP", "LepIDstat_2016_DOWN"),
    "LepIDstat_2017":                 ("LepIDstat_2017_UP", "LepIDstat_2017_DOWN"),
    "LepIDstat_2018":                 ("LepIDstat_2018_UP", "LepIDstat_2018_DOWN"),
    "LepIDsys":                       ("LepIDsys_UP", "LepIDsys_DOWN"),
    "PU":                             ("PU_UP", "PU_DOWN"),
    # "JES":                            ("JES_UP", "JES_DOWN"),
    # "JER":                            ("JER_UP", "JER_DOWN"),
    "Lumi_uncorrelated_2016":         ("Lumi_uncorrelated_2016_UP", "Lumi_uncorrelated_2016_DOWN"),
    "Lumi_uncorrelated_2017":         ("Lumi_uncorrelated_2017_UP", "Lumi_uncorrelated_2017_DOWN"),
    "Lumi_uncorrelated_2018":         ("Lumi_uncorrelated_2018_UP", "Lumi_uncorrelated_2018_DOWN"),
    "Lumi_correlated_161718":         ("Lumi_correlated_161718_UP", "Lumi_correlated_161718_DOWN"),
    "Lumi_correlated_1718":           ("Lumi_correlated_1718_UP", "Lumi_correlated_1718_DOWN"),
    "ISR":                            ("ISR_UP", "ISR_DOWN"),
    "FSR":                            ("FSR_UP", "FSR_DOWN"),
    "muR":                            ("Scale_UPNONE", "Scale_DOWNNONE"), # muR
    "muF":                            ("Scale_NONEUP", "Scale_NONEDOWN"), # muF
    "PDF":                            (), # TREAT DIFFERENTLY
}



################################################################################
### Read Histograms and write to outfile
logger.info( "Collect hstograms" )

if args.twoD:
    inname = 'Results_twoD.root'
    if args.triplet:
        inname = 'Results_twoD_triplet.root'
else:         inname = 'Results.root'

for signalpoint in signalnames:
    logger.info( '--------------------------------------------------------' )
    logger.info( "EFT point = %s", signalpoint )
    outname = outdir+'/CombineInput_'+goodnames[signalpoint]+'.root'
    if args.twoD:
        outname = outdir+'/CombineInput_2D_'+goodnames[signalpoint]+'.root'
    outfile = ROOT.TFile(outname, 'recreate')
    outfile.cd()
    for region in regions:
        outfile.mkdir(region+"__"+histname)
    outfile.Close()
    for region in regions:
        logger.info( 'Filling region %s', region )
        if signalpoint == SMpointName:
            p = Plotter(args.year+"__"+region+"__"+histname)
            p.plot_dir = plot_directory+"/PreFit/"
            p.lumi = lumi[args.year]
            p.drawRatio = True
        # print dirs[region]+inname
        for process in processes:
            logger.info( '  %s', process )
            if process == "nonpromt":
                # Get prompt backgrounds in CR
                firstbkg = True
                for proc in processes:
                    if not "nonprompt" in proc:
                        h_bkg = getHist(dirs[region+"_CR"]+inname, histname+"__"+process)
                        if firstbkg:
                            h_bkg_CR = h_bkg.Clone()
                            firstbkg = False
                        else:
                            h_bkg_CR.Add(h_bkg)
                # Get nonpromt = Data in CR * fakerate and subtract backgrounds
                hist = getHist(dirs[region+"_CR"]+inname, histname+"__data")
                hist.Add(h_bkg_CR, -1)
                writeObjToDirInFile(outname, region+"__"+histname, hist, "nonpromt", update=True)
                if signalpoint == SMpointName:
                    p.addBackground(hist, processinfo[process][0], processinfo[process][1])
            else:
                if process in backgrounds:
                    name = histname+"__"+process
                elif process in signals:
                    name = histname+"__"+process+"__"+signalpoint
                # print dirs[region]+inname, name
                hist = getHist(dirs[region]+inname, name)
                writeObjToDirInFile(outname, region+"__"+histname, hist, process, update=True)
                if signalpoint == SMpointName:
                    p.addBackground(hist, processinfo[process][0], processinfo[process][1])
            # Systematics
            logger.info( '    Get systematic variations' )
            for sys in sysnames.keys():
                # logger.info( '    sys = %s', sys )
                if sys == "PDF":
                    pdfvariations = []
                    if process == "nonpromt":
                        pdfUP = hist.Clone("nonpromt_PDFUp")
                        pdfDOWN = hist.Clone("nonpromt_PDFDown")
                    else:
                        for i in range(100):
                            pdfdir = dirs[region].replace('/Run', '_PDF_'+str(i+1)+'/Run').replace('/UL', '_PDF_'+str(i+1)+'/UL')
                            h_pdf = getHist(pdfdir+inname, name)
                            pdfvariations.append(h_pdf)
                        pdfUP, pdfDOWN = getRMS(hist, pdfvariations)
                    writeObjToDirInFile(outname, region+"__"+histname, pdfUP, process+"__PDFUp", update=True)
                    writeObjToDirInFile(outname, region+"__"+histname, pdfDOWN, process+"__PDFDown", update=True)

                    if signalpoint == SMpointName:
                        p.addSystematic(pdfUP, pdfDOWN, sys, processinfo[process][0])
                elif sys == "Fakerate":
                    if "nonpromt" in process:
                        h_nonpromt_up = getHist(dirs[region+"_CR"].replace('/Run', '_Fakerate_UP/Run').replace('/UL', '_Fakerate_UP/UL')+inname, histname+"__data")
                        h_nonpromt_up.Add(h_bkg_CR, -1)
                        h_nonpromt_down = getHist(dirs[region+"_CR"].replace('/Run', '_Fakerate_DOWN/Run').replace('/UL', '_Fakerate_DOWN/UL')+inname, histname+"__data")
                        h_nonpromt_down.Add(h_bkg_CR, -1)
                    else:
                        # For all processes that are non prompt,
                        # there is no variation, so simply copy nominal
                        h_nonpromt_up = hist.Clone()
                        h_nonpromt_down = hist.Clone()
                    writeObjToDirInFile(outname, region+"__"+histname, h_nonpromt_up, process+"__"+sys+"Up", update=True)
                    writeObjToDirInFile(outname, region+"__"+histname, h_nonpromt_down, process+"__"+sys+"Down", update=True)
                    if signalpoint == SMpointName:
                        p.addSystematic(h_nonpromt_up, h_nonpromt_down, sys, processinfo[process][0])
                else:
                    (upname, downname) = sysnames[sys]
                    if process == "nonpromt":
                        histUP = hist.Clone("nonpromt_"+sys+"Up")
                        histDOWN = hist.Clone("nonpromt_"+sys+"Down")
                    else:
                        sysdirUP = dirs[region]
                        sysdirUP = sysdirUP.replace('/Run', '_'+upname+'/Run').replace('/UL', '_'+upname+'/UL')
                        sysdirDOWN = dirs[region]
                        sysdirDOWN = sysdirDOWN.replace('/Run', '_'+downname+'/Run').replace('/UL', '_'+downname+'/UL')
                        histUP   = getHist(sysdirUP+inname, name)
                        histDOWN = getHist(sysdirDOWN+inname, name)
                    writeObjToDirInFile(outname, region+"__"+histname, histUP, process+"__"+sys+"Up", update=True)
                    writeObjToDirInFile(outname, region+"__"+histname, histDOWN, process+"__"+sys+"Down", update=True)
                    if signalpoint == SMpointName:
                        p.addSystematic(histUP, histDOWN, sys, processinfo[process][0])

        # Write observed
        # Add all relevant samples
        logger.info( '  - DATA' )
        is_first = True
        observed = ROOT.TH1F()
        for bkg in backgrounds:
            hist = getHist(dirs[region]+inname, histname+"__"+bkg)
            if is_first:
                observed = hist.Clone()
                is_first = False
            else:
                observed.Add(hist)
        # now add all signals at SM point
        for signal in signals:
            hist = getHist(dirs[region]+inname, histname+"__"+signal+"__"+SMpointName)
            observed.Add(hist)
        observed = setPseudoDataErrors(observed)
        writeObjToDirInFile(outname, region+"__"+histname, observed, "data_obs", update=True)
        if signalpoint == SMpointName:
            p.addData(observed, "Asimov data")
        if signalpoint == SMpointName:
            p.draw()
    # Write one file per EFT point
    logger.info( 'Written file: %s' , outname)



# Analysis.Tools.syncer.sync()
