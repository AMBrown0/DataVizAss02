#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 15:15:56 2020

@author: andy
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn
from numpy import median, mean
import json, urllib.request
import sys
from pathlib import Path
from datetime import datetime
import matplotlib.dates as mdate
import plotly.graph_objects as go
import math
import numpy as np
from sklearn.linear_model import LinearRegression
import scipy.stats as stats
from fbprophet import Prophet
import seaborn as sns
from fbprophet.plot import plot_plotly
from scipy.stats import ttest_ind
from dateutil.relativedelta import *
from scipy.stats import ttest_ind
from scipy.stats import chi2_contingency
from dateutil.relativedelta import *
from scipy.stats import normaltest
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs

# =============================================================================
# Global varaibles
# =============================================================================
answer_text_lookup=["a","b","c","d","e","f","g"]
correct_answer=-1


# =============================================================================
# Functions
# =============================================================================
def return_span_text(span_text):
    soup=bs(span_text)
    raw_text=soup.text
    return raw_text
    

    
# # =============================================================================
# # Import Data  
# # =============================================================================
dataFolder=Path(r'.')
filename="questions-Dell-EMC.xml"
dataFile= dataFolder / filename
tree = ET.parse(dataFile)
root = tree.getroot()
for child in root:
    print(child.tag, child.attrib)

all_elements=[elem.tag for elem in root.iter()]
question_count=1
question_text=""
for question in root.iter('question'):
    answer_count=0
    #print("Question %s" %question_count)
    try:
        question_text=question.find('./questiontext/text').text
        raw_question_text=return_span_text(question_text)
    except:
        print("No q text")
        question_text="none"
        #break
    #question.findall('./questiontext/text')[0].text
    if (question_text != "none"):
        print("Q%s %s" %(question_count,raw_question_text))
        for a in question.iter('answer'):
            #Check for correct answer fraction=100
            fraction=a.attrib.get('fraction')
            if (fraction == "100"):
                correct_answer=answer_count            
            answer_letter=answer_text_lookup[answer_count]
            answer_text=a.findall('text')[0].text
            raw_answer_text=return_span_text(answer_text)
            print("    %s) %s" % (answer_letter,raw_answer_text))
            answer_count+=1
        #print(question.attrib)
        question_count+=1
        
    print("Answer:%s\n\n" % answer_text_lookup[correct_answer])
    #response=input("Press enter")

#df = pd.read_excel (dataFile)

# filename="Lapsed Clients - June 20 with CDpw.xlsx"
# dataFile= dataFolder / filename
# clientStickyness_df = pd.read_excel (dataFile)

# #Client Name lookup data
# filename="ClientLookupFinal.xlsx"
# dataFile= dataFolder / filenameues
# clientLookup_df = pd.read_excel (dataFile)



# def update_cd_active_status(row,column_name):
#     if (row[column_name]=="Active"):
#         active_flag=1
#     else:
#         active_flag=0
#     row['active_flag']=active_flag
#     return row

# def update_em_active_status(row,column_name):
#     if (row[column_name]=="Active"):
#         active_flag=1
#     else:
#         active_flag=0
#     row['active_flag']=active_flag
#     return row

# def update_active_status(row,date_lookup_df,new_column_name):    
#     stats_year=row['StartDate'].year
#     #print("Stats Year1=%s" % stats_year )
#     column_to_check=date_lookup_df['column'][date_lookup_df['year'] == stats_year].values[0]
#     active_or_lapsed=row[column_to_check]
#     if (active_or_lapsed == "Active"):
#         active_flag=1
#     else:
#         active_flag=0
    
#     #print("Stats Year=%s,column_to_check=%s,active_or_lasped=%s,active_flag=%s" %(stats_year,column_to_check,active_or_lapsed,active_flag))
#     row[new_column_name]=active_flag
#     return row




# # =============================================================================
# # Genrate t-test stats
# # =============================================================================
# def generate_stats(data_df,grouping_column,scoring_column,significance_threshold):
#     #Remove nulls
#     #data_df[scoring_column]=data_df[scoring_column].notnull()
#     data_df = data_df.dropna(subset=[scoring_column,grouping_column])

#     stat, p = normaltest(data_df[scoring_column])
#     print('Statistics=%.3f, p=%.3f' % (stat, p))
 
        
#     print("Grouping column=%s" % grouping_column)
#     print("scoring_column=%s" % scoring_column)
#     print("Data Print Test=%s" % data_df.iloc[1,5])
    
#     overall_mean=data_df[scoring_column].mean()
#     #print("Overall mean for %s=%s" %(scoring_column,overall_mean))
    
#     data_groups=data_df.groupby(grouping_column)
#     stats_df=pd.DataFrame()

#     for this_group_name,this_group_df in data_groups:
#         #print("Group Name=%s"%this_group_name)
#         t_test=ttest_ind(data_df[scoring_column], this_group_df[scoring_column], nan_policy='omit')
#         if (t_test.pvalue <=p_value_threshold):
#             significant=True
#         else:
#              significant=False
#         effect_size=this_group_df[scoring_column].mean() - overall_mean
             
#         group_stats={grouping_column:this_group_name, 'p_value':t_test.pvalue, 'effect_size':effect_size,'significant':significant}
#         stats_df=stats_df.append(group_stats,ignore_index=True)
#         #print("Goupr=%s,p_value=%s,effect_size=%s, significant=%s" % (this_group_name,t_test.pvalue,effect_size,significant))
    
        
#     stats_df=stats_df.sort_values('effect_size')    
    
#     return stats_df

# def generate_chi2_stats(data_df,group_column):
#     column_group=cs_all.groupby(group_column)
#     chi_df=pd.DataFrame()
    
#     total_active=0
#     total_lapsed=0
    
#     for name,group in column_group:        
#         active_series=group['Account Name'][group['Last 6 months']=='Active']
#         active_count=len(active_series.unique())
#         lapsed_series=group['Account Name'][group['Last 6 months']!='Active']
#         lapsed_count=len(lapsed_series.unique())
#         #print("Group Name=%s,active=%s lapsed=%s" % (name,active_count,lapsed_count))
#         chi_df[name]=[active_count,lapsed_count]
#         #Chi^2 contingency table
#     total_active=total_active+active_count
#     total_lapsed=total_lapsed+lapsed_count
    
#     chi_df.index=['active','lapsed']    
#     chi2=chi2_contingency(chi_df)
#     p_value=chi2[1]
    
#     return chi_df,chi2,p_value
    
# def generate_value_data(row,date_column_list):
#     account_name=row['Account Name']
#     client_director=row['Client Director']
#     value_data_df=pd.DataFrame()
#     values=row[date_column_list]
#     value_data_df['values']=values
#     value_data_df['Account Name']=account_name
#     value_data_df['Client Director']=client_director
    
#     #print(value_data_df)
#     return value_data_df
    
    
# # =============================================================================
# # Import Data  
# # =============================================================================
# dataFolder=Path(r'.')
# filename="Copy of All Clients L1 data 1 Jan 2016 to 31 July 2020.xlsx"
# dataFile= dataFolder / filename
# df = pd.read_excel (dataFile)

# filename="Lapsed Clients - June 20 with CDpw.xlsx"
# dataFile= dataFolder / filename
# clientStickyness_df = pd.read_excel (dataFile)

# #Client Name lookup data
# filename="ClientLookupFinal.xlsx"
# dataFile= dataFolder / filename
# clientLookup_df = pd.read_excel (dataFile)

# # =============================================================================
# # Setup statisics output file  
# # =============================================================================
# #Stats output
# filename="stats.csv"
# dataFileOut= dataFolder / filename

# # =============================================================================
# # Merge the data
# # =============================================================================
# #Create lookup for retention data (last 6 months, last 12 months, 2019) and actual stats date range
# data_gen_date=datetime.strptime("25-07-2020","%d-%m-%Y")
# date_6months_ago = data_gen_date + relativedelta(months=-6)
# date_12months_ago = data_gen_date + relativedelta(months=-12)
# date_2019_start=datetime.strptime("01-01-2019","%d-%m-%Y")
# date_2019_end=datetime.strptime("31-12-2019","%d-%m-%Y")
# date_2018_start=datetime.strptime("01-01-2018","%d-%m-%Y")
# date_2018_end=datetime.strptime("31-12-2018","%d-%m-%Y")
# date_2017_start=datetime.strptime("01-01-2017","%d-%m-%Y")
# date_2017_end=datetime.strptime("31-12-2017","%d-%m-%Y")
# date_2016_start=datetime.strptime("01-01-2016","%d-%m-%Y")
# date_2016_end=datetime.strptime("31-12-2016","%d-%m-%Y")

# # date_column_lookup=[{"year":2020,"column":"Last 6 months","startdate":date_6months_ago,"enddate":data_gen_date},
# #                     {"year":2019,"column":"Last 12 months","startdate":date_12months_ago,"enddate":data_gen_date},
# #                     {"year":2019,"column":2019,"startdate":date_2019_start,"enddate":date_2019_end},
# #                     {"year":2019,"column":2018,"startdate":date_2018_start,"enddate":date_2018_end},
# #                     {"year":2019,"column":2017,"startdate":date_2017_start,"enddate":date_2017_end}

# # ]

# date_column_lookup=[{"year":2020,"column":"Last 6 months","startdate":date_6months_ago,"enddate":data_gen_date},                    
#                     {"year":2019,"column":"Last 6 months","startdate":date_2019_start,"enddate":date_2019_end},
#                     {"year":2018,"column":2019,"startdate":date_2018_start,"enddate":date_2018_end},
#                     {"year":2017,"column":2018,"startdate":date_2017_start,"enddate":date_2017_end},
#                     {"year":2016,"column":2017,"startdate":date_2016_start,"enddate":date_2016_end}

# ]
# date_column_lookup_df=pd.DataFrame(date_column_lookup)




# cs_stats=pd.DataFrame()

# clientStickyness_df.rename(columns={"Account Name  ↑":'Account Name'},inplace=True)

# #Select only rows where client in client lookup
# clientStickyness_sel_df=clientStickyness_df[clientStickyness_df['Account Name'].isin(clientLookup_df['Account Name'])]
# sel_df=df[ df['Client'].isin(clientLookup_df['Lookup'])]
# all_data=pd.merge(sel_df, clientLookup_df, left_on='Client', right_on='Lookup')

# #Convert date string to datetime


# #Select only rows where client in client lookup
# clientStickyness_sel_df=clientStickyness_df[clientStickyness_df['Account Name'].isin(clientLookup_df['Account Name'])]
# cs_withlookup=pd.merge(clientStickyness_sel_df, clientLookup_df, left_on='Account Name', right_on='Account Name')
# cs_all=pd.merge(cs_withlookup, df, left_on='Lookup', right_on='Client')

# #Convert StartDate to datetime 
# cs_all['StartDate']=pd.to_datetime(cs_all['StartDate'])

# #Add column active=1 not active=0
# #2017 scores assumed to effect 2018 Lapsed/Active
# #2018 scores assumed to effect 2010 Lapsed/Active
# cs_all=cs_all.apply(lambda row: update_active_status(row,date_column_lookup_df,'active_flag'),axis=1)


# #Add a column containing the year extracted from teh StartDate
# all_data_year = [ row.year for row in cs_all['StartDate'] ]
# cs_all['year']=all_data_year

# # =============================================================================
# # Heatmap of correlation 
# # =============================================================================
# # Correlation columns
# correlaton_columns=[
                                 
#                                     'Satisfaction',
#                                'ManagerDiscussion',
#                                'CareerDevelopment',
#                                 'ContentRelevance',
#                           'NewSkillsApplicability',
#                             'NewSkillsAcquisition',
#                            'ImproveJobPerformance',
#                                'PreWorkEnablement',
#                                'WorkshopStructure',
#                              'SufficientExercises',
#                            'SufficientSubjectTime',
#                              'TheoryApplicability',
#                           'InteractionImprovement',
#                         'FacilitationSatisfaction',
#                                    'TheoryClarity',
#                                       'Supportive',
#                              'AnswerAcceptability',
#                          'FacilitatorAvailability',
#                                              'NPS',
#                      'ProgrammeComparableToOthers',
#                            'DifficultyOfProgramme',
#                                'ImpactOfProgramme',
#    'NoForeseeableOpportunityToUseTheContentSkills',
#            'PreventedOrDiscouragedFromApplication',
#    'ContentNotRelevantToMyCurrentPositionRoleSoWillNotImp',
#      'MyIncompleteUnderstandingOfTheSkillsLearned',
#                            'OtherHigherPriorities',
#              'LackOfInternalSupportForTheTraining'                                   
#                       ]



# reactionary_df=cs_all[correlaton_columns]
# corrMatrix = reactionary_df.corr()

# #Plot corelation matrix
# fig, ax = plt.subplots(figsize=(20,20))
# svm = sn.heatmap(corrMatrix, annot=True,fmt='.2f')
# sv_figure = svm.get_figure() 

# ax.set_title('Attendee survey corelation',fontsize=18)
# sv_figure.savefig("fig1.png")
# plt.show()



# # =============================================================================
# # Calculate facilitator stats based on the merged data
# # =============================================================================
# p_value_threshold=0.05
# #facilitator_stats_df=generate_stats(cs_all,"Facilitator","Satisfaction",p_value_threshold)
# facilitator_stats_df=generate_stats(cs_all,"Facilitator","NPS",p_value_threshold)
# print(facilitator_stats_df)

# fac_best_df=facilitator_stats_df.tail(10)
# print(fac_best_df)
# fac_worst_df=facilitator_stats_df.head(10)
# #facilitator_stats_df=pd.DataFrame()
# print(fac_worst_df)

# # =============================================================================
# # Calculate satisfaction against active/not active
# # =============================================================================
# active_stats_df=generate_stats(cs_all,"active_flag","NPS",p_value_threshold)
# print("Lapsed Account Related to NPS p_value 0.05>%s" % (active_stats_df.loc[0].p_value))
# print("Active Account Related to NPS p_value 0.05>%s" % (active_stats_df.loc[1].p_value))
# #print(active_stats_df)
# cd_stats_df=generate_stats(cs_all,"Client Director","Satisfaction",p_value_threshold)
# #print(cd_stats_df)
# em_stats_df=generate_stats(cs_all,"EM","Satisfaction",p_value_threshold)
# #print(em_stats_df)
# facilitator_sat_stats_df=generate_stats(cs_all,"Facilitator","Satisfaction",p_value_threshold)
# #print(facilitator_sat_stats_df)

# # =============================================================================
# # Plot best and worst facilitators by NPS 
# # =============================================================================
# fig = plt.figure(figsize=(12,10), dpi=800)
# plt.title('Best Performing Facilitators',fontsize=18) 
# plt.xlabel("Facilitator",fontsize=16)
# plt.ylabel("Effect size",fontsize=16)
# plt.xticks(rotation=90)
# plt.bar(fac_best_df.Facilitator,fac_best_df.effect_size)
# fig.savefig("fig2.png")
# plt.show()



# fig = plt.figure(figsize=(12,10), dpi=800)
# plt.title('Worst Performing Facilitators',fontsize=18) 
# plt.xlabel("Facilitator",fontsize=16)
# plt.ylabel("Effect size",fontsize=16)
# plt.xticks(rotation=90)
# plt.bar(fac_worst_df.Facilitator,fac_worst_df.effect_size)
# fig.savefig("fig3.png")
# plt.show()

 

# # =============================================================================
# # Box plot all faciliator NPS scores ordered by mean
# # =============================================================================
# #Box plot instructor
# box_df=pd.DataFrame()
# for f in facilitator_stats_df.Facilitator:
#     box_df=box_df.append(cs_all[cs_all['Facilitator']==f])
#     #print(f)
# fig1=plt.figure(figsize=(20,30))
# ax=sns.boxplot(x=box_df['NPS'],y=box_df['Facilitator'])
# fig1.savefig("fig4.png")
# plt.show()

# # =============================================================================
# # Volin plot of the best and worst 
# # =============================================================================
# violin_df=pd.DataFrame()
# worst_best_df=fac_worst_df.append(fac_best_df)
# for f in worst_best_df.Facilitator:
#     violin_df=violin_df.append(cs_all[cs_all['Facilitator']==f])
#     #print(f)


# fig1=plt.figure(figsize=(20,30))
# ax = sns.violinplot(x=violin_df['NPS'],y=violin_df.Facilitator,width=1,color="green")
# # Add labels
# plt.title('NPS distibution for best and worst facilitators',size=24)
# plt.ylabel("NPS",size=20);
# plt.yticks(fontsize=20)
# fig1.savefig("fig5.png")
# plt.show()
# # =============================================================================
# # Volin plot of the all
# # =============================================================================
# violin_df=pd.DataFrame()
# all_facilitators_series=facilitator_stats_df.Facilitator.unique()


# for f in all_facilitators_series:
#     violin_df=violin_df.append(cs_all[cs_all['Facilitator']==f])
#     #print(f)
 

# fig1=plt.figure(figsize=(20,60))
# ax = sns.violinplot(x=violin_df['NPS'],y=violin_df.Facilitator,width=1,color="green")
# # Add labels
# plt.title('NPS distibution for all facilitators',size=24)
# plt.ylabel("NPS",size=20);
# plt.yticks(fontsize=20)
# fig1.savefig("fig6.png")
# plt.show()


# # =============================================================================
# # Calculate mean for lapsed/active accounts 
# # =============================================================================
# #retention_stats_df=generate_stats(cs_all,"active_flag","NPS",p_value_threshold)
# #Box plot instructor
# box_df=pd.DataFrame()
# for active_flag_value in [0,1]:
#     box_df=box_df.append(cs_all[cs_all['active_flag']==active_flag_value])
#     #print(active_flag_value)
# fig1=plt.figure(figsize=(20,20))
# box_df['active_flag'].loc[box_df['active_flag'] == 0] = "Lapsed"
# box_df['active_flag'].loc[box_df['active_flag'] == 1] = "Active"
# ax=sns.boxplot(x=box_df['NPS'],y=box_df['active_flag'])
# fig1.savefig("fig7.png")
# plt.show()

# # =============================================================================
# # Updated Calculate and plot retension 
# # =============================================================================
# p_value_threshold=0.05
# all_data=cs_all.dropna(axis=0, subset=['year'])
# overall_mean_NPS=all_data['NPS'].mean()
# overall_mean_satisfacion=all_data['Satisfaction'].mean()
# cs_stats=pd.DataFrame()
# lapsed_df=pd.DataFrame()
# active_df=pd.DataFrame()
# all_data_group=all_data.groupby(["Account Name","year"])
# for name,group in all_data_group:
#     account=name[0]
#     year=name[1]
#     column_with_active_status=date_column_lookup_df[date_column_lookup_df['year'] == year].column.values[0]
#     active_status=group[column_with_active_status].values[0]
#     if (active_status == "Active"):
#         logic_active=True
#         retention="Active"
#         active_df=active_df.append(group)
#     else:   
#         logic_active=False
#         retention="Lapsed"
#         lapsed_df=lapsed_df.append(group)
    
#     #print("Account=%s,year=%s,column_with_active_status=%s,status=%s,logic=%s" % (account,year,column_with_active_status,active_status,logic_active))
    
#     #Create stats for this group 
#     mean_statisfaction=group['Satisfaction'].mean()
#     mean_NPS=group['NPS'].mean()
#     mean_fac_satisfaction=group['FacilitationSatisfaction'].mean()

#     all_data_nonulls=all_data[all_data['NPS'].notnull()]
#     t_test_NPS=ttest_ind(all_data_nonulls['NPS'], group['NPS'])
        
#     p_value=t_test_NPS.pvalue
#     if (p_value <= sig):
#         significantNPS="Y"
#     else:
#         significantNPS="N"
        
#     effectsize_NPS=mean_NPS-overall_mean_NPS
#     effectsize_satisfaction= overall_mean_satisfacion - mean_statisfaction
    
    
#     data={"Account Name":name,"retentionTF":logic_active,"Mean_Satisfaction":mean_statisfaction,
#           "effectsize_satisfaction":effectsize_satisfaction,"Mean_NPS":mean_NPS,
#           "effectsize_NPS":effectsize_NPS,"p_value":p_value,"SignificantNPS":significantNPS,
#           "mean_fac_satisfaction":mean_fac_satisfaction,"Active":retention}    
    
#     cs_stats=cs_stats.append(data,ignore_index=True)
    

# corrMatrix = cs_stats[["retentionTF","Mean_Satisfaction","effectsize_satisfaction","Mean_NPS","effectsize_NPS"]].corr()
# #Plot corelation matrix
# fig, ax = plt.subplots(figsize=(10,10))
# svm=sn.heatmap(corrMatrix, annot=True)
# sv_figure = svm.get_figure()    
# sv_figure.savefig("fig8.png")
# plt.show()


# active_nonull_df=active_df[active_df['NPS'].notnull()]
# lapsed_nonull_df=lapsed_df[lapsed_df['NPS'].notnull()]

# t_test_NPS=ttest_ind(active_nonull_df['NPS'], lapsed_nonull_df['NPS'])
# p_value=t_test_NPS.pvalue
# if (p_value <= sig):
#     significantNPS="Y"
# else:
#     significantNPS="N"
        

    
# effectsize_NPS=active_nonull_df['NPS'].mean() - lapsed_nonull_df['NPS'].mean()
#     #effectsize_satisfaction= overall_mean_satisfacion - mean_statisfaction
# # =============================================================================
# # Calculate if NPS has an effect on active/lapsed accounts
# # =============================================================================
# print("Active-Lapsed NPS Effect Size=%s significance=%s" %(effectsize_NPS,p_value))


# #Plot satisfaction/retained

# plt.scatter(cs_stats['Active'],cs_stats["Mean_Satisfaction"])
# plt.title('Mean satisfaction for company and year',fontsize=14) 
# plt.xlabel("Account Active/Lapsed/Null")
# plt.ylabel("Mean statisfation")
# plt.savefig("fig9.png")
# plt.show()

# #Plot NPS/retained

# plt.scatter(cs_stats['Active'],cs_stats["Mean_NPS"])
# plt.title('Mean NPS for company and year',fontsize=14) 
# plt.xlabel("Account Active/Lapsed/Null")
# plt.ylabel("Mean NP")
# plt.savefig("fig10.png")
# plt.show()


# plt.scatter(cs_stats['Active'],cs_stats["mean_fac_satisfaction"])
# plt.title('Mean Facilitator_satisfaction for company and year',fontsize=14) 
# plt.xlabel("Account Active/Lapsed/Null")
# plt.ylabel("Mean Facilitator")
# plt.savefig("fig11.png")
# plt.show()
# #Merge retention and facilitation data
# #all_data_ret_and_feedback=pd.merge(all_data, all_data, left_on='Client', right_on='Lookup')
# cs_stats.to_csv(dataFileOut)

# # =============================================================================
# # Calculate Chi2 and plot lapsed/active accounts by EM, Client Director, Facilitator
# # =============================================================================
# fig = plt.figure()
# chi_EM_df,chi_EM,p_value=generate_chi2_stats(cs_all,"EM")
# chi_EM_df_T=chi_EM_df.T
# chi_EM_df_T.plot(kind='bar', stacked=True,title="Active/Lapsed account by engagement manager")
# plt.subplots_adjust(bottom=0.4)
# plt.savefig("fig12.png")
# print("EM Makes impact: if 0.05>%s" %p_value)
# print("Chi2")
# print(chi_EM)

# chi_F_df,chi_F,p_value=generate_chi2_stats(cs_all,"Facilitator")
# p_value=chi_F[1]
# chi_F_df_T=chi_F_df.T
# chi_F_df_T.plot.barh(stacked=True,title="Active/Lapsed account by facilitator",figsize=(20,30))
# plt.savefig("fig13.png")
# print("Facilitator Makes impact: if 0.05>%s" %p_value)
# print("Chi2")
# print(chi_F)   

# chi_CD_df,chi_CD,p_value=generate_chi2_stats(cs_all,"Client Director")
# chi_CD_df_T=chi_CD_df.T
# chi_CD_df_T.plot.barh(stacked=True,title="Active/Lapsed account by Client Director",figsize=(20,30))
# plt.savefig("fig14.png")
# print("Client Director Makes impact: if 0.05>%s" %p_value)
# print("Chi2")
# print(chi_CD)   
 

# #cs_all['Total']
# # Re-read the lapsed client list so that those not in the lookuplist get included for these calcs
# cs_cd_stats=clientStickyness_df
# cs_cd_stats=cs_cd_stats.apply(lambda row: update_cd_active_status(row,"Last 6 months"),axis=1)


# client_director_group=cs_cd_stats.groupby(["Client Director","Account Name"])

# active_lapsed_cd_totals_df=pd.DataFrame()

# for group_names,this_group_df in client_director_group:
#     cd=group_names[0]
#     an=group_names[1]
#     total_this_group=this_group_df['Total'].values[0]
#     active=this_group_df['active_flag'].values[0]
#     data={"Client Director":cd,"Account Name":an,"Total":total_this_group,"active_flag":active}
#     active_lapsed_cd_totals_df=active_lapsed_cd_totals_df.append(data,ignore_index=True)
#     print("Clinet Director=%s account name=%s active=%s" % (cd,an,active))
    
# # Calculate total active total lapsed count and values
# client_directory_totals_df=pd.DataFrame()
# client_director_totals_group=active_lapsed_cd_totals_df.groupby(["Client Director","active_flag"])

# for group_names,this_group_df in client_director_totals_group:
#     cd=group_names[0]
#     af=group_names[1]
#     overall_total=this_group_df['Total'].sum()
#     overall_total_count=len(this_group_df)
#     data={"Client Director":cd,"active_flag":af,"Total Value":overall_total,"Total Count":overall_total_count}
#     client_directory_totals_df=client_directory_totals_df.append(data,ignore_index=True)
#     #print(data)
    

# #Cacluate % count and value
# client_director_pc_df=pd.DataFrame()
# client_director_totals_group=client_directory_totals_df.groupby(["Client Director"])
# for group_name,this_group_df in client_director_totals_group:                                                     
#     cd=group_name

#     # Exact active and lapsed value        
#     active_len=len(this_group_df[this_group_df['active_flag'] == 1] )
#     #print("active_len=%s" %active_len) 
#     if (active_len >0):
#         active_value=this_group_df[this_group_df['active_flag'] == 1]['Total Value'].values[0]
#         active_count=this_group_df[this_group_df['active_flag'] == 1]['Total Count'].values[0]
#     else: 
#         active_value=0
#         active_count=0
        
        
#     lapsed_len=len(this_group_df[this_group_df['active_flag'] == 0] )
#     #print("lapsed_len=%s" %lapsed_len) 
#     if (lapsed_len >0):
#         lapsed_value=this_group_df[this_group_df['active_flag'] == 0]['Total Value'].values[0]
#         lapsed_count=this_group_df[this_group_df['active_flag'] == 0]['Total Count'].values[0]
#     else: 
#         #print("Lapsed setting to 0 for %s" % cd)
#         lapsed_value=0
#         lapsed_count=0

#     acitve_value_pc=active_value / (active_value + lapsed_value ) * 100
#     lapsed_value_pc=lapsed_value / (active_value + lapsed_value ) * 100

#     acitve_count_pc=active_count / (active_count + lapsed_count ) * 100
#     lapsed_count_pc=lapsed_count / (active_count + lapsed_count ) * 100


        
#     data={"Client Director":cd,
#           "active_total_value":active_value,"lapsed_total_value":lapsed_value,
#           "active_count":active_count,"lapsed_count":lapsed_count,
#           "active_value_pc":acitve_value_pc,"lapsed_value_pc":lapsed_value_pc,
#           "acitve_count_pc":acitve_count_pc,"lapsed_count_pc":lapsed_count_pc
#           }
#     client_director_pc_df=client_director_pc_df.append(data,ignore_index=True)
#     print("Client Diretcor=%s,Active_value=%s Lasped_value=%s active_value_pc=%s lapsed_value_pc=%s" %(cd,active_value,lapsed_value,acitve_value_pc,lapsed_value_pc))


# #Plot active/lapsed % 
# client_director_pc_df.set_index('Client Director',inplace=True)

# client_director_pc_count_plot_df=client_director_pc_df[['acitve_count_pc','lapsed_count_pc']]
# client_director_pc_count_plot_df=client_director_pc_count_plot_df.sort_values('lapsed_count_pc')    


# #client_director_pc_count_plot_df.plot.barh(stacked=True,title="Active/Lapsed count % by Client Director",figsize=(20,30),fontsize=14)
# #fig = plt.figure()
# #fig.suptitle("Active/Lapsed count % by Client Director", fontsize=50) 

# ax=client_director_pc_count_plot_df.plot.barh(stacked=True,title="lapsed account count by Client Director (%)",figsize=(20,30),fontsize= 14)
# ax.set_title('Lapsed account count by Client Director (%)',fontsize= 35,fontweight="bold") 
# for p in ax.patches:
#     left, bottom, width, height = p.get_bbox().bounds
#     if (width != 0):        
#         number_text="{:.0f}".format(width)
#     else:
#         number_text=""
#     ax.annotate(number_text, xy=(left+width/2, bottom+height/2), 
#                 ha='center', va='center',fontweight="bold")
# lgd = ax.legend(loc=9, bbox_to_anchor=(0.5,-0.02))
# plt.savefig("fig15.png")



# client_director_pc_value_plot_df=client_director_pc_df[['active_value_pc','lapsed_value_pc']]
# client_director_pc_value_plot_df=client_director_pc_value_plot_df.sort_values('lapsed_value_pc')   
# ax=client_director_pc_value_plot_df.plot.barh(stacked=True,figsize=(20,30),fontsize= 14)
# ax.set_title('Lapsed account value by Client Director (%)',fontsize= 35,fontweight="bold") 
# for p in ax.patches:
#     left, bottom, width, height = p.get_bbox().bounds
#     if (width != 0):        
#         number_text="{:.1f}".format(width)
#     else:
#         number_text=""
#     ax.annotate(number_text, xy=(left+width/2, bottom+height/2), 
#                 ha='center', va='center',fontweight="bold")
# lgd = ax.legend(loc=9, bbox_to_anchor=(0.5,-0.02))
# plt.savefig("fig16.png")


# #cs_all['Total']
# # Re-read the lapsed client list so that those not in the lookuplist get included for these calcs
# cs_em_stats=cs_all
# cs_em_stats=cs_em_stats.apply(lambda row: update_em_active_status(row,"Last 6 months"),axis=1)




# em_group=cs_em_stats.groupby(["EM","Account Name"])

# active_lapsed_em_totals_df=pd.DataFrame()

# for group_names,this_group_df in em_group:
#     em=group_names[0]
#     an=group_names[1]
#     total_this_group=this_group_df['Total'].values[0]
#     active=this_group_df['active_flag'].values[0]
#     data={"Engagement Manager":em,"Account Name":an,"Total":total_this_group,"active_flag":active}
#     active_lapsed_em_totals_df=active_lapsed_em_totals_df.append(data,ignore_index=True)
#     print("Engamement Mananger=%s account name=%s active=%s" % (em,an,active))
    
# # Calculate total active total lapsed count and values
# em_totals_df=pd.DataFrame()
# em_totals_group=active_lapsed_em_totals_df.groupby(["Engagement Manager","active_flag"])

# for group_names,this_group_df in em_totals_group:
#     em=group_names[0]
#     af=group_names[1]
#     overall_total=this_group_df['Total'].sum()
#     overall_total_count=len(this_group_df)
#     data={"Engagement Manager":em,"active_flag":af,"Total Value":overall_total,"Total Count":overall_total_count}
#     em_totals_df=em_totals_df.append(data,ignore_index=True)
#     #print(data)
    

# #Cacluate % count and value
# em_pc_df=pd.DataFrame()
# em_totals_group=em_totals_df.groupby(["Engagement Manager"])
# for group_name,this_group_df in em_totals_group:                                                     
#     em=group_name
#     print("Engagement Manager=%s" % em)
#     # Exact active and lapsed value        
#     active_len=len(this_group_df[this_group_df['active_flag'] == 1] )
#     #print("active_len=%s" %active_len) 
#     if (active_len >0):
#         active_value=this_group_df[this_group_df['active_flag'] == 1]['Total Value'].values[0]
#         active_count=this_group_df[this_group_df['active_flag'] == 1]['Total Count'].values[0]
#     else: 
#         active_value=0
#         active_count=0
        
        
#     lapsed_len=len(this_group_df[this_group_df['active_flag'] == 0] )
#     #print("lapsed_len=%s" %lapsed_len) 
#     if (lapsed_len >0):
#         lapsed_value=this_group_df[this_group_df['active_flag'] == 0]['Total Value'].values[0]
#         lapsed_count=this_group_df[this_group_df['active_flag'] == 0]['Total Count'].values[0]
#     else: 
#         #print("Lapsed setting to 0 for %s" % cd)
#         lapsed_value=0
#         lapsed_count=0

#     acitve_value_pc=active_value / (active_value + lapsed_value ) * 100
#     lapsed_value_pc=lapsed_value / (active_value + lapsed_value ) * 100

#     acitve_count_pc=active_count / (active_count + lapsed_count ) * 100
#     lapsed_count_pc=lapsed_count / (active_count + lapsed_count ) * 100


        
#     data={"Engagement Manager":em,
#           "active_total_value":active_value,"lapsed_total_value":lapsed_value,
#           "active_count":active_count,"lapsed_count":lapsed_count,
#           "active_value_pc":acitve_value_pc,"lapsed_value_pc":lapsed_value_pc,
#           "acitve_count_pc":acitve_count_pc,"lapsed_count_pc":lapsed_count_pc
#           }
#     em_pc_df=em_pc_df.append(data,ignore_index=True)
#     print("Engagement Manager=%s,Active_value=%s Lasped_value=%s active_value_pc=%s lapsed_value_pc=%s" %(em,active_value,lapsed_value,acitve_value_pc,lapsed_value_pc))


# #Plot active/lapsed % 
# em_pc_df.set_index('Engagement Manager',inplace=True)

# em_pc_count_plot_df=em_pc_df[['acitve_count_pc','lapsed_count_pc']]
# em_pc_count_plot_df=em_pc_count_plot_df.sort_values('lapsed_count_pc')    


# #client_director_pc_count_plot_df.plot.barh(stacked=True,title="Active/Lapsed count % by Client Director",figsize=(20,30),fontsize=14)
# #fig = plt.figure()
# #fig.suptitle("Active/Lapsed count % by Client Director", fontsize=50) 

# ax=em_pc_count_plot_df.plot.barh(stacked=True,title="lapsed account count by Engagement Manager (%)",figsize=(20,30),fontsize= 14)
# ax.set_title('Lapsed account count by Engagement Manager (%)',fontsize= 35,fontweight="bold") 
# for p in ax.patches:
#     left, bottom, width, height = p.get_bbox().bounds
#     if (width != 0):        
#         number_text="{:.0f}".format(width)
#     else:
#         number_text=""
#     ax.annotate(number_text, xy=(left+width/2, bottom+height/2), 
#                 ha='center', va='center',fontweight="bold")
# lgd = ax.legend(loc=9, bbox_to_anchor=(0.5,-0.02))
# plt.savefig("fig15a.png")


# em_pc_value_plot_df=em_pc_df[['active_value_pc','lapsed_value_pc']]
# em_pc_value_plot_df=em_pc_value_plot_df.sort_values('lapsed_value_pc')   
# ax=em_pc_value_plot_df.plot.barh(stacked=True,figsize=(20,30),fontsize= 14)
# ax.set_title('Lapsed account value by Engagement Manager (%)',fontsize= 35,fontweight="bold") 
# for p in ax.patches:
#     left, bottom, width, height = p.get_bbox().bounds
#     if (width != 0):        
#         number_text="{:.1f}".format(width)
#     else:
#         number_text=""
#     ax.annotate(number_text, xy=(left+width/2, bottom+height/2), 
#                 ha='center', va='center',fontweight="bold")
# lgd = ax.legend(loc=9, bbox_to_anchor=(0.5,-0.02))
# plt.savefig("fig16a.png")


# cs_em_stats=cs_all
# cs_em_stats=cs_em_stats.apply(lambda row: update_em_active_status(row,2019),axis=1)




# em_group=cs_em_stats.groupby(["EM","Account Name"])

# active_lapsed_em_totals_df=pd.DataFrame()

# for group_names,this_group_df in em_group:
#     em=group_names[0]
#     an=group_names[1]
#     total_this_group=this_group_df['Total'].values[0]
#     active=this_group_df['active_flag'].values[0]
#     data={"Engagement Manager":em,"Account Name":an,"Total":total_this_group,"active_flag":active}
#     active_lapsed_em_totals_df=active_lapsed_em_totals_df.append(data,ignore_index=True)
#     print("Engamement Mananger=%s account name=%s active=%s" % (em,an,active))
    
# # Calculate total active total lapsed count and values
# em_totals_df=pd.DataFrame()
# em_totals_group=active_lapsed_em_totals_df.groupby(["Engagement Manager","active_flag"])

# for group_names,this_group_df in em_totals_group:
#     em=group_names[0]
#     af=group_names[1]
#     overall_total=this_group_df['Total'].sum()
#     overall_total_count=len(this_group_df)
#     data={"Engagement Manager":em,"active_flag":af,"Total Value":overall_total,"Total Count":overall_total_count}
#     em_totals_df=em_totals_df.append(data,ignore_index=True)
#     #print(data)
    

# #Cacluate % count and value
# em_pc_df=pd.DataFrame()
# em_totals_group=em_totals_df.groupby(["Engagement Manager"])
# for group_name,this_group_df in em_totals_group:                                                     
#     em=group_name
#     print("Engagement Manager=%s" % em)
#     # Exact active and lapsed value        
#     active_len=len(this_group_df[this_group_df['active_flag'] == 1] )
#     #print("active_len=%s" %active_len) 
#     if (active_len >0):
#         active_value=this_group_df[this_group_df['active_flag'] == 1]['Total Value'].values[0]
#         active_count=this_group_df[this_group_df['active_flag'] == 1]['Total Count'].values[0]
#     else: 
#         active_value=0
#         active_count=0
        
        
#     lapsed_len=len(this_group_df[this_group_df['active_flag'] == 0] )
#     #print("lapsed_len=%s" %lapsed_len) 
#     if (lapsed_len >0):
#         lapsed_value=this_group_df[this_group_df['active_flag'] == 0]['Total Value'].values[0]
#         lapsed_count=this_group_df[this_group_df['active_flag'] == 0]['Total Count'].values[0]
#     else: 
#         #print("Lapsed setting to 0 for %s" % cd)
#         lapsed_value=0
#         lapsed_count=0

#     acitve_value_pc=active_value / (active_value + lapsed_value ) * 100
#     lapsed_value_pc=lapsed_value / (active_value + lapsed_value ) * 100

#     acitve_count_pc=active_count / (active_count + lapsed_count ) * 100
#     lapsed_count_pc=lapsed_count / (active_count + lapsed_count ) * 100


        
#     data={"Engagement Manager":em,
#           "active_total_value":active_value,"lapsed_total_value":lapsed_value,
#           "active_count":active_count,"lapsed_count":lapsed_count,
#           "active_value_pc":acitve_value_pc,"lapsed_value_pc":lapsed_value_pc,
#           "acitve_count_pc":acitve_count_pc,"lapsed_count_pc":lapsed_count_pc
#           }
#     em_pc_df=em_pc_df.append(data,ignore_index=True)
#     print("Engagement Manager=%s,Active_value=%s Lasped_value=%s active_value_pc=%s lapsed_value_pc=%s" %(em,active_value,lapsed_value,acitve_value_pc,lapsed_value_pc))


# #Plot active/lapsed % 
# em_pc_df.set_index('Engagement Manager',inplace=True)

# em_pc_count_plot_df=em_pc_df[['acitve_count_pc','lapsed_count_pc']]
# em_pc_count_plot_df=em_pc_count_plot_df.sort_values('lapsed_count_pc')    


# #client_director_pc_count_plot_df.plot.barh(stacked=True,title="Active/Lapsed count % by Client Director",figsize=(20,30),fontsize=14)
# #fig = plt.figure()
# #fig.suptitle("Active/Lapsed count % by Client Director", fontsize=50) 

# ax=em_pc_count_plot_df.plot.barh(stacked=True,title="lapsed account count by Engagement Manager (%)",figsize=(20,30),fontsize= 14)
# ax.set_title('Lapsed account count by Engagement Manager 2019 (%)',fontsize= 35,fontweight="bold") 
# for p in ax.patches:
#     left, bottom, width, height = p.get_bbox().bounds
#     if (width != 0):        
#         number_text="{:.0f}".format(width)
#     else:
#         number_text=""
#     ax.annotate(number_text, xy=(left+width/2, bottom+height/2), 
#                 ha='center', va='center',fontweight="bold")
# lgd = ax.legend(loc=9, bbox_to_anchor=(0.5,-0.02))
# plt.savefig("fig15b.png")


# em_pc_value_plot_df=em_pc_df[['active_value_pc','lapsed_value_pc']]
# em_pc_value_plot_df=em_pc_value_plot_df.sort_values('lapsed_value_pc')   
# ax=em_pc_value_plot_df.plot.barh(stacked=True,figsize=(20,30),fontsize= 14)
# ax.set_title('Lapsed account value by Engagement Manager 2019 (%)',fontsize= 35,fontweight="bold") 
# for p in ax.patches:
#     left, bottom, width, height = p.get_bbox().bounds
#     if (width != 0):        
#         number_text="{:.1f}".format(width)
#     else:
#         number_text=""
#     ax.annotate(number_text, xy=(left+width/2, bottom+height/2), 
#                 ha='center', va='center',fontweight="bold")
# lgd = ax.legend(loc=9, bbox_to_anchor=(0.5,-0.02))
# plt.savefig("fig16b.png")

# cs_em_stats=cs_all
# cs_em_stats=cs_em_stats.apply(lambda row: update_em_active_status(row,2018),axis=1)




# em_group=cs_em_stats.groupby(["EM","Account Name"])

# active_lapsed_em_totals_df=pd.DataFrame()

# for group_names,this_group_df in em_group:
#     em=group_names[0]
#     an=group_names[1]
#     total_this_group=this_group_df['Total'].values[0]
#     active=this_group_df['active_flag'].values[0]
#     data={"Engagement Manager":em,"Account Name":an,"Total":total_this_group,"active_flag":active}
#     active_lapsed_em_totals_df=active_lapsed_em_totals_df.append(data,ignore_index=True)
#     print("Engamement Mananger=%s account name=%s active=%s" % (em,an,active))
    
# # Calculate total active total lapsed count and values
# em_totals_df=pd.DataFrame()
# em_totals_group=active_lapsed_em_totals_df.groupby(["Engagement Manager","active_flag"])

# for group_names,this_group_df in em_totals_group:
#     em=group_names[0]
#     af=group_names[1]
#     overall_total=this_group_df['Total'].sum()
#     overall_total_count=len(this_group_df)
#     data={"Engagement Manager":em,"active_flag":af,"Total Value":overall_total,"Total Count":overall_total_count}
#     em_totals_df=em_totals_df.append(data,ignore_index=True)
#     #print(data)
    

# #Cacluate % count and value
# em_pc_df=pd.DataFrame()
# em_totals_group=em_totals_df.groupby(["Engagement Manager"])
# for group_name,this_group_df in em_totals_group:                                                     
#     em=group_name
#     print("Engagement Manager=%s" % em)
#     # Exact active and lapsed value        
#     active_len=len(this_group_df[this_group_df['active_flag'] == 1] )
#     #print("active_len=%s" %active_len) 
#     if (active_len >0):
#         active_value=this_group_df[this_group_df['active_flag'] == 1]['Total Value'].values[0]
#         active_count=this_group_df[this_group_df['active_flag'] == 1]['Total Count'].values[0]
#     else: 
#         active_value=0
#         active_count=0
        
        
#     lapsed_len=len(this_group_df[this_group_df['active_flag'] == 0] )
#     #print("lapsed_len=%s" %lapsed_len) 
#     if (lapsed_len >0):
#         lapsed_value=this_group_df[this_group_df['active_flag'] == 0]['Total Value'].values[0]
#         lapsed_count=this_group_df[this_group_df['active_flag'] == 0]['Total Count'].values[0]
#     else: 
#         #print("Lapsed setting to 0 for %s" % cd)
#         lapsed_value=0
#         lapsed_count=0

#     acitve_value_pc=active_value / (active_value + lapsed_value ) * 100
#     lapsed_value_pc=lapsed_value / (active_value + lapsed_value ) * 100

#     acitve_count_pc=active_count / (active_count + lapsed_count ) * 100
#     lapsed_count_pc=lapsed_count / (active_count + lapsed_count ) * 100


        
#     data={"Engagement Manager":em,
#           "active_total_value":active_value,"lapsed_total_value":lapsed_value,
#           "active_count":active_count,"lapsed_count":lapsed_count,
#           "active_value_pc":acitve_value_pc,"lapsed_value_pc":lapsed_value_pc,
#           "acitve_count_pc":acitve_count_pc,"lapsed_count_pc":lapsed_count_pc
#           }
#     em_pc_df=em_pc_df.append(data,ignore_index=True)
#     print("Engagement Manager=%s,Active_value=%s Lasped_value=%s active_value_pc=%s lapsed_value_pc=%s" %(em,active_value,lapsed_value,acitve_value_pc,lapsed_value_pc))


# #Plot active/lapsed % 
# em_pc_df.set_index('Engagement Manager',inplace=True)

# em_pc_count_plot_df=em_pc_df[['acitve_count_pc','lapsed_count_pc']]
# em_pc_count_plot_df=em_pc_count_plot_df.sort_values('lapsed_count_pc')    


# #client_director_pc_count_plot_df.plot.barh(stacked=True,title="Active/Lapsed count % by Client Director",figsize=(20,30),fontsize=14)
# #fig = plt.figure()
# #fig.suptitle("Active/Lapsed count % by Client Director", fontsize=50) 

# ax=em_pc_count_plot_df.plot.barh(stacked=True,title="lapsed account count by Engagement Manager (%)",figsize=(20,30),fontsize= 14)
# ax.set_title('Lapsed account count by Engagement Manager 2018 (%)',fontsize= 35,fontweight="bold") 
# for p in ax.patches:
#     left, bottom, width, height = p.get_bbox().bounds
#     if (width != 0):        
#         number_text="{:.0f}".format(width)
#     else:
#         number_text=""
#     ax.annotate(number_text, xy=(left+width/2, bottom+height/2), 
#                 ha='center', va='center',fontweight="bold")
# lgd = ax.legend(loc=9, bbox_to_anchor=(0.5,-0.02))
# plt.savefig("fig15c.png")


# em_pc_value_plot_df=em_pc_df[['active_value_pc','lapsed_value_pc']]
# em_pc_value_plot_df=em_pc_value_plot_df.sort_values('lapsed_value_pc')   
# ax=em_pc_value_plot_df.plot.barh(stacked=True,figsize=(20,30),fontsize= 14)
# ax.set_title('Lapsed account value by Engagement Manager 2018 (%)',fontsize= 35,fontweight="bold") 
# for p in ax.patches:
#     left, bottom, width, height = p.get_bbox().bounds
#     if (width != 0):        
#         number_text="{:.1f}".format(width)
#     else:
#         number_text=""
#     ax.annotate(number_text, xy=(left+width/2, bottom+height/2), 
#                 ha='center', va='center',fontweight="bold")
# lgd = ax.legend(loc=9, bbox_to_anchor=(0.5,-0.02))
# plt.savefig("fig16c.png")





# # Reshape the data to plot stacked bar chart 
# lapsed_data=em_totals_df[em_totals_df['active_flag'] == 0]
# active_data=em_totals_df[em_totals_df['active_flag'] == 1]





# data_lapsed_plot_df=lapsed_data[['Total Value','Engagement Manager']]
# data_lapsed_plot_df.rename(columns={"Total Value":'Total Value Lapsed'},inplace=True)
# #data_lapsed_plot_df.index=data_lapsed_plot_df['Client Director']




# data_active_plot_df=active_data[['Total Value','Engagement Manager']]
# data_active_plot_df.rename(columns={"Total Value":'Total Value Active'},inplace=True)


# all_plot_data=pd.merge(data_active_plot_df, data_lapsed_plot_df, left_on='Engagement Manager', right_on='Engagement Manager',how="outer")
# all_plot_data.update(all_plot_data[['Total Value Active','Total Value Lapsed']].fillna(0))
# all_plot_data.set_index('Engagement Manager',inplace=True)




# all_plot_data['total']=all_plot_data['Total Value Active'] + all_plot_data['Total Value Lapsed']
# all_plot_data=all_plot_data.sort_values('total')    
# ax=all_plot_data[['Total Value Active','Total Value Lapsed']].plot.barh(stacked=True,figsize=(20,30))
# ax.set_title("Active/Lapsed total account value by Engagement Manager",fontsize= 35,fontweight="bold") 

# for p in ax.patches:
#     left, bottom, width, height = p.get_bbox().bounds
#     print("left=%s,bottom=%s,width=%d,height=%d" % (left, bottom, width, height))
#     if (width != 0):        
#         number_text="{:.1f}K".format(width/1000)
#     else:
#         number_text=""
        
    

#     ax.annotate(number_text, xy=(left+width/2 , bottom+height/2), 
#                     ha='center', va='center',fontweight="bold")
    
# lgd = ax.legend(loc=9, bbox_to_anchor=(0.5,-0.02))
# plt.savefig("fig17a.png")

# #Cacluate if sped is increasting
# spend=cs_all[['2019.1','2018.1','Account Name']]
# difference=(spend['2019.1'] - spend['2018.1']).copy()
# spend.loc[:,'difference']=difference
# increase_spend_list=spend[spend['difference'] >0]
# plt.figure()






# # Reshape the data to plot stacked bar chart 
# lapsed_data=client_directory_totals_df[client_directory_totals_df['active_flag'] == 0]
# active_data=client_directory_totals_df[client_directory_totals_df['active_flag'] == 1]





# data_lapsed_plot_df=lapsed_data[['Total Value','Client Director']]
# data_lapsed_plot_df.rename(columns={"Total Value":'Total Value Lapsed'},inplace=True)
# #data_lapsed_plot_df.index=data_lapsed_plot_df['Client Director']




# data_active_plot_df=active_data[['Total Value','Client Director']]
# data_active_plot_df.rename(columns={"Total Value":'Total Value Active'},inplace=True)


# all_plot_data=pd.merge(data_active_plot_df, data_lapsed_plot_df, left_on='Client Director', right_on='Client Director',how="outer")
# all_plot_data.update(all_plot_data[['Total Value Active','Total Value Lapsed']].fillna(0))
# all_plot_data.set_index('Client Director',inplace=True)




# all_plot_data['total']=all_plot_data['Total Value Active'] + all_plot_data['Total Value Lapsed']
# all_plot_data=all_plot_data.sort_values('total')    
# ax=all_plot_data[['Total Value Active','Total Value Lapsed']].plot.barh(stacked=True,figsize=(20,30))
# ax.set_title("Active/Lapsed total account value by Client Director",fontsize= 35,fontweight="bold") 

# for p in ax.patches:
#     left, bottom, width, height = p.get_bbox().bounds
#     print("left=%s,bottom=%s,width=%d,height=%d" % (left, bottom, width, height))
#     if (width != 0):        
#         number_text="{:.1f}K".format(width/1000)
#     else:
#         number_text=""
        
    

#     ax.annotate(number_text, xy=(left+width/2 , bottom+height/2), 
#                     ha='center', va='center',fontweight="bold")
    
# lgd = ax.legend(loc=9, bbox_to_anchor=(0.5,-0.02))
# plt.savefig("fig17.png")

# #Cacluate if sped is increasting
# spend=cs_all[['2019.1','2018.1','Account Name']]
# difference=(spend['2019.1'] - spend['2018.1']).copy()
# spend.loc[:,'difference']=difference
# increase_spend_list=spend[spend['difference'] >0]
# plt.figure()


# # =============================================================================
# # Plot business value over time per client director colour coded by customer 
# # =============================================================================
# #Generate column names for dates
# value_data_df=clientStickyness_df
# value_plot_df=pd.DataFrame()
# start_date=datetime.strptime("01-2017","%m-%Y")
# end_date=datetime.strptime("06-2020","%m-%Y")

# this_date=start_date


# date_column_list=[]
# while (this_date <= end_date):
#     this_year=this_date.strftime("%Y")
#     this_month=this_date.strftime("%B")
#     #print("Month=%s Year=%s" %(this_month,this_year))
#     column_name= this_month + " " + this_year
#     #print("Column name=%s" % column_name)
#     date_column_list.append(column_name)
#     this_date=this_date+ relativedelta(months=+1)


# #value_data_df

# #a=value_data_df.apply(lambda row: generate_value_data(row,date_column_list),axis=1)

# for index,row in value_data_df.iterrows():
#     data_df=pd.DataFrame()
#     #print(row)
#     account_name=row['Account Name']
#     client_director=row['Client Director']
#     values=row[date_column_list].values
#     data_df['values']=values
#     dates=[datetime.strptime(x,"%B %Y") for x in date_column_list]
#     data_df['date']=dates
#     data_df['Account Name']=account_name
#     data_df['Client Director']=client_director
#     #data={"Account Name":row['Account Name'],"Client Director":row['Client Director']}
    
#     value_plot_df=value_plot_df.append(data_df)
    

# group_plot_df=pd.DataFrame()
# value_plot_group=value_plot_df.groupby(["Client Director","date"])
# for name,group in value_plot_group:
#     this_client_director=name[0]
#     this_date=name[1]
#     values_sum=group['values'].sum()
#     #print("Client Director=%s date=%s sum=%s group=%s" %(this_client_director,this_date,values_sum,group))
#     data={'Client Director':this_client_director,"date":this_date,"value_total":values_sum}
#     group_plot_df=group_plot_df.append(data,ignore_index=True)
    
# fig,ax = plt.subplots(figsize=(30,40))


# group_plot_group=group_plot_df.groupby(["Client Director"])
# for name,group in group_plot_group:
#     label_text=name
#     ax.plot(group.date.values,group.value_total.values,label=label_text)
    
# ax.set_title('Value by Client Diretor over time',fontsize=18)
# ax.set_xlabel("date")
# ax.set_ylabel("value (£)")
# ax.legend(loc='best')
# plt.savefig("fig19.png")
# plt.show()
