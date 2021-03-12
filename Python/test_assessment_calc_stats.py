# Generated by Selenium IDE
# =============================================================================
# LIbraries
# =============================================================================

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
from datetime import datetime
from pathlib import Path
import pandas as pd

# =============================================================================
# Global varaibles
# =============================================================================
#answers=['0','1','2','3','0','1','2','3','0','1','2','3','0','1','2','3','0','1','2','3']
#answers=['0','1','2','3','0','1','2','3','0','1','2','3','0','1','2','3']
answer_lookup={'A':0,'B':1,'C':2,'D':3}


# =============================================================================
# Functions
# =============================================================================
def get_file_path(directory_name,filename):    
    director_path=Path(directory_name)
    full_file_path=director_path / filename
    return full_file_path
    



# =============================================================================
# Import Data  
# =============================================================================

data_orginal_file=get_file_path(r"C:\Users\Andy.JIVEDIVE.000\OneDrive - University of Buckingham\Assignments\Final Project\Python","DST_CORE_1-Digital Support Technician - Core-grades.csv")

#dataset=pd.read_excel(data_orginal_file, sheet_name="TestData",skiprows=range(1,1))
#dataset=pd.read_excel(data_orginal_file, sheet_name="DST_CORE_1-Digital Support Tech")
#dataset_df=pd.read_excel(data_orginal_file)
dataset_df=pd.read_csv(data_orginal_file)

#Headers and redundant columns
#dataset_cleansed=dataset.iloc[1:,1:]



# =============================================================================
# Classes and Functions
# =============================================================================
