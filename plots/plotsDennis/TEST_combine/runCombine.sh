text2workspace.py topEFT__1_13TeV_.txt -m 125
combineTool.py -M Impacts -d topEFT__1_13TeV_.root -m 125 --doInitialFit --robustFit 1
combineTool.py -M Impacts -d topEFT__1_13TeV_.root -m 125 --robustFit 1 --doFits
combineTool.py -M Impacts -d topEFT__1_13TeV_.root -m 125 -o impacts_datacard.json
plotImpacts.py -i impacts_datacard.json -o impacts_datacard


combine topEFT__1_13TeV_.root -M FitDiagnostics --saveShapes --saveWithUnc
