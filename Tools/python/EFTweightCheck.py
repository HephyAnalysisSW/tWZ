

def removeDamagedFiles( year, samples, filelist ):
    if year not in [ 'UL2016', 'UL2016_preVFP', 'UL2017', 'UL2018' ]:
        raise Exception("EFTweightCheck: Year %s not known"%year)

    if len(samples)>1 or samples[0] not in [ 'TTZ_EFT', 'WZ_EFT', 'ZZ_EFT' ]:
        return filelist

    samplename = samples[0]

    damagedFiles = {
        "UL2016" : {
            "TTZ_EFT": ["tree_269.root", "tree_573.root"], # done
            "WZ_EFT" : ["tree_90.root"], # done
            "ZZ_EFT" : [], # done
        },
        "UL2016_preVFP" : {
            "TTZ_EFT": ["tree_540.root", "tree_634.root"], # done
            "WZ_EFT" : [], # done
            "ZZ_EFT" : [], # done
        },
        "UL2017" : {
            "TTZ_EFT": [],
            "WZ_EFT" : [],
            "ZZ_EFT" : [],
        },
        "UL2018" : {
            "TTZ_EFT": ["tree_302.root", "tree_304.root", "tree_309.root", "tree_310.root", "tree_313.root", "tree_314.root", "tree_316.root", "tree_317.root", "tree_93.root", "tree_95.root"], # done
            "WZ_EFT" : ["tree_555.root", "tree_643.root"], # done
            "ZZ_EFT" : ["tree_207.root", "tree_208.root", "tree_209.root", "tree_212.root", "tree_217.root"], # done
        },
    }

    newlist = []
    for f in filelist:
        keepFile = True
        for d in damagedFiles[year][samplename]:
            if d in f:
                keepFile = False
        if keepFile:
            newlist.append(f)

    return newlist
