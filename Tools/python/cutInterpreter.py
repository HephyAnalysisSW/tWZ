''' Class to interpret string based cuts
'''

import logging
logger = logging.getLogger(__name__)

jetSelection    = "nJetGood"
bJetSelectionM  = "nBTag"

mIsoWP = { "VT":5, "T":4, "M":3 , "L":2 , "VL":1, 0:"None" }


################################################################################
# build string for lepton fake region 
# first list all the cases of 1, 2 or 3 leptons failing a WP
leptonTCRstring = ""
failcases = [
    (">=", ">=",  "<"),
    (">=",  "<", ">="),
    ( "<", ">=", ">="),
    (">=",  "<",  "<"),
    ( "<", ">=",  "<"),
    ( "<",  "<", ">="),
    ( "<",  "<",  "<"),
]

WPtight = "4"
leptonTCRstring += "("
firstIteration = True
for (l1cut, l2cut, l3cut) in failcases:
    if firstIteration:
        leptonTCRstring += "("
        firstIteration = False 
    else:
        leptonTCRstring += " || ("
    leptonTCRstring += "l1_mvaTOPv2WP"+l1cut+WPtight+"&&l2_mvaTOPv2WP"+l2cut+WPtight+"&&l3_mvaTOPv2WP"+l3cut+WPtight
    leptonTCRstring += ")"
leptonTCRstring += ")"
################################################################################

from tWZ.Tools.objectSelection import lepString
special_cuts = {
    "singlelepVL":     "l1_pt>10&&l1_mvaTOPv2WP>=1",
    "singlelepL":      "l1_pt>10&&l1_mvaTOPv2WP>=2",
    "singlelepM":      "l1_pt>10&&l1_mvaTOPv2WP>=3",
    "singlelepT":      "l1_pt>10&&l1_mvaTOPv2WP>=4",
    "vetoAddLepVL":    "Sum$(lep_pt>10&&abs(lep_eta)<2.4&&lep_mvaTOPv2WP>=1)==1",
    "vetoAddLepL":     "Sum$(lep_pt>10&&abs(lep_eta)<2.4&&lep_mvaTOPv2WP>=2)==1",
    "trilepVL":        "l1_pt>40&&l2_pt>20&&l3_pt>10",
    "trilepL" :        "l1_pt>40&&l2_pt>20&&l3_pt>10&&l1_mvaTOPv2WP>=2&&l2_mvaTOPv2WP>=2&&l3_mvaTOPv2WP>=2",
    "trilepM" :        "l1_pt>40&&l2_pt>20&&l3_pt>10&&l1_mvaTOPv2WP>=3&&l2_mvaTOPv2WP>=3&&l3_mvaTOPv2WP>=3",
    "trilepT" :        "l1_pt>40&&l2_pt>20&&l3_pt>10&&l1_mvaTOPv2WP>=4&&l2_mvaTOPv2WP>=4&&l3_mvaTOPv2WP>=4",
    "qualepM" :        "l1_pt>40&&l2_pt>20&&l3_pt>10&&l4_pt>10&&l1_mvaTOPv2WP>=3&&l2_mvaTOPv2WP>=3&&l3_mvaTOPv2WP>=3&&l4_mvaTOPv2WP>=3",
    "qualepT" :        "l1_pt>40&&l2_pt>20&&l3_pt>10&&l4_pt>10&&l1_mvaTOPv2WP>=4&&l2_mvaTOPv2WP>=4&&l3_mvaTOPv2WP>=4&&l4_mvaTOPv2WP>=4",
    "trilepMCR":       "l1_pt>40&&l2_pt>20&&l3_pt>10&&( (l1_mvaTOPv2WP>=3&&l2_mvaTOPv2WP>=3&&l3_mvaTOPv2WP<3) || (l1_mvaTOPv2WP>=3&&l2_mvaTOPv2WP<3&&l3_mvaTOPv2WP>=3) || (l1_mvaTOPv2WP<3&&l2_mvaTOPv2WP>=3&&l3_mvaTOPv2WP>=3) )",
    "trilepTCR":       "l1_pt>40&&l2_pt>20&&l3_pt>10&&"+leptonTCRstring,
    "qualepMCR" :      "l1_pt>40&&l2_pt>20&&l3_pt>10&&l4_pt>10&&((l1_mvaTOPv2WP>=3&&l2_mvaTOPv2WP>=3&&l3_mvaTOPv2WP>=3&&l4_mvaTOPv2WP<3) || (l1_mvaTOPv2WP>=3&&l2_mvaTOPv2WP>=3&&l3_mvaTOPv2WP<3&&l4_mvaTOPv2WP>=3) || (l1_mvaTOPv2WP>=3&&l2_mvaTOPv2WP<3&&l3_mvaTOPv2WP>=3&&l4_mvaTOPv2WP>=3) || (l1_mvaTOPv2WP<3&&l2_mvaTOPv2WP>=3&&l3_mvaTOPv2WP>=3&&l4_mvaTOPv2WP>=3) )",
    "qualepTCR" :      "l1_pt>40&&l2_pt>20&&l3_pt>10&&l4_pt>10&&((l1_mvaTOPv2WP>=4&&l2_mvaTOPv2WP>=4&&l3_mvaTOPv2WP>=4&&l4_mvaTOPv2WP<4) || (l1_mvaTOPv2WP>=4&&l2_mvaTOPv2WP>=4&&l3_mvaTOPv2WP<4&&l4_mvaTOPv2WP>=4) || (l1_mvaTOPv2WP>=4&&l2_mvaTOPv2WP<4&&l3_mvaTOPv2WP>=4&&l4_mvaTOPv2WP>=4) || (l1_mvaTOPv2WP<4&&l2_mvaTOPv2WP>=4&&l3_mvaTOPv2WP>=4&&l4_mvaTOPv2WP>=4) )",
    "trilepVetoL":      "l1_pt>40&&l2_pt>20&&l3_pt>10&&l1_mvaTOPv2WP<2&&l2_mvaTOPv2WP<2&&l3_mvaTOPv2WP<2",
    "trilepVetoM":      "l1_pt>40&&l2_pt>20&&l3_pt>10&&l1_mvaTOPv2WP<3&&l2_mvaTOPv2WP<3&&l3_mvaTOPv2WP<3",
    "trilepVetoT":      "l1_pt>40&&l2_pt>20&&l3_pt>10&&l1_mvaTOPv2WP<4&&l2_mvaTOPv2WP<4&&l3_mvaTOPv2WP<4",
    "trilepLnoT":      "l1_pt>40&&l2_pt>20&&l3_pt>10&&l1_mvaTOPv2WP>=2&&l2_mvaTOPv2WP>=2&&l3_mvaTOPv2WP>=2&&l1_mvaTOPv2WP<4&&l2_mvaTOPv2WP<4&&l3_mvaTOPv2WP<4",
    "trilep4tVL":      "l1_pt>60&&l2_pt>30&&l3_pt>20",
    "trilep4tL" :      "l1_pt>60&&l2_pt>30&&l3_pt>20&&l1_mvaTOPv2WP>=2&&l2_mvaTOPv2WP>=2&&l3_mvaTOPv2WP>=2",
    "trilep4tM" :      "l1_pt>60&&l2_pt>30&&l3_pt>20&&l1_mvaTOPv2WP>=3&&l2_mvaTOPv2WP>=3&&l3_mvaTOPv2WP>=3",
    "trilep4tT" :      "l1_pt>60&&l2_pt>30&&l3_pt>20&&l1_mvaTOPv2WP>=4&&l2_mvaTOPv2WP>=4&&l3_mvaTOPv2WP>=4",
    "dilepVL":        "l1_pt>40&&l2_pt>20",
    "dilepL" :        "l1_pt>40&&l2_pt>20&&l1_mvaTOPv2WP>=2&&l2_mvaTOPv2WP>=2",
    "dilepM" :        "l1_pt>40&&l2_pt>20&&l1_mvaTOPv2WP>=3&&l2_mvaTOPv2WP>=3",
    "dilepT" :        "l1_pt>40&&l2_pt>20&&l1_mvaTOPv2WP>=4&&l2_mvaTOPv2WP>=4",
    "onZ1"   : "abs(Z1_mass-91.2)<10",
    "onZ2"   : "abs(Z2_mass-91.2)<10",
    "offZ1"    : "(abs(Z1_mass-91.2)>10)",
    "offZ2"  : "(!(abs(Z2_mass-91.2)<20))",
    "trilep": "l1_pt>40&&l2_pt>20&&l3_pt>10",
    "triMuon": "Sum$(lep_pt>40&&abs(lep_eta)<2.4&&lep_mediumId&&abs(lep_pdgId)==13)>=1 && Sum$(lep_pt>20&&abs(lep_eta)<2.4&&lep_mediumId&&abs(lep_pdgId)==13)>=2 && Sum$(lep_pt>10&&abs(lep_eta)<2.4&&lep_mediumId&&abs(lep_pdgId)==13)==3",
    "vetoElec": "Sum$(lep_pt>10&&abs(lep_eta)<2.4&&abs(lep_pdgId)==11)==0",
    "vetoMET" : "met_pt<20"
  }

continous_variables = [ ('ht','Sum$(JetGood_pt*(JetGood_pt>30&&abs(JetGood_eta)<2.4))'), ("met", "met_pt"), ("Z2mass", "Z2_mass"), ("Z1mass", "Z1_mass"), ("minDLmass", "minDLmass"), ("mT", "mT")]
discrete_variables  = [ ("njet", "nJetGood"), ("btag", "nBTag"), ("nLeptons", "nGoodLeptons"), ("deepjet", "Sum$(JetGood_pt>30&&abs(JetGood_eta)<2.4&&((year==2016)*(JetGood_btagDeepFlavB>0.7221)+(year==2017)*(JetGood_btagDeepFlavB>0.7489)+(year==2018)*(JetGood_btagDeepFlavB>0.7264)))") ]

class cutInterpreter:
    ''' Translate var100to200-var2p etc.
    '''

    @staticmethod
    def translate_cut_to_string( string ):

        if string.startswith("multiIso"):
            str_ = mIsoWP[ string.replace('multiIso','') ]
            return "l1_mIsoWP>%i&&l2_mIsoWP>%i" % (str_, str_)
        elif string.startswith("relIso"):
           iso = float( string.replace('relIso','') )
           raise ValueError("We do not want to use relIso for our analysis anymore!")
           return "l1_relIso03<%3.2f&&l2_relIso03<%3.2f"%( iso, iso )
        elif string.startswith("miniIso"):
           iso = float( string.replace('miniIso','') )
           return "l1_miniRelIso<%3.2f&&l2_miniRelIso<%3.2f"%( iso, iso )
        # special cuts
        if string in special_cuts.keys(): return special_cuts[string]

        # continous Variables
        for var, tree_var in continous_variables:
            if string.startswith( var ):
                num_str = string[len( var ):].replace("to","To").split("To")
                upper = None
                lower = None
                if len(num_str)==2:
                    lower, upper = num_str
                elif len(num_str)==1:
                    lower = num_str[0]
                else:
                    raise ValueError( "Can't interpret string %s" % string )
                res_string = []
                if lower: res_string.append( tree_var+">="+lower )
                if upper: res_string.append( tree_var+"<"+upper )
                return "&&".join( res_string )

        # discrete Variables
        for var, tree_var in discrete_variables:
            logger.debug("Reading discrete cut %s as %s"%(var, tree_var))
            if string.startswith( var ):
                # So far no njet2To5
                if string[len( var ):].replace("to","To").count("To"):
                    raise NotImplementedError( "Can't interpret string with 'to' for discrete variable: %s. You just volunteered." % string )

                num_str = string[len( var ):]
                # logger.debug("Num string is %s"%(num_str))
                # var1p -> tree_var >= 1
                if num_str[-1] == 'p' and len(num_str)==2:
                    # logger.debug("Using cut string %s"%(tree_var+">="+num_str[0]))
                    return tree_var+">="+num_str[0]
                # var123->tree_var==1||tree_var==2||tree_var==3
                else:
                    vls = [ tree_var+"=="+c for c in num_str ]
                    if len(vls)==1:
                      # logger.debug("Using cut string %s"%vls[0])
                      return vls[0]
                    else:
                      # logger.debug("Using cut string %s"%'('+'||'.join(vls)+')')
                      return '('+'||'.join(vls)+')'
        raise ValueError( "Can't interpret string %s. All cuts %s" % (string,  ", ".join( [ c[0] for c in continous_variables + discrete_variables] +  special_cuts.keys() ) ) )

    @staticmethod
    def cutString( cut, select = [""], ignore = []):
        ''' Cutstring syntax: cut1-cut2-cut3
        '''
        cuts = cut.split('-')
        # require selected
        cuts = filter( lambda c: any( sel in c for sel in select ), cuts )
        # ignore
        cuts = filter( lambda c: not any( ign in c for ign in ignore ), cuts )

        cutString = "&&".join( map( cutInterpreter.translate_cut_to_string, cuts ) )

        return cutString

    @staticmethod
    def cutList ( cut, select = [""], ignore = []):
        ''' Cutstring syntax: cut1-cut2-cut3
        '''
        cuts = cut.split('-')
        # require selected
        cuts = filter( lambda c: any( sel in c for sel in select ), cuts )
        # ignore
        cuts = filter( lambda c: not any( ign in c for ign in ignore ), cuts )
        return [ cutInterpreter.translate_cut_to_string(cut) for cut in cuts ]
        #return  "&&".join( map( cutInterpreter.translate_cut_to_string, cuts ) )

if __name__ == "__main__":
    print cutInterpreter.cutString("njet2-btag0p-multiIsoVT-relIso0.12-looseLeptonVeto-mll20-onZ-met80-metSig5-dPhiJet0-dPhiJet1-mt2ll100")
    print
    print cutInterpreter.cutList("njet2-btag0p-multiIsoVT-relIso0.12-looseLeptonVeto-mll20-onZ-met80-metSig5-dPhiJet0-dPhiJet1-mt2ll100")
