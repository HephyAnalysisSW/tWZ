#!/usr/bin/env python
''' Analysis script for standard plots
'''
#
# Standard imports and batch mode
#
import ROOT, os
ROOT.gROOT.SetBatch(True)
c1 = ROOT.TCanvas() # do this to avoid version conflict in png.h with keras import ...
c1.Draw()
c1.Print('delete.png')
import itertools
import copy
import array
import operator
from math                                import sqrt, cos, sin, pi, atan2, cosh, exp

# RootTools
from RootTools.core.standard             import *

# MyRootTools
from MyRootTools.ttbarReconstruction.ttbarReco  import ttbarReco


# tWZ
from tWZ.Tools.user                      import plot_directory
from tWZ.Tools.cutInterpreter            import cutInterpreter
from tWZ.Tools.objectSelection_UL        import lepString, lepStringNoMVA
from tWZ.Tools.helpers                   import getCollection, cosThetaStarNew, getTheta, gettheta, getphi
from tWZ.Tools.leptonSF_topMVA           import leptonSF_topMVA

# Analysis
from Analysis.Tools.helpers              import deltaPhi, deltaR
from Analysis.Tools.puProfileCache       import *
from Analysis.Tools.puReweighting        import getReweightingFunction
from Analysis.Tools.leptonJetArbitration     import cleanJetsAndLeptons
from Analysis.Tools.WeightInfo           import WeightInfo

import Analysis.Tools.syncer
import numpy as np

################################################################################
# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--noData',         action='store_true', default=False, help='also plot data?')
argParser.add_argument('--small',          action='store_true', help='Run only on a small subset of the data?', )
#argParser.add_argument('--sorting',       action='store', default=None, choices=[None, "forDYMB"],  help='Sort histos?', )
argParser.add_argument('--dataMCScaling',  action='store_true', help='Data MC scaling?', )
argParser.add_argument('--plot_directory', action='store', default='ULtest_v1')
argParser.add_argument('--era',            action='store', type=str, default="UL2018")
argParser.add_argument('--selection',      action='store', default='trilepVL-njet4p-btag1p')
argParser.add_argument('--sys',            action='store', default='central')
argParser.add_argument('--nicePlots',      action='store_true', default=False)
argParser.add_argument('--twoD',           action='store_true', default=False)
argParser.add_argument('--triplet',        action='store_true', default=False)
argParser.add_argument('--doTTbarReco',    action='store_true', default=False)
args = argParser.parse_args()

################################################################################
# Logger
import tWZ.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

################################################################################
# Some info messages
if args.small:                        args.plot_directory += "_small"
if args.noData:                       args.plot_directory += "_noData"
if args.sys is not 'central':         args.plot_directory += "_%s" %(args.sys)


logger.info( "Working in era %s", args.era)
if args.dataMCScaling:
    logger.info( "Data/MC scaling active")
else:
    logger.info( "Data/MC scaling not active")

if args.nicePlots:
    logger.info( "Only draw the plots")
else:
    logger.info( "Only saving into root file")

if args.twoD:
    logger.info( "Create EFT points in 2D")
else:
    logger.info( "Create EFT points in 1D")

if args.noData:
    logger.info( "Running without data")
else:
    logger.info( "Data included in analysis cycle")


################################################################################
# Define the MC samples
from tWZ.samples.nanoTuples_ULRunII_nanoAODv9_postProcessed import *

if args.era == "UL2016":
    mc = [UL2016.TWZ_NLO_DR, UL2016.TTZ, UL2016.TTX_rare, UL2016.TZQ, UL2016.WZ, UL2016.triBoson, UL2016.ZZ, UL2016.nonprompt_3l]
elif args.era == "UL2016preVFP":
    mc = [UL2016preVFP.TWZ_NLO_DR, UL2016preVFP.TTZ, UL2016preVFP.TTX_rare, UL2016preVFP.TZQ, UL2016preVFP.WZ, UL2016preVFP.triBoson, UL2016preVFP.ZZ, UL2016preVFP.nonprompt_3l]
elif args.era == "UL2017":
    mc = [UL2017.TWZ_NLO_DR, UL2017.TTZ, UL2017.TTX_rare, UL2017.TZQ, UL2017.WZ, UL2017.triBoson, UL2017.ZZ, UL2017.nonprompt_3l]
elif args.era == "UL2018":
    mc = [UL2018.TWZ_NLO_DR, UL2018.TTZ, UL2018.TTX_rare, UL2018.TZQ, UL2018.WZ, UL2018.triBoson, UL2018.ZZ, UL2018.nonprompt_3l]
elif args.era == "ULRunII":
    mc = [TWZ_NLO_DR, TTZ, TTX_rare, TZQ, WZ, triBoson, ZZ, nonprompt_3l]

################################################################################
# Creating a list of weights
plotweights = []
weights_SM = []
# Add MC weights
weight_mc = []
for sample in mc:
    weight_ = lambda event, sample: 1. # Add event.weight and lumi weight to sample.weight later
    weight_mc.append(weight_)
plotweights.append(weight_mc)

# Add data weight
if not args.noData:
    plotweights.append([lambda event, sample: event.weight])

################################################################################
# Define the data sample
if   args.era == "UL2016": 
    datastring = "Run2016"
    lumistring = "2016"
elif args.era == "UL2016preVFP": 
    datastring = "Run2016_preVFP"
    lumistring = "2016_preVFP"
elif args.era == "UL2017": 
    datastring = "Run2017"
    lumistring = "2017"
elif args.era == "UL2018": 
    datastring = "Run2018"
    lumistring = "2018"

try:
  data_sample = eval(datastring)
except Exception as e:
  logger.error( "Didn't find %s", datastring )
  raise e

lumi_scale                 = lumi_year[lumistring]/1000.
data_sample.scale          = 1.

# Set up MC sample
for sample in mc:
    sample.scale           = 1


if args.small:
    for sample in mc + [data_sample]:
        sample.normalization = 1.
        sample.reduceFiles( to = 1 )
        sample.scale /= sample.normalization
        

################################################################################
# Text on the plots
tex = ROOT.TLatex()
tex.SetNDC()
tex.SetTextSize(0.04)
tex.SetTextAlign(11) # align right

################################################################################
# Functions needed specifically for this analysis routine

def drawObjects( plotData, lumi_scale ):
    lines = [
      (0.15, 0.95, 'CMS Preliminary' if plotData else 'CMS Simulation'),
      (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV)'% ( lumi_scale ) ) if plotData else (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV)' % lumi_scale)
    ]
    if "mt2ll100" in args.selection and args.noData: lines += [(0.55, 0.5, 'M_{T2}(ll) > 100 GeV')] # Manually put the mt2ll > 100 GeV label
    return [tex.DrawLatex(*l) for l in lines]

def drawPlots(plots, mode="all"):
    for log in [False, True]:
        plot_directory_ = os.path.join(plot_directory, 'analysisPlots', args.plot_directory, args.era, mode + ("_log" if log else ""), args.selection)
        for plot in plots:
            if not max(l.GetMaximum() for l in sum(plot.histos,[])): continue # Empty plot
            if not args.noData:
                if mode == "all": plot.histos[1][0].legendText = "Data"
                if mode == "SF":  plot.histos[1][0].legendText = "Data (SF)"

            _drawObjects = []
            n_stacks=len(plot.histos)
            if isinstance( plot, Plot):
                plotting.draw(plot,
                  plot_directory = plot_directory_,
                  ratio = {'histos': [[i+1,0] for i in range(n_stacks-1)], 'yRange':(0.1,1.9)} if not args.noData else None,
                  logX = False, logY = log, sorting = True,
                  yRange = (0.03, "auto") if log else (0.001, "auto"),
                  scaling = {0:1} if args.dataMCScaling else {},
                  legend = ( (0.18,0.88-0.03*sum(map(len, plot.histos)),0.9,0.88), 2),
                  drawObjects = drawObjects( not args.noData, lumi_scale ) + _drawObjects,
                  copyIndexPHP = True, extensions = ["png", "pdf", "root"],
                )


################################################################################
# Define sequences
sequence       = []

# def readWeights(sample,event):
#     if event.year == 2016 and not event.preVFP:
#         yearstring = "2016"
#     elif event.year == 2016 and event.preVFP:
#         yearstring = "2016_preVFP"
#     elif event.year == 2017:
#         yearstring = "2017"
#     elif event.year == 2018:
#         yearstring = "2018"
#     lumi_weight = lumi_year[yearstring]/1000.
# 
#     print "-------------------------"
#     print "Weight  =", event.weight
#     print "Lumi    =", lumi_weight
#     return
# 
# sequence.append(readWeights)

def getM3l( event, sample ):
    l = []
    for i in range(3):
        l.append(ROOT.TLorentzVector())
        l[i].SetPtEtaPhiM(event.lep_pt[i], event.lep_eta[i], event.lep_phi[i],0)
    event.m3l = (l[0] + l[1] + l[2]).M()
sequence.append( getM3l )


def getLeptons( event, sample ):
    channel = 0.5
    nElectrons = 0
    nMuons = 0
    nElectrons_VL = 0
    nMuons_VL = 0
    nElectrons_T = 0
    nMuons_T = 0
    nMuons_mediumId = 0
    nMuons_mediumId_VL = 0
    nMuons_mediumId_T = 0
    for i in range(event.nlep):
        if abs(event.lep_pdgId[i]) == 11:
            nElectrons += 1
            if event.lep_mvaTOPWP[i] >= 1:
                nElectrons_VL += 1
            if event.lep_mvaTOPWP[i] == 4:
                nElectrons_T += 1
        elif abs(event.lep_pdgId[i]) == 13:
            nMuons += 1
            if event.lep_mediumId[i] == 1:
                nMuons_mediumId += 1
                if event.lep_mvaTOPWP[i] >= 1:
                    nMuons_VL += 1
                    if event.lep_mediumId[i] == 1:
                        nMuons_mediumId_VL += 1
                if event.lep_mvaTOPWP[i] == 4:
                    nMuons_T += 1
                    if event.lep_mediumId[i] == 1:
                        nMuons_mediumId_T += 1
    event.nElectrons_all = nElectrons
    event.nElectrons_VL  = nElectrons_VL
    event.nElectrons_T   = nElectrons_T
    event.nMuons_all = nMuons
    event.nMuons_VL  = nMuons_VL
    event.nMuons_T   = nMuons_T   
    event.nMuons_mediumId_all = nMuons_mediumId
    event.nMuons_mediumId_VL  = nMuons_mediumId_VL
    event.nMuons_mediumId_T   = nMuons_mediumId_T     
    if nMuons_T==3 and nElectrons_T==0:
        channel = 1.5
    elif nMuons_T==2 and nElectrons_T==1:
        channel = 2.5
    elif nMuons_T==1 and nElectrons_T==2:
        channel = 3.5   
    elif nMuons_T==0 and nElectrons_T==3:
        channel = 4.5 
    event.channel = channel
sequence.append( getLeptons )

################################################################################
# Read variables

read_variables = [
    "weight/F", "year/I", "preVFP/O", "met_pt/F", "met_phi/F", "nJetGood/I", "PV_npvsGood/I",  "nJet/I", "nBTag/I", 
    "nlep/I",
    "l1_pt/F", "l1_eta/F" , "l1_phi/F", "l1_mvaTOP/F", "l1_mvaTOPv2/F", "l1_mvaTOPWP/I", "l1_mvaTOPv2WP/I", "l1_index/I",
    "l2_pt/F", "l2_eta/F" , "l2_phi/F", "l2_mvaTOP/F", "l2_mvaTOPv2/F", "l2_mvaTOPWP/I", "l2_mvaTOPv2WP/I", "l2_index/I",
    "l3_pt/F", "l3_eta/F" , "l3_phi/F", "l3_mvaTOP/F", "l3_mvaTOPv2/F", "l3_mvaTOPWP/I", "l3_mvaTOPv2WP/I", "l3_index/I",
    "JetGood[pt/F,eta/F,phi/F,area/F,btagDeepB/F,btagDeepFlavB/F,index/I]",
    "Jet[pt/F,eta/F,phi/F,mass/F,btagDeepFlavB/F]",
    "lep[pt/F,eta/F,phi/F,pdgId/I,muIndex/I,eleIndex/I,mvaTOP/F,mvaTOPWP/I,mediumId/I]",
    "Z1_l1_index/I", "Z1_l2_index/I", "nonZ1_l1_index/I", "nonZ1_l2_index/I",
    "Z1_phi/F", "Z1_pt/F", "Z1_mass/F", "Z1_cosThetaStar/F", "Z1_eta/F", "Z1_lldPhi/F", "Z1_lldR/F",
    "Muon[pt/F,eta/F,phi/F,dxy/F,dz/F,ip3d/F,sip3d/F,jetRelIso/F,miniPFRelIso_all/F,pfRelIso03_all/F,mvaTTH/F,pdgId/I,segmentComp/F,nStations/I,nTrackerLayers/I,mediumId/O,tightId/O,isPFcand/B,isTracker/B,isGlobal/B]",
    "Electron[pt/F,eta/F,phi/F,dxy/F,dz/F,ip3d/F,sip3d/F,jetRelIso/F,miniPFRelIso_all/F,pfRelIso03_all/F,mvaTTH/F,pdgId/I,vidNestedWPBitmap/I,deltaEtaSC/F]",
]

if "nLeptons4" in args.selection:
    read_variables.append("Z2_phi/F")
    read_variables.append("Z2_pt/F")
    read_variables.append("Z2_eta/F")
    read_variables.append("Z2_mass/F")

read_variables_MC = [
    "weight/F", 'reweightBTag_SF/F', 'reweightPU/F', 'reweightL1Prefire/F', 'reweightTrigger/F',
    "genZ1_pt/F", "genZ1_eta/F", "genZ1_phi/F",
    "Muon[genPartFlav/I]",
    VectorTreeVariable.fromString( "GenPart[pt/F,mass/F,phi/F,eta/F,pdgId/I,genPartIdxMother/I,status/I,statusFlags/I]", nMax=1000),
    'nGenPart/I',
    # 'LHEScaleWeight/F',
]


################################################################################
# define 3l selections
if "lepVeto" in args.selection:
    mu_string  = lepString('mu','VL')
else:
    mu_string  = lepString('mu','T') + "&&lep_mediumId"
    
ele_string = lepString('ele','T')

# print mu_string
# print ele_string
def getLeptonSelection( mode ):
    if   mode=="mumumu":   return "Sum$({mu_string})==3&&Sum$({ele_string})==0".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="mumue":    return "Sum$({mu_string})==2&&Sum$({ele_string})==1".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="muee":     return "Sum$({mu_string})==1&&Sum$({ele_string})==2".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="eee":      return "Sum$({mu_string})==0&&Sum$({ele_string})==3".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="mumumumu": return "Sum$({mu_string})==4&&Sum$({ele_string})==0".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="mumuee":   return "Sum$({mu_string})==2&&Sum$({ele_string})==2".format(mu_string=mu_string,ele_string=ele_string)
    elif mode=="eeee":     return "Sum$({mu_string})==0&&Sum$({ele_string})==4".format(mu_string=mu_string,ele_string=ele_string)

################################################################################
# Set up channels and values for plotting
yields     = {}
allPlots   = {}
allPlots_SM= {}

if not args.noData:
    data_sample.texName = "data"
    data_sample.setSelectionString([getLeptonSelection("mumumu")])
    data_sample.name           = "data"
    data_sample.style          = styles.errorStyle(ROOT.kBlack)

for sample in mc: sample.style = styles.fillStyle(sample.color)

weightnames = ['weight']
getters = map( operator.attrgetter, weightnames)
def weight_function( event, sample):
    # Calculate weight, this becomes: w = event.weightnames[0]*event.weightnames[1]*...
    w = reduce(operator.mul, [g(event) for g in getters], 1)
    # Get Lumi weight and multiply to weight
    yearstring = ""
    if event.year == 2016 and not event.preVFP:
        yearstring = "2016"
    elif event.year == 2016 and event.preVFP:
        yearstring = "2016_preVFP"
    elif event.year == 2017:
        yearstring = "2017"
    elif event.year == 2018:
        yearstring = "2018"
    lumi_weight = lumi_year[yearstring]/1000.
    w *= lumi_weight
    return w


for sample in mc:
    sample.read_variables = read_variables_MC
    sample.setSelectionString([getLeptonSelection("mumumu")])
    sample.weight = weight_function

stack = Stack(mc)
if not args.noData:
    stack = Stack(mc, data_sample)
    
    
# Use some defaults
selection_string = cutInterpreter.cutString(args.selection)
Plot.setDefaults(stack = stack, weight = plotweights, selectionString = selection_string)

################################################################################
# Now define the plots

plots = []

plots.append(Plot(
  name = 'yield', texX = '', texY = 'Number of Events',
  attribute = lambda event, sample: 0.5,
  binning=[4, 0, 4],
))

plots.append(Plot(
    name = "channel",
    texX = '', texY = 'Number of Events',
    attribute = lambda event, sample: event.channel,
    binning=[5, 0, 5],
))

plots.append(Plot(
    name = "Z1_pt",
    texX = 'p_{T}(Z_{1}) (GeV)', texY = 'Number of Events / 20 GeV',
    attribute = TreeVariable.fromString( "Z1_pt/F" ),
    binning=[50, 0, 1000],
))

plots.append(Plot(
    name = "M3l",
    texX = 'M(3l) (GeV)', texY = 'Number of Events',
    attribute = lambda event, sample:event.m3l,
    binning=[25,0,500],
))
    
plots.append(Plot(
    name = "l1_pt",
    texX = 'Leading lepton p_{T} (GeV)', texY = 'Number of Events / 40 GeV',
    attribute = TreeVariable.fromString( "l1_pt/F" ),
    binning=[25, 0, 1000],
))


plots.append(Plot(
    name = "Z1_pt_rebin5",
    texX = 'p_{T}(Z_{1}) (GeV)', texY = 'Number of Events / 100 GeV',
    attribute = TreeVariable.fromString( "Z1_pt/F" ),
    binning=[10, 0, 1000],
))


plots.append(Plot(
    name = "N_jets",
    texX = 'Number of jets', texY = 'Number of Events',
    attribute = lambda event, sample: event.nJetGood,
    binning=[16, -0.5, 15.5],
))
        
plots.append(Plot(
    name = "N_bjets",
    texX = 'Number of b-tagged jets', texY = 'Number of Events',
    attribute = lambda event, sample: event.nBTag,
    binning=[16, -0.5, 15.5],
))
        

plots.append(Plot(
    name = "mvaTOPscore",
    texX = 'Leading lepton MVA score', texY = 'Number of Events',
    attribute = lambda event, sample: event.l1_mvaTOP,
    binning=[30, -1.5, 1.5],
))
    
plots.append(Plot(
    name = "mvaTOPscore_v2",
    texX = 'Leading lepton MVA v2 score', texY = 'Number of Events',
    attribute = lambda event, sample: event.l1_mvaTOPv2,
    binning=[30, -1.5, 1.5],
))
                
plots.append(Plot(
    name = "nLeptons",
    texX = 'Number of leptons', texY = 'Number of Events',
    attribute = lambda event, sample: event.nlep,
    binning=[11, -0.5, 10.5],
))  

plots.append(Plot(
    name = "nLeptons_VL",
    texX = 'Number of leptons (very loose WP)', texY = 'Number of Events',
    attribute = lambda event, sample: event.nMuons_VL + event.nElectrons_VL,
    binning=[11, -0.5, 10.5],
))  

plots.append(Plot(
    name = "nLeptons_T",
    texX = 'Number of leptons (tight WP)', texY = 'Number of Events',
    attribute = lambda event, sample: event.nMuons_T + event.nElectrons_T,
    binning=[11, -0.5, 10.5],
))  

plots.append(Plot(
    name = "nElectrons",
    texX = 'Number of electrons', texY = 'Number of Events',
    attribute = lambda event, sample: event.nElectrons_all,
    binning=[11, -0.5, 10.5],
))   

plots.append(Plot(
    name = "nElectrons_VL",
    texX = 'Number of electrons (very loose WP)', texY = 'Number of Events',
    attribute = lambda event, sample: event.nElectrons_VL,
    binning=[11, -0.5, 10.5],
))  

plots.append(Plot(
    name = "nElectrons_T",
    texX = 'Number of electrons (tight WP)', texY = 'Number of Events',
    attribute = lambda event, sample: event.nElectrons_T,
    binning=[11, -0.5, 10.5],
))   

plots.append(Plot(
    name = "nMuons",
    texX = 'Number of muons', texY = 'Number of Events',
    attribute = lambda event, sample: event.nMuons_all,
    binning=[11, -0.5, 10.5],
))   

plots.append(Plot(
    name = "nMuons_VL",
    texX = 'Number of muons (very loose WP)', texY = 'Number of Events',
    attribute = lambda event, sample: event.nMuons_VL,
    binning=[11, -0.5, 10.5],
))  

plots.append(Plot(
    name = "nMuons_T",
    texX = 'Number of muons (tight WP)', texY = 'Number of Events',
    attribute = lambda event, sample: event.nMuons_T,
    binning=[11, -0.5, 10.5],
))   

plots.append(Plot(
    name = "nMuons_mediumID",
    texX = 'Number of muons (mediumId)', texY = 'Number of Events',
    attribute = lambda event, sample: event.nMuons_mediumId_all,
    binning=[11, -0.5, 10.5],
))   

plots.append(Plot(
    name = "nMuons_mediumID_VL",
    texX = 'Number of muons (mediumId + very loose WP)', texY = 'Number of Events',
    attribute = lambda event, sample: event.nMuons_mediumId_VL,
    binning=[11, -0.5, 10.5],
))  

plots.append(Plot(
    name = "nMuons_mediumID_T",
    texX = 'Number of muons (mediumId + tight WP)', texY = 'Number of Events',
    attribute = lambda event, sample: event.nMuons_mediumId_T,
    binning=[11, -0.5, 10.5],
))   

plotting.fill(plots, read_variables = read_variables, sequence = sequence)


for plot in plots:
    if plot.name == "channel":
        for i, l in enumerate(plot.histos):
            for j, h in enumerate(l):
                h.GetXaxis().SetBinLabel(1, "other")
                h.GetXaxis().SetBinLabel(2, "#mu#mu#mu")
                h.GetXaxis().SetBinLabel(3, "#mu#mue")
                h.GetXaxis().SetBinLabel(4, "#muee")
                h.GetXaxis().SetBinLabel(5, "eee")

drawPlots(plots)







logger.info( "Done with prefix %s and selectionString %s", args.selection, cutInterpreter.cutString(args.selection) )
