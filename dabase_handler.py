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

class database:
    def __init__(self,host,user,password,db_name,table_name):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.table_name = table_name
    
    def show_db(self):
        try:
            mydb = connection.connect(host=self.host,user=self.user, passwd=self.password,use_pure=True)
            # check if the connection is established

            query = "SHOW DATABASES"

            cursor = mydb.cursor() #create a cursor to execute queries
            cursor.execute(query)
            #print(cursor.fetchall())
            logger.info(f"All databases : {cursor.fetchall()}")

        except Exception as e:
            mydb.close()
            print(str(e))
    
    def create_db(self):
        try:
            mydb = connection.connect(host=self.host,user=self.user, passwd=self.password,use_pure=True)
            # check if the connection is established
            print(mydb.is_connected())

            query = f"Create database {self.db_name}"
            cursor = mydb.cursor() #create a cursor to execute queries
            cursor.execute(query)
            logger.info(f"Database {self.db_name} Created!!")
            mydb.close()
        except Exception as e:
            if input("database already present, drop it and create new? y/n : ") == 'y':
                cursor.execute(f"drop database {self.db_name}")
                cursor.execute(f"Create database {self.db_name}")
                mydb.close()
                logger.warning(f"error rectified by drop: {e}")
            else:
                mydb.close()
                logger.warning(f"warning: {e}")
                
    def create_table(self):
        try:
            mydb = connection.connect(host=self.host,database = self.db_name,user=self.user, passwd=self.password,use_pure=True)
            # check if the connection is established
            print(mydb.is_connected())

            query = f"create table if not exists {self.db_name}.{self.table_name} (Chiralindicen varchar(10) ,Chiralindicem varchar(10) , Initialatomiccoordinateu varchar(10) ,Initialatomiccoordinatev varchar(10) , Initialatomiccoordinatew varchar(10) ,Calculatedatomiccoordinatesu varchar(10) , Calculatedatomiccoordinatesv varchar(10) ,Calculatedatomiccoordinatesw varchar(10) )"

            cursor = mydb.cursor() #create a cursor to execute queries
            cursor.execute(query)
            logger.info(f"Table {self.table_name} Created!!")
            mydb.close()
        except Exception as e:
            mydb.close()
            print(str(e))
                
    def insert_data_db(self,path):
        try:
            mydb = connection.connect(host=self.host,database = self.db_name,user=self.user, passwd=self.password,use_pure=True)
            # check if the connection is established
            logger.info(f'connection established for insert : {mydb.is_connected()}')
            
            with open(path,'r') as data:
                next(data)
                db_csv = csv.reader(data,delimiter = '\n')
                #next(db_csv)
                print(db_csv)
                for j in db_csv:
                    #print('insert into carbonnanotube.nanotube_details values (' + str(j[0]) + ')')
                    query = f'insert into {self.db_name}.{self.table_name} values (' + str(j[0]) + ')'
                    #query = 'insert into carbonnanotube.nanotube_details values ({})'.format(', '.join([value for value in j]))
                    cursor = mydb.cursor() #create a cursor to execute queries
                    cursor.execute(query)
                mydb.commit()
                logger.info(f"data inserted into db:{self.db_name}; Table : {self.table_name}")
            mydb.close()
        except Exception as e:
            mydb.close()
            #print(str(e))
            logger.error(e)