import pandas as pd


def generate_possible_parties(run: str, df_jobs: pd.DataFrame, duplicates: bool = False) -> list:
    """ Generate the list of all possible parties given a particular Four Job Fiesta style. These
    are consistent with the definitions on the event pages as of 19.09.23. See:
    https://www.fourjobfiesta.com/help.php

    The generated jobs are returned in a list of tuples with each tuple of the form:
    [["Job1", "Job2", "Job3", "Job4"], [...], ...]

    :param run: the Four Job Fiesta run style ("Regular", "Typhoon", "Volcano", or "Meteor").
    :param df_jobs: the DataFrame of jobs data
    :param duplicates: flag to allow duplicates. Doesn't do anything for Regular runs.
    :return: the generated jobs
    """

    valid_parties = []

    if run == "Regular":
        for job1 in df_jobs[df_jobs["Crystal"] == "Wind"].index:
            for job2 in df_jobs[df_jobs["Crystal"] == "Water"].index:
                for job3 in df_jobs[df_jobs["Crystal"] == "Fire"].index:
                    for job4 in df_jobs[df_jobs["Crystal"] == "Earth"].index:
                        valid_parties.append([job1, job2, job3, job4])
    elif run == "Meteor":
        for job1 in df_jobs.index:
            for job2 in df_jobs.index:
                for job3 in df_jobs.index:
                    for job4 in df_jobs.index:
                        valid_parties.append([job1, job2, job3, job4])
    else:
        raise ValueError(f"Bad game style {run}.")

    if not duplicates and not run == "Regular":
        valid_parties_no_duplicates = []
        for party in valid_parties:
            if len(party) == len(set(party)):
                valid_parties_no_duplicates.append(party)
        valid_parties = valid_parties_no_duplicates

    return valid_parties
