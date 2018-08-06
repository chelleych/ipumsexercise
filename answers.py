
"""
    Michelle Henry's answers to the IPUMS Exercises.
    
    
    There are two files that you will receive:

    1) “1870_CT.csv” This file lists the first 1000 people who was enumerated in the 1870 census and listed a birthplace of Connecticut.
    2) “1880_CT.csv” This file lists every person who was enumerated in the 1880 census and listed a birthplace of Connecticut.

You will find these variables within the files:

    1) “id” A unique identifier for this individual in this census. (An individual will have different “id”s throughout different censuses.)
    2) “SERIAL” The identifier for the household that the individual is in.
    3) “NAMEFRST” The individual’s first name.
    4) “NAMELAST” The individual’s last name.
    5) “AGE” The individual’s age in that census year.
    6) “SEX” The individual’s sex.
        a) See https://usa.ipums.org/usa-action/variables/SEX#codes_section for code labels.
        b) 9 = UNKNOWN
    7) “BPL”. The individual’s birthplace.
        a) See https://usa.ipums.org/usa-action/variables/BPL#codes_section for code labels.

Questions:
    1. For the first record in 1870, “Catherine Beebe”, find the best match in 1880. Doing this manually by searching through the data is fine.
        a. What is the best match?
        b. How did you find the best match?
    2. Do the same for the second and third records, “Frances E Bird” and “J S Luff”.
        a. What are the best matches for these records?
        b. How did you find these best matches?
    3. Write a program (or function) which does the following: Given one record from 1870 and the entire 1880 dataset, return the best matched record in 1880. Run the program on the same first 3 records above and verify that it gives the correct results.
        a. Give a general overview of your program.
        b. What is the criteria that you used to determine a best match?
    4. Now input the 4th 1870 record into the program, “John Smith”.
        a. What happens?
    5. Modify your program to return the top 3 best matches and rerun the 4th 1870 record, “John Smith”. You can decide what criteria determines how good a specific match is, but make sure that the top match for the first 3 records remains the same.
        a. How did you modify your program?
        b. What criteria did you use to order the best matches?
    6. Run your program on all 1,000 1870 records and record the runtime. Save the best match for each 1870 record out to a csv file, where one column is the id of the 1870 record and one column is the id of the 1880 record. If it takes a long time to run, stop the program after 10 minutes, but make sure to get a partial output.
        a. What is the run time total? What is the run time per 1870 record?
        b. What would happen to the run time if you doubled the size of the 1880 file and why?
        c. Where are the performance bottlenecks?
        d. How could you modify the program to run faster as a single thread/process (i.e. without parallelizing it)?
        e. How could you go about parallelizing it?
        f. What techniques could you explore to get better matches?
"""

import pandas as pd
from pyjarowinkler import distance
import time

def read_data(file_path):
    """
    Inputs:
    file_path : str
        File path of the census data
    Outputs:
    df : pandas.DataFrame
    DataFrame containing the data from the input files

    You will find these variables within the file:

        1) “id” A unique identifier for this individual in this census. (An
            individual will have different “id”s throughout different censuses.)
        2) “SERIAL” The identifier for the household that the individual is in.
        3) “NAMEFRST” The individual’s first name.
        4) “NAMELAST” The individual’s last name.
        5) “AGE” The individual’s age in that census year.
        6) “SEX” The individual’s sex.
            a) See https://usa.ipums.org/usa-action/variables/SEX#codes_section for code labels.
            b) 9 = UNKNOWN
        7) “BPL”. The individual’s birthplace.
            a) See https://usa.ipums.org/usa-action/variables/BPL#codes_section for code labels.

    """
    df = pd.read_csv(file_path)
    
    return df




def load_1870_1880_data(file_1870='inputdata/1870_CT.csv', file_1880='inputdata/1880_CT.csv'):
    """
    Inputs:
    file_1870 : str
        File path of 1870 census data
        This file lists the first 1000 people who was enumerated in the 1870 census
        and listed a birthplace of Connecticut.
    file_1880 : str
        File path of 1870 census data
        This file lists every person who was enumerated in the 1880 census and
        listed a birthplace of Connecticut.
    Outputs:
    df_1870,df_1880 : pandas.DataFrame
        DataFrames containingdata from the input files
    """
    df_1870 = read_data(file_1870)
    df_1880 = read_data(file_1880)
    return df_1870, df_1880


df_1870, df_1880 = load_1870_1880_data()

"""
Questions:
    1. For the first record in 1870, “Catherine Beebe”, find the best match in
    1880. Doing this manually by searching through the data is fine.
        a. What is the best match?
        b. How did you find the best match?
"""

df_match1 = df_1880[(df_1880.NAMELAST=='beebe'.upper()) & 
                    (df_1880.NAMEFRST=='catherine'.upper())]
print(df_match1)

"""
    2. Do the same for the second and third records, “Frances E Bird” and “J S Luff”.
        a. What are the best matches for these records?
        b. How did you find these best matches?
"""
print(df_1870.iloc[1,:]) # see info on second row for “Frances E Bird”
df_search2_row2 = df_1880[(df_1880.NAMELAST=='bird'.upper())]
print(df_search2_row2)
# print match for “Frances E Bird”
df_match2_row2 = df_search2_row2.iloc[[0],:]
print(df_match2_row2)

print(df_1870.iloc[2,:]) # see info on second row for “Frances E Bird”
df_search2_row3 = df_1880[(df_1880.NAMELAST=='luff'.upper())]
print(df_search2_row3.sort_values(by='NAMEFRST'))
# “J. S. LUFF" is likely to be a match. Print this row
df_match2_row3 = df_search2_row3[df_search2_row3.NAMEFRST=='J. S.']
print(df_match2_row3)


"""
    3. Write a program (or function) which does the following: Given one record 
    from 1870 and the entire 1880 dataset, return the best matched record in 
    1880. Run the program on the same first 3 records above and verify that 
    it gives the correct results.
        a. Give a general overview of your program.
        b. What is the criteria that you used to determine a best match?
"""
def score_matches(series_1, series_2):
    """
    Inputs:
    series_1, series_2 : pd.Series
        Series that each contain a single record of census data.
        Labels are the columns in the read_data function above
        Data from series_1 must be 10 years earlier than data from series_2
    Outputs:
    score : float
        Score rating the match between the two inputs. Higher is closer.
    """
    if not pd.isnull(series_1.NAMELAST) and not pd.isnull(series_2.NAMELAST):
        dist_NAMELAST = distance.get_jaro_distance(series_1.NAMELAST, series_2.NAMELAST, 
                                                   winkler=True, scaling=0.1)
    else:
        dist_NAMELAST = 0
    if not pd.isnull(series_1.NAMEFRST) and not pd.isnull(series_2.NAMEFRST):
        dist_NAMEFRST = distance.get_jaro_distance(series_1.NAMEFRST, series_2.NAMEFRST, 
                                                   winkler=True, scaling=0.1)
    else:
        dist_NAMEFRST = 0
    dist_BPL = int(series_1.BPL == series_2.BPL)
    dist_SEX = int(series_1.SEX == series_2.SEX)
    dist_AGE = int(series_1.AGE == series_2.AGE - 10 or
                   series_1.AGE == series_2.AGE - 11 or
                   series_1.AGE == series_2.AGE - 9 )
    dist_SERIAL = int(series_1.SERIAL == series_2.SERIAL)
    
    # Weight columns, where important columns get heigher weights
    weight_NAMELAST = 16
    weight_NAMEFRST = 15
    weight_BPL = 4
    weight_SEX = 3
    weight_AGE = 2
    weight_SERIAL = 1
    
    # add scores weighted by importance
    score = weight_NAMELAST * dist_NAMELAST + \
            weight_NAMEFRST * dist_NAMEFRST + \
            weight_BPL * dist_BPL + \
            weight_SEX * dist_SEX + \
            weight_AGE * dist_AGE + \
            weight_SERIAL * dist_SERIAL
    
    return score

def match_record(series_record, df_census):
    """
    Inputs:
    series_record : pd.Series
        Series that contains a ingle record of census data
        Labels are the columns in the read_data function above
        Data from series_record must be 10 years earlier than data from df_census
    df_census : pd.DataFrame
        DataFrame that contains census data
        Column labels as in the read_data function above
        Data from series_record must be 10 years earlier than data from df_census
    Outputs:
    df_match : pd.DataFrame
        DataFrame row match from df_census
    
    Given one record and the entire df_census dataset, return the best 
    matched record in df_census.
    In cases of a tie, all best matches are returned
    """
    # Score each entry in df_census
    series_score = df_census.apply(lambda row: score_matches(series_record, row),axis=1)
    
    # Best is the row with the max score
    df_match = df_census.loc[series_score==series_score.max(),:]
    
    return df_match


# Run the program on the same first 3 records above and verify that it gives 
# the correct results.
df_match3_row2 = match_record(df_1870.iloc[0,:], df_1880)
pd.testing.assert_frame_equal(df_match1,df_match3_row2)

df_match3_row2 = match_record(df_1870.iloc[1,:], df_1880)
pd.testing.assert_frame_equal(df_match2_row2, df_match3_row2)    

df_match3_row3 = match_record(df_1870.iloc[2,:], df_1880)
pd.testing.assert_frame_equal(df_match2_row2, df_match3_row2)



"""
    4. Now input the 4th 1870 record into the program, “John Smith”.
        a. What happens?
"""
df_match4_row4 = match_record(df_1870.iloc[3,:], df_1880)
print(df_match4_row4)

"""
    5. Modify your program to return the top 3 best matches and rerun the 4th 1870 record, “John Smith”. You can decide what criteria determines how good a specific match is, but make sure that the top match for the first 3 records remains the same.
        a. How did you modify your program?
        b. What criteria did you use to order the best matches?
"""
def match_record_top3(series_record, df_census):
    """
    Inputs:
    series_record : pd.Series
        Series that contains a ingle record of census data
        Labels are the columns in the read_data function above
        Data from series_record must be 10 years earlier than data from df_census
    df_census : pd.DataFrame
        DataFrame that contains census data
        Column labels as in the read_data function above
        Data from series_record must be 10 years earlier than data from df_census
    Outputs:
    df_match : pd.DataFrame
        DataFrame row match from df_census
    
    Given one record and the entire df_census dataset, return the best 3
    matched records in df_census.
    """
    # Score each entry in df_census
    series_score = df_census.apply(lambda row: score_matches(series_record, row),axis=1)
    
    # Best is the row with the max score. Uses index of top 3 scores.
    index_match = series_score.sort_values(ascending=False)[:3].index
    df_match = df_census.loc[index_match,:]
    
    return df_match

df_match5_row4 = match_record_top3(df_1870.iloc[3,:], df_1880)
print(df_match5_row4)

"""
    6. Run your program on all 1,000 1870 records and record the runtime. Save the best match for each 1870 record out to a csv file, where one column is the id of the 1870 record and one column is the id of the 1880 record. If it takes a long time to run, stop the program after 10 minutes, but make sure to get a partial output.
        a. What is the run time total? What is the run time per 1870 record?
        b. What would happen to the run time if you doubled the size of the 1880 file and why?
        c. Where are the performance bottlenecks?
        d. How could you modify the program to run faster as a single thread/process (i.e. without parallelizing it)?
        e. How could you go about parallelizing it?
        f. What techniques could you explore to get better matches?
"""
start = time.time()
df_matches = pd.DataFrame(columns=['id_1870','id_1880'], index=df_1870.index)
for i in range(1000):
    df_match6_rowi = match_record(df_1870.loc[i,:], df_1880)
    df_matches.loc[i,:] = [df_1870.loc[i,'id'], df_match6_rowi.id.iloc[0]]

    # Cancel after 10 minutes
    end = time.time()
    if (end - start)/60 > 10:
        break

print('Run time: %s'%(end - start))
df_matches.dropna().to_csv('matches.csv', index=False)
