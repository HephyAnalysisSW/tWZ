# --impacts
# --postFit


################################################################################
## DATA POSTFIT
# python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --binning=A --SMZero --region=combined --postFit --noScan --twoD=cHqMRe1122-cHqMRe33
# python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --binning=A --SMZero --region=combined --postFit --noScan --twoD=cHq3MRe1122-cHq3MRe33
#
# python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --binning=A --SMZero --region=combined --postFit --noScan --twoD=cHqMRe1122-cHqMRe33 --float
# python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --binning=A --SMZero --region=combined --postFit --noScan --twoD=cHq3MRe1122-cHq3MRe33 --float
#
# python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --binning=A --SMZero --region=combined --postFit --noScan --SM

python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --binning=A --SMZero --region=combined --postFit --noScan --fullFit

################################################################################
## DATA IMPACTS
# python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --binning=A --SMZero --region=combined --impacts --noScan --twoD=cHqMRe1122-cHqMRe33
# python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --binning=A --SMZero --region=combined --impacts --noScan --twoD=cHq3MRe1122-cHq3MRe33
#
# python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --binning=A --SMZero --region=combined --impacts --noScan --twoD=cHqMRe1122-cHqMRe33 --float
# python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --binning=A --SMZero --region=combined --impacts --noScan --twoD=cHq3MRe1122-cHq3MRe33 --float
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --binning=A --SMZero --region=combined --impacts --noScan --fullFit
# python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --binning=A --SMZero --region=combined --impacts --noScan --oneD=cHqMRe1122
# python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --binning=A --SMZero --region=combined --impacts --noScan --oneD=cHqMRe33


################################################################################
## IMPACTS ASIMOV
# python runCombine_threePoint.py --year=ULRunII --light --minus --binning=A --SMZero --region=combined --impacts --noScan --twoD=cHqMRe1122-cHqMRe33
# python runCombine_threePoint.py --year=ULRunII --light --minus --binning=A --SMZero --region=combined --impacts --noScan --twoD=cHq3MRe1122-cHq3MRe33
#
# python runCombine_threePoint.py --year=ULRunII --light --minus --binning=A --SMZero --region=combined --impacts --noScan --twoD=cHqMRe1122-cHqMRe33 --float
# python runCombine_threePoint.py --year=ULRunII --light --minus --binning=A --SMZero --region=combined --impacts --noScan --twoD=cHq3MRe1122-cHq3MRe33 --float
python runCombine_threePoint.py --year=ULRunII --light --minus --binning=A --SMZero --region=combined --impacts --noScan --fullFit
