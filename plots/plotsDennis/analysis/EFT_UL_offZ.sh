# SR
python EFT_UL.py  --selection=trilepT-minDLmass12-offZ1 --nicePlots --era=UL2018

# CR with data fake rates applied
python EFT_UL.py  --selection=trilepL-trilepTCR-minDLmass12-offZ1 --nicePlots --era=UL2018 --applyFakerate --useDataSF

# CR, no fake rates applied
python EFT_UL.py  --selection=trilepL-trilepTCR-minDLmass12-offZ1 --nicePlots --era=UL2018 
