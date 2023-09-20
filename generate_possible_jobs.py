import pandas as pd


def generate_possible_parties(run: str, df_jobs: pd.DataFrame, stat_cols: list, duplicates: bool = False) -> list:
    """ Generate the list of all possible parties given a particular Four Job Fiesta style. These
    are consistent with the definitions on the event pages as of 19.09.23. See:
    https://www.fourjobfiesta.com/help.php

    The generated jobs are returned in a list of tuples with each tuple of the form:
    [["Job1", "Job2", "Job3", "Job4"], [...], ...]

    :param run: the Four Job Fiesta run style ("Regular", "Typhoon", "Volcano", or "Meteor").
    :param df_jobs: the DataFrame of jobs data
    :param stat_cols: the columns in df_jobs holding the stats
    :param duplicates: flag to allow duplicates. Doesn't do anything for Regular runs.
    :return: the generated jobs
    """

    valid_parties = []

    if run == "Meteor":
        for idx1, job1 in df_jobs[stat_cols].iterrows():
            for idx2, job2 in df_jobs[stat_cols].iterrows():
                for idx3, job3 in df_jobs[stat_cols].iterrows():
                    for idx4, job4 in df_jobs[stat_cols].iterrows():
                        valid_parties.append([idx1, idx2, idx3, idx4])
    else:
        raise ValueError(f"Bad game style {run}.")

    if not duplicates:
        valid_parties_no_duplicates = []
        for party in valid_parties:
            if len(party) == len(set(party)):
                valid_parties_no_duplicates.append(party)
        valid_parties = valid_parties_no_duplicates

    return valid_parties
