#!/bin/bash
npoints1=20 # put one less here because of bash loop logic
npoints2=20
dir=/users/dennis.schwarz/CMSSW_10_6_0/src/tWZ/plots/plotsDennis/DataCards/data_twoD_triplet/
submitdir=/users/dennis.schwarz/CMSSW_10_6_0/src/tWZ/plots/plotsDennis/DataCards/submitScripts_twoD_triplet

output=submitScript.sh

if [ -d "$submitdir" ]; then
    echo "[ERROR] $submitdir already exists, delete work dir before executing this script"
    return
else
    echo "Creating submit directory $submitdir..."
    mkdir $submitdir  
fi

WC1=cHq3Re1122
WC2=cHq3Re33

echo 'Combining combine cards...'
cd ${dir}
for i in {0..${npoints1}}
do
  # First combine regions to a final card and name region 'combined'
  for j in {0..${npoints2}}
  do
    combineCards.py topEFT_2D_${WC1}_${WC2}_1_13TeV_${i}_${j}.txt topEFT_2D_${WC1}_${WC2}_2_13TeV_${i}_${j}.txt topEFT_2D_${WC1}_${WC2}_3_13TeV_${i}_${j}.txt topEFT_2D_${WC1}_${WC2}_4_13TeV_${i}_${j}.txt > topEFT_2D_${WC1}_${WC2}_combined_13TeV_${i}_${j}.txt
  done
done

cd ..

# Now write a python file for each region and WCname
cd ${submitdir}
echo "Write python files in ${submitdir}"
for region in 1 2 3 4 combined
do
  pythonoutput=twoD_triplet__${WC1}_${WC2}__${region}.py
  echo "   - ${pythonoutput}"
  echo "python ${pythonoutput}" >> ${output}
  rm -f ${pythonoutput}
  echo "#!/usr/bin/env python" >> ${pythonoutput}
  echo "import os" >> ${pythonoutput}
  echo "os.chdir('${dir}')" >> ${pythonoutput}
  for i in {0..${npoints1}}
  do
    for j in {0..${npoints2}}
    do
      command1="text2workspace.py topEFT_2D_${WC1}_${WC2}_${region}_13TeV_${i}_${j}.txt -m ${i}${j} -o topEFT_2D_${WC1}_${WC2}_${region}_13TeV_${i}_${j}.root"
      command2="combine -M MultiDimFit topEFT_2D_${WC1}_${WC2}_${region}_13TeV_${i}_${j}.root -n .part3E_${i}_${j}_${region}_${WC1}_${WC2} --saveNLL --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --expectSignal=1 --cminDefaultMinimizerStrategy=0 --cminDefaultMinimizerTolerance=0.0001 --freezeParameters r  --setParameterRanges r=-10,10"
      echo "os.system('${command1}')" >> ${pythonoutput}
      echo "os.system('${command2}')" >> ${pythonoutput}
    done
  done
done
cd ..
