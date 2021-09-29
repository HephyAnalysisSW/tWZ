#!/usr/bin/env python

import ROOT
from math                                import sqrt
from plotDistribution import plotDistribution
import Analysis.Tools.syncer


import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--plotOnly',         action='store_true', default=False, help='only plot without re-creating root file?')
argParser.add_argument('--noPlots',          action='store_true', default=False, help='No plots?')
argParser.add_argument('--twoD',             action='store_true', default=False, help='No plots?')
args = argParser.parse_args()

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
################################################################################
### Setup
regions = ["WZ", "ZZ", "ttZ"]
print 'Reading regions:', regions

# histname
histname = "Z1_pt"
print 'Reading Histogram:', histname

# Directories
dirs = {
    "ZZ":  "/mnt/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_SYS_v1_noData/Run2018/all/trilepVL-minDLmass12-onZ1-onZ2-nLeptons4/",
    "WZ":  "/mnt/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_SYS_v1_noData/Run2018/all/trilepT-minDLmass12-onZ1-deepjet0-met60/",
    "ttZ": "/mnt/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_SYS_v1_noData/Run2018/all/trilepT-minDLmass12-onZ1-njet4p-deepjet1p/",
}

# Define backgrounds
processes = ["ttZ", "WZ", "ZZ", "tWZ", "ttX", "tZq", "triBoson", "nonprompt"]
backgrounds = ["tWZ", "ttX", "tZq", "triBoson", "nonprompt"]
signals = ["ttZ", "WZ", "ZZ"]

# Define Signal points
signalnames = []
WCs = ["cHq1Re11", "cHq1Re22", "cHq1Re33", "cHq3Re11", "cHq3Re22", "cHq3Re33"]
minval = -10.0
maxval = 10.0
Npoints = 51
SMpointName = ""
goodnames = {}
value_to_number = {}
for WCname in WCs:
    vtn = {}
    for i in range(Npoints):
        value = round(minval + ((maxval-minval)/(Npoints-1))*i,2)
        signalname='%s=%3.2f'%(WCname, value)
        if abs(value) < 0.001:
            print 'Found SM point'
            SMpointName = signalname
        signalnames.append(signalname)
        goodnames[signalname]="%s_%s"%(WCname,i)
        vtn[value] = i
    value_to_number[WCname] = vtn

if args.twoD:
    signalnames = []
    goodnames = {}
    minval = -4.0
    maxval = 4.0
    Npoints = 11
    for i in range(Npoints):
        value1 = minval + ((maxval-minval)/(Npoints-1))*i
        for j in range(Npoints):
            value2 = minval + ((maxval-minval)/(Npoints-1))*j
            signalname='%i,%i'%(i, j)
            signalnames.append(signalname)
            number = j+Npoints*i
            goodnames[signalname]="%i"%(number)

# Define Systematics
sysnames = [
    'BTag_b',
    'BTag_l',
    'Trigger',
    'PU',
    'JES',
]


################################################################################
### Read Histograms and write to outfile
if not args.plotOnly:
    for signalpoint in signalnames:
        print '--------------------------------------------------------'
        print 'Working on', signalpoint
        outname = '/mnt/hephy/cms/dennis.schwarz/www/tWZ/limits/CombineInput_'+goodnames[signalpoint]+'.root'
        outfile = ROOT.TFile(outname, 'recreate')
        outfile.cd()
        for region in regions:
            print 'Filling region', region
            file = ROOT.TFile(dirs[region]+'/Results.root')
            outfile.mkdir(region+"__"+histname)
            outfile.cd(region+"__"+histname)
            for process in processes:
                if process in backgrounds:
                    name = histname+"__"+process
                elif process in signals:
                    name = histname+"__"+process+"__"+signalpoint

                hist = file.Get(name)
                # hist.Rebin(5)
                hist = removeNegative(hist)
                hist.Write(process)
                # Systematics
                for sys in sysnames:
                    sysdirUP = dirs[region]
                    sysdirUP = sysdirUP.replace('/Run', '_'+sys+'_UP/Run')
                    sysdirDOWN = dirs[region]
                    sysdirDOWN = sysdirDOWN.replace('/Run', '_'+sys+'_DOWN/Run')
                    fileUP   = ROOT.TFile(sysdirUP+'/Results.root')
                    fileDOWN = ROOT.TFile(sysdirDOWN+'/Results.root')
                    outfile.cd(region+"__"+histname)
                    histUP   = fileUP.Get(name)
                    histDOWN = fileDOWN.Get(name)
                    # histUP.Rebin(5)
                    # histDOWN.Rebin(5)
                    histUP   = removeNegative(histUP)
                    histDOWN = removeNegative(histDOWN)
                    histUP.Write(process+"__"+sys+"Up")
                    histDOWN.Write(process+"__"+sys+"Down")

            # Write observed
            # Add all relevant samples
            is_first = True
            observed = ROOT.TH1F()
            for bkg in backgrounds:
                hist = file.Get(histname+"__"+bkg)
                if is_first:
                    observed = hist.Clone()
                    is_first = False
                else:
                    observed.Add(hist)
            # now add all signals at SM point
            for signal in signals:
                hist = file.Get(histname+"__"+signal+"__"+SMpointName)
                observed.Add(hist)
            observed = setPseudoDataErrors(observed)
            observed.Write("data_obs")
        outfile.cd()
        outfile.Close()
        print 'Written to ', outname


if not args.noPlots:
    signals_at_SM = signals
    for s in signals_at_SM:
        s = s+"__"+SMpointName
    for region in ["WZ", "ZZ", "ttZ"]:
        for WCname in WCs:
            SMpoint = 0
            EFTpoints = [-2, 2]
            if 'cHq3' in WCname: EFTpoints = [-0.4, 0.4]
            plotDistribution(None, region, 'Z1_pt', 'Z #it{p}_{T}', backgrounds, signals, WCname, SMpoint, EFTpoints, value_to_number, sysnames)

        plotDistribution("SM", region, 'Z1_pt', 'Z #it{p}_{T}', backgrounds+signals_at_SM, [], WCname, SMpoint, [], value_to_number, sysnames)


    Analysis.Tools.syncer.sync()