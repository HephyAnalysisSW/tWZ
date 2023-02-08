# SR
python EFT_UL.py  --selection=trilepT-minDLmass12-offZ1 --nicePlots --era=UL2017
python EFT_UL.py  --selection=trilepT-minDLmass12-offZ1 --nicePlots --era=UL2018

python EFT_UL.py  --selection=trilepT-minDLmass12-offZ1-njet3p-btag1p --nicePlots --era=UL2017
python EFT_UL.py  --selection=trilepT-minDLmass12-offZ1-njet3p-btag1p --nicePlots --era=UL2018

python EFT_UL.py  --selection=trilepT-minDLmass12-offZ1-btag0-met60 --nicePlots --era=UL2017
python EFT_UL.py  --selection=trilepT-minDLmass12-offZ1-btag0-met60 --nicePlots --era=UL2018


# CR with data fake rates applied
python EFT_UL.py  --selection=trilepFOnoT-minDLmass12-offZ1 --nicePlots --era=UL2017 --applyFakerate --useDataSF
python EFT_UL.py  --sys=Fakerate_UP --selection=trilepFOnoT-minDLmass12-offZ1 --nicePlots --era=UL2017 --applyFakerate --useDataSF
python EFT_UL.py  --sys=Fakerate_DOWN --selection=trilepFOnoT-minDLmass12-offZ1 --nicePlots --era=UL2017 --applyFakerate --useDataSF

python EFT_UL.py  --selection=trilepFOnoT-minDLmass12-offZ1 --nicePlots --era=UL2018 --applyFakerate --useDataSF
python EFT_UL.py  --sys=Fakerate_UP   --selection=trilepFOnoT-minDLmass12-offZ1 --nicePlots --era=UL2018 --applyFakerate --useDataSF
python EFT_UL.py  --sys=Fakerate_DOWN --selection=trilepFOnoT-minDLmass12-offZ1 --nicePlots --era=UL2018 --applyFakerate --useDataSF

python EFT_UL.py  --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --nicePlots --era=UL2017 --applyFakerate --useDataSF
python EFT_UL.py  --sys=Fakerate_UP   --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --nicePlots --era=UL2017 --applyFakerate --useDataSF
python EFT_UL.py  --sys=Fakerate_DOWN --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --nicePlots --era=UL2017 --applyFakerate --useDataSF

python EFT_UL.py  --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --nicePlots --era=UL2018 --applyFakerate --useDataSF
python EFT_UL.py  --sys=Fakerate_UP   --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --nicePlots --era=UL2018 --applyFakerate --useDataSF
python EFT_UL.py  --sys=Fakerate_DOWN --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --nicePlots --era=UL2018 --applyFakerate --useDataSF

python EFT_UL.py  --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --nicePlots --era=UL2017 --applyFakerate --useDataSF
python EFT_UL.py  --sys=Fakerate_UP   --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --nicePlots --era=UL2017 --applyFakerate --useDataSF
python EFT_UL.py  --sys=Fakerate_DOWN --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --nicePlots --era=UL2017 --applyFakerate --useDataSF

python EFT_UL.py  --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --nicePlots --era=UL2018 --applyFakerate --useDataSF
python EFT_UL.py  --sys=Fakerate_UP   --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --nicePlots --era=UL2018 --applyFakerate --useDataSF
python EFT_UL.py  --sys=Fakerate_DOWN --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --nicePlots --era=UL2018 --applyFakerate --useDataSF

# CR, no fake rates applied
python EFT_UL.py  --selection=trilepFOnoT-minDLmass12-offZ1 --nicePlots --era=UL2017 
python EFT_UL.py  --selection=trilepFOnoT-minDLmass12-offZ1 --nicePlots --era=UL2018 

python EFT_UL.py  --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --nicePlots --era=UL2017 
python EFT_UL.py  --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --nicePlots --era=UL2018 

python EFT_UL.py  --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --nicePlots --era=UL2017 
python EFT_UL.py  --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --nicePlots --era=UL2018 
