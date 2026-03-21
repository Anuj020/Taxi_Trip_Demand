import sys
from taxidemand.logging.logger import logging

class TaxiDemandException(Exception):
    def __init__(self, error_message,error_details:sys):
        self.error_message = error_message
        _,_,exc_traceback = error_details.exc_info()
        # exc_traceback  gives us errors details such as filename, from which line error occuring
        self.lineno = exc_traceback.tb_lineno
        self.file_name = exc_traceback.tb_frame.f_code.co_filename
    
    def __str__(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(self.file_name,self.lineno,str(self.error_message))
    

if __name__ == '__main__':
    try:
        logging.info("Enter try block")
        a = 1/0
        print("This wil not be printed",a)
        logging.info("Divided by Zero")
    except Exception as e:
        raise TaxiDemandException(e,sys)