import pandas as pd
import os 
df=pd.read_csv(os.path.join(os.getenv('ML_DATAFRAME_OUTPUT'),'REF.csv'))
print(len(df))
print(df.head())