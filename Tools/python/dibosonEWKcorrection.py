
# factors from https://arxiv.org/pdf/1912.00068.pdf, Figure 8
def getNNLOtoNLO(pt, process="WZ", correctNorm = True):
    # First describe shape effect
    if pt < 100:
        pt = 100.
    if pt > 2000:
        pt = 2000.
    factor = 1.
    if process == "ZZ":
        # ZZ
        # 100 -> 1.2
        # 1000 -> 1.3
        factor = 1.2 + 0.1 * pt/900.
    elif process == "WZ":
        # WZ
        # 100 -> 1.15
        # 1000 -> 1.3
        factor = 1.15 + 0.15 * pt/900.
    # Now account for the fact that the samples are already scaled to NNLO cross section
    # Thus, get NNLO/NLO from Table 3 and divide
    norm = 1.
    if correctNorm:
        if process == "ZZ":
            norm = 1.0/1.153
        elif process == "WZ":
            norm = 1.0/1.109
    return factor * norm

def getEWKtoQCD(pt, process="WZ", mode="add"):
    if pt < 100:
        pt = 100.
    if pt > 2000:
        pt = 2000.
    factor = 1.
    if process == "ZZ":
        if mode == "add":
            factor = 0.96 - 0.07 * pt/1900.
        elif mode == "mul":
            factor = 0.925 - 0.65 * pt/1900.
    elif process == "WZ":
        if mode == "add":
            factor = 1. + 0.04 * pt/1900.
        elif mode == "mul":
            factor = 0.975 - 0.37 * pt/1900.
    return factor
