# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 09:00:32 2020

@author: andy
"""

import pandas as pd
from pathlib import Path
import re 
import matplotlib.pyplot as plt
import numpy as np
import math
from datetime import datetime
from os import path

# =============================================================================
# Global varaibles
# =============================================================================
question_statistics=pd.DataFrame()
difficult_threshold={"min":0.3,"max":0.9}

# =============================================================================
# Functions
# =============================================================================
def get_file_path(directory_name,filename):    
    director_path=Path(directory_name)
    full_file_path=director_path / filename
    return full_file_path
    

    
# # =============================================================================
# # Import Data  
# # =============================================================================

# select qa.id,qa.questionid,qa.questionusageid,q.name,qa.questionsummary,qa.rightanswer,qa.responsesummary,qa.timemodified,qas.state,qas.fraction,qas.userid, username, from_unixtime(qa.timemodified)
# from {question_attempts} qa
# join {question} as q 
# on qa.questionid = q.id
# join {question_attempt_steps} as qas
# on qas.questionattemptid=qa.id
# join {user} as u
# on qas.userid=u.id
# where qas.state in ('gradedright','gradedwrong')
# order by qa.id 



attempts_data_filename=get_file_path(r"C:\Users\Andy.JIVEDIVE.000\OneDrive - University of Buckingham\Assignments\Final Project\Python","AttemptsQueryFinal.xlsx")


#dataset=pd.read_excel(data_orginal_file, sheet_name="TestData",skiprows=range(1,1))
attempts_df=pd.read_excel(attempts_data_filename)
attempts_df=attempts_df.sort_values(by=['questionusageid','questionid'])
attempts_df=attempts_df.rename(columns={'name':'question_name'})

# Read random choice questions
random_question_filename=get_file_path(r"C:\Users\Andy.JIVEDIVE.000\OneDrive - University of Buckingham\Assignments\Final Project\Python","RandomQuestionsFInal.xlsx")
random_quesions_df=pd.read_excel(random_question_filename)
random_quesions_df=random_quesions_df.rename(columns={'id':'questionid'})

# Read non-random questions
non_random_question_filename=get_file_path(r"C:\Users\Andy.JIVEDIVE.000\OneDrive - University of Buckingham\Assignments\Final Project\Python","NonRandomQuestionsFInal.xlsx")
non_random_quesions_df=pd.read_excel(non_random_question_filename)
non_random_quesions_df=non_random_quesions_df.rename(columns={'id':'questionid'})

# Read quiz slots info
quiz_slots_filename=get_file_path(r"C:\Users\Andy.JIVEDIVE.000\OneDrive - University of Buckingham\Assignments\Final Project\Python","QuizSlotsFinal.xlsx")
quiz_slots_df=pd.read_excel(quiz_slots_filename)

#Read quiz_attempts
quiz_attempts_filename=get_file_path(r"C:\Users\Andy.JIVEDIVE.000\OneDrive - University of Buckingham\Assignments\Final Project\Python","QuizAttemptsFinal.xlsx")
quiz_attempts_df=pd.read_excel(quiz_attempts_filename)


#Join randon questions by categoyr id to quiz_slots
all_random_data_df=pd.merge(attempts_df,quiz_slots_df,left_on='category',right_on='questioncategoryid')
all_random_data_df=all_random_data_df.drop(columns=['questionid_y'])
all_random_data_df=all_random_data_df.rename(columns={'questionid_x':'questionid'})


#join non-random questions to quiz_slots bu quizid
non_random_quesions_df=pd.merge(attempts_df,quiz_slots_df,left_on='questionid',right_on='questionid')


#Merge random and non-random data
all_data_df=pd.concat([all_random_data_df,non_random_quesions_df], ignore_index=True)
#Add marks

all_data_df['marks']=all_data_df[all_data_df['state'] == 'gradedright']['maxmark']
all_data_df['marks']=all_data_df['marks'].fillna(0)

#all_data_df['marks']=all_data_df[all_data_df['state'] == 'gradedwrong']=0


#Count attempts at each quiz
attempts_at_each_question_df=all_data_df.groupby(['questionid']).count()
attempts_at_each_question_df=attempts_at_each_question_df['id_x']
correct_answers_each_question=(all_data_df[all_data_df['state'] == 'gradedright']).groupby(['questionid']).count()
correct_answers_each_question=correct_answers_each_question['id_x']

attempts_at_each_quiz=quiz_attempts_df.groupby(['quiz']).count()
attempts_at_each_quiz=attempts_at_each_quiz['id']

quiz_question_count_series=quiz_slots_df.groupby('quizid')['id'].count()
#a=quiz_attempts_df.groupby('quiz').sumgrades.quantile([0.25,0.5,0.75])
#a=quiz_attempts_df.groupby('quiz','questionid').sum()






#quartiles_series=quiz_attempts_df.groupby('quiz').sumgrades.quantile([0.25,0.5,0.75])

quiz_scores_df=all_data_df.groupby(['quizid','questionusageid']).sum()
quiz_scores_quartiles_series=quiz_scores_df.groupby('quizid').marks.quantile([0.25,0.5,0.75])




question_stats_df=pd.DataFrame()
quiz_stats_df=pd.DataFrame()
exam_stats_df=pd.DataFrame()

#Calculate all quiz scores

quiz_groups=all_data_df.groupby(['quizid'])
for quizid,group in quiz_groups: 
    attempts=(group.groupby('questionusageid')['questionusageid'].nunique().count())
    attempt_score=group[group['state'] == 'gradedright']['questionid'].count()
    print("Quiz={} Attepts={}".format(quizid,attempts))
    grade_per_attempt_df=group[group['state'] == 'gradedright'].groupby('questionusageid').count()
    grade_per_attempt_df['quizid']=quizid
    grade_per_attempt_df=grade_per_attempt_df[['quizid','questionid']]
    grade_per_attempt_df=grade_per_attempt_df.rename(columns={"questionid": "score"})
    
    
    quiz_stats_df=quiz_stats_df.append(grade_per_attempt_df,ignore_index=True)
    #Calculate Ferguson's delta calulate f the number of students with this score
    scores_in_this_quiz=quiz_stats_df[quiz_stats_df['quizid'] == quizid]
    count_scores_in_quiz=scores_in_this_quiz.groupby('score').count()
    
    #grade_per_attempt=grade_per_attempt['quiz','questionusageid']
    pass_score_for_quiz=quiz_slots_df[quiz_slots_df['quizid'] == quizid]['gradepass'].iloc[0]
    
    
    
    # Set counter to zero for this quiz to calucalte r_test - Kruder Richardson - calculate sum(Pi(1-Pi))
    sum_p1_1_minus_p1=0
    
    
    #Number of attempts at this quiz
    N=grade_per_attempt_df.count()[0]
    
    
    #Fergusons delta - count number at each grade
    f_sqr_sum=0
    quiz_score_group=quiz_scores_df.loc[quizid].groupby('marks')
    for group_name,group_of_marks in quiz_score_group:
        mark_count=len(group_of_marks)
        mark_count_squared=mark_count**2
        f_sqr_sum=f_sqr_sum+mark_count_squared
    print("quiz={} f_sqr_sum={}".format(quizid,f_sqr_sum))
    #f_sqr_sum=np.square(grade_per_attempt_df).sum()
    
    question_inquiz_group=group.groupby('questionid')
    for questionid,group in question_inquiz_group:
        question_attempt_count=group['questionid'].count()
        question_gradedright_count=group[group['state'] == 'gradedright']['questionid'].count()
        question_gradedwrong_count=group[group['state'] == 'gradedwrong']['questionid'].count()
        
        N_1=question_gradedright_count
        
        Q1=quiz_scores_quartiles_series[quizid,0.25]
        Q3=quiz_scores_quartiles_series[quizid,0.75]
        this_quiz_scores=quiz_scores_df.loc[quizid]
        this_quiz_Q1_list=this_quiz_scores[this_quiz_scores['marks'] < Q1]
        N_L=this_quiz_Q1_list['questionid'].count()
        
        this_quiz_Q4_list=this_quiz_scores[this_quiz_scores['marks'] >= Q3]
        N_H=this_quiz_Q4_list['questionid'].count()
        K=quiz_question_count_series[quizid]
        N_1=question_gradedright_count
        pass_grade=quiz_slots_df[quiz_slots_df['quizid'] == quizid]['gradepass'].iloc[0]
        #N_L=quiz_scores_quartiles_series[quizid,]
        
        #d=all_data_df[(all_data_df['state']=='gradedright') & ( all_data_df['quizid'] == 13)]
        #select all attempts that got this quesiton right
        
        # X_1_mean = Average total score for those who correctly answer the entire test
        #Llist all attempts that answered the question correctly 
        item_correct_attempts_series=group[group['state'] == 'gradedright']['questionusageid']
        item_incorrect_attempts_series=group[group['state'] == 'gradedwrong']['questionusageid']
        
        # (X_1 ) ̅Average total score for those who correctly answer the item
        X_1_mean=(all_data_df.marks[all_data_df['questionusageid'].isin(item_correct_attempts_series)].sum())/(len(item_correct_attempts_series))
        
        #(X_0 ) ̅=Average total score for those who incorrectly answer the item
        X_0_mean=(all_data_df.marks[all_data_df['questionusageid'].isin(item_incorrect_attempts_series)].sum())/(len(item_incorrect_attempts_series))
        
        # Sigma_x==Standard deviation of the total score of the this quiz
        Sigma_x=quiz_stats_df[quiz_stats_df['quizid']==quizid].groupby('quizid').std().iloc[0][0]
        Sigma2_x=quiz_stats_df[quiz_stats_df['quizid']==quizid].groupby('quizid').var().iloc[0][0]
        
        
        # =============================================================================
        #
        # Item difficulty P=N1/N 
        #
        # Ideal figure 0.5
        # P=1 - easy question
        # P=0.05 Difficult question
        # Anecdotoally acceptable figures  0.3 < P < 0.9
        # =============================================================================
        P=N_1/N
        if (P>=1):
            P=1


        # =============================================================================
        # Descrimination index D
        # Measures how powerfully an item distinguishes higher performing apprentices
        # (N_H-N_L)/(N/4)
        # if an item discriminatesD>=0.3  
        #
        # =============================================================================
        D=(N_H-N_L)/(N/4)
        
                
        # =============================================================================
        # Point Biserial coefficient (r_pbi )
        # r_pbi=(X_1_mean-X_0_mean)/Sigma_x * SQRT(p(1-p))
        # r_pbi≥0.2 - good item reliability 
        # =============================================================================
        r_pbi=(X_1_mean-X_0_mean)/Sigma_x * (math.sqrt(P*(1-P)))
        
        
        
        stats={'questionid':questionid,'N':N,
               'N_1':N_1,'question_gradedright_count':question_gradedright_count,
               'question_gradedwrong_count':question_gradedwrong_count,'Q1':Q1,
               'Q3':Q3,'quizid':quizid,'N_L':N_L,'N_H':N_H,'K':K,
               'P':P,'D':D,'X_1_mean':X_1_mean,'X_0_mean':X_0_mean,'Sigma_x':Sigma_x,
               'Sigma2_x':Sigma2_x,'r_pbi':r_pbi
               
               }
        question_stats_df=question_stats_df.append(stats,ignore_index=True)
        print("stats={}".format(stats))
        
        # Add next item to list - this quiz to calucalte r_test - Kruder Richardson - calculate sum(Pi(1-Pi))
        sum_p1_1_minus_p1=sum_p1_1_minus_p1+(P*(1-P))
    
    # =============================================================================
    # r_(test )→ (KR-20) Kuder-Richardson reliablity index - higher correlation between individual items increases Kuder-Richardson index
    # K/(K-1)*(1-(sum(Pi(1-Pi))/Sigma))
    #
    #    
    # =============================================================================
    r_test=K/(K-1)*(1-(sum_p1_1_minus_p1)/Sigma2_x)
    print("r_test={}".format(r_test))
    
    
    # =============================================================================
    # f=N^2-sum(f_i^2)/(N^2-N^2/(K+1))
    # =============================================================================
    print("f_sqr_sum={}".format(f_sqr_sum))
    f=((N**2) - f_sqr_sum)/(N**2-(N**2/(K+1)))
    print("f={}".format(f))
    
    exam_stats={'r_test':r_test,'f':r_test}
    exam_stats_df=exam_stats_df.append(exam_stats,ignore_index=True)
    
question_stats_df.to_excel("question_stats.xlsx")
exam_stats_df.to_excel("exam_stats.xlsx")

