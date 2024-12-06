################################################################################
## POSTFIT
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --postFit --region=1 --EFTpoint
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --postFit --region=2 --EFTpoint
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --postFit --region=3 --EFTpoint
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --postFit --region=combined --EFTpoint

################################################################################
## IMPACTS
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --impacts --region=1 --EFTpoint
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --impacts --region=2 --EFTpoint
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --impacts --region=3 --EFTpoint
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --impacts --region=combined --EFTpoint

# ################################################################################
# ## GOF
# python runCombine_threePoint_GoF.py --year=ULRunII --unblind --light --minus --impacts --region=1 --EFTpoint
# python runCombine_threePoint_GoF.py --year=ULRunII --unblind --light --minus --impacts --region=2 --EFTpoint
# python runCombine_threePoint_GoF.py --year=ULRunII --unblind --light --minus --impacts --region=3 --EFTpoint
# python runCombine_threePoint_GoF.py --year=ULRunII --unblind --light --minus --impacts --region=combined --EFTpoint
