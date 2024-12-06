################################################################################
## DATA
python plotLimit2D.py --unblind --year=ULRunII --light --minus --binning=A --SMZero --wc=cHqMRe1122-cHqMRe33
python plotLimit2D.py --unblind --year=ULRunII --light --minus --binning=A --SMZero --wc=cHq3MRe1122-cHq3MRe33
python plotLimit2D.py --unblind --year=ULRunII --light --minus --binning=A --SMZero --wc=cW-cWtil

python plotLimit2D.py --unblind --year=ULRunII --light --minus --binning=A --SMZero --wc=cHqMRe1122-cHqMRe33 --float
python plotLimit2D.py --unblind --year=ULRunII --light --minus --binning=A --SMZero --wc=cHq3MRe1122-cHq3MRe33 --float
python plotLimit2D.py --unblind --year=ULRunII --light --minus --binning=A --SMZero --wc=cW-cWtil --float

################################################################################
## ASIMOV
python plotLimit2D.py           --year=ULRunII --light --minus --binning=A --SMZero --wc=cHqMRe1122-cHqMRe33
python plotLimit2D.py           --year=ULRunII --light --minus --binning=A --SMZero --wc=cHq3MRe1122-cHq3MRe33
python plotLimit2D.py           --year=ULRunII --light --minus --binning=A --SMZero --wc=cW-cWtil

python plotLimit2D.py           --year=ULRunII --light --minus --binning=A --SMZero --wc=cHqMRe1122-cHqMRe33 --float
python plotLimit2D.py           --year=ULRunII --light --minus --binning=A --SMZero --wc=cHq3MRe1122-cHq3MRe33 --float
python plotLimit2D.py           --year=ULRunII --light --minus --binning=A --SMZero --wc=cW-cWtil --float
