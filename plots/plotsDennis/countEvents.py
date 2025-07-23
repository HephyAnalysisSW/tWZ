import ROOT
from tWZ.Tools.helpers import getObjFromFile

string_template = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_threePoint_onlyData/YEAR/all/SELECTION/Results.root"

years = ["UL2016preVFP", "UL2016", "UL2017", "UL2018"]
selections = [
    "trilepT-minDLmass12-onZ1-njet3p-btag1p",
    "trilepT-minDLmass12-onZ1-btag0-met60",
    "qualepT-minDLmass12-onZ1-onZ2",
]

histname = "Z1_pt__data"

bin_low, bin_high = 41, 50
printedBounds = False

for sel in selections:
    count = 0
    for year in years:
        filename = string_template.replace("YEAR", year).replace("SELECTION", sel)
        hist = getObjFromFile(filename, histname)
        if not printedBounds:
            low = hist.GetBinCenter(bin_low) - 0.5*hist.GetBinWidth(bin_low)
            high = hist.GetBinCenter(bin_high) + 0.5*hist.GetBinWidth(bin_high)
            print("Lower = %.f, higher = %.f"%(low, high))
            printedBounds = True
        count += hist.Integral(bin_low, bin_high)
    print(sel, count)
