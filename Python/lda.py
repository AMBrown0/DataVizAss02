# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 12:07:25 2021

@author: andy
"""

# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import pandas as pd
import os
import glob
import shutil
import pandas as pd
from pathlib import Path
import re 
import matplotlib.pyplot as plt
import numpy as np
import math
from datetime import datetime

from os import path
from docx import Document
from sklearn.linear_model import LinearRegression

#LDA Imports
import gensim
import nltk
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
from gensim import corpora, models
from pprint import pprint
np.random.seed(2018)
#nltk.download('wordnet')

#plot
import matplotlib.pyplot as plt
import seaborn as sns

#Lexicon sentiment analysis 
from afinn import Afinn
from textblob import TextBlob


from sklearn.metrics import r2_score

if __name__ == '__main__':
    # =============================================================================
    # Global varaibles
    # =============================================================================
    question_statistics=pd.DataFrame()
    difficult_threshold={"min":0.3,"max":0.9}
    stemmer = SnowballStemmer('english')
    
    # =============================================================================
    # Functions
    # =============================================================================
    def get_file_path(directory_name,filename):    
        director_path=Path(directory_name)
        full_file_path=director_path / filename
        return full_file_path
        
    def lemmatise_stemming(word):
        return stemmer.stem(WordNetLemmatizer().lemmatize(word, pos='v'))
    
    def preprocess(text):
        result = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS:
                result.append(lemmatise_stemming(token))
        return result
    
    # # =============================================================================
    # # Import Data  
    # # =============================================================================
    
    
    apprentice_EPA_feedback_path=get_file_path(r"C:\Users\Andy.JIVEDIVE.000\OneDrive - University of Buckingham\Assignments\Final Project\Archive","Apprentice End-point Assessment (EPA) Feedback 1.xlsx")
    
    
    #dataset=pd.read_excel(data_orginal_file, sheet_name="TestData",skiprows=range(1,1))
 
    #Read in comments
    apprentice_EPA_feedback_df=pd.read_excel(apprentice_EPA_feedback_path)
    apprentice_EPA_comments_df=apprentice_EPA_feedback_df.iloc[0:-1,20]
 
    #Read in overall scores
    index_of_null_comments=np.where(apprentice_EPA_feedback_df.iloc[0:-1,20].notnull())[0]
    apprentice_EPA_overallscore_df=apprentice_EPA_feedback_df.loc[index_of_null_comments]
    apprentice_EPA_overallscore_df=apprentice_EPA_overallscore_df.iloc[0:-1,19]
       
 
    
    # =============================================================================
    #  Swentiment Analysis initialisation    
    # =============================================================================
    af = Afinn()
    
    
    # =============================================================================
    # Clean the datat 
    # =============================================================================
    apprentice_EPA_comments_df=apprentice_EPA_comments_df.dropna()
    apprentice_EPA_comments_df.to_excel("cleansed_comments.xlsx")
    
    #Lematise
    a=lemmatise_stemming("was")
    print(a)
    
    
    b="I was told i would receive a grade after 5 days. I was told i had a grade but it couldnt be released pending a functional skills exam"
    c=preprocess(b)
    
    processed_comments_df=apprentice_EPA_comments_df.map(preprocess)
    dictionary = gensim.corpora.Dictionary(processed_comments_df)
    dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_comments_df]
    bow_doc_68=bow_corpus[68]
    for i in range(len(bow_doc_68)):
        print("Word {} (\"{}\") appears {} time.".format(bow_doc_68[i][0], 
                                                         dictionary[bow_doc_68[i][0]], 
                                                         bow_doc_68[i][1]))
    # for i in range(len(bow_corpus)):
    #     print("Word {} (\"{}\") appears {} time.".format(processed_comments_df.iloc[i][0], 
    #                                                      dictionary[processed_comments_df.iloc[i][0]], 
    #                                                      processed_comments_df.iloc[i][1]))
    
    tfidf = models.TfidfModel(bow_corpus)
    corpus_tfidf = tfidf[bow_corpus]
    
    for doc in corpus_tfidf:
        pprint(doc)
        break


    #     origonal_comment=processed_comments_df.iloc[comment_number]
    #comment_number=21    
    number_of_words_in_topics=1
    nummber_of_topics=5
    
    #lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=10, id2word=dictionary, passes=1, workers=1)
    lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=nummber_of_topics, id2word=dictionary, passes=1, workers=1)
    for idx, topic in lda_model.print_topics(-1):
        print('Topic: {} \nWords: {}'.format(idx, topic))
        
    results_list_df=pd.DataFrame()
    textblob_sentiment_score_df=pd.DataFrame()
    
    #Create a list of origonal comments
    for comment_number in range(len(processed_comments_df)):
        afin_sentiment_score=af.score(apprentice_EPA_comments_df.iloc[comment_number]) 
        tb=TextBlob(apprentice_EPA_comments_df.iloc[comment_number])
        textblob_sentiment_score=tb.sentiment.polarity
        textblob_sentiment_score_record={'textblob_score':textblob_sentiment_score}
        textblob_sentiment_score_df=textblob_sentiment_score_df.append(textblob_sentiment_score_record,ignore_index=True)
        
        
        apprentice_overall_score=apprentice_EPA_overallscore_df.iloc[comment_number]
        print("Comment={}".format(comment_number))

        print("=====================LDA TOPICS Doc={}================================".format(comment_number))
        # for index, score in sorted(lda_model[bow_corpus[4]], key=lambda tup: -1*tup[1]):
            # print("\nScore: {}\t \nTopic: {}".format(score, lda_model.print_topic(index, 10)))
        for index, score in sorted(lda_model[bow_corpus[comment_number]], key=lambda tup: -1*tup[1]):
            #print("\nScore: {}\t \nTopic: {}".format(score, lda_model.print_topic(index, 10)))
            #print("Score: {}\t \nTopic: {}".format(score, lda_model.print_topic(index, number_of_words_in_topics)))
            
            print("Doc={},Topic={}, Score: {:.2f}\t sentiment_afin:{} sentiment_textblob:{} [ {}]".format(comment_number,
                                                                                                          index,score,afin_sentiment_score,textblob_sentiment_score ,lda_model.print_topic(index, number_of_words_in_topics)))
            result_dict={'document':comment_number,'topic_no':index,'lda_score':"{:.2f}".format(score),
                         'sentiment_textblob':textblob_sentiment_score,'sentiment_afin':afin_sentiment_score,
                         'topic':lda_model.print_topic(index, number_of_words_in_topics),
                         'orgigonal_text':apprentice_EPA_comments_df.iloc[comment_number],
                         'apprentices_score':apprentice_overall_score
                         }
            results_list_df=results_list_df.append(result_dict,ignore_index=True)
        lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=nummber_of_topics, id2word=dictionary, passes=1, workers=1)
        
        # for index, score in sorted(lda_model_tfidf[bow_corpus[4]], key=lambda tup: -1*tup[1]):
        #     print("\nScore: {}\t \nTopic: {}".format(score, lda_model_tfidf.print_topic(index, 10)))
            
        
        print("=====================LDA TFIDF TOPICS Doc={}================================".format(comment_number))
        for index, score in sorted(lda_model_tfidf[bow_corpus[comment_number]], key=lambda tup: -1*tup[1]):
            #print("Score: {:.2f}\t \nTopic: {}".format(score, lda_model_tfidf.print_topic(index, number_of_words_in_topics)))
            print("Doc={},Topic={}, Score: {:.2f}\t [ {}]".format(comment_number,index,score,lda_model_tfidf.print_topic(index, number_of_words_in_topics)))
            
    
    results_list_df.to_excel("results.xlsx")
    
    sent_topics_df = pd.DataFrame()

    apprentice_overall_score=apprentice_EPA_feedback_df.iloc[0:-1,19]
    plt.hist(apprentice_overall_score, color = 'blue', edgecolor = 'black',
         bins = 10)
    plt.show()
    ax = sns.boxplot(data=apprentice_overall_score, orient="h", palette="Set2")
    x=np.array(apprentice_overall_score[index_of_null_comments])
    x=x.reshape(1,-1)
    y=np.array(textblob_sentiment_score_df)
    y=y.reshape(1,-1)
    
    
    plt.scatter(x,y)
    plt.show()
    # reg = LinearRegression().fit(x, y)
    
    
    # y_pred=reg.predict(x)
    # y_pred=y_pred.reshape(-1,1)
    # #y=y.reshape(-1,1)
    # r2=r2_score(y,y_pred)
    # print("Intercept={} coefficent={} r2={}".format(reg.intercept_,reg.coef_,r2))
    #Regression of Overall score provided by apprentcies against 

    # # Get main topic in each document
    # for i, row_list in enumerate(lda_model[bow_corpus]):
    #     row = row_list[0] if lda_model.per_word_topics else row_list            
    #     # print(row)
    #     row = sorted(row, key=lambda x: (x[1]), reverse=True)
    #     # Get the Dominant topic, Perc Contribution and Keywords for each document
    #     for j, (topic_num, prop_topic) in enumerate(row):
    #         if j == 0:  # => dominant topic
    #             wp = lda_model.show_topic(topic_num)
    #             topic_keywords = ", ".join([word for word, prop in wp])
    #             sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
    #         else:
    #             break
    # sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # # Add original text to the end of the output
    # contents = apprentice_EPA_comments_df.reset_index(drop=True)
    # sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    
    #a=apprentice_EPA_feedback_df[apprentice_EPA_feedback_df.iloc[0:-1,20].notnull()]
    

    