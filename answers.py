
"""

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
