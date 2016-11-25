#!/usr/bin/env python

src = "PUT YOUR SOURCE HERE"
dst = "PUT YOUR DESTINATION HERE"

grouby_header = "eid"
sort_header = "end_time"
#eid column actually patient ID?

import pandas as pd 

#reading data in from src
df_in = pd.read_csv(src)
#group data by pid
df_by_patient = df_in.groupby(by=groupby_header)
#deleted to save space
del df_in

#accumulate results here
pids = []
results =[]

#pid is patient id, patient_df is dataframe of all rows with same pid
for pid, patient_df in df_by_patient:
	result = consider(patient_df) 
	pids.append(pid)
	results.append(result)

	
#dictionary for populating dataframe
out_dict = {"patient":patients,"results":results}
#dataframe for output
df_out = pd.DataFrame.from_dict(out_dict) 
#write to output
df_out.to_csv(dst)

#WRITE LOGIC HERE
#ACCESS ARDS BY dataframe["pid"]
def consider(df):
	ards = None
	#rows should be sorted by date
	df.sort_values(by = sort_header)
	#check rows in order earliest to latest
	for idx, row in df.iterrows():
		break	
		#consider each row here!
		#access column data with row["header"]
	return ards
	


