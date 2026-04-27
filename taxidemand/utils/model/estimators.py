from taxidemand.constants import training_pipeline
from taxidemand.exception.exception import TaxiDemandException 
from taxidemand.logging.logger import logging
import os,sys

class TaxiDemandModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise TaxiDemandException(e,sys)
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise TaxiDemandException(e,sys)