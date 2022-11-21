python fakerate.py --channel=muon --selection=singlelepL-vetoAddLepL-vetoMET
python fakerate.py --channel=elec --selection=singlelepL-vetoAddLepL-vetoMET

# python fakerate.py --channel=muon --selection=singlelepL-vetoAddLepL-vetoMET --noLargeWeights
# python fakerate.py --channel=elec --selection=singlelepL-vetoAddLepL-vetoMET --noLargeWeights

# python fakerate.py --channel=muon --selection=singlelepL-vetoAddLepL-vetoMET --reduce
# python fakerate.py --channel=elec --selection=singlelepL-vetoAddLepL-vetoMET --reduce

# python fakerate.py --channel=muon --selection=singlelepL-vetoAddLepL-vetoMET --noLooseSel
# python fakerate.py --channel=elec --selection=singlelepL-vetoAddLepL-vetoMET --noLooseSel

# python fakerate.py --channel=muon --selection=singlelepL-vetoAddLepL-vetoMET --noLooseSel --reduce
# python fakerate.py --channel=elec --selection=singlelepL-vetoAddLepL-vetoMET --noLooseSel --reduce

# python fakerate.py --channel=muon --selection=singlelepVL-vetoAddLepVL-vetoMET --noLooseWP
# python fakerate.py --channel=elec --selection=singlelepVL-vetoAddLepVL-vetoMET --noLooseWP

# python fakerate.py --channel=muon --selection=singlelepVL-vetoAddLepVL-vetoMET --noLooseWP --reduce
# python fakerate.py --channel=elec --selection=singlelepVL-vetoAddLepVL-vetoMET --noLooseWP --reduce

# python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepL-met40
# python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepL-met40
# 


python fakerate.py --channel=muon --selection=singlelepL-vetoAddLepL-vetoMET --mvaTOPv1
python fakerate.py --channel=elec --selection=singlelepL-vetoAddLepL-vetoMET --mvaTOPv1

python fakerate.py --channel=muon --selection=singlelepL-vetoAddLepL-vetoMET --noLooseSel --mvaTOPv1
python fakerate.py --channel=elec --selection=singlelepL-vetoAddLepL-vetoMET --noLooseSel --mvaTOPv1

python fakerate.py --channel=muon --selection=singlelepVL-vetoAddLepVL-vetoMET --noLooseWP --mvaTOPv1
python fakerate.py --channel=elec --selection=singlelepVL-vetoAddLepVL-vetoMET --noLooseWP --mvaTOPv1

# Prescale
# python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepL-met40 --noPreScale --era=UL2018
# python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepL-met40 --noPreScale --era=UL2018
# 
# python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepL-met40 --noPreScale --era=UL2017
# python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepL-met40 --noPreScale --era=UL2017
