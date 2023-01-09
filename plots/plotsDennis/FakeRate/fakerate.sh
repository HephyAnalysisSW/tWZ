python fakerate.py --channel=muon --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2017
python fakerate.py --channel=elec --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2017

python fakerate.py --channel=muon --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2017 --reduce
python fakerate.py --channel=elec --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2017 --reduce

python fakerate.py --channel=muon --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2018
python fakerate.py --channel=elec --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2018

python fakerate.py --channel=muon --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2018 --reduce
python fakerate.py --channel=elec --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2018 --reduce

# Prescale
# python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2018
# python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2018


# python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2018 --reduce
# python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2018 --reduce

python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2017
python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2017

python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2017 --reduce
python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2017 --reduce
