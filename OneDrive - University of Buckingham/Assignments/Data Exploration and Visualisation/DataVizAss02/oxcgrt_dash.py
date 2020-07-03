# -*- coding: utf-8 -*-
"""
Created on Mon May 11 00:59:29 2020

@author: 
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import seaborn as sns
from numpy import median, mean
import json, urllib.request
import sys
from pathlib import Path
from datetime import datetime
import matplotlib.dates as mdate
import plotly.graph_objects as go
import math
from matplotlib.ticker import StrMethodFormatter, NullFormatter
import matplotlib.ticker as mticker
from matplotlib.ticker import ScalarFormatter
import matplotlib.ticker as mtick

#%matplotlib inline

# # open a request to read the data
# data = urllib.request.urlopen("https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/actions/GBR/2020-04-06").read()
# # load the data (will be saved as dictionary in output)
# output = json.loads(data)


#==============================Part 1 =================================
dataFolder=Path(r'.')
filename="OxCGRT_summary20200520.csv"
dataFile= dataFolder / filename
#sheetname='stringencyindex_legacy'
ocgrt_df=pd.read_csv(dataFile)
ocgrt_df_null=ocgrt_df[ocgrt_df.isnull().any(axis=1)]

filename="country-and-continent.csv"
dataFile= dataFolder / filename
cc_df=pd.read_csv(dataFile)
cc_df_null=cc_df[cc_df.isnull().any(axis=1)]



ocgrt_all_df = (ocgrt_df.set_index('CountryCode').join(cc_df.set_index('CountryCode'))).reset_index()

ocgrt_all_null_df=ocgrt_all_df[ocgrt_all_df.isnull().any(axis=1)]
ocgrt_cc_null_df=ocgrt_all_df.CountryName[ocgrt_all_df['Continent_Name'].isnull()].unique()
print("Countries with Null Continent_Name=%s" %ocgrt_cc_null_df)

#As Kosovo has a null contient, RKS Not in offieal ISO3166 codes country-and-continent.csv 
# Setting Kosovo to same contient as Serbia = Europe
ocgrt_all_df.loc[ocgrt_all_df['Continent_Name'].isnull(),'Continent_Name']="Europe"
#ocgrt_all_df[ocgrt_all_df['Continent_Name'].isnull()]

#stringencyindex_legacy_df = pd.read_excel (dataFile,sheet_name='stringencyindex_legacy')
#confirmedcases_df = pd.read_excel (dataFile,sheet_name='confirmedcases')
#confirmeddeaths_df = pd.read_excel (dataFile,sheet_name='confirmeddeaths')
#null_rows=data_df[data_df.isnull().any(axis=1)]
# Fill stringency data with teh last known values 
#stringencyindex_legacy_df=stringencyindex_legacy_df.ffill(axis=1)



#==============================Part 2 - Question 3 =================================

# country_list=['China','South Korea','United States','France','United Kingdom','Italy']
# #country_list=['United Kingdom']
# #country_list=['South Korea']
# #country_list=['Italy']

# fig = plt.figure(figsize=(12,10), dpi=1600)
# for country in country_list:
#     stringencyindex_legacy_c_df=stringencyindex_legacy_df[stringencyindex_legacy_df['CountryName'] == country]
#     confirmedcases_c_df=confirmedcases_df[confirmedcases_df['CountryName'] == country]
#     #country=confirmedcases_df.iloc[:,0].iloc[0]
#     s_t_df=stringencyindex_legacy_c_df.transpose()
#     c_t_df=confirmedcases_c_df.transpose()
#     X=c_t_f_df=c_t_df.iloc[2:,:]
#     X.set_axis(['confirmedcases'],axis=1,inplace=True)
#     Y=s_t_df.iloc[2:,:]
#     Y.set_axis(['stringency'],axis=1,inplace=True)
#     Y.rename(index={0:"stringency"})
#     result=pd.concat([X,Y], axis=1)
#     result.set_index("confirmedcases",inplace=True) 
#     result.sort_index(inplace=True)
#     #result=result[result.index < 10]
#     plt.title('Comparison of stringency of COVID-19 repsonse in six countries',fontsize=18) 
#     plt.xlabel("Reported number of cases of COVID-19",fontsize=16)
#     plt.ylabel("Stringency index",fontsize=16)
#     plt.plot(result,label=country)
#     ax=plt.gca()
#     plt.ylim(0, 100)
#     plt.xlim(1, 1000000)
#     plt.xscale("log")
#     ax.xaxis.set_major_formatter(ScalarFormatter())
#     fmt = '{x:,.0f}'
#     tick = mtick.StrMethodFormatter(fmt)
#     ax.xaxis.set_major_formatter(tick) 


    
# plt.legend(loc="lower right")
# plt.show()


# #==============================Part 2 - Question 4 =================================
# #X=confirmedcases_df.transpose()
# cc_df=confirmedcases_df.transpose()
# country_list=confirmedcases_df['CountryName']
# cc_df=cc_df.iloc[2:,]


# #Calcaulte the increase from the previous day select date and average per week
# cc_df.index = pd.to_datetime(cc_df.index)
# cc_df=cc_df.diff(axis=0)
# avg_df=cc_df.loc['2020-03-02':'2020-05-10']
# gr = avg_df.groupby(pd.Grouper(level=0,freq='W'))
# gr_mean =pd.DataFrame([ g.mean() for i,g in gr ])

# #Create a list of the countries with largest values
# largest_ten=gr_mean.max().nlargest(10)
# largest_ten_country_list=country_list[largest_ten.index]

# #Generate the data to plot
# values_of_largest_ten=gr_mean[largest_ten_country_list.index]
# values_of_largest_ten=values_of_largest_ten.transpose()
# values_of_largest_ten.index=largest_ten_country_list
# column_names=(pd.date_range(start='2020-03-02', periods=10, freq='W-MON')).date
# values_of_largest_ten.columns=column_names
# values_of_largest_ten.index.name="Country Name"
# fig = plt.figure(figsize=(18,10), dpi=1600)

# ax = plt.axes()
# ax.set_title('Average new weekly confirmed cases ',fontsize=18)

# sns.heatmap(values_of_largest_ten,cmap="YlOrRd")

# plt.show()
# #==============================Part 2 - Question 5 =================================

# cc_may1_df=confirmedcases_df[['CountryName','01may2020']]
# cc_may1_us=cc_may1_df[cc_may1_df['CountryName'] == 'United States']['01may2020']
# cc_may1_rest=float(cc_may1_df.sum()) - float(cc_may1_us)
# cc_plt=[cc_may1_us,cc_may1_rest]

# cd_may1_df=confirmeddeaths_df[['CountryName','01may2020']]
# cd_may1_us=cd_may1_df[cd_may1_df['CountryName'] == 'United States']['01may2020']
# cd_may1_rest=float(cd_may1_df.sum()) - float(cd_may1_us)
# cd_plt=[cd_may1_us,cd_may1_rest]
# pop_us=328000000
# pop_world=7800000000


# fig = plt.figure(figsize=(14,6),dpi=1200)
# fig.suptitle("US COVID-19 vs Rest of World", fontsize=16)
# ax1 = plt.subplot(131)
# ax2 = plt.subplot(132)
# ax3 = plt.subplot(133)

# percentage = [pop_us,pop_world]
# labels= ['United States','Other']


# ax1 = plt.subplot2grid((1,3),(0,0))
# plt.title('Population')
# explodes = (0.1, 0)
# plt.pie(percentage, explode=explodes, labels=labels, autopct='%1.0f%%',startangle=90,counterclock=False, textprops={'color':"w"})
# legend_values=[]
# legend_values.append(("{:0,.0f}".format(percentage[0])))
# legend_values.append(("{:0,.0f}".format(percentage[1])))
# plt.legend(legend_values,loc="upper center",bbox_to_anchor=(1, 0),fontsize=10)


# ax1 = plt.subplot2grid((1,3),(0,1))
# plt.title('Confirmed Cases')
# explodes = (0.1, 0)
# #ax1.annotate( "Text",horizontalalignment='left',verticalalignment='bottom',xy=(0,0))
# plt.pie(cc_plt, explode=explodes, labels=labels, autopct='%1.0f%%',startangle=90,counterclock=False, 
#        textprops={'color':"w"})

# #plt.subplots_adjust(left=0.1, bottom=0.8, right=0.75)
# legend_values=[]
# legend_values.append(("{:0,.0f}".format(cc_plt[0].values[0])))
# legend_values.append(("{:0,.0f}".format(cc_plt[1])))
# plt.legend(legend_values,loc="upper center",bbox_to_anchor=(1, 0),fontsize=10)

# ax1 = plt.subplot2grid((1,3),(0,2))
# plt.title('Deaths')
# explodes = (0.1, 0)
# plt.pie(cd_plt, explode=explodes, labels=labels, autopct='%1.0f%%',startangle=90,counterclock=False, textprops={'color':"w"})
# legend_values=[]
# legend_values.append(("{:0,.0f}".format(cd_plt[0].values[0])))
# legend_values.append(("{:0,.0f}".format(cd_plt[1])))
# plt.legend(legend_values,loc="upper center",bbox_to_anchor=(1, 0),fontsize=10)

# plt.show()


# # to explode the 4th slice

# # autopct: control the labels inside the wedges
# #plt.pie(percentage, explode=explodes, labels=labels, autopct='%1.0f%%')
# #==============================Part 3 - Question 6 =================================
# cd_uk_df=confirmeddeaths_df[confirmeddeaths_df['CountryName'] == 'United Kingdom']
# cd_uk_df=cd_uk_df.transpose()
# cd_uk_df=cd_uk_df.iloc[2:,]
# start_date='2020-03-07'
# end_date='2020-05-10'

# #x_axis=(pd.date_range(start=start_date, end=end_date, freq='W-SUN')).date

# fig = plt.figure(figsize=(8,8), dpi=1600)
# #Calcaulte the increase from the previous day select date and average per week
# cd_uk_df.index = pd.to_datetime(cd_uk_df.index)
# cd_uk_df=cd_uk_df.loc[start_date:end_date]
# #cc_uk_df=cc_uk_df.diff(axis=0)
# ax=plt.plot(cd_uk_df)
# #ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
# #ax.get_xaxis().get_major_formatter().set_scientific(False)
# #locator = mdate.YearLocator()
# locator = mdate.DayLocator(interval=7)
# plt.gca().xaxis.set_major_locator(locator)
# plt.gcf().autofmt_xdate()
# plt.yscale('log')
# plt.xticks(rotation=90)
    
# plt.title('Confirmed deaths UK between 7th March and 10th May 2020') 
# plt.xlabel("Date")
# plt.ylabel("Confirmed Deaths (logerithmic scale)")
# #plt.ticklabel_format(style='plain')
# ax=plt.gca()
# #plt.ylim(0, 200000)
# plt.yscale("log")
# ax.yaxis.set_major_formatter(ScalarFormatter())
# fmt = '{x:,.0f}'
# tick = mtick.StrMethodFormatter(fmt)
# ax.yaxis.set_major_formatter(tick) 

# plt.show()


# #==============================Part 3 - Question 7 =================================
# country_list=['United Kingdom','Spain','Italy','France','United States']
# #country_list=['United Kingdom']
# #country_list=['South Korea']

# fig = plt.figure(figsize=(18,10), dpi=1600)
# #ndc_df=confirmedcases_df[confirmedcases_df['CountryName'] in country_list]
# ndc_df=confirmedcases_df[confirmedcases_df['CountryName'].isin(country_list)]
# ndc_df=ndc_df.transpose()
# ndc_df.columns=ndc_df.loc['CountryName']
# ndc_df=ndc_df.iloc[2:,]
# start_date='2020-03-01'
# end_date='2020-05-01'
# ndc_df.index = pd.to_datetime(ndc_df.index)
# ndc_df=ndc_df.loc[start_date:end_date]
# ndc_df=ndc_df.diff(axis=0)
# ndc_df.dropna(inplace=True)

# fig, ax = plt.subplots(dpi=1600)
# X=ndc_df.index
# Y_all = pd.DataFrame([ ndc_df[c] for c in country_list ])

# ax.stackplot(X,Y_all)
# fmt = '{x:,.0f}'
# tick = mtick.StrMethodFormatter(fmt)
# ax.yaxis.set_major_formatter(tick) 
# plt.title('New daily cases') 
# ax.legend(Y_all.index,loc='upper left')
# plt.xticks(rotation=90)
# plt.xlabel("Date")
# plt.ylabel("Number of new daily cases)")
# plt.show()

# #==============================Part 3 - Question 8 =================================
# date='04may2020'
# X=confirmedcases_df.set_index('CountryName')
# X=X.iloc[:,1:]
# X=X.transpose()
# X=X.loc[date]
# X=X.dropna()

# Y=stringencyindex_legacy_df.set_index('CountryName')
# Y=Y.iloc[:,1:]
# Y=Y.transpose()
# Y=Y.loc[date]

# Y=Y.dropna()

# fig = plt.figure(dpi=1600)
# ax = plt.gca()
# ax.plot(X,Y, 'o', c='red', alpha=0.4)
# ax.set_xscale('log')
# plt.title("Confirmed cases - all counties - 4th May " )
# plt.xlabel("Confirmed Cases (logerthimic scale)")
# plt.ylabel("Stringency")

# ax=plt.gca()
# #plt.ylim(0, 100)
# #plt.xlim(1, 1000000)
# #plt.xscale("log")

# plt.ylim(0, 100)
# plt.xlim(1, 2000000)
# plt.xscale("log")
# ax.xaxis.set_major_formatter(ScalarFormatter())
# matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ','))
# ax.xaxis.set_major_formatter(ScalarFormatter())
# fmt = '{x:,.0f}'
# tick = mtick.StrMethodFormatter(fmt)
# ax.xaxis.set_major_formatter(tick) 

# plt.show()

# #==============================Part 3 - Question 9 =================================
# #find all counties with over 1000 cases
# countries_over1k=X[X > 1000].index
# X_over1k=X[countries_over1k]
# Y_over1k=Y[countries_over1k]
# f=3000/X_over1k.max()
# S=f*X_over1k
# #Set bubble areas to represent X value
# SA=np.sqrt(X_over1k/math.pi)

# fig = plt.figure(dpi=1600)
# ax = plt.gca()

# #ax.plot(X_over1k,Y_over1k, 'o', c='blue', alpha=0.6, markeredgecolor='black'')
# #ax.scatter(X_over1k,Y_over1k,s=S,alpha=0.6,makeredgecolor='black')


# ax.scatter(X_over1k,Y_over1k,s=SA,alpha=0.6,c='red')

# plt.title("Confirmed cases coutries >1000 4th May" )
# plt.xlabel("Confirmed Cases (Bubble areas=Confirmed cases)")
# plt.ylabel("Stringency")


# plt.ylim(0, 100)
# plt.xlim(1, 2000000)
# plt.xscale("log")
# ax.xaxis.set_major_formatter(ScalarFormatter())
# fmt = '{x:,.0f}'
# tick = mtick.StrMethodFormatter(fmt)
# ax.xaxis.set_major_formatter(tick) 


# plt.show()

