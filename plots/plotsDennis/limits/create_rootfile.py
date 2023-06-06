#!/usr/bin/env python


################################################################################
################################################################################
################################################################################
# TODO

################################################################################
################################################################################
################################################################################


import ROOT
from math                                import sqrt
import array
import Analysis.Tools.syncer

from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--twoD',             action='store_true', default=False, help='2D limits?')
argParser.add_argument('--triplet',          action='store_true', default=False)
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
args = argParser.parse_args()

################################################################################
### Functions
def getRMS(nominal, variations):
    up   = nominal.Clone()
    down = nominal.Clone()
    Nvars = len(variations)
    nominal = hist.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        diff_sum2_up = 0
        diff_sum2_down = 0
        for var in variations:
            diff = var.GetBinContent(bin)-nominal.GetBinContent(bin)
            if diff > 0:
                diff_sum2_up += diff*diff
            else:
                diff_sum2_down += diff*diff
        rmsup = sqrt(diff_sum2_up/Nvars)
        rmsdown = sqrt(diff_sum2_down/Nvars)
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

def simulateFlatSystematic(hist, size):
    sys = hist.Clone()
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        content = hist.GetBinContent(bin)
        sys.SetBinContent(bin, (1+size)*content)
    return sys

def simulateSystematic(hist, size):
    sys = hist.Clone()
    Nbins = hist.GetSize()-2
    start = -1 * size
    stop = size
    stepsize = (stop-start)/Nbins
    for i in range(Nbins):
        bin = i+1
        value = start + i*stepsize
        content = hist.GetBinContent(bin)
        sys.SetBinContent(bin, (1+value)*content)
    return sys

def removeNegative(hist):
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        content = hist.GetBinContent(bin)
        if content < 0:
            hist.SetBinContent(bin, 0.0)
    return hist

def setupHist(hist, bins):
    hist = hist.Rebin(len(bins)-1, "h", array.array('d',bins))
    hist = removeNegative(hist)
    return hist

################################################################################
### Setup
regions = ["WZ", "ZZ", "ttZ"]

print 'Reading regions:', regions

# binning
bins  = [0, 60, 120, 180, 240, 300, 400, 1000]

# histname
histname = "Z1_pt"
print 'Reading Histogram:', histname

version = "v8"
era = "ULRunII"

# Directories
dirs = {
    "ZZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_noData/"+era+"/all/trilepVL-minDLmass12-onZ1-onZ2-nLeptons4/",
    "WZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_noData/"+era+"/all/trilepT-minDLmass12-onZ1-deepjet0-met60/",
    "ttZ":    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_noData/"+era+"/all/trilepT-minDLmass12-onZ1-njet3-deepjet1p/",
    "WZ_CR":  "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_FakeRateSF_useDataSF/"+era+"/all/trilepFOnoT-minDLmass12-onZ1-deepjet0-met60/",
    "ttZ_CR": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_FakeRateSF_useDataSF/"+era+"/all/trilepFOnoT-minDLmass12-onZ1-njet3-deepjet1p/",
}

outdir = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL/"

if args.twoD:
    outdir = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_twoD"
    if args.triplet:
        outdir = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_twoD_triplet"

# Define backgrounds
processes = ["ttZ", "WZ", "ZZ", "tWZ", "ttX", "tZq", "triBoson", "nonprompt"]
backgrounds = ["ttX", "tZq", "triBoson", "tWZ", "nonprompt"]
signals = ["ttZ", "WZ", "ZZ"]
processinfo = {
    "tWZ":       ("tWZ", color.TWZ),
    "ttZ":       ("ttZ", color.TTZ),
    "ttX":       ("ttX", color.TTX_rare),
    "tZq":       ("tZq", color.TZQ),
    "WZ":        ("WZ",  color.WZ),
    "triBoson":  ("Triboson", color.triBoson),
    "ZZ":        ("ZZ", color.ZZ),
    "nonprompt": ("Nonprompt", color.nonprompt),
}

# Define Signal points
signalnames = []
WCs = ["cHq1Re11", "cHq1Re22", "cHq1Re33", "cHq3Re11", "cHq3Re22", "cHq3Re33"]
Npoints = 21
SMpointName = ""
goodnames = {}
value_to_number = {}
if not args.twoD:
    for WCname in WCs:
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
                print 'Found SM point'
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
    "BTag_b":                         ("BTag_b_UP", "BTag_b_DOWN"),
    "BTag_l":                         ("BTag_l_UP", "BTag_l_DOWN"),
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
    "JES":                            ("JES_UP", "JES_DOWN"),
    "JER":                            ("JER_UP", "JER_DOWN"),
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
if args.twoD:
    inname = 'Results_twoD.root'
    if args.triplet:
        inname = 'Results_twoD_triplet.root'
else:         inname = 'Results.root'

if not args.plotOnly:
    for signalpoint in signalnames:
        print '--------------------------------------------------------'
        print 'Working on', signalpoint
        if signalpoint == SMpointName:
            p = Plotter(region+"__"+histname)
            p.plot_dir = plot_directory+"/PreFit/"
            p.lumi = "138"
        outname = outdir+'/CombineInput_'+goodnames[signalpoint]+'.root'
        if args.twoD:
            outname = outdir+'/CombineInput_2D_'+goodnames[signalpoint]+'.root'
        outfile = ROOT.TFile(outname, 'recreate')
        outfile.cd()
        for region in regions:
            print 'Filling region', region
            # print dirs[region]+inname
            outfile.mkdir(region+"__"+histname)
            outfile.cd(region+"__"+histname)
            for process in processes:
                if process == "nonpromt":
                    # Get prompt backgrounds in CR
                    firstbkg = True
                    for proc in processes:
                        if not "nonprompt" in proc:
                            h_bkg = getObjFromFile(dirs[region+"_CR"]+inname, histname+"__"+process)
                            if firstbkg:
                                h_bkg_CR = h_bkg.Clone()
                                firstbkg = False
                            else:
                                h_bkg_CR.Add(h_bkg)
                    # Get nonpromt = Data in CR * fakerate and subtract backgrounds
                    h_nonpromt = getObjFromFile(dirs[region+"_CR"]+inname, histname+"__data")
                    h_nonpromt.Add(h_bkg_CR, -1)
                    h_nonpromt = setupHist(h_nonpromt, bins)
                    h_nonpromt.Write("nonprompt")
                    if signalpoint == SMpointName:
                        p.addBackground(h_nonpromt, processinfo[process][0], processinfo[process][1])
                else:
                    if process in backgrounds:
                        name = histname+"__"+process
                    elif process in signals:
                        name = histname+"__"+process+"__"+signalpoint
                    # print name
                    hist = getObjFromFile(dirs[region]+inname), name)
                    hist = setupHist(hist, bins)
                    hist.Write(process)
                    if signalpoint == SMpointName:
                        p.addBackground(hist, processinfo[process][0], processinfo[process][1])
                # Systematics
                for sys in sysnames.keys():
                    if sys == "PDF":
                        pdfvariations = []
                        for i in range(100):
                            pdfdir = dirs[region].replace('/Run', '_PDF_'+str(i+1)+'/Run')
                            h_pdf = getObjFromFile(pdfdir+inname, name)
                            pdfvariations.append(h_pdf)
                        pdfUP, pdfDOWN = getRMS(hist, pdfvariations)
                        pdfUP.Write(process+"__PDFUp")
                        pdfDOWN.Write(process+"__PDFDown")
                        if signalpoint == SMpointName:
                            p.addSystematic(pdfUP, pdfDOWN, sys, processinfo[process][0])
                    elif sys == "Fakerate":
                        if "nonpromt" in process:
                            h_nonpromt_up = getObjFromFile(dirs[region+"_CR"].replace('/Run', '_Fakerate_UP/Run')+inname, histname+"__data")
                            h_nonpromt_up.Add(h_bkg_CR, -1)
                            h_nonpromt_down = getObjFromFile(dirs[region+"_CR"].replace('/Run', '_Fakerate_DOWN/Run')+inname, histname+"__data")
                            h_nonpromt_down.Add(h_bkg_CR, -1)
                        else:
                            # For all processes that are non prompt,
                            # there is no variation, so simply copy nominal
                            h_nonpromt_up = hist.Clone()
                            h_nonpromt_down = hist.Clone()
                        h_nonpromt_up.Write(process+"__"+sys+"Up")
                        h_nonpromt_down.Write(process+"__"+sys+"Down")
                        if signalpoint == SMpointName:
                            p.addSystematic(h_nonpromt_up, h_nonpromt_down, sys, processinfo[process][0])
                    else:
                        # print sys
                        (upname, downname) = sysnames[sys]
                        sysdirUP = dirs[region]
                        sysdirUP = sysdirUP.replace('/Run', '_'+upname+'/Run')
                        # print sysdirUP+inname
                        sysdirDOWN = dirs[region]
                        sysdirDOWN = sysdirDOWN.replace('/Run', '_'+downname+'/Run')

                        histUP = getObjFromFile(sysdirUP+inname, name)
                        histDOWN = getObjFromFile(sysdirDOWN+inname, name)
                        histUP   = setupHist(histUP, bins)
                        histDOWN = setupHist(histDOWN, bins)
                        outfile.cd(region+"__"+histname)
                        histUP.Write(process+"__"+sys+"Up")
                        histDOWN.Write(process+"__"+sys+"Down")
                        if signalpoint == SMpointName:
                            p.addSystematic(histUP, histDOWN, sys, processinfo[process][0])

            # Write observed
            # Add all relevant samples
            is_first = True
            observed = ROOT.TH1F()
            for bkg in backgrounds:
                hist = getObjFromFile(dirs[region]+inname), histname+"__"+bkg)
                if is_first:
                    observed = hist.Clone()
                    is_first = False
                else:
                    observed.Add(hist)
            # now add all signals at SM point
            for signal in signals:
                hist = getObjFromFile(dirs[region]+inname), histname+"__"+signal+"__"+SMpointName)

                observed.Add(hist)
            observed = setupHist(observed, bins)
            observed = setPseudoDataErrors(observed)
            observed.Write("data_obs")
            if signalpoint == SMpointName:
                p.addData(observed, "Asimov data")
        outfile.cd()
        outfile.Close()
        print 'Written to ', outname
        p.draw()



# Analysis.Tools.syncer.sync()
