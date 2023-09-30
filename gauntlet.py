import pandas as pd
from numpy.random import randint


def generate_gauntlet_runs(run_style: str, df_jobs: pd.DataFrame) -> list:
    """ Generate a gauntlet run. This generates a coalition of parties in such a way as to select jobs uniquely. Of
    course, the last party will not have enough "new" jobs, so some old one will be selected. df_jobs should come from
    a call to data.load_data. The number of parties in the coalition is determined by the run_style, probably 6.

    :param run_style: the style of the run, currently only "Regular" and "Meteor"
    :param df_jobs: the DataFrame of jobs. Only the index is used.
    :return: a list of lists containing each chosen party in the coalition
    """

    num_jobs_in_party = 4  # 4 characters => 4 jobs

    if run_style == "Regular":

        num_parties = 6
        selected_parties = []
        crystal_order = ["Wind", "Water", "Fire", "Earth"]
        jobs_by_crystal = [list(
            df_jobs[df_jobs["Crystal"] == crystal_order[i]].index) for i in range(4)]

        for party_idx in range(num_parties):

            party = []
            for i in range(num_jobs_in_party):

                # Refresh the job lists, if they're empty
                if len(jobs_by_crystal[i]) == 0:
                    jobs_by_crystal[i] = list(
                        df_jobs[df_jobs["Crystal"] == crystal_order[i]].index)

                # Assign jobs from each crystal
                job = jobs_by_crystal[i][randint(0, len(jobs_by_crystal[i]))]
                party.append(job)
                jobs_by_crystal[i].remove(job)

            selected_parties.append(party)

    elif run_style == "Meteor":

        num_parties = 6
        selected_parties = []
        available_jobs = list(df_jobs.index)

        for party_idx in range(num_parties):
            party = []
            for i in range(num_jobs_in_party):
                if len(available_jobs) == 0:
                    available_jobs = list(df_jobs.index)
                job = available_jobs[randint(0, len(available_jobs))]
                party.append(job)
                available_jobs.remove(job)

            selected_parties.append(party)

    else:
        raise ValueError(f"Bad game style {run_style}.")

    return selected_parties
