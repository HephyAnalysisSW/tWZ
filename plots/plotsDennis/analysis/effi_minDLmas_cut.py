import ROOT
from tWZ.Tools.helpers import getObjFromFile

selections = {
    "ttZ": "trilepT-minDLmassVETO-onZ1-njet3p-btag1p",
    "WZ" : "trilepT-minDLmassVETO-onZ1-btag0-met60",
    "ZZ" : "qualepT-minDLmassVETO-onZ1-onZ2",
}

path = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_noData/UL2018/all/<SELECTION>/Results.root"

for region in selections.keys():
    path_fail = path.replace("<SELECTION>", selections[region])
    path_pass = path_fail.replace("minDLmassVETO", "minDLmass12")
    h_fail = getObjFromFile(path_fail, "Z1_pt__"+region)
    h_pass = getObjFromFile(path_pass, "Z1_pt__"+region)
    N_fail = h_fail.Integral()
    N_pass = h_pass.Integral()
    print(region, ": efficiency =", N_pass/(N_pass+N_fail))
