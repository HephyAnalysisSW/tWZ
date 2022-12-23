
class triggerPrescale:
    
    def __init__(self, year, useBril=False):
        if useBril:
            # From BRIL
            if year == 2016:
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  1.,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1.,
                    "HLT_Mu3_PFJet40":                    1.,
                    "HLT_Mu8":                            1.,
                    "HLT_Mu17":                           1.,
                }
            elif year == 2017:
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  1.,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1.,
                    "HLT_Mu3_PFJet40":                    1.,
                    "HLT_Mu8":                            1.,
                    "HLT_Mu17":                           1.,
                    "HLT_Mu20":                           1.,
                    "HLT_Mu27":                           1.,
                }
            elif year == 2018:
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
                raise NotImplementedError("Trigger prescaling not implemented for year = %i"%year)
        else:      
            # Measured myself
            if year == 2016:
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  1.,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1.,
                    "HLT_Mu3_PFJet40":                    1.,
                    "HLT_Mu8":                            1.,
                    "HLT_Mu17":                           1.,
                }
            elif year == 2017:
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  11341.9201097,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1077.31361125,
                    "HLT_Mu3_PFJet40":                    5942.16123582,
                    "HLT_Mu8":                            14223.0827619,
                    "HLT_Mu17":                           667.316989991,
                    "HLT_Mu20":                           82.2314694334,
                    "HLT_Mu27":                           210.915192962,
                }
            elif year == 2018:
                self.prescales={
                    "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  7681,
                    "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1259, 
                    "HLT_Mu3_PFJet40":                    10215,
                    "HLT_Mu8":                            7420,
                    "HLT_Mu17":                           947, 
                    "HLT_Mu20":                           715,  
                    "HLT_Mu27":                           339,
                }
            else:
                raise NotImplementedError("Trigger prescaling not implemented for year = %i"%year)

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
            
            
