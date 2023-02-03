
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
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  1.,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1.,
                    "HLT_Mu3_PFJet40":                    1.,
                    "HLT_Mu8":                            1.,
                    "HLT_Mu17":                           1.,
                    "HLT_Mu20":                           1.,
                    "HLT_Mu27":                           1.,
                }
            elif year == "UL2016":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  1.,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1.,
                    "HLT_Mu3_PFJet40":                    1.,
                    "HLT_Mu8":                            1.,
                    "HLT_Mu17":                           1.,
                    "HLT_Mu20":                           1.,
                    "HLT_Mu27":                           1.,
                }
            elif year == "UL2017":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  1.,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1.,
                    "HLT_Mu3_PFJet40":                    1.,
                    "HLT_Mu8":                            1.,
                    "HLT_Mu17":                           1.,
                    "HLT_Mu20":                           1.,
                    "HLT_Mu27":                           1.,
                }
            elif year == "UL2018":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  1.,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1., 
                    "HLT_Mu3_PFJet40":                    1.,
                    "HLT_Mu8":                            1.,
                    "HLT_Mu17":                           1., 
                    "HLT_Mu20":                           1.,  
                    "HLT_Mu27":                           1.,
                }  
            else:
                raise NotImplementedError("Trigger prescaling not implemented for year = %s"%year)
        elif mode == "mine":      
            # Measured myself
            if year == "UL2016preVFP":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  6229.62660079,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 440.740081094,
                    "HLT_Mu3_PFJet40":                    7178.45712872,
                    "HLT_Mu8":                            4203.38687734,
                    "HLT_Mu17":                           72.2525081456,
                    "HLT_Mu20":                           153.637292859,
                    "HLT_Mu27":                           99.089848659,
                }
            elif year == "UL2016":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  7922.26097063,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1801.8398497,
                    "HLT_Mu3_PFJet40":                    7737.95144378,
                    "HLT_Mu8":                            18921.8348027,
                    "HLT_Mu17":                           569.536792274,
                    "HLT_Mu20":                           432.703777024,
                    "HLT_Mu27":                           132.47687128,
                }
            elif year == "UL2017":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  11378.4826614,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1078.97277512,
                    "HLT_Mu3_PFJet40":                    5996.83773323,
                    "HLT_Mu8":                            14280.9420492,
                    "HLT_Mu17":                           668.742986599,
                    "HLT_Mu20":                           82.3808120496,
                    "HLT_Mu27":                           211.32230202,
                }
            elif year == "UL2018":
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  7284.59076069,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1207.62241777,
                    "HLT_Mu3_PFJet40":                    10215,
                    "HLT_Mu8":                            7420,
                    "HLT_Mu17":                           947, 
                    "HLT_Mu20":                           715,  
                    "HLT_Mu27":                           339,
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
            
            
