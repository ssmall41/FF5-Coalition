import numpy as np
import pandas as pd


def generate_possible_jobs(style: str, df_jobs: pd.DataFrame, stat_cols: list) -> list:
    """ Generate the list of all possible parties given a particular Four Job Fiesta style. These
    are consistent with the definitions on the event pages as of 19.09.23. See:
    https://www.fourjobfiesta.com/help.php

    The generated jobs are returned in a list of tuples with each tuple of the form:
    ("Job1,Job2,Job3,Job4", np.ndarray([val,val,val,...]))

    :param style: the Four Job Fiesta style ("Regular", "Typhoon", "Volcano", or "Meteor").
    :param df_jobs: the DataFrame of jobs data
    :param stat_cols: the columns in df_jobs holding the stats
    :return: the generated jobs with their embeddings
    """

    valid_jobs = []

    if style == "Meteor":
        for idx1, job1 in df_jobs[stat_cols].iterrows():
            for idx2, job2 in df_jobs[stat_cols].iterrows():
                for idx3, job3 in df_jobs[stat_cols].iterrows():
                    for idx4, job4 in df_jobs[stat_cols].iterrows():

                        valid_jobs.append([idx1, idx2, idx3, idx4])
                        
                        #party_index = ",".join([idx1, idx2, idx3, idx4])
                        #party_embedding = np.concatenate((job1.to_numpy(), job2.to_numpy(), job3.to_numpy(), job4.to_numpy()))
                        #valid_jobs.append((party_index, party_embedding))
    else:
        raise ValueError(f"Bad game style {style}.")

    return valid_jobs
