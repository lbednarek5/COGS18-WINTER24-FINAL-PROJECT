""" Collection of Functions for Creating Severity and Variable Count Dataframes"""

import pandas as pd

def severity(score, severity_label_and_score_bounds):
    """
    Categorizes a score
    
    Parameters
    ----------
    score : int
        score from a scale, to be categorized
    severity_label_and_score_bounds : dictionary, strings are keys and values are \n
    tuples of integers
        indicates labels for severity and associated bounds for the given measure \n
        (inclusive)
    
    Returns
    -------
    severity_category : string
        string with the severity category of the given score. If not a valid score,\n
        returns "Score out of range"
    """
    severity_category = "Score out of range"
    for severity_label, bounds in severity_label_and_score_bounds.items():
        if score in range(bounds[0], bounds[1] + 1):
            severity_category = severity_label
    return severity_category
    
def add_severity_column(severity_label_and_score_bounds, measure, dataframe):
    """
    Applies severity function to all values for a given measure
    
    Parameters
    ----------
    severity_label_and_score_bounds : dictionary, strings are keys and values are 
    tuples of integers
        indicates labels for severity and associated bounds for the given measure \n
        (inclusive)
    measure : string
        title of column name containing measure of interest
    dataframe: pandas.core.frame.DataFrame 
        dataframe of interest
        
    Returns
    -------
    None. Modifies original dataframe, unless the specified measure is not in \n
    the dataframe
    """
    try: 
        new_column = list(severity(score, severity_label_and_score_bounds) \
                          for score in dataframe[measure])
        dataframe["Severity"] = new_column
    except KeyError:
        print("The column", measure, "is not present in the DataFrame.") 
    
def df_severity_counts(measure, dataframe):
    """
    Given a dataframe and column/variable of interest, return a new dataframe that \n
    includes the counts of each variable value within each severity type
    
    Parameters
    ----------
    measure : string
        name of the measure/column of interest
    dataframe: pandas.core.frame.DataFrame 
        dataframe of interest
    
    Returns
    -------
    severity_df : pandas.core.frame.DataFrame 
        If the specified measure or severity column is not in the dataframe, returns \n
        original dataframe
    """
    try:
        severity_df = dataframe.groupby(['Severity', measure]).size().\
        reset_index(name = measure + ' Count')
        return severity_df
    except KeyError as e: 
        print(e) 
        return dataframe
    
def dict_of_count_dfs(dataframe):
    """
    Given a dataframe, return a dictionary of dataframes that includes
    the severity count dataframes of each columns
    
    Parameters
    ----------
    dataframe: pandas.core.frame.DataFrame 
        dataframe of interest
    
    Returns
    -------
    all_dfs : dictionary, with strings as keys and pandas.core.frame.DataFrame as values
        dataframe with column name and associated count dataframe
    """
    all_columns = dataframe.columns.tolist()[:-1]
    all_dfs = {}
    for column in all_columns:
        df_column_counts = df_severity_counts(column, dataframe)
        all_dfs[column] = df_column_counts
    return all_dfs