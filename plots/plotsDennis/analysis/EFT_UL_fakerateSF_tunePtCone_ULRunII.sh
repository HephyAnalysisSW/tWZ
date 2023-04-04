
################################################################################
# minDLmass12-onZ1-btag0-met60

# CR nonprompt only, apply fakerate
python EFT_UL.py  --noData --selection=trilepFOnoT-minDLmass12-onZ1-btag0-met60 --nicePlots --era=ULRunII --nonpromptOnly --applyFakerate --tunePtCone
python EFT_UL.py --sys=Fakerate_UP --noData --selection=trilepFOnoT-minDLmass12-onZ1-btag0-met60 --nicePlots --era=ULRunII --nonpromptOnly --applyFakerate --tunePtCone
python EFT_UL.py --sys=Fakerate_DOWN --noData --selection=trilepFOnoT-minDLmass12-onZ1-btag0-met60 --nicePlots --era=ULRunII --nonpromptOnly --applyFakerate --tunePtCone


################################################################################
# minDLmass12-onZ1-njet3p-btag1p

# CR nonprompt only, apply fakerate
python EFT_UL.py  --noData --selection=trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p --nicePlots --era=ULRunII --nonpromptOnly --applyFakerate --tunePtCone
python EFT_UL.py --sys=Fakerate_UP --noData --selection=trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p --nicePlots --era=ULRunII --nonpromptOnly --applyFakerate --tunePtCone
python EFT_UL.py --sys=Fakerate_DOWN --noData --selection=trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p --nicePlots --era=ULRunII --nonpromptOnly --applyFakerate --tunePtCone
