################################################################################
# SR
python EFT_UL.py --tunePtCone --selection=trilepT-minDLmass12-offZ1 --nicePlots --era=ULRunII

################################################################################
# SR ttz 

python EFT_UL.py --tunePtCone --selection=trilepT-minDLmass12-offZ1-njet3p-btag1p --nicePlots --era=ULRunII

################################################################################
# SR WZ

python EFT_UL.py --tunePtCone --selection=trilepT-minDLmass12-offZ1-btag0-met60 --nicePlots --era=ULRunII


################################################################################
# CR with data fake rates applied
python EFT_UL.py --tunePtCone --selection=trilepFOnoT-minDLmass12-offZ1 --nicePlots --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py --tunePtCone --sys=Fakerate_UP   --selection=trilepFOnoT-minDLmass12-offZ1 --nicePlots --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py --tunePtCone --sys=Fakerate_DOWN --selection=trilepFOnoT-minDLmass12-offZ1 --nicePlots --era=ULRunII --applyFakerate --useDataSF

################################################################################
# CR ttZ with data fake rates applied
python EFT_UL.py --tunePtCone --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --nicePlots --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py --tunePtCone --sys=Fakerate_UP   --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --nicePlots --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py --tunePtCone --sys=Fakerate_DOWN --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --nicePlots --era=ULRunII --applyFakerate --useDataSF

################################################################################
# CR WZ with data fake rates applied
python EFT_UL.py --tunePtCone --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --nicePlots --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py --tunePtCone --sys=Fakerate_UP   --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --nicePlots --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py --tunePtCone --sys=Fakerate_DOWN --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --nicePlots --era=ULRunII --applyFakerate --useDataSF

################################################################################
# CR, no fake rates applied
python EFT_UL.py --tunePtCone --selection=trilepFOnoT-minDLmass12-offZ1 --nicePlots --era=ULRunII 

################################################################################
# CR ttZ, no fake rates applied
python EFT_UL.py --tunePtCone --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --nicePlots --era=ULRunII 

################################################################################
# CR WZ, no fake rates applied
python EFT_UL.py --tunePtCone --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --nicePlots --era=ULRunII 
