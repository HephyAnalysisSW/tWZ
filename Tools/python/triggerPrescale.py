
class triggerPrescale:
    
    def __init__(self, year):
        # Prescales are from 
        if year == 2016:
            self.prescales={
                "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  5140,
                "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 572.4,
                "HLT_Mu3_PFJet40":                    4849,
                "HLT_Mu8":                            9123,
                "HLT_Mu17":                           127,
            }
        elif year == 2017:
            self.prescales={
                "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  11364,
                "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1167,
                "HLT_Mu3_PFJet40":                    9006,
                "HLT_Mu8":                            15943,
                "HLT_Mu17":                           592.9,
                "HLT_Mu20":                           72.3,
                "HLT_Mu27":                           224.5,
            }
        elif year == 2018:
            self.prescales={
                "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":  7569,
                "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1194, 
                "HLT_Mu3_PFJet40":                    10713,
                "HLT_Mu8":                            7261,
                "HLT_Mu17":                           974, 
                "HLT_Mu20":                           755,  
                "HLT_Mu27":                           301,
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
            
            
