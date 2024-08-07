################################################################################
## DATA
python plotLimit2D.py --year=ULRunII --unblind --wc=cHq1Re1122-cHq1Re33 --light
python plotLimit2D.py --year=ULRunII --unblind --wc=cHq3Re1122-cHq3Re33 --light

python plotLimit2D.py --year=ULRunII --unblind --wc=cHqMRe1122-cHqMRe33 --light --minus
python plotLimit2D.py --year=ULRunII --unblind --wc=cHq3MRe1122-cHq3MRe33 --light --minus

python plotLimit2D.py --year=ULRunII --unblind --wc=cHq1Re1122-cHq1Re33 --light --noBB
python plotLimit2D.py --year=ULRunII --unblind --wc=cHq3Re1122-cHq3Re33 --light --noBB

python plotLimit2D.py --year=ULRunII --unblind --wc=cHqMRe1122-cHqMRe33 --light --minus --noBB
python plotLimit2D.py --year=ULRunII --unblind --wc=cHq3MRe1122-cHq3MRe33 --light --minus --noBB

################################################################################
## ASIMOV
python plotLimit2D.py --year=ULRunII --wc=cHq1Re1122-cHq1Re33 --light
python plotLimit2D.py --year=ULRunII --wc=cHq3Re1122-cHq3Re33 --light

python plotLimit2D.py --year=ULRunII --wc=cHqMRe1122-cHqMRe33 --light --minus
python plotLimit2D.py --year=ULRunII --wc=cHq3MRe1122-cHq3MRe33 --light --minus

python plotLimit2D.py --year=ULRunII --wc=cHq1Re1122-cHq1Re33 --light --noBB
python plotLimit2D.py --year=ULRunII --wc=cHq3Re1122-cHq3Re33 --light --noBB

python plotLimit2D.py --year=ULRunII --wc=cHqMRe1122-cHqMRe33 --light --minus --noBB
python plotLimit2D.py --year=ULRunII --wc=cHq3MRe1122-cHq3MRe33 --light --minus --noBB

# python plotLimit2D.py --year=ULRunII --wc=cHq1Re1122-cHq1Re33 --light --signalInjectionLight --onlyCombined
# python plotLimit2D.py --year=ULRunII --wc=cHq1Re1122-cHq1Re33 --light --signalInjectionHeavy --onlyCombined
# python plotLimit2D.py --year=ULRunII --wc=cHq1Re1122-cHq1Re33 --light --signalInjectionMixed --onlyCombined
# python plotLimit2D.py --year=ULRunII --wc=cHq1Re1122-cHq1Re33 --light --signalInjectionWZjets --onlyCombined
#
# python plotLimit2D.py --year=ULRunII --wc=cHq1Re1122-cHq1Re33 --light --signalInjectionLight --onlyCombined --fluctuatePseudoData
# python plotLimit2D.py --year=ULRunII --wc=cHq1Re1122-cHq1Re33 --light --signalInjectionHeavy --onlyCombined --fluctuatePseudoData
# python plotLimit2D.py --year=ULRunII --wc=cHq1Re1122-cHq1Re33 --light --signalInjectionMixed --onlyCombined --fluctuatePseudoData
# python plotLimit2D.py --year=ULRunII --wc=cHq1Re1122-cHq1Re33 --light --signalInjectionWZjets --onlyCombined --fluctuatePseudoData


# python plotLimit2D.py --year=UL2018 --wc=cHq1Re1122-cHq1Re33 --light
# python plotLimit2D.py --year=UL2018 --wc=cHq3Re1122-cHq3Re33 --light
#
# python plotLimit2D.py --year=UL2017 --wc=cHq1Re1122-cHq1Re33 --light
# python plotLimit2D.py --year=UL2017 --wc=cHq3Re1122-cHq3Re33 --light
#
# python plotLimit2D.py --year=UL2016 --wc=cHq1Re1122-cHq1Re33 --light
# python plotLimit2D.py --year=UL2016 --wc=cHq3Re1122-cHq3Re33 --light
#
# python plotLimit2D.py --year=UL2016preVFP --wc=cHq1Re1122-cHq1Re33 --light
# python plotLimit2D.py --year=UL2016preVFP --wc=cHq3Re1122-cHq3Re33 --light
