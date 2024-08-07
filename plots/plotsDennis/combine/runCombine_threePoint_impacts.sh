# --impacts
# --postFit

################################################################################
## Combined light generations

# python runCombine_threePoint.py --year=ULRunII --light --postFit --region=1 --oneD=cHq1Re1122
# python runCombine_threePoint.py --year=ULRunII --light --postFit --region=2 --oneD=cHq1Re1122 --minimizerStrategy
# python runCombine_threePoint.py --year=ULRunII --light --postFit --region=3 --oneD=cHq1Re1122
#
# python runCombine_threePoint.py --year=ULRunII --light --postFit --region=1 --oneD=cHq1Re33
# python runCombine_threePoint.py --year=ULRunII --light --postFit --region=2 --oneD=cHq1Re33 --minimizerStrategy
# python runCombine_threePoint.py --year=ULRunII --light --postFit --region=3 --oneD=cHq1Re33
#
# python runCombine_threePoint.py --year=ULRunII --light --minus --postFit --region=1 --oneD=cHqMRe1122
# python runCombine_threePoint.py --year=ULRunII --light --minus --postFit --region=2 --oneD=cHqMRe1122 --minimizerStrategy
# python runCombine_threePoint.py --year=ULRunII --light --minus --postFit --region=3 --oneD=cHqMRe1122
#

################################################################################
## POSTFIT
python runCombine_threePoint.py --year=ULRunII --unblind --light --postFit --region=combined --oneD=cHq1Re1122
python runCombine_threePoint.py --year=ULRunII --unblind --light --postFit --region=combined --oneD=cHq1Re33
python runCombine_threePoint.py --year=ULRunII --unblind --light --postFit --region=combined --oneD=cHq3Re1122
python runCombine_threePoint.py --year=ULRunII --unblind --light --postFit --region=combined --oneD=cHq3Re33

python runCombine_threePoint.py --year=ULRunII --unblind --light --postFit --region=combined --oneD=cHq1Re1122 --noBB
python runCombine_threePoint.py --year=ULRunII --unblind --light --postFit --region=combined --oneD=cHq1Re33   --noBB
python runCombine_threePoint.py --year=ULRunII --unblind --light --postFit --region=combined --oneD=cHq3Re1122 --noBB
python runCombine_threePoint.py --year=ULRunII --unblind --light --postFit --region=combined --oneD=cHq3Re33   --noBB

python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --postFit --region=combined --oneD=cHqMRe1122
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --postFit --region=combined --oneD=cHqMRe33
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --postFit --region=combined --oneD=cHq3MRe1122
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --postFit --region=combined --oneD=cHq3MRe33

python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --postFit --region=combined --oneD=cHqMRe1122  --noBB
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --postFit --region=combined --oneD=cHqMRe33    --noBB
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --postFit --region=combined --oneD=cHq3MRe1122 --noBB
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --postFit --region=combined --oneD=cHq3MRe33   --noBB

################################################################################
## IMPACTS
python runCombine_threePoint.py --year=ULRunII --unblind --light --impacts --region=combined --oneD=cHq1Re1122
python runCombine_threePoint.py --year=ULRunII --unblind --light --impacts --region=combined --oneD=cHq1Re33
python runCombine_threePoint.py --year=ULRunII --unblind --light --impacts --region=combined --oneD=cHq3Re1122
python runCombine_threePoint.py --year=ULRunII --unblind --light --impacts --region=combined --oneD=cHq3Re33

python runCombine_threePoint.py --year=ULRunII --unblind --light --impacts --region=combined --oneD=cHq1Re1122 --noBB
python runCombine_threePoint.py --year=ULRunII --unblind --light --impacts --region=combined --oneD=cHq1Re33   --noBB
python runCombine_threePoint.py --year=ULRunII --unblind --light --impacts --region=combined --oneD=cHq3Re1122 --noBB
python runCombine_threePoint.py --year=ULRunII --unblind --light --impacts --region=combined --oneD=cHq3Re33   --noBB

python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --impacts --region=combined --oneD=cHqMRe1122
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --impacts --region=combined --oneD=cHqMRe33
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --impacts --region=combined --oneD=cHq3MRe1122
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --impacts --region=combined --oneD=cHq3MRe33

python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --impacts --region=combined --oneD=cHqMRe1122  --noBB
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --impacts --region=combined --oneD=cHqMRe33    --noBB
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --impacts --region=combined --oneD=cHq3MRe1122 --noBB
python runCombine_threePoint.py --year=ULRunII --unblind --light --minus --impacts --region=combined --oneD=cHq3MRe33   --noBB

################################################################################
## IMPACTS ASIMOV
python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq1Re1122
python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq1Re33
python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq3Re1122
python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq3Re33

python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq1Re1122 --noBB
python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq1Re33   --noBB
python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq3Re1122 --noBB
python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq3Re33   --noBB

python runCombine_threePoint.py --year=ULRunII --light --minus --impacts --region=combined --oneD=cHqMRe1122
python runCombine_threePoint.py --year=ULRunII --light --minus --impacts --region=combined --oneD=cHqMRe33
python runCombine_threePoint.py --year=ULRunII --light --minus --impacts --region=combined --oneD=cHq3MRe1122
python runCombine_threePoint.py --year=ULRunII --light --minus --impacts --region=combined --oneD=cHq3MRe33

python runCombine_threePoint.py --year=ULRunII --light --minus --impacts --region=combined --oneD=cHqMRe1122  --noBB
python runCombine_threePoint.py --year=ULRunII --light --minus --impacts --region=combined --oneD=cHqMRe33    --noBB
python runCombine_threePoint.py --year=ULRunII --light --minus --impacts --region=combined --oneD=cHq3MRe1122 --noBB
python runCombine_threePoint.py --year=ULRunII --light --minus --impacts --region=combined --oneD=cHq3MRe33   --noBB
