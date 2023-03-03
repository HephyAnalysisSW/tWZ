#!/usr/bin/env python


'''
This command would read the lumi of the full UL2018 run:
brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt --begin 314472 --end 325175 -u /fb

Now, add a HLT path and calculate the lumi then:
brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt --begin 314472 --end 325175 -u /fb --hltpath="HLT_Mu20_v*"

The prescale is the ratio of the recorded lumi with a trigger path divided by the total lumi
'''



lumi = {
    "UL2016": 36.313753344, 
    "UL2017": 41.479680529, 
    "UL2018": 59.832045316,
}

lumi_hlt = {
    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  {"UL2016": 0.007062323, "UL2017": 0.003651209, "UL2018": 0.006423083},
    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": {"UL2016": 0.063420776, "UL2017": 0.035578856, "UL2018": 0.038929257},
    "HLT_Mu3_PFJet40":                    {"UL2016": 0.007489934, "UL2017": 0.004607783, "UL2018": 0.002704227},
    "HLT_Mu8":                            {"UL2016": 0.003977769, "UL2017": 0.002602078, "UL2018": 0.008566587},
    "HLT_Mu17":                           {"UL2016": 0.285841356, "UL2017": 0.070005239, "UL2018": 0.045851701},
    "HLT_Mu20":                           {"UL2016": 0.141374480, "UL2017": 0.575585018, "UL2018": 0.055360247},
    "HLT_Mu27":                           {"UL2016": 0.253106305, "UL2017": 0.184843129, "UL2018": 0.125966158},
}

years = ["UL2016", "UL2017", "UL2018"]
triggers = [
    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30", 
    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30", 
    "HLT_Mu3_PFJet40",
    "HLT_Mu8",
    "HLT_Mu17",
    "HLT_Mu20",
    "HLT_Mu27",
]


for year in years:
    print "---------------------------------------"
    print year
    for trigger in triggers:
        ratio = lumi_hlt[trigger][year]/lumi[year]
        prescale = 1.0/ratio
        print trigger, prescale
