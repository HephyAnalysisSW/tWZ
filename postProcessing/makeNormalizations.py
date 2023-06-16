#!/usr/bin/env python

# Standard imports
import ROOT
import os
import sys

import tWZ.Tools.user as user

def get_parser():
    ''' Argument parser for post-processing module.
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser for cmgPostProcessing")

    argParser.add_argument('--logLevel',    action='store',        nargs='?',  choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'],   default='INFO', help="Log level for logging" )
    argParser.add_argument('--DAS',         action='store',        nargs='?',  type=str, default=None,   help="DAS name" )
    argParser.add_argument('--sampleFile',  action='store',        nargs='?',  type=str, default=None,   help="E.g. Samples.nanoAOD.UL16_nanoAODv9" )
    argParser.add_argument('--small',       action='store_true',                                         help="Run the file on a small sample (for test purpose), bool flag set to True if used" )
    argParser.add_argument('--vector',      action='store',        nargs='?',  type=str, default=None,   help="Which vector shall we add up?" )
    argParser.add_argument('--sample',      action='store',        nargs='?',  type=str, default=None,   help="Which sample?" )
    argParser.add_argument('--len',         action='store',        nargs='?',  type=int, default=-1,     help="What is the length?" )
    argParser.add_argument('--overwrite',   action='store_true',   help="Overwrite?" )
    argParser.add_argument('--TopNanoAOD',action='store_true',     help="Is the sample a TopNanoAOD?")
    return argParser

args = get_parser().parse_args()

# dirDB
from Analysis.Tools.DirDB import DirDB
dirDB = DirDB(os.path.join( user.cache_dir, 'normalizationCache'))

jobFileName = "jobsNormalizations.sh"

# If no sample argument, let us write all possible samples to the job file
if args.DAS is None:
    exec( "from %s import allSamples as samples"%args.sampleFile )
    with open( jobFileName, 'w' if not os.path.exists(jobFileName) else "a" ) as f:
        for sample in samples:
            if not hasattr(sample, "DAS") or (not sample.DAS):
                continue
            f.write("python makeNormalizations.py --sampleFile %s --sample %s --DAS %s %s --vector LHEPdfWeight --len 103\n"%(args.sampleFile, sample.name, sample.DAS, '--overwrite' if args.overwrite else ''))
            if args.TopNanoAOD:
                f.write("python makeNormalizations.py --sampleFile %s --sample %s --DAS %s %s --vector PSWeight --len 44\n"      %(args.sampleFile, sample.name, sample.DAS, '--overwrite' if args.overwrite else ''))
            else:
                f.write("python makeNormalizations.py --sampleFile %s --sample %s --DAS %s %s --vector PSWeight --len 4\n"      %(args.sampleFile, sample.name, sample.DAS, '--overwrite' if args.overwrite else ''))
            f.write("python makeNormalizations.py --sampleFile %s --sample %s --DAS %s %s --vector LHEScaleWeight --len 9\n"%(args.sampleFile, sample.name, sample.DAS, '--overwrite' if args.overwrite else ''))
        f.write("\n")

    print ("%i job commands added to %s" % ( 3*len(samples), jobFileName))
    sys.exit(0)

# Logging
import tttt.Tools.logger as _logger
logger  = _logger.get_logger(args.logLevel)
#import RootTools.core.logger as _logger_rt
#logger_rt = _logger_rt.get_logger(args.logLevel)
import Analysis.Tools.logger as _logger_an
logger_an = _logger_an.get_logger(args.logLevel)

exec( "from %s import allSamples as samples"% args.sampleFile )

# Catch the rare cases where the sample.name is different from the name in the file (otherwise we could do an import...)
sample = None
for _sample in samples:
    if _sample.name == args.sample:
        sample = _sample
        break
if sample==None:
    raise RuntimeError( "Did not find sample %s in %s"%( args.sample, args.sampleFile) )

if args.small:
    sample.reduceFiles(to=1)

key = (args.DAS, args.vector)

if (not dirDB.contains( key )) or args.overwrite:
    h    = sample.get1DHistoFromDraw("Iteration$", [args.len,0,args.len], weightString=args.vector+"*genWeight")
    norm = sample.getYieldFromDraw(weightString="genWeight")
    h.Scale(1./norm['val'])

    if not args.small:
        dirDB.add( key=(args.DAS, args.vector), data=h, overwrite=args.overwrite )
else:
    print ("Found key %s"%repr( key ) )
