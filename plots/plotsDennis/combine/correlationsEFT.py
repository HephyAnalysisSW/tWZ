import ROOT
from tWZ.Tools.helpers                           import getObjFromFile

file = "/users/dennis.schwarz/CMSSW_10_6_28/src/tWZ/plots/plotsDennis/combine/DataCards_threePoint_light_minus_UNBLINDED_binning-A_SMZero/ULRunII/fitDiagnostics.topEFT_ULRunII_combined_13TeV_ULRunII_2D-cHq3MRe1122-cHq3MRe33_float_noScan_SHAPES.root"

POInames = [
    "k_cHqMRe1122",
    "k_cHqMRe33",
    "k_cHq3MRe1122",
    "k_cHq3MRe33",
]



h_full_cor = getObjFromFile(file, "covariance_fit_s")

NbinsX = h_full_cor.GetXaxis().GetNbins()
NbinsY = h_full_cor.GetYaxis().GetNbins()

for i in range(NbinsX):
    binX = i+1
    labelX = h_full_cor.GetXaxis().GetBinLabel(binX)
    if labelX not in POInames:
        continue
    for j in range(NbinsY):
        binY = j+1
        labelY = h_full_cor.GetYaxis().GetBinLabel(binY)
        if labelY not in POInames:
            continue
        print labelX, labelY, h_full_cor.GetBinContent(binX,binY)
