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
argParser.add_argument('--plot_directory', action='store', default='FakeRate_v1')
argParser.add_argument('--era',            action='store', type=str, default="UL2018")
argParser.add_argument('--selection',      action='store', default='trilepT-minDLmass12-onZ1-njet4p-btag1p')
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
# Possible SYS variations
variations = [
    "Trigger_UP", "Trigger_DOWN",
    "LepID_UP", "LepID_DOWN",
    "BTag_b_UP", "BTag_b_DOWN",
    "BTag_l_UP", "BTag_l_DOWN",
    "PU_UP", "PU_DOWN",
    "JES_UP", "JES_DOWN",
    "Scale_UPUP", "Scale_UPNONE", "Scale_NONEUP", "Scale_NONEDOWN", "Scale_DOWNNONE", "Scale_DOWNDOWN",
]

jet_variations = {
    "JES_UP": "jesTotalUp",
    "JES_DOWN": "jesTotalDown",
    "JER_UP": "jerUp",
    "JER_DOWN": "jerDown",
}
################################################################################
# Check if we know the variation else don't use data!
if args.sys not in variations:
    if args.sys == "central":
        logger.info( "Running central samples (no sys variation)")
    else:
        raise RuntimeError( "Variation %s not among the known: %s", args.sys, ",".join( variations ) )
else:
    logger.info( "Running sys variation %s, noData is set to 'True'", args.sys)
    args.noData = True


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
# Selection modifier
def jetSelectionModifier( sys, returntype = "func"):
    #Need to make sure all jet variations of the following observables are in the ntuple
    variiedJetObservables = ['nJetGood', 'nBTag', 'met_pt']
    if returntype == "func":
        def changeCut_( string ):
            for s in variiedJetObservables:
                string = string.replace(s, s+'_'+sys)
                if "met_pt" in string:
                    string = string.replace("met_pt", "MET_T1_pt")
            return string
        return changeCut_
    elif returntype == "list":
        list = []
        for v in variiedJetObservables:
            string = v+'_'+sys
            if "met_pt" in string:
                string = string.replace("met_pt", "MET_T1_pt")
            list.append(string)    
        return list

def metSelectionModifier( sys, returntype = 'func'):
    #Need to make sure all MET variations of the following observables are in the ntuple
    variiedMetObservables = ['met_pt']
    if returntype == "func":
        def changeCut_( string ):
            for s in variiedMetObservables:
                string = string.replace(s, s+'_'+sys)
                if "met_pt" in string:
                    string = string.replace("met_pt", "MET_T1_pt")
            return string
        return changeCut_
    elif returntype == "list":
        list = []
        for v in variiedMetObservables:
            string = v+'_'+sys
            if "met_pt" in string:
                string = string.replace("met_pt", "MET_T1_pt")
            list.append(string)    
        return list

################################################################################
# get scale weight
def getScaleWeight(event, sys):
    # Sometimes the nominal entry [4] is missing, so be careful
    weights_9point = {
        "Scale_DOWNDOWN": 0,
        "Scale_DOWNNONE": 1,
        "Scale_NONEDOWN": 3,
        "Scale_NONEUP"  : 5,
        "Scale_UPNONE"  : 7,
        "Scale_UPUP"    : 8,
    }
    weights_8point = {
        "Scale_DOWNDOWN": 0,
        "Scale_DOWNNONE": 1,
        "Scale_NONEDOWN": 3,
        "Scale_NONEUP"  : 4,
        "Scale_UPNONE"  : 6,
        "Scale_UPUP"    : 7,
    }
    index = -1
    if event.nScale == 9:
        index = weights_9point[sys]
    elif event.nScale == 8:
        index = weights_8point[sys]
    else:
        print "UNEXPECTED NUMBER OF SCALE WEIGHTS:", event.nScale,", not applying any weight"
        return 1.0
    return event.Scale_Weight[index]
################################################################################
# Add a selection selectionModifier

if args.sys in jet_variations.keys():
    selectionModifier = jetSelectionModifier(jet_variations[args.sys])
else:
    selectionModifier = None

################################################################################
# Define the MC samples
from tWZ.samples.nanoTuples_ULRunII_nanoAODv9_postProcessed import *

if args.era == "UL2016":
    mc = []
elif args.era == "UL2016preVFP":
    mc = []
elif args.era == "UL2017":
    mc = []
elif args.era == "UL2018":
    mc = []
elif args.era == "ULRunII":
    mc = []

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
elif args.era == "ULRunII":
    datastring = "RunII"
    lumistring = "RunII"

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
# Lepton SF
LeptonWP = "tight"
if "trilepVL" in args.selection:
    LeptonWP = "VL"
    
### TODO: SETUP SF FOR MEDIUM WP
    
leptonSF16 = leptonSF_topMVA(2016, LeptonWP)
leptonSF17 = leptonSF_topMVA(2017, LeptonWP)
leptonSF18 = leptonSF_topMVA(2018, LeptonWP)

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
      (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV)'% ( lumi_scale) ) if plotData else (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV)' % lumi_scale)
    ]
    if "mt2ll100" in args.selection and args.noData: lines += [(0.55, 0.5, 'M_{T2}(ll) > 100 GeV')] # Manually put the mt2ll > 100 GeV label
    return [tex.DrawLatex(*l) for l in lines]

def drawPlots(plots, mode):
    for log in [False, True]:
        plot_directory_ = os.path.join(plot_directory, 'FakeRate', args.plot_directory, args.era, mode + ("_log" if log else ""), args.selection)
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



################################################################################
# Read variables

read_variables = [
    "weight/F", "year/I", "preVFP/O", "met_pt/F", "met_phi/F", "nJetGood/I", "PV_npvsGood/I",  "nJet/I", "nBTag/I", 
    "l1_pt/F", "l1_eta/F" , "l1_phi/F", "l1_mvaTOP/F", "l1_mvaTOPv2/F", "l1_mvaTOPWP/I", "l1_mvaTOPv2WP/I", "l1_index/I",
    # "l2_pt/F", "l2_eta/F" , "l2_phi/F", "l2_mvaTOP/F", "l2_mvaTOPv2/F", "l2_mvaTOPWP/I", "l2_mvaTOPv2WP/I", "l2_index/I",
    # "l3_pt/F", "l3_eta/F" , "l3_phi/F", "l3_mvaTOP/F", "l3_mvaTOPv2/F", "l3_mvaTOPWP/I", "l3_mvaTOPv2WP/I", "l3_index/I",
    # "l4_pt/F", "l4_eta/F" , "l4_phi/F", "l4_mvaTOP/F", "l4_mvaTOPv2/F", "l4_mvaTOPWP/I", "l4_mvaTOPv2WP/I", "l4_index/I",
    "JetGood[pt/F,eta/F,phi/F,area/F,btagDeepB/F,btagDeepFlavB/F,index/I]",
    "Jet[pt/F,eta/F,phi/F,mass/F,btagDeepFlavB/F]",
    "lep[pt/F,eta/F,phi/F,pdgId/I,muIndex/I,eleIndex/I,mediumId/O]",
    # "Z1_l1_index/I", "Z1_l2_index/I", "nonZ1_l1_index/I", "nonZ1_l2_index/I",
    # "Z1_phi/F", "Z1_pt/F", "Z1_mass/F", "Z1_cosThetaStar/F", "Z1_eta/F", "Z1_lldPhi/F", "Z1_lldR/F",
    "Muon[pt/F,eta/F,phi/F,dxy/F,dz/F,ip3d/F,sip3d/F,jetRelIso/F,miniPFRelIso_all/F,pfRelIso03_all/F,mvaTTH/F,pdgId/I,segmentComp/F,nStations/I,nTrackerLayers/I,mediumId/O,tightId/O,isPFcand/B,isTracker/B,isGlobal/B]",
    "Electron[pt/F,eta/F,phi/F,dxy/F,dz/F,ip3d/F,sip3d/F,jetRelIso/F,miniPFRelIso_all/F,pfRelIso03_all/F,mvaTTH/F,pdgId/I,vidNestedWPBitmap/I,deltaEtaSC/F]",
]

read_variables_MC = [
    "weight/F", 'reweightBTag_SF/F', 'reweightPU/F', 'reweightL1Prefire/F', 'reweightTrigger/F',
    "genZ1_pt/F", "genZ1_eta/F", "genZ1_phi/F",
    "Muon[genPartFlav/I]",
    VectorTreeVariable.fromString( "GenPart[pt/F,mass/F,phi/F,eta/F,pdgId/I,genPartIdxMother/I,status/I,statusFlags/I]", nMax=1000),
    'nGenPart/I',
    # 'nScale/I', 'Scale[Weight/F]',
    # 'nPDF/I', VectorTreeVariable.fromString('PDF[Weight/F]',nMax=150),    
]



################################################################################
# MVA

################################################################################
# Set up plotting

if not args.noData:
    data_sample.texName = "data"
    data_sample.setSelectionString([getLeptonSelection(mode)])
    data_sample.name           = "data"
    data_sample.style          = styles.errorStyle(ROOT.kBlack)

for sample in mc: sample.style = styles.fillStyle(sample.color)

###### SYS #################################################################
if args.sys in jet_variations:
    new_variables = ['%s/F'%v for v in jetSelectionModifier(jet_variations[args.sys],'list')]
    read_variables_MC += new_variables
    read_variables    += new_variables

weightnames = ['weight', 'reweightBTag_SF', 'reweightPU', 'reweightL1Prefire' , 'reweightTrigger'] # 'reweightLeptonMVA'
# weightnames = ['weight']
sys_weights = {
    "BTag_b_UP"     : ('reweightBTag_SF','reweightBTag_SF_b_Up'),
    "BTag_b_DOWN"   : ('reweightBTag_SF','reweightBTag_SF_b_Down'),
    "BTag_l_UP"     : ('reweightBTag_SF','reweightBTag_SF_l_Up'),
    "BTag_l_DOWN"   : ('reweightBTag_SF','reweightBTag_SF_l_Down'),
    'Trigger_UP'    : ('reweightTrigger','reweightTriggerUp'),
    'Trigger_DOWN'  : ('reweightTrigger','reweightTriggerDown'),
    'PU_UP'         : ('reweightPU','reweightPUUp'),
    'PU_DOWN'       : ('reweightPU','reweightPUDown'),
    # For lepton SF this is set in the sequence
}

if args.sys in sys_weights:
    oldname, newname = sys_weights[args.sys]
    for i, weight in enumerate(weightnames):
        if weight == oldname:
            weightnames[i] = newname
            read_variables_MC += ['%s/F'%(newname)]

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
    # Multiply Scale weight 
    if "Scale_" in args.sys:
        scale_weight = getScaleWeight(event, args.sys)
        w *= scale_weight
    return w


for sample in mc:
    sample.read_variables = read_variables_MC
    sample.setSelectionString([getLeptonSelection(mode)])
    sample.weight = weight_function


if not args.noData:
    stack = Stack(mc, data_sample)
else:
    stack = Stack(mc)


# Use some defaults
selection_string = cutInterpreter.cutString(args.selection)
Plot.setDefaults(stack = stack, weight = plotweights, selectionString = selection_string)

################################################################################
# Now define the plots

plots = []

plots.append(Plot(
    name = "l1_pt",
    texX = 'Leading lepton p_{T} (GeV)', texY = 'Number of Events / 40 GeV',
    attribute = TreeVariable.fromString( "l1_pt/F" ),
    binning=[25, 0, 1000],
))
           

plotting.fill(plots, read_variables = read_variables, sequence = sequence)


################################################################################
# Draw Plots
drawPlots(plots, mode)


plots_root = ["l1_pt"]

# Write Result Hist in root file
print "Now write results in root file."
plot_dir = os.path.join(plot_directory, 'FakeRate', args.plot_directory, args.era, args.selection)
if not os.path.exists(plot_dir):
    try:
        os.makedirs(plot_dir)
    except:
        print 'Could not create', plot_dir
outfilename = plot_dir+'/Results.root'
print "Saving in", outfilename
outfile = ROOT.TFile(outfilename, 'recreate')
outfile.cd()
for plot in plots:
    if plot.name in plots_root:
        for idx, histo_list in enumerate(plot.histos):
            for j, h in enumerate(histo_list):
                histname = h.GetName()
                if "TWZ_NLO_DR" in histname: process = "tWZ"
                elif "tWZToLL01j_lepWFilter" in histname: process = "tWZ"
                elif "TTZ" in histname: process = "ttZ"
                elif "ttZ01j" in histname: process = "ttZ"
                elif "ttZ01j_lepWFilter" in histname: process = "ttZ"
                elif "TTX_rare" in histname: process = "ttX"
                elif "TZQ" in histname: process = "tZq"
                elif "WZTo3LNu" in histname: process = "WZ"
                elif "WZ" in histname: process = "WZ"
                elif "ZZ" in histname: process = "ZZ"
                elif "triBoson" in histname: process = "triBoson"
                elif "nonprompt" in histname: process = "nonprompt"
                elif "data" in histname: process = "data"
                h.Write(plot.name+"__"+process)
outfile.Close()



logger.info( "Done with prefix %s and selectionString %s", args.selection, cutInterpreter.cutString(args.selection) )
