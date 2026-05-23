import pandas as pd
import joblib


def predict():
        df1=pd.read_csv('media/input/test/test.csv')

        df1.head()


        df=df1.iloc[:,1:-1]

        model=joblib.load("ML/ds1.joblib")



        file=open("ML/map.txt","r")
        maps=file.read()
        file.close()
        maps=eval(maps)
        maps

        pred=model.predict(df)
        pred[0]


        if pred[0]==0:
                out='NetBIOS'
        elif pred[0]==1:
                out='LDAP'
        elif pred[0]==2:
                out='Benign'
        elif pred[0]==3:
                out='MSSQL'
        elif pred[0]==4:
                out='Portmap' 
        elif pred[0]==5:
                out='UDP' 
        elif pred[0]==6:
                out='Syn' 
        elif pred[0]==7:
                out='UDPLag' 
                
        
        return out


# df1=pd.read_csv('upload/testing.csv')

# df1.head()


# df=df1.iloc[:,1:-1]

# model=joblib.load("ds1.joblib")



# file=open("map.txt","r")
# maps=file.read()
# file.close()
# maps=eval(maps)
# maps

# pred=model.predict(df)
# pred[0]


# if pred[0]==0:
#         out="NO MALWARE DETECTED"
# elif pred[0]==1:
#         out="DOWNLOADER Virus Detected"
# elif pred[0]==2:
#         out="KEYLOGGES Virus Detected"
# elif pred[0]==3:
#         out="MINER Virus Detected"
# elif pred[0]==4:
#         out="RANSOMWARE Virus Detected" 
# elif pred[0]==5:
#         out="ROUGE Virus Detected"  
# elif pred[0]==6:
#         out="TROJAN Virus Detected"
# elif pred[0]==7:
#         out="WORM Virus Detected"        
# print(out)