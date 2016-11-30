#!/usr/bin/env python

src = "PUT SOURCE HERE"
dst = "PUT DESTINATION HERE"

grouby_header = "eid"
sort_header = "end_time"
rad_report = "rad_report"
#eid column actually patient ID?

import pandas as pd 
#can sort by pt and dates at the end (faster) if considering each line individually
#reading data in from src
df_in = pd.read_csv(src)
#group data by pid
df_by_patient = df_in.groupby(by=groupby_header)
#deleted to save space
del df_in

#pid is patient id, patient_df is dataframe of all rows with same pid
for pid, patient_df in df_by_patient:
	consider(patient_df) 


#dataframe for output
df_out = pd.concat([patient_df for pid, patient_df in df_by_patient])
#write to output
df_out.to_csv(dst)

#WRITE LOGIC HERE
#ACCESS ARDS BY dataframe["pid"]

#rule1 positive for infiltrate without "no", "chronic","without" or followed by "which may represent atelectasis"
#if rule 1 negative skip rules 2-4
rule1 = ["infiltrate", "opacity", "opacification", "opacities", "hazy lung disease", "consolidation", "edema"]
#placeholders
rule2 = ["bilateral"]
rule3 = ["new"]
rule4 = ["worsening", "increased", "increasing"]
negatives = ["no", "without", "chronic", "not"]

def consider(df):
	#rows should be sorted by date
	df.sort_values(by = sort_header)
	#check rows in order earliest to latest via timestamp
	#if we're considering each rad report individually then we can scrap sorting by timestamp (slow)
	
	ards_lst = []
	infiltrate_lst = []
	bi_or_uni_lst = []
	new_infiltrate_lst = []
	worsening_lst = []

	for idx, row in df.iterrows():
		#consider each row here!
		#report ARDS date if ARDS >= 3
   		ards_yn, infiltrate, worsening, new_infiltrate, bi_or_uni = checkReport(row['rad_report'])
   		
   		infiltrate_lst.append(infiltrate)
   		worsening_lst.append(worsening)
   		new_infiltrate_lst.append(new_infiltrate)
   		bi_or_uni_lst.append(bi_or_uni)
   		ards_lst.append(ards_yn)

   	df['ards_prediction'] = ards_lst
   	df['bi_or_uni_prediction'] = bi_or_uni_lst
   	df['worsening_prediction'] = worsening_lst
   	df['new_infiltrate_prediction'] = new_infiltrate_lst 

def checkReport(report):
	#These are the values to update based on the report
	ards_yn = 0
	infiltrate = 0
	worsening = 0
	new_infiltrate = 0
	bi_or_uni = 0
	
	#############
	##THE LOGIC##
	#############
	candidate_lst = []
	search_lst = []
	lines = str.split(report,'.')
	for word in rule1:
    	for sentence in lines:
        	if word in sentence:
            	candidate_lst.append(sentence)
            	search_lst.append(word)
            	for element in candidate_lst:
            		elements = str.split(element, ' ')
            		for term in search_lst:
            			if term in elements:
            				#if the word before term is a negative skip the rest of the loop (infiltrates must be present)
            				#how many indices before "infiltrate" do we need to check?
            				x = elements.index(term) - 1
            				if elements[x] in negatives:
            					#move on to next iteration
            					continue
            				else:
            					infiltrate = 1
    #since rules 2 and describe the infiltrate limit search to sentences already identified in 1st loop
    #otherwise could hit words not directly targeting infiltrate

    #checking if infiltrate is bilateral
    for word in rule2:
	    for element in candidate_lst:
	        if word in element:
	            x = elements.index(word) - 1
	            if elements[x] in negatives:
	            	continue
	            else:
	            	bi_or_uni = 1

	#checking if infiltrate is new
	for word in rule3:
	    for element in candidate_lst:
	        if word in element:
	            x = elements.index(word)
	            if elements[x] in negatives:
	            	continue
	            else:
	            	bi_or_uni = 1
    
    for word in rule3:
    	for sentence in lines:
        	if word in sentence:
            	candidate_lst.append(sentence)
            	search_lst.append(word)
            	for element in candidate_lst:
            		elements = str.split(element, ' ')
            		for term in search_lst:
            			if term in elements:
            				x = elements.index(term) - 1
            				if elements[x] in negatives:
            					continue
            				else:
            					new_infiltrate = 1
    #right now data is grouped by 1) patient, 2) timestamp. if new is an adjective describing the infiltrate this loop should
    #be in the infiltrate loop above, and bilateral should be as well. 

    for word in rule4:
    	for sentence in lines:
        	if word in sentence:
            	candidate_lst.append(sentence)
            	search_lst.append(word)
            	for element in candidate_lst:
            		elements = str.split(element, ' ')
            		for term in search_lst:
            			if term in elements:
            				x = elements.index(term) - 1
            				if elements[x] in negatives:
            					continue
            				else:
            					worsening = 1




            				#be careful with pulmonary edema (can only search one word if structuret this way)
            				#not sure how to handle this
            				#if elements.index(term) - 1 is a *negative* like no or without then infiltrate = 0


     		#parse sentences here
     		#kill line
		if any(word in rad_report for word in rule2):
    		bi_or_uni = 1
		if any(word in rad_report for word in rule3):
   			new_infiltrate = 1
		if any(word in rad_report for word in rule4):
    		worsening = 1

   	return ards_yn, infiltrate, worsening, new_infiltrate, bi_or_uni
	

