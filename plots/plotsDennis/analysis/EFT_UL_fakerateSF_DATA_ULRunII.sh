################################################################################
# CR ttZ with data fake rates applied
python EFT_UL.py  --selection=trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p --nicePlots --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py  --sys=Fakerate_UP   --selection=trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p --nicePlots --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py  --sys=Fakerate_DOWN --selection=trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p --nicePlots --era=ULRunII --applyFakerate --useDataSF

python EFT_UL.py  --selection=trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p --nicePlots --era=ULRunII --applyFakerate --useDataSF --tunePtCone
python EFT_UL.py  --sys=Fakerate_UP   --selection=trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p --nicePlots --era=ULRunII --applyFakerate --useDataSF --tunePtCone
python EFT_UL.py  --sys=Fakerate_DOWN --selection=trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p --nicePlots --era=ULRunII --applyFakerate --useDataSF --tunePtCone

################################################################################
# CR WZ with data fake rates applied
python EFT_UL.py  --selection=trilepFOnoT-minDLmass12-onZ1-btag0-met60 --nicePlots --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py  --sys=Fakerate_UP   --selection=trilepFOnoT-minDLmass12-onZ1-btag0-met60 --nicePlots --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py  --sys=Fakerate_DOWN --selection=trilepFOnoT-minDLmass12-onZ1-btag0-met60 --nicePlots --era=ULRunII --applyFakerate --useDataSF

python EFT_UL.py  --selection=trilepFOnoT-minDLmass12-onZ1-btag0-met60 --nicePlots --era=ULRunII --applyFakerate --useDataSF --tunePtCone
python EFT_UL.py  --sys=Fakerate_UP   --selection=trilepFOnoT-minDLmass12-onZ1-btag0-met60 --nicePlots --era=ULRunII --applyFakerate --useDataSF --tunePtCone
python EFT_UL.py  --sys=Fakerate_DOWN --selection=trilepFOnoT-minDLmass12-onZ1-btag0-met60 --nicePlots --era=ULRunII --applyFakerate --useDataSF --tunePtCone

################################################################################
# SR ttZ
python EFT_UL.py --selection=trilepT-minDLmass12-onZ1-njet3p-btag1p --nicePlots --era=ULRunII

################################################################################
# SR WZ
python EFT_UL.py --selection=trilepT-minDLmass12-onZ1-btag0-met60 --nicePlots --era=UL2018
