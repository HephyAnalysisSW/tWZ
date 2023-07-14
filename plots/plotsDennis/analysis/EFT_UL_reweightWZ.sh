################################################################################
# SR on-Z WZ
python EFT_UL.py --WZreweight --reduceEFT --noData --threePoint --selection=trilepT-minDLmass12-onZ1-btag0-met60 --era=ULRunII
python EFT_UL.py              --reduceEFT --noData --threePoint --selection=trilepT-minDLmass12-onZ1-btag0-met60 --era=ULRunII

################################################################################
# SR on-Z ttz
python EFT_UL.py --WZreweight --reduceEFT --noData --threePoint --selection=trilepT-minDLmass12-onZ1-njet3p-btag1p --era=ULRunII
python EFT_UL.py              --reduceEFT --noData --threePoint --selection=trilepT-minDLmass12-onZ1-njet3p-btag1p --era=ULRunII

################################################################################
# SR on-Z WZ
python EFT_UL.py --WZreweight --reduceEFT --threePoint --selection=trilepT-minDLmass12-offZ1-btag0-met60 --era=ULRunII
python EFT_UL.py              --reduceEFT --threePoint --selection=trilepT-minDLmass12-offZ1-btag0-met60 --era=ULRunII

################################################################################
# SR off-Z ttz
python EFT_UL.py --WZreweight --reduceEFT --threePoint --selection=trilepT-minDLmass12-offZ1-njet3p-btag1p --era=ULRunII
python EFT_UL.py              --reduceEFT --threePoint --selection=trilepT-minDLmass12-offZ1-njet3p-btag1p --era=ULRunII

################################################################################
# SR off-Z WZ
python EFT_UL.py --WZreweight  --reduceEFT --threePoint --selection=trilepT-minDLmass12-offZ1-btag0-met60 --era=ULRunII
python EFT_UL.py               --reduceEFT --threePoint --selection=trilepT-minDLmass12-offZ1-btag0-met60 --era=ULRunII

################################################################################
# CR ttZ with data fake rates applied
python EFT_UL.py --WZreweight                      --reduceEFT --threePoint --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py --WZreweight --sys=Fakerate_UP    --reduceEFT --threePoint --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py --WZreweight --sys=Fakerate_DOWN  --reduceEFT --threePoint --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --era=ULRunII --applyFakerate --useDataSF

python EFT_UL.py                                    --reduceEFT --threePoint --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py               --sys=Fakerate_UP    --reduceEFT --threePoint --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py               --sys=Fakerate_DOWN  --reduceEFT --threePoint --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --era=ULRunII --applyFakerate --useDataSF

################################################################################
# CR WZ with data fake rates applied
python EFT_UL.py --WZreweight                      --reduceEFT --threePoint --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py --WZreweight --sys=Fakerate_UP    --reduceEFT --threePoint --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py --WZreweight --sys=Fakerate_DOWN  --reduceEFT --threePoint --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --era=ULRunII --applyFakerate --useDataSF

python EFT_UL.py                                    --reduceEFT --threePoint --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py               --sys=Fakerate_UP    --reduceEFT --threePoint --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --era=ULRunII --applyFakerate --useDataSF
python EFT_UL.py               --sys=Fakerate_DOWN  --reduceEFT --threePoint --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --era=ULRunII --applyFakerate --useDataSF

################################################################################
# CR ttZ, no fake rates applied
python EFT_UL.py --WZreweight --reduceEFT --threePoint --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --era=ULRunII
python EFT_UL.py              --reduceEFT --threePoint --selection=trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p --era=ULRunII

################################################################################
# CR WZ, no fake rates applied
python EFT_UL.py --WZreweight --reduceEFT --threePoint --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --era=ULRunII
python EFT_UL.py              --reduceEFT --threePoint --selection=trilepFOnoT-minDLmass12-offZ1-btag0-met60 --era=ULRunII
