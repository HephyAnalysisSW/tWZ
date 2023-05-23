#!/usr/bin/env python
import ROOT, os

from Analysis.Tools.DirDB import DirDB
normalizationDB = DirDB(os.path.join( "/users/dennis.schwarz/caches", 'normalizationCache'))


def printBins(hist):
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        print i+1, hist.GetBinContent(i+1)




from Samples.nanoAOD.UL18_privateDennis_nanoAODv9  import ZZ_EFT

DASname = ZZ_EFT.DAS

scale_norm_histo = normalizationDB.get( key=(DASname, "LHEScaleWeight" ) )
pdf_norm_histo   = normalizationDB.get( key=(DASname, "LHEPdfWeight" ) )
ps_norm_histo    = normalizationDB.get( key=(DASname, "PSWeight" ) )

print "-----------------"
printBins(scale_norm_histo)
print "-----------------"
printBins(pdf_norm_histo)
print "-----------------"
printBins(ps_norm_histo)
