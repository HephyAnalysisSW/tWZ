### NORMAL FAKERATE RUN ########################################################

# python fakerate.py --channel=muon --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2016preVFP
# python fakerate.py --channel=elec --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2016preVFP
# python fakerate.py --channel=muon --selection=singlelepFOconept-vetoAddLepFOconept-vetoMET --era=UL2016preVFP
# python fakerate.py --channel=elec --selection=singlelepFOconept-vetoAddLepFOconept-vetoMET --era=UL2016preVFP
# 
# python fakerate.py --channel=muon --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2016
# python fakerate.py --channel=elec --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2016
# python fakerate.py --channel=muon --selection=singlelepFOconept-vetoAddLepFOconept-vetoMET --era=UL2016
# python fakerate.py --channel=elec --selection=singlelepFOconept-vetoAddLepFOconept-vetoMET --era=UL2016
# 
# python fakerate.py --channel=muon --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2017
# python fakerate.py --channel=elec --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2017
# python fakerate.py --channel=muon --selection=singlelepFOconept-vetoAddLepFOconept-vetoMET --era=UL2017
# python fakerate.py --channel=elec --selection=singlelepFOconept-vetoAddLepFOconept-vetoMET --era=UL2017
# 
# python fakerate.py --channel=muon --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2018
# python fakerate.py --channel=elec --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2018
# python fakerate.py --channel=muon --selection=singlelepFOconept-vetoAddLepFOconept-vetoMET --era=UL2018
# python fakerate.py --channel=elec --selection=singlelepFOconept-vetoAddLepFOconept-vetoMET --era=UL2018

### FAKERATE RUN WITH BRIL PRESCALES ###########################################

# python fakerate.py --prescalemode=bril --channel=muon --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2016preVFP
# python fakerate.py --prescalemode=bril --channel=elec --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2016preVFP
# python fakerate.py --prescalemode=bril --channel=muon --selection=singlelepFOconept-vetoAddLepFOconept-vetoMET --era=UL2016preVFP
# python fakerate.py --prescalemode=bril --channel=elec --selection=singlelepFOconept-vetoAddLepFOconept-vetoMET --era=UL2016preVFP
# 
# python fakerate.py --prescalemode=bril --channel=muon --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2016
# python fakerate.py --prescalemode=bril --channel=elec --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2016
# python fakerate.py --prescalemode=bril --channel=muon --selection=singlelepFOconept-vetoAddLepFOconept-vetoMET --era=UL2016
# python fakerate.py --prescalemode=bril --channel=elec --selection=singlelepFOconept-vetoAddLepFOconept-vetoMET --era=UL2016

# python fakerate.py --prescalemode=bril --channel=muon --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2017
# python fakerate.py --prescalemode=bril --channel=elec --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2017
# python fakerate.py --prescalemode=bril --channel=muon --selection=singlelepFOconept-vetoAddLepFOconept-vetoMET --era=UL2017
# python fakerate.py --prescalemode=bril --channel=elec --selection=singlelepFOconept-vetoAddLepFOconept-vetoMET --era=UL2017

# python fakerate.py --prescalemode=bril --channel=muon --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2018
# python fakerate.py --prescalemode=bril --channel=elec --selection=singlelepFO-vetoAddLepFO-vetoMET --era=UL2018
# python fakerate.py --prescalemode=bril --channel=muon --selection=singlelepFOconept-vetoAddLepFOconept-vetoMET --era=UL2018
# python fakerate.py --prescalemode=bril --channel=elec --selection=singlelepFOconept-vetoAddLepFOconept-vetoMET --era=UL2018

### FAKERATE RUN TO MEASURE PRESCALES (REDUCE TT) ##############################

python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2016preVFP --reduce
python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2016preVFP --reduce
python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepFOconept-met40 --noPreScale --era=UL2016preVFP --reduce
python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepFOconept-met40 --noPreScale --era=UL2016preVFP --reduce

python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2016 --reduce
python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2016 --reduce
python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepFOconept-met40 --noPreScale --era=UL2016 --reduce
python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepFOconept-met40 --noPreScale --era=UL2016 --reduce

python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2017 --reduce
python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2017 --reduce
python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepFOconept-met40 --noPreScale --era=UL2017 --reduce
python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepFOconept-met40 --noPreScale --era=UL2017 --reduce

python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2018 --reduce
python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2018 --reduce
python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepFOconept-met40 --noPreScale --era=UL2018 --reduce
python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepFOconept-met40 --noPreScale --era=UL2018 --reduce

### FAKERATE RUN TO MEASURE PRESCALES ##########################################

# python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2016preVFP
# python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2016preVFP

# python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2016
# python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2016

# python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2017
# python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2017

# python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2018
# python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepFO-met40 --noPreScale --era=UL2018
