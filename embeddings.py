import pandas as pd
import numpy as np


def calculate_party_embeddings(valid_parties: list, df_jobs: pd.DataFrame,
                               stat_cols: list, special_weight_jobs: list = None, equip_factor: float = 1.0) -> list:
    """ Go through each valid party and calculate the embeddings for each party. The return value
    is an embedding list with one row per valid party of the form
    [("job1,job2,job3,job4", [v1,v2,v3,...]), ()...].
    :param valid_parties: a list of parties that are possible
    :param df_jobs: the DataFrame of job's data
    :param stat_cols: a list of the column names in df_jobs for stats
    :param special_weight_jobs: double the weight of these jobs
    :param equip_factor: the weight to give the embeddings for equipment
    :return: the embedding list
    """

    counter = 0
    valid_parties_embeddings = []

    # For the stats embedding, calculate the max values of each stat
    # Divide by 4 to keep the values between -1 and 1
    #max_values = abs(df_jobs[stat_cols]).max() * 4.0
    
    for chosen_party in valid_parties:

        # Provide some output so we know things are working
        if counter % 10000 == 0:
            print(f"On {counter} / {len(valid_parties)}")
        counter += 1

        # Calculate the stats embeddings
        #stats_embedding = calculate_stats_embedding(chosen_party, df_jobs, stat_cols, max_values)

        # Calculate the style and equipment embeddings
        style_equip_embedding = calculate_style_equip_embedding(chosen_party, df_jobs, equip_factor)

        # Calculate the jobs embeddings
        jobs_embedding = calculate_jobs_embedding(chosen_party, df_jobs, special_weight_jobs)
        
        # Put the embeddings together
        valid_parties_embeddings.append(
            (",".join(chosen_party), 
             np.concatenate([style_equip_embedding, jobs_embedding])))

    return valid_parties_embeddings


def calculate_style_equip_embedding(chosen_party: list, df_jobs: pd.DataFrame, equip_factor: float = 1.0) -> np.ndarray:
    """ Calculate embeddings based on the style and equipment for the chosen party.
    For style, this computes the number of jobs of each style (heavy, clothes, mage, misc) in the
    party and multiplies by 0.25, keeping values between 0.0 and 1.0.
    
    For equipment, this uses a 0 or 1 for each equipment type that a job in the party can use, 
    per crystal. The value for each equipment is always boolean, so if multiple jobs can use e.g.
    knives after the Fire Crystal, the embedding at the Fire Crystal for knives will be 1. This 
    embedding DOES consider that jobs can be assigned but not available. For example, if the chosen 
    party is ["Ninja", "Knight", "Red Mage", "Dragoon"], the embedding will assume the party is 
    only Freelancers for the Wind Crystal. Then at the Water Crystal, it assumes the party is 
    only Knights.

    The equip_factor scales the importance of the equipment in the embedding. Smaller means 
    less important, and 1.0 means to not scale at all. This is a hyperparameter to tune: values of
    1.0 tend to encourage Freelancers in parties with Meteor runs, while smaller values give a 
    bit more diversity. 
    
    :param chosen_party: list of jobs in the party, e.g. ["Knight", "Red Mage", "Ninja", "Dragoon"]
    :param df_jobs: the DataFrame with data on each job
    :param equip_factor: the scaling factor for the equipment embeddings
    :return: the embeddings for style and equipment for the chosen party
    """
    
    crystal_order = ["Wind", "Water", "Fire", "Earth"]
    crystal_col = "Crystal"
    style_order = ["Heavy", "Clothes", "Mage", "Misc"]
    style_col = "Style"
    
    equip_cols = df_jobs.columns[6:]  # Crystal + Style + stat_cols + equip_cols
    available_embeddings = []
    
    for curr_crystal in range(0, len(crystal_order)):
        
        equip_embedding = np.zeros((len(equip_cols), ), dtype=int)
        style_embedding = np.zeros((len(style_order), ), dtype=float)
        is_any_job_available = False

        # We have available all jobs through curr_crystal available
        for job_idx in range(0, curr_crystal+1):
            job = chosen_party[job_idx]
            crystal_idx = get_crystal_idx(job, df_jobs, crystal_order, crystal_col)
            if crystal_idx <= curr_crystal:

                is_any_job_available = True

                # Set the style embedding
                job_style = df_jobs.loc[job][style_col]
                style_embedding[style_order.index(job_style)] += 1.0
                
                # Set the equipment embedding
                job_equip_embedding = df_jobs.loc[job][equip_cols].to_numpy()
                equip_embedding = np.logical_or(job_equip_embedding, equip_embedding)

        # If no jobs are available, then every character is a freelancer
        if is_any_job_available:
            available_embeddings.append(
                np.concatenate([style_embedding * 0.25, equip_embedding.astype(float) * equip_factor]))
        else:
            style_embedding[style_order.index("Misc")] = 0.25  # Add a Freelancer
            equip_embedding = df_jobs.loc["Freelancer"][equip_cols].to_numpy(dtype=float) * equip_factor
            available_embeddings.append(
                np.concatenate([style_embedding, equip_embedding]))

    return np.concatenate(available_embeddings)


def calculate_stats_embedding(chosen_party: list, df_jobs: pd.DataFrame, stat_cols: list,
                              max_values: np.ndarray or None = None) -> np.ndarray:
    """ Calculate the embeddings for the stats. We'll just sum them up over the jobs in the party
    and dividing them by max_values.
    :param chosen_party: list of jobs in the party, e.g. ["Knight", "Red Mage", "Ninja", "Dragoon"]
    :param df_jobs: the DataFrame with data on each job
    :param stat_cols: the column names in df_jobs of the stats
    :param max_values: values used to scale the stats embeddings. If None, then the maximum
    values found in df_jobs is used.
    :return: the embedding for the stats
    """

    stats_embedding = np.zeros((len(stat_cols), ), dtype=float)

    if max_values is None:
        # For the stats embedding, calculate the max values of each stat
        # Divide by 4 to keep the values between -1 and 1
        max_values = abs(df_jobs[stat_cols]).max() * 4.0

    assert len(stat_cols) == max_values.shape[0]
    
    for job in chosen_party:
        stats_embedding += df_jobs.loc[job][stat_cols].to_numpy().astype(float)

    return stats_embedding / max_values


def calculate_jobs_embedding(chosen_party: list, df_jobs: pd.DataFrame, special_weight_jobs: list = None):
    """ Checks the jobs in the chosen party and turns this info into an embedding. The embedding
    contains one 0/1 value for each job (order is the same as df_jobs). Note that duplicate jobs
    do not increase the value beyond 1, otherwise duplicate jobs would be heavily favored. Jobs
    in double_weight_jobs have their weights multiplied by 2. This discourages selecting jobs
    after they've already been selected once.

    :param chosen_party: list of jobs in the party, e.g. ["Knight", "Red Mage", "Ninja", "Dragoon"]
    :param df_jobs: the DataFrame with data on each job
    :param special_weight_jobs: jobs to weight double
    :return: the embedding for the stats
    """

    jobs_embedding = np.zeros((len(df_jobs), ), dtype=float)
    for job in chosen_party:
        idx = np.where((df_jobs.index == job))[0][0]
        if job in special_weight_jobs:
            jobs_embedding[idx] = 0.1
        else:
            jobs_embedding[idx] = 1.0

    return jobs_embedding


def get_crystal_idx(job: str, df_jobs: pd.DataFrame, crystal_order: list, crystal_col: str) -> int:
    """ Get the index of the crystal that a given job belongs to, where the order of the crystals is 
    defined in crystal_order.
    For example, in the actual game, Knight -> Wind Crystal -> 0, Berserker -> Water Crystal -> 1.
    :param job: the job as a string: "Knight", "White Mage", "Freelancer", etc.
    :param df_jobs: the DataFrame of jobs data
    :param crystal_order: the list of crystals defining their order. Probably
    ["Wind", "Water", "Fire", "Earth"]
    :param crystal_col: the column in df_jobs with crystal for each job
    :return: the index in crystal_order for the crystal of the given job
    """
    
    if job == "Freelancer":
        crystal_idx = -1
    elif job == "Mime":
        crystal_idx = 4
    else:
        crystal_idx = crystal_order.index(df_jobs.loc[job][crystal_col])
    return crystal_idx
