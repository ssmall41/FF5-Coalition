import numpy as np

def calculate_job_embedding(chosen_party, df_jobs, stat_cols, equip_factor=1.0):
    """ Uses style and equipment.
    !!!! The naming here is crap !!!!
    """
    
    crystal_order = ["Wind", "Water", "Fire", "Earth"]
    crystal_col = "Crystal"
    num_crystals = 4
    style_order = ["Heavy", "Clothes", "Mage", "Misc"]
    num_styles = 4  # Heavy, Clothes, Mage
    equip_cols = df_jobs.columns[6:]  # Crystal + Style + stat_cols
    style_col = "Style"
    available_equip_embeddings = []
    
    for curr_crystal in range(0, num_crystals):
        
        equip_embedding = np.zeros((len(equip_cols), ), dtype=int)
        style_embedding = np.zeros((num_styles, ), dtype=float)
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
            available_equip_embeddings.append(
                np.concatenate([style_embedding * 0.25, equip_embedding.astype(float) * equip_factor]))
        else:
            style_embedding[style_order.index("Misc")] = 0.25  # Add a Freelancer
            available_equip_embeddings.append(
                np.concatenate([style_embedding, 
                               df_jobs.loc["Freelancer"][equip_cols].to_numpy().astype(float) * equip_factor]))

    return np.concatenate(available_equip_embeddings)


def calculate_stats_embedding(chosen_party, df_jobs, stats_cols, max_values):
    """ Calculate the embeddings for the stats. We'll just sum them up over the jobs in the party
    and standardize them to be between -1 and 1. """

    stats_embedding = np.zeros((len(stats_cols), ), dtype=float)
    
    for job in chosen_party:
        stats_embedding += df_jobs.loc[job][stats_cols].to_numpy().astype(float)

    return stats_embedding / max_values


def get_crystal_idx(job, df_jobs, crystal_order, crystal_col):

    if job == "Freelancer":
        crystal_idx = -1
    elif job == "Mime":
        crystal_idx = 4
    else:
        crystal_idx = crystal_order.index(df_jobs.loc[job][crystal_col])
    return crystal_idx
    
