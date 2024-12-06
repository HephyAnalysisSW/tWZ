import ROOT
from math                                        import sqrt
from tWZ.Tools.helpers                           import getObjFromFile


for year in ["2016preVFP", "2016", "2017", "2018"]:
    path = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v14_reduceEFT_threePoint_noData/UL"+year+"/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/"

    sysnames = {
        "JES":                            ("JES_UP", "JES_DOWN"),
        "JES_AbsoluteMPFBias":            ("AbsoluteMPFBias_UP", "AbsoluteMPFBias_DOWN"),
        "JES_AbsoluteScale":              ("AbsoluteScale_UP", "AbsoluteScale_DOWN"),
        "JES_AbsoluteStat_"+year:         ("AbsoluteStat_"+year+"_UP", "AbsoluteStat_"+year+"_DOWN"),
        "JES_RelativeBal":                ("RelativeBal_UP", "RelativeBal_DOWN"),
        "JES_RelativeFSR":                ("RelativeFSR_UP", "RelativeFSR_DOWN"),
        "JES_RelativeJEREC1_"+year:       ("RelativeJEREC1_"+year+"_UP", "RelativeJEREC1_"+year+"_DOWN"),
        "JES_RelativeJEREC2_"+year:       ("RelativeJEREC2_"+year+"_UP", "RelativeJEREC2_"+year+"_DOWN"),
        "JES_RelativeJERHF":              ("RelativeJERHF_UP", "RelativeJERHF_DOWN"),
        "JES_RelativePtBB":               ("RelativePtBB_UP", "RelativePtBB_DOWN"),
        "JES_RelativePtEC1_"+year:        ("RelativePtEC1_"+year+"_UP", "RelativePtEC1_"+year+"_DOWN"),
        "JES_RelativePtEC2_"+year:        ("RelativePtEC2_"+year+"_UP", "RelativePtEC2_"+year+"_DOWN"),
        "JES_RelativePtHF":               ("RelativePtHF_UP", "RelativePtHF_DOWN"),
        "JES_RelativeStatEC_"+year:       ("RelativeStatEC_"+year+"_UP", "RelativeStatEC_"+year+"_DOWN"),
        "JES_RelativeStatFSR_"+year:      ("RelativeStatFSR_"+year+"_UP", "RelativeStatFSR_"+year+"_DOWN"),
        "JES_RelativeStatHF_"+year:       ("RelativeStatHF_"+year+"_UP", "RelativeStatHF_"+year+"_DOWN"),
        "JES_RelativeSample_"+year:       ("RelativeSample_"+year+"_UP", "RelativeSample_"+year+"_DOWN"),
        "JES_PileUpDataMC":               ("PileUpDataMC_UP", "PileUpDataMC_DOWN"),
        "JES_PileUpPtBB":                 ("PileUpPtBB_UP", "PileUpPtBB_DOWN"),
        "JES_PileUpPtEC1":                ("PileUpPtEC1_UP", "PileUpPtEC1_DOWN"),
        "JES_PileUpPtEC2":                ("PileUpPtEC2_UP", "PileUpPtEC2_DOWN"),
        "JES_PileUpPtHF":                 ("PileUpPtHF_UP", "PileUpPtHF_DOWN"),
        "JES_PileUpPtRef":                ("PileUpPtRef_UP", "PileUpPtRef_DOWN"),
        "JES_FlavorQCD":                  ("FlavorQCD_UP", "FlavorQCD_DOWN"),
        "JES_Fragmentation":              ("Fragmentation_UP", "Fragmentation_DOWN"),
        "JES_SinglePionECAL":             ("SinglePionECAL_UP", "SinglePionECAL_DOWN"),
        "JES_SinglePionHCAL":             ("SinglePionHCAL_UP", "SinglePionHCAL_DOWN"),
        "JES_TimePtEta_"+year:            ("TimePtEta_"+year+"_UP", "TimePtEta_"+year+"_DOWN"),
    }

    binOfChoice = 2

    deltaUp_total = 0
    deltaDown_total = 0
    deltaUp_sum2 = 0
    deltaDown_sum2 = 0
    histname = "Z1_pt"
    process = "ttZ_sm"

    for sys in sysnames.keys():
        hist = getObjFromFile(path+"Results.root", histname+"__"+process)
        upname, downname = sysnames[sys]
        sysdirUP = path.replace('/Run', '_'+upname+'/Run').replace('/UL', '_'+upname+'/UL')
        sysdirDOWN = path.replace('/Run', '_'+downname+'/Run').replace('/UL', '_'+downname+'/UL')
        histUP   = getObjFromFile(sysdirUP+"Results.root", histname+"__"+process)
        histDOWN = getObjFromFile(sysdirDOWN+"Results.root", histname+"__"+process)
        deltaUp = histUP.GetBinContent(binOfChoice) - hist.GetBinContent(binOfChoice)
        deltaDown = histDOWN.GetBinContent(binOfChoice) - hist.GetBinContent(binOfChoice)
        if sys == "JES":
            deltaUp_total = deltaUp
            deltaDown_total = deltaDown
        else:
            deltaUp_sum2 += deltaUp*deltaUp
            deltaDown_sum2 += deltaDown*deltaDown

    print "====================================================================="
    print year
    print deltaUp_total, deltaDown_total
    print sqrt(deltaUp_sum2), sqrt(deltaDown_sum2)
