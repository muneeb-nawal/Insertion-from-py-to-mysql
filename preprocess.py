import mysql.connector as connection
import logging as lg
import csv
import os

logger = lg.getLogger(__name__) #new logger
logger.setLevel(lg.ERROR)
logger.setLevel(lg.INFO)

formatter = lg.Formatter(' %(name)s : %(asctime)s : %(levelname)s : %(message)s')

filehandler= lg.FileHandler('preprocess.log')
filehandler.setFormatter(formatter)

logger.addHandler(filehandler)

stream_handler = lg.StreamHandler() #no need to set log level as its set to error by logger

logger.addHandler(stream_handler)
#lg.basicConfig(filename = '{}.log'.format(__name__), level = lg.INFO,format = '%(asctime)s : %(levelname)s : %(message)s')

class preprocess:
    """Enter proper file path"""
    
    def __init__(self,file_path):
        self.file_path = file_path
    
    def genlist(self,_delim=';'):
        """provide delim. default = ';' """
        try:
            with open(self.file_path,mode='r') as data:
                d = csv.reader(data,delimiter = _delim)
                dlist = [i for i in d]
                return dlist
        except Exception as e:
            logger.error(e)
    
    def write_csv(self,new_name,lst):
        with open(f'{new_name}.csv',mode='w',newline="") as data:
            d = csv.writer(data)
            d.writerows(lst)
    
    def create_updated(self,new_name,lst):
        """
        1st arg : new file name
        2nd arg : pass the list generated"""
        try:
            if not os.path.exists(os.getcwd()+f'\\{new_name}.csv'):
                self.write_csv(new_name,lst)
                logger.info(f'file created in {os.getcwd()}')
            else:
                logger.info(f"file already present at {os.getcwd()}")
        except Exception as e:
            logger.error(e)
        finally:
            if input("save path ? : y/n ") == 'y':
                return os.getcwd()+f'\\{new_name}.csv'
            else:
                logger.info("path not saved")