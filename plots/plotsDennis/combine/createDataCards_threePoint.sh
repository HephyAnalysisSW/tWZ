################################################################################
## ASIMOV
python createDataCards_threePoint.py           --year=ULRunII --light --minus --binning=A --SMZero
python createDataCards_threePoint.py           --year=ULRunII --light --minus --binning=A --SMZero --noQuad
# python createDataCards_threePoint.py           --year=ULRunII --light --minus --binning=A --SMZero --half


################################################################################
## DATA
python createDataCards_threePoint.py --unblind --year=ULRunII --light --minus --binning=A --SMZero
python createDataCards_threePoint.py --unblind --year=ULRunII --light --minus --binning=A --SMZero --noQuad
# python createDataCards_threePoint.py --unblind --year=ULRunII --light --minus --binning=A --SMZero --half

################################################################################
## DATA SM
# python createDataCards_threePoint.py --unblind --year=ULRunII --light --minus --binning=A --SMZero --SM
