
class triggerPrescale:
    
    def __init__(self, year, mode="mine"):
        if mode not in ["mine", "ghent", "bril"]:
            raise NotImplementedError("Trigger prescaling not implemented for mode = %s"%mode)
        
        if mode == "ghent":
            # From Ghent
            if year == "UL2016preVFP":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  3686.33696069,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 341.677087818,
                    "HLT_Mu3_PFJet40":                    6063.39889889,
                    "HLT_Mu8":                            4851.09561995,
                    "HLT_Mu17":                           85.2464047329,
                    "HLT_Mu20":                           206.371514127,
                    "HLT_Mu27":                           141.425312585,
                }
            elif year == "UL2016":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  3404.02355584,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1054.62315151,
                    "HLT_Mu3_PFJet40":                    6672.36041422,
                    "HLT_Mu8":                            16557.3330772,
                    "HLT_Mu17":                           519.969425798,
                    "HLT_Mu20":                           445.337097916,
                    "HLT_Mu27":                           137.418510823,
                }
            elif year == "UL2017":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  8583.61730801,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 928.100086313,
                    "HLT_Mu3_PFJet40":                    3930.43136484,
                    "HLT_Mu8":                            8408.80233428,
                    "HLT_Mu17":                           399.558886989,
                    "HLT_Mu20":                           50.9772335675,
                    "HLT_Mu27":                           157.130915193,
                }
            elif year == "UL2018":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  3797.64621887,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 748.895379316, 
                    "HLT_Mu3_PFJet40":                    5076.11636489,
                    "HLT_Mu8":                            3517.60915141,
                    "HLT_Mu17":                           749.782563057, 
                    "HLT_Mu20":                           631.109933039,  
                    "HLT_Mu27":                           278.72389054,
                }  
            else:
                raise NotImplementedError("Trigger prescaling not implemented for year = %s"%year)            
        elif mode == "bril":
            # From BRIL
            if year == "UL2016preVFP":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  5141.899251,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 572.584500448,
                    "HLT_Mu3_PFJet40":                    4848.34089913,
                    "HLT_Mu8":                            9129.17601399,
                    "HLT_Mu17":                           127.041635445,
                    "HLT_Mu20":                           256.862153226,
                    "HLT_Mu27":                           143.472338012,
                }
            elif year == "UL2016":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  5141.899251,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 572.584500448,
                    "HLT_Mu3_PFJet40":                    4848.34089913,
                    "HLT_Mu8":                            9129.17601399,
                    "HLT_Mu17":                           127.041635445,
                    "HLT_Mu20":                           256.862153226,
                    "HLT_Mu27":                           143.472338012,
                }
            elif year == "UL2017":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  11360.5330533,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1165.85200291,
                    "HLT_Mu3_PFJet40":                    9002.09070805,
                    "HLT_Mu8":                            15940.9827565,
                    "HLT_Mu17":                           592.522518622,
                    "HLT_Mu20":                           72.0652540143,
                    "HLT_Mu27":                           224.404773677,
                }
            elif year == "UL2018":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  9315.15991869,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1536.9429043, 
                    "HLT_Mu3_PFJet40":                    22125.3782748,
                    "HLT_Mu8":                            6984.35039719,
                    "HLT_Mu17":                           1304.90350437, 
                    "HLT_Mu20":                           1080.77634328,  
                    "HLT_Mu27":                           474.985077468,
                }  
            else:
                raise NotImplementedError("Trigger prescaling not implemented for year = %s"%year)
        elif mode == "mine":      
            # Measured myself
            if year == "UL2016preVFP":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  6465.5767026,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 526.134215655,
                    "HLT_Mu3_PFJet40":                    7310.09061493,
                    "HLT_Mu8":                            4982.8340468,
                    "HLT_Mu17":                           74.7897935104,
                    "HLT_Mu20":                           162.651473263,
                    "HLT_Mu27":                           112.836933305,
                }
            elif year == "UL2016":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  8309.00642408,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 2448.77749586,
                    "HLT_Mu3_PFJet40":                    8341.62859509,
                    "HLT_Mu8":                            24111.8217713,
                    "HLT_Mu17":                           600.532648006,
                    "HLT_Mu20":                           435.516828392,
                    "HLT_Mu27":                           139.29890913,
                }
            elif year == "UL2017":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  10921.9128316,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1135.00059454,
                    "HLT_Mu3_PFJet40":                    5998.44830411,
                    "HLT_Mu8":                            19275.0825695,
                    "HLT_Mu17":                           704.719311802,
                    "HLT_Mu20":                           67.721568649,
                    "HLT_Mu27":                           211.943332799,
                }
            elif year == "UL2018":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  6579.1822458,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1336.75017094,
                    "HLT_Mu3_PFJet40":                    8697.97949292,
                    "HLT_Mu8":                            9507.38839664,
                    "HLT_Mu17":                           1547.61001665, 
                    "HLT_Mu20":                           970.223642099,  
                    "HLT_Mu27":                           425.548142026,
                }
            else:
                raise NotImplementedError("Trigger prescaling not implemented for year = %s"%year)

    def getWeight(self, triggerlist):
        # trigger list must contain the names of all triggers that fired (of those implemented here)
        
        # weight = 1 - (1-1/prescale_1)*(1-1/prescale_2)*...*(1-1/prescale_N)
        prescaleproduct = 1.0
        for trigger in triggerlist:
            if trigger not in self.prescales.keys():
                raise NotImplementedError("Prescale not implemented for trigger %s"%trigger)
            factor = (1.0-1.0/self.prescales[trigger])
            prescaleproduct *= factor
        weight = 1.0 - prescaleproduct
        return weight 
            
            
