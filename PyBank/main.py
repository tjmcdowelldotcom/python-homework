#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Analyze PyBank Financial Data

#Import pathlib & csv library
from pathlib import Path
import csv
import os
import pandas as pd


# In[ ]:


#Set filepath for budget_data
budget_data = Path('budget_data.csv')


# In[ ]:


#Initialize budget_data list
budget_list = []
#Initialize total month count
total_months = ()


# In[ ]:


#import budget_data as object
with open(budget_data, 'r') as budget_file:
    budget_reader = csv.reader(budget_file, delimiter=',')
    
    # Read the header row first (skip this step if there is no header)
    budget_header = next(budget_reader)

    # Append the header to the list of records
    budget_list.append(budget_header)
    
    for row in budget_reader:
        budget_list.append(row)


# In[ ]:


#Count number of months
total_months = (len(budget_list[1:]))


# In[ ]:


#The net total amount of Profit/Losses over the entire period.
pnl_list = []
for row in budget_list[1:]:
    pnl_list.append(row[1])        
pnl_int = [int(x) for x in pnl_list]
pnl_sum = (sum(pnl_int))
pnl_sum_fmt = ("${:,.2f}".format(pnl_sum))


# In[ ]:


import numpy as np

#Create array beginning at first months pnl, (less the final month)
A = np.array(pnl_int[:-1])

#Create array beginning at second months pnl, (less first month)
B = np.array(pnl_int[1:])

#Variable that holds the diffence of the above arrays
C = (B-A)

#Subtract integers in B from int in A to find each months difference in PNL, then apply mean function to find average.

res = np.mean(C)
res_curr = "${:,.2f}".format(res)

#res_str = str(round(res,2))
#print(res_str)


#https://stackoverflow.com/questions/49690851/average-difference-between-ints-in-two-lists-in-one-line-python


# In[ ]:


#Initialize inc with first element of array.    
inc = C[0];    
r = 0
#Loop through the array    
for i in range(0, len(C)):    
    #Compare elements of array with inc    
    if(C[i] > inc):    
        inc = C[i]
        
#format monthly increase 
form_inc = ("${:,.2f}".format(inc))


# In[ ]:


#Find the month-year that corresponds with this increase 
inc_month = np.where(C==inc)
month_val = int(B[inc_month])

budget_data_pd = pd.read_csv('budget_data.csv')
budget_data_pd.set_index(budget_data_pd['Profit/Losses'], inplace=True)
inc_date = budget_data_pd.loc[budget_data_pd['Profit/Losses'] == month_val, 'Date'].iloc[0]
#budget_data_pd.head(86)


# In[ ]:


#Initialize dec with first element of array.    
dec = C[0];    
     
#Loop through the array    
for i in range(0, len(C)):    
    #Compare elements of array with smol    
    if(C[i] < dec):    
        dec = C[i]
        
#format monthly decrease
form_dec = ("${:,.2f}".format(dec))


# In[ ]:


#Find the month-year that corresponds with this decrease
dec_month = np.where(C==dec)
month_val_dec = int(B[dec_month])

budget_data_pd = pd.read_csv('budget_data.csv')
budget_data_pd.set_index(budget_data_pd['Profit/Losses'], inplace=True)
dec_date = budget_data_pd.loc[budget_data_pd['Profit/Losses'] == month_val_dec, 'Date'].iloc[0]


# In[ ]:


#Print results to terminal

results = (f"Financial Analysis\n----------------------------\nTotal Months: {total_months}\nTotal: {pnl_sum_fmt}\nAverage Change: {res_curr}\nGreatest Increase in Profits: {inc_date} ~ {form_inc}\nGreatest Decrease in Profits: {dec_date} ~ {form_dec}")
print(results)

#Create local text file w results
file_obj = open("PyBank Analysis.txt", "w+")
file_obj.write(results)

