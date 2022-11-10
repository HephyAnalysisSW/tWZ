# python fakerate.py --channel=muon --selection=singlelepL-vetoAddLepL-vetoMET
# python fakerate.py --channel=elec --selection=singlelepL-vetoAddLepL-vetoMET

# python fakerate.py --channel=muon --selection=singlelepL-vetoAddLepL-vetoMET --noLargeWeights
# python fakerate.py --channel=elec --selection=singlelepL-vetoAddLepL-vetoMET --noLargeWeights

python fakerate.py --channel=muon --selection=singlelepL-vetoAddLepL-vetoMET --reduce
python fakerate.py --channel=elec --selection=singlelepL-vetoAddLepL-vetoMET --reduce

python fakerate.py --channel=muon --selection=singlelepL-vetoAddLepL-vetoMET --noLooseSel
python fakerate.py --channel=elec --selection=singlelepL-vetoAddLepL-vetoMET --noLooseSel

python fakerate.py --channel=muon --selection=singlelepL-vetoAddLepL-vetoMET --noLooseSel --reduce
python fakerate.py --channel=elec --selection=singlelepL-vetoAddLepL-vetoMET --noLooseSel --reduce

python fakerate.py --channel=muon --selection=singlelepVL-vetoAddLepVL-vetoMET --noLooseWP
python fakerate.py --channel=elec --selection=singlelepVL-vetoAddLepVL-vetoMET --noLooseWP

python fakerate.py --channel=muon --selection=singlelepVL-vetoAddLepVL-vetoMET --noLooseWP --reduce
python fakerate.py --channel=elec --selection=singlelepVL-vetoAddLepVL-vetoMET --noLooseWP --reduce

# python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepL-met40
# python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepL-met40
# 
# python fakerate.py --channel=muon --selection=singlelepT-vetoAddLepL-met40 --noPreScale
# python fakerate.py --channel=elec --selection=singlelepT-vetoAddLepL-met40 --noPreScale
