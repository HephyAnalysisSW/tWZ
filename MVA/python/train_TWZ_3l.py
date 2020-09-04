#!/usr/bin/env python

# Analysis
from Analysis.TMVA.Trainer       import Trainer
from Analysis.TMVA.Reader        import Reader
from Analysis.TMVA.defaults      import default_methods, default_factory_settings 
import Analysis.Tools.syncer

# TopEFT
from tWZ.Tools.user              import plot_directory, mva_directory
from tWZ.Tools.cutInterpreter    import cutInterpreter

# MVA configuration
from tWZ.MVA.MVA_TWZ_3l          import sequence, read_variables, mva_variables 
from tWZ.MVA.MVA_TWZ_3l          import mlp1 #,bdt 

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--plot_directory',     action='store',             default=None)
argParser.add_argument('--selection',          action='store', type=str,   default='trilepM-onZ1')
argParser.add_argument('--trainingFraction',   action='store', type=float, default=0.5)
argParser.add_argument('--small',              action='store_true')
argParser.add_argument('--overwrite',          action='store_true')

args = argParser.parse_args()

#Logger
import tWZ.Tools.logger as logger
logger = logger.get_logger("DEBUG", logFile = None )
#import Analysis.Tools.logger as logger_an
#logger_an = logger_an.get_logger("DEBUG", logFile = None )

if args.plot_directory == None:
    args.plot_directory = plot_directory

if args.selection == None:
    selectionString = "(1)"
else:
    selectionString = cutInterpreter.cutString( args.selection )

# Samples
#from tWZ.samples.nanoTuples_RunII_nanoAODv6_private_postProcessed    import *
from tWZ.samples.nanoTuples_Summer16_nanoAODv6_private_postProcessed import *

signal = TWZ_NLO_DR 
#signal.reduceFiles(factor=20)
#TTZ.reduceFiles(factor=3)

# TTZ
backgrounds = [ TTZ ]

samples = backgrounds + [signal]
for sample in samples:
    sample.setSelectionString( selectionString )
    if args.small:
        sample.reduceFiles(to = 1)

mvas = [mlp1]

## TMVA Trainer instance
trainer = Trainer( 
    signal = signal, 
    backgrounds = backgrounds, 
    output_directory = mva_directory, 
    plot_directory   = plot_directory, 
    mva_variables    = mva_variables,
    label            = "TWZ_3l", 
    fractionTraining = args.trainingFraction, 
    )

weightString = "(1)"
trainer.createTestAndTrainingSample( 
    read_variables   = read_variables,   
    sequence         = sequence,
    weightString     = weightString,
    overwrite        = args.overwrite, 
    )

#trainer.addMethod(method = default_methods["BDT"])
#trainer.addMethod(method = default_methods["MLP"])

for mva in mvas:
    trainer.addMethod(method = mva)

trainer.trainMVA( factory_settings = default_factory_settings )
trainer.plotEvaluation()

#reader.addMethod(method = bdt1)
#reader.addMethod(method = default_methods["MLP"])

#print reader.evaluate("BDT", met_pt=100, ht=-210, Z1_pt_4l=100, lnonZ1_pt=100, lnonZ1_eta=0)
#prinMt reader.evaluate("BDT", met_pt=120, ht=-210)
