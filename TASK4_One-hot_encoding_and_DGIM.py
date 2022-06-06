__author__ = "Dara da Silva Weirich"
__copyright__ = "Copyright 2022"
__version__ = "1.0"
__email__ = "s3193076@stud.uni-frankfurt.de"
__status__ = "Development"


# Parameter Setting
import pandas as pd
import streamlit as st
from dgim import Dgim
from PIL import Image

file = r"HCV-Egy-Data\HCV-Egy-Data.csv"
df = pd.read_csv(file)
st.title("""
STREAM MINING: One-hot encoding and DGIM""")
st.subheader("""By Dara da Silva Weirich in Data Science I
""")

def main_window():
    """
    Interface between functions and streamlit
    """
    
    # LIST OF COLUMNS IN DATAFRAME
    column_chooser = ['Age ', 'Gender', 'BMI', 'Fever', 'Nausea/Vomting', 'Headache ',
        'Diarrhea ', 'Fatigue & generalized bone ache ', 'Jaundice ',
        'Epigastric pain ', 'WBC', 'RBC', 'HGB', 'Plat', 'AST 1', 'ALT 1',
        'ALT4', 'ALT 12', 'ALT 24', 'ALT 36', 'ALT 48', 'ALT after 24 w',
        'RNA Base', 'RNA 4', 'RNA 12', 'RNA EOT', 'RNA EF',
        'Baseline histological Grading', 'Baselinehistological staging']
    
    st.write(""" ## Orignal Dataframe
    """)
    # DISPLAY ORIGINAL DATAFRAME
    display_df()

    # MORE INFORMATIONEN ABOUT THE DATA PROVIDED
    with st.expander("Informationen About the Data Provided"):
        st.write("""
         Egyptian patients who underwent treatment dosages for HCV about 18 months.\n
         Age: Age; Gender: Gender; BMI: Body Mass Index; Fever: Fever; Nausea/Vomting: Nausea/Vomting; Headache: Headache;
         Diarrhea: Diarrhea; Fatigue & generalized bone ache: Fatigue & generalized bone ache; Jaundice: Jaundice; Epigastric pain: Epigastric pain; WBC: White blood cell;
         RBC: red blood cells; HGB: Hemoglobin; Plat: Platelets; AST 1: aspartate transaminase ratio; ALT 1: alanine transaminase ratio 1 week; ALT 4: alanine transaminase ratio 12 weeks;
         ALT 12: alanine transaminase ratio 4 weeks; ALT 24: alanine transaminase ratio 24 weeks;
         ALT 36: alanine transaminase ratio 36 weeks;
         ALT 48: alanine transaminase ratio 48 weeks; ALT: after 24 w alanine transaminase ratio 24 weeks; RNA Base: RNA Base; RNA 4:
         RNA 4; RNA 12: RNA 12; RNA EOT: RNA end-of-treatment; RNA EF; RNA Elongation Factor; Baseline histological Grading Baseline histological Grading: Baseline histological staging:
         Baseline histological staging.\n
         [Link to Dataset](https://archive-beta.ics.uci.edu/ml/datasets/hepatitis+c+virus+hcv+for+egyptian+patients)""")

    # One-hot encoding
    st.sidebar.markdown("""
    ## One-hot encoding""")    
    selected_col = st.sidebar.selectbox(f"Choose the Column to Apply One-hot Encoding", column_chooser)     
    df_dummies = one_hot_encoder(selected_col)
    # DGIM
    st.sidebar.markdown("""
    ## Datar-Gionis-Indyk-Motwani Algorithm (DGIM)""")
    # GET USER-INPUT
    choosen_col = st.sidebar.selectbox("Choose the Column to Analyze with DGIM", list(df_dummies.columns))
    error_rate = (st.sidebar.number_input("Select Error Rate for DGIM in [%]", min_value=1, max_value=100))/100
    N = st.sidebar.number_input("Choose N from 1 to 99999", min_value=1, max_value=99999)
    # DISPLAY DGIM RESULT
    dgim_result = display_dgim(error_rate, N, choosen_col, df_dummies)
    st.write("## Results After DGIM-Algorithm")
    st.write(f"The Approximated Number of One's is: {dgim_result[0]}")
    st.write(f"The Number we Expected was: {dgim_result[1]}")
    image = Image.open('GU-Logo-blau-gross.png')
    image = image.resize((250,250))
    st.image(image)
    
    
def display_df():
    """
    Simple function to display the original data frame
    """
    
    st.write(df)


def one_hot_encoder(col):
    """
    Function to provide One-hot encoding
    """
    st.write("""
    ## One-hot Encoding for the Choosen Column""")
    df_with_dummies = pd.get_dummies(df[col])
    st.write(df_with_dummies)
    return df_with_dummies


def display_dgim(rate, n, col, df):
    """
    DGIM Algorithm Implementation
    """ 
    # APPLY DGIM
    chosen_column = df[col]
    dgim = Dgim(N=n, error_rate=rate)
    for i in range(len(chosen_column)):
        if chosen_column[i] == 1:
            dgim.update(True)
        else:
            dgim.update(False)
            
    # DGIM RESULT
    dgim_result = dgim.get_count()

    # COMPARE OUR RESULT WITH THE TRUTH
    no_ones = len([x for x in chosen_column if x == 1])

    
    return dgim_result, no_ones


main_window()

