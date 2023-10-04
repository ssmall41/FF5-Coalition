import pandas as pd
from numpy.random import randint


def generate_gauntlet_runs(run_style: str, df_jobs: pd.DataFrame) -> list:
    """ Generate a gauntlet run of 5 parties. This generates a group of parties in such a way as to select jobs
    uniquely. Of course, the last party will not have enough "new" jobs, so some old one will be selected. df_jobs
    should come from a call to data.load_data.

    For Regular runs, one job from the Wind crystal is moved to the Earth crystal.

    Note that Mime and Freelancer are excluded.

    :param run_style: the style of the run, currently only "Regular" and "Meteor"
    :param df_jobs: the DataFrame of jobs. Only the index is used.
    :return: a list of lists containing each chosen party in the coalition
    """

    num_parties = 5
    num_jobs_in_party = 4  # 4 characters => 4 jobs
    crystal_order = ["Wind", "Water", "Fire", "Earth"]
    wind_crystal_idx = crystal_order.index("Wind")
    earth_crystal_idx = crystal_order.index("Earth")

    if run_style == "Regular":

        selected_parties = []

        # Set the available jobs to choose at each crystal, moving one job from Wind to Earth
        jobs_by_crystal = [list(df_jobs[df_jobs["Crystal"] == crystal_order[i]].index) for i in range(4)]
        wind_to_earth_job = jobs_by_crystal[wind_crystal_idx][randint(0, len(jobs_by_crystal[wind_crystal_idx]))]
        jobs_by_crystal[wind_crystal_idx].remove(wind_to_earth_job)
        jobs_by_crystal[earth_crystal_idx].append(wind_to_earth_job)

        for party_idx in range(num_parties):

            party = []
            for i in range(num_jobs_in_party):
                # Assign jobs from each crystal
                job = jobs_by_crystal[i][randint(0, len(jobs_by_crystal[i]))]
                party.append(job)
                jobs_by_crystal[i].remove(job)

            selected_parties.append(party)

    elif run_style == "Meteor":

        selected_parties = []
        available_jobs = list(df_jobs[df_jobs["Crystal"] != "Misc"].index)

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
