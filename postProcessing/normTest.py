#!/usr/bin/env python
import ROOT, os

from Analysis.Tools.DirDB import DirDB
normalizationDB = DirDB(os.path.join( "/users/dennis.schwarz/caches", 'normalizationCache'))


def printBins(hist):
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        print i+1, hist.GetBinContent(i+1)



from Samples.nanoAOD.UL16_privateDennis_nanoAODAPVv9  import allSamples as eftSamples16pre
from Samples.nanoAOD.UL16_privateDennis_nanoAODv9  import allSamples as eftSamples16
from Samples.nanoAOD.UL17_privateDennis_nanoAODv9  import allSamples as eftSamples17
from Samples.nanoAOD.UL18_privateDennis_nanoAODv9  import allSamples as eftSamples18

from Samples.nanoAOD.UL16_nanoAODAPVv9  import allSamples as mcSamples16pre
from Samples.nanoAOD.UL16_nanoAODv9  import allSamples as mcSamples16
from Samples.nanoAOD.UL17_nanoAODv9  import allSamples as mcSamples17
from Samples.nanoAOD.UL18_nanoAODv9  import allSamples as mcSamples18

samples = {
    "2016preVFP": eftSamples16pre+mcSamples16pre,
    "2016": eftSamples16+mcSamples16,
    "2017": eftSamples17+mcSamples17,
    "2018": eftSamples18+mcSamples18,
}



missing = []

for year in ["2016preVFP", "2016", "2017", "2018"]:
    print "--------------------------------------------------------------------"
    print year
    for sample in samples[year]:
        print sample.name, sample.DAS

        scale_norm_histo = normalizationDB.get( key=(sample.DAS, "LHEScaleWeight" ) )
        pdf_norm_histo   = normalizationDB.get( key=(sample.DAS, "LHEPdfWeight" ) )
        ps_norm_histo    = normalizationDB.get( key=(sample.DAS, "PSWeight" ) )

        stuffmissing = []

        if scale_norm_histo is None:
            print "-- SCALE MISSING"
            stuffmissing.append("scale")
            print "-- PDF MISSING"
            stuffmissing.append("pdf")
        if ps_norm_histo is None:
            print "-- PS MISSING"
            stuffmissing.append("ps")

        if len(stuffmissing) > 0:
            missing.append( (year, sample, stuffmissing) )


        print "-----------------"
        printBins(ps_norm_histo)

        # if "TTHTobb" in sample.name:
        #     print "-----------------"
        #     printBins(scale_norm_histo)
        #     print "-----------------"
        #     printBins(pdf_norm_histo)
        #     print "-----------------"
        #     printBins(ps_norm_histo)
print "--------------------------------------------------------------------"
print "--------------------------------------------------------------------"
print "--------------------------------------------------------------------"
for m in missing:
    print m
