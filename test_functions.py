""" Testing My Functions """

import pandas as pd
from functions import severity, add_severity_column, df_severity_counts, \
dict_of_count_dfs

def test_severity():
    """ Tests if the severity function correctly categorizes each score """
    test_dict = {"Small": (0, 9), "Medium": (10, 19), "Large": (20, 39)}
    assert severity(10, test_dict) == "Medium"
    assert severity(25, test_dict) == "Large"
    assert severity(40, test_dict) == "Score out of range"
    return
    
def test_add_severity_column():
    """ Tests if the severity_column function correctly adds a severity column """
    test_df = {"Value": [1, 2, 3, 4, 5, 6], "score": [-5, 5, 15, 25, 35, 45]}
    test_df = pd.DataFrame(test_df)
    add_severity_column({"Small": (0, 9), "Medium": (10, 19), "Large": (20, 39)},\
                        "measure", test_df)
    assert "Severity" not in test_df.columns
    add_severity_column({"Small": (0, 9), "Medium": (10, 19), "Large": (20, 39)},\
                        "score", test_df)
    expected_list = ["Score out of range", "Small", "Medium", "Large", "Large", \
                     "Score out of range"]
    assert "Severity" in test_df.columns
    assert list(test_df["Severity"]) ==  expected_list
    return
    
def test_df_severity_counts():
    """ Tests if the df_severity_column function correctly creates a count dataframe """
    test_df = {"Day": ["Mon", "Tues", "Fri", "Thurs", "Fri", "Mon"], \
               "score": [4, 10, 15, 25, 13, 20]}
    test_df = pd.DataFrame(test_df)
    add_severity_column({"Small": (0, 9), "Medium": (10, 19), "Large": (20, 39)}, \
                        "score", test_df)
    count_df = df_severity_counts("Day", test_df)
    assert "Day Count" in count_df.columns
    assert count_df.shape[0] == 5
    check_fri = count_df[(count_df["Day"] == "Fri") & (count_df["Day Count"] == 2)]
    assert check_fri.shape[0] == 1
    return
       
def test_dict_of_count_dfs():
    """ Tests if the dict_of_count_dfs function correctly creates a \n
    dictionary of count dataframes """
    test_df = {"Day": ["Mon", "Tues", "Fri", "Thurs", "Fri", "Mon"], \
               "Week": [1, 2, 3, 4, 5, 6], "score": [4, 10, 15, 25, 13, 20]}
    test_df = pd.DataFrame(test_df)
    add_severity_column({"Small": (0, 9), "Medium": (10, 19), "Large": (20, 39)}, \
                        "score", test_df)
    dict_dfs = dict_of_count_dfs(test_df)
    assert len(dict_dfs) == 3
    assert list(dict_dfs.keys()) == ["Day", "Week", "score"]
    assert "Week Count" in dict_dfs["Week"].columns
    return 