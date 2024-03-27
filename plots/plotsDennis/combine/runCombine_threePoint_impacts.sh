# --impacts
# --postFit

################################################################################
## Combined light generations

python runCombine_threePoint.py --year=ULRunII --light --postFit --region=1 --oneD=cHq1Re1122
python runCombine_threePoint.py --year=ULRunII --light --postFit --region=2 --oneD=cHq1Re1122 --minimizerStrategy
python runCombine_threePoint.py --year=ULRunII --light --postFit --region=3 --oneD=cHq1Re1122

python runCombine_threePoint.py --year=ULRunII --light --postFit --region=1 --oneD=cHq1Re33 
python runCombine_threePoint.py --year=ULRunII --light --postFit --region=2 --oneD=cHq1Re33 --minimizerStrategy
python runCombine_threePoint.py --year=ULRunII --light --postFit --region=3 --oneD=cHq1Re33 

# python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq1Re1122
# python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq1Re33
# python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq3Re1122
# python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq3Re33
#
# python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq1Re1122 --signalInjectionLight
# python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq1Re33 --signalInjectionLight
#
# python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq1Re1122 --signalInjectionHeavy
# python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq1Re33 --signalInjectionHeavy
#
# python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq1Re1122 --signalInjectionMixed
# python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq1Re33 --signalInjectionMixed

# python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq1Re1122 --signalInjectionWZjets
# python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq1Re33 --signalInjectionWZjets
# python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq3Re1122 --signalInjectionWZjets
# python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --oneD=cHq3Re33 --signalInjectionWZjets

# python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --twoD=cHq1Re1122-cHq1Re33
# python runCombine_threePoint.py --year=ULRunII --light --impacts --region=combined --twoD=cHq3Re1122-cHq3Re33

# python runCombine_threePoint.py --year=ULRunII --light --postFit --region=2 --oneD=cHq1Re1122 --minimizerStrategy
# python runCombine_threePoint.py --year=ULRunII --light --postFit --region=2 --oneD=cHq1Re33   --minimizerStrategy
# python runCombine_threePoint.py --year=ULRunII --light --postFit --region=2 --oneD=cHq3Re1122 --minimizerStrategy
# python runCombine_threePoint.py --year=ULRunII --light --postFit --region=2 --oneD=cHq3Re33   --minimizerStrategy
#
# python runCombine_threePoint.py --year=ULRunII --light --postFit --region=2 --oneD=cHq1Re1122 --ignoreCovWarning
# python runCombine_threePoint.py --year=ULRunII --light --postFit --region=2 --oneD=cHq1Re33   --ignoreCovWarning
# python runCombine_threePoint.py --year=ULRunII --light --postFit --region=2 --oneD=cHq3Re1122 --ignoreCovWarning
# python runCombine_threePoint.py --year=ULRunII --light --postFit --region=2 --oneD=cHq3Re33   --ignoreCovWarning

# python runCombine_threePoint.py --impacts --year=ULRunII --light --oneD=cHq1Re1122 --NjetSplit
# python runCombine_threePoint.py --impacts --year=ULRunII --light --oneD=cHq1Re33   --NjetSplit
# python runCombine_threePoint.py --impacts --year=ULRunII --light --oneD=cHq3Re1122 --NjetSplit
# python runCombine_threePoint.py --impacts --year=ULRunII --light --oneD=cHq3Re33   --NjetSplit

# python runCombine_threePoint.py --postFit --year=ULRunII --light --oneD=cHq1Re1122
# python runCombine_threePoint.py --postFit --year=ULRunII --light --oneD=cHq1Re33
# python runCombine_threePoint.py --postFit --year=ULRunII --light --oneD=cHq3Re1122
# python runCombine_threePoint.py --postFit --year=ULRunII --light --oneD=cHq3Re33
# python runCombine_threePoint.py --postFit --year=ULRunII --light --twoD=cHq1Re1122-cHq1Re33
# python runCombine_threePoint.py --postFit --year=ULRunII --light --twoD=cHq3Re1122-cHq3Re33


# python runCombine_threePoint.py --impacts --year=ULRunII --light --oneD=cHq1Re1122
# python runCombine_threePoint.py --impacts --year=ULRunII --light --oneD=cHq1Re33
# python runCombine_threePoint.py --impacts --year=ULRunII --light --oneD=cHq3Re1122
# python runCombine_threePoint.py --impacts --year=ULRunII --light --oneD=cHq3Re33
# python runCombine_threePoint.py --impacts --year=ULRunII --light --twoD=cHq1Re1122-cHq1Re33
# python runCombine_threePoint.py --impacts --year=ULRunII --light --twoD=cHq3Re1122-cHq3Re33

# python runCombine_threePoint.py --impacts --year=ULRunII --light --oneD=cHq1Re1122 --scaleCorrelation
# python runCombine_threePoint.py --impacts --year=ULRunII --light --oneD=cHq1Re33   --scaleCorrelation
# python runCombine_threePoint.py --impacts --year=ULRunII --light --oneD=cHq3Re1122 --scaleCorrelation
# python runCombine_threePoint.py --impacts --year=ULRunII --light --oneD=cHq3Re33   --scaleCorrelation

#
# python runCombine_threePoint.py --impacts --year=UL2018 --light --oneD=cHq1Re1122
# python runCombine_threePoint.py --impacts --year=UL2018 --light --oneD=cHq1Re33
# python runCombine_threePoint.py --impacts --year=UL2018 --light --oneD=cHq3Re1122
# python runCombine_threePoint.py --impacts --year=UL2018 --light --oneD=cHq3Re33
# python runCombine_threePoint.py --impacts --year=UL2018 --twoD=cHq1Re1122-cHq1Re33 --light
# python runCombine_threePoint.py --impacts --year=UL2018 --twoD=cHq3Re1122-cHq3Re33 --light
#
# python runCombine_threePoint.py --impacts --year=UL2017 --light --oneD=cHq1Re1122
# python runCombine_threePoint.py --impacts --year=UL2017 --light --oneD=cHq1Re33
# python runCombine_threePoint.py --impacts --year=UL2017 --light --oneD=cHq3Re1122
# python runCombine_threePoint.py --impacts --year=UL2017 --light --oneD=cHq3Re33
# python runCombine_threePoint.py --impacts --year=UL2017 --twoD=cHq1Re1122-cHq1Re33 --light
# python runCombine_threePoint.py --impacts --year=UL2017 --twoD=cHq3Re1122-cHq3Re33 --light
#
# python runCombine_threePoint.py --impacts --year=UL2016 --light --oneD=cHq1Re1122
# python runCombine_threePoint.py --impacts --year=UL2016 --light --oneD=cHq1Re33
# python runCombine_threePoint.py --impacts --year=UL2016 --light --oneD=cHq3Re1122
# python runCombine_threePoint.py --impacts --year=UL2016 --light --oneD=cHq3Re33
# python runCombine_threePoint.py --impacts --year=UL2016 --twoD=cHq1Re1122-cHq1Re33 --light
# python runCombine_threePoint.py --impacts --year=UL2016 --twoD=cHq3Re1122-cHq3Re33 --light
#
# python runCombine_threePoint.py --impacts --year=UL2016preVFP --light --oneD=cHq1Re1122
# python runCombine_threePoint.py --impacts --year=UL2016preVFP --light --oneD=cHq1Re33
# python runCombine_threePoint.py --impacts --year=UL2016preVFP --light --oneD=cHq3Re1122
# python runCombine_threePoint.py --impacts --year=UL2016preVFP --light --oneD=cHq3Re33
# python runCombine_threePoint.py --impacts --year=UL2016preVFP --twoD=cHq1Re1122-cHq1Re33 --light
# python runCombine_threePoint.py --impacts --year=UL2016preVFP --twoD=cHq3Re1122-cHq3Re33 --light


################################################################################
# All three generations
# python runCombine_threePoint.py --impacts --year=ULRunII --oneD=cHq1Re11
# python runCombine_threePoint.py --impacts --year=ULRunII --oneD=cHq1Re22
# python runCombine_threePoint.py --impacts --year=ULRunII --oneD=cHq1Re33
# python runCombine_threePoint.py --impacts --year=ULRunII --oneD=cHq3Re11
# python runCombine_threePoint.py --impacts --year=ULRunII --oneD=cHq3Re22
# python runCombine_threePoint.py --impacts --year=ULRunII --oneD=cHq3Re33
#
# python runCombine_threePoint.py --postFit --year=ULRunII --oneD=cHq1Re11
# python runCombine_threePoint.py --postFit --year=ULRunII --oneD=cHq1Re22
# python runCombine_threePoint.py --postFit --year=ULRunII --oneD=cHq1Re33
# python runCombine_threePoint.py --postFit --year=ULRunII --oneD=cHq3Re11
# python runCombine_threePoint.py --postFit --year=ULRunII --oneD=cHq3Re22
# python runCombine_threePoint.py --postFit --year=ULRunII --oneD=cHq3Re33

# python runCombine_threePoint.py --impacts --year=UL2018 --oneD=cHq1Re11
# python runCombine_threePoint.py --impacts --year=UL2018 --oneD=cHq1Re22
# python runCombine_threePoint.py --impacts --year=UL2018 --oneD=cHq1Re33
# python runCombine_threePoint.py --impacts --year=UL2018 --oneD=cHq3Re11
# python runCombine_threePoint.py --impacts --year=UL2018 --oneD=cHq3Re22
# python runCombine_threePoint.py --impacts --year=UL2018 --oneD=cHq3Re33
#
# python runCombine_threePoint.py --impacts --year=UL2017 --oneD=cHq1Re11
# python runCombine_threePoint.py --impacts --year=UL2017 --oneD=cHq1Re22
# python runCombine_threePoint.py --impacts --year=UL2017 --oneD=cHq1Re33
# python runCombine_threePoint.py --impacts --year=UL2017 --oneD=cHq3Re11
# python runCombine_threePoint.py --impacts --year=UL2017 --oneD=cHq3Re22
# python runCombine_threePoint.py --impacts --year=UL2017 --oneD=cHq3Re33
#
# python runCombine_threePoint.py --impacts --year=UL2016 --oneD=cHq1Re11
# python runCombine_threePoint.py --impacts --year=UL2016 --oneD=cHq1Re22
# python runCombine_threePoint.py --impacts --year=UL2016 --oneD=cHq1Re33
# python runCombine_threePoint.py --impacts --year=UL2016 --oneD=cHq3Re11
# python runCombine_threePoint.py --impacts --year=UL2016 --oneD=cHq3Re22
# python runCombine_threePoint.py --impacts --year=UL2016 --oneD=cHq3Re33
#
# python runCombine_threePoint.py --impacts --year=UL2016preVFP --oneD=cHq1Re11
# python runCombine_threePoint.py --impacts --year=UL2016preVFP --oneD=cHq1Re22
# python runCombine_threePoint.py --impacts --year=UL2016preVFP --oneD=cHq1Re33
# python runCombine_threePoint.py --impacts --year=UL2016preVFP --oneD=cHq3Re11
# python runCombine_threePoint.py --impacts --year=UL2016preVFP --oneD=cHq3Re22
# python runCombine_threePoint.py --impacts --year=UL2016preVFP --oneD=cHq3Re33
