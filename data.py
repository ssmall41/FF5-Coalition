import pandas as pd

def load_data(filename: str) -> pd.DataFrame:
    """ Loads a csv file with the job definitions. The csv file must have a column called "Job" which
    is a string representing the job. This will be the index of the returned DataFrame. The column names
    for the stats, crystal, and style are defined below. All other columns form the equipment columns.
    :param filename: the filename of the csv file to load
    :return: the DataFrame containing the contents of the csv file with job information.
    """
    
    df_jobs = pd.read_csv(filename, index_col="Job")
    stat_cols = ["Strength", "Agility", "Vitality", "Magic"]
    crystal_col = "Crystal"
    style_col = "Style"

    assert set([crystal_col, style_col] + stat_cols).issubset(df_jobs.columns)

    return df_jobs, stat_cols

def save_party_embeddings(filename: str, embeddings: list):
    """ Saves a list of party embeddings to a csv file. The embedding list is of the form
    [("job1,job2,job3,job4", [v1,v2,v3,...]), ()...].
    :param filename: the filename to save the embeddings
    :param embeddings: the embedding list to save
    """

    df = pd.DataFrame(data=[t[1] for t in embeddings], index=[t[0] for t in embeddings])
    df.to_csv(filename)

def load_party_embeddings(filename: str):
    """ Loads a set of party embeddings from a csv file. The csv file is assumed to have the same
    format as save_party_embeddings.
    :param filename: the filename with the party embeddings to load
    """

    df_embeddings = pd.read_csv(filename, index_col=0)
    embeddings = _dataframe_to_tuple_array(df_embeddings)
    return embeddings

#def embeddings_to_dataframe(embeddings: list):
#    """ Converts embeddings from valid parties to a dataframe. Saving and loading is easier. """
#    
#    df = pd.DataFrame(data=[t[1] for t in valid_parties_embeddings], index=[t[0] for t in valid_parties_embeddings])
#    return df

def _dataframe_to_tuple_array(df_embeddings):
    tuple_array = []
    for idx, row in df_embeddings.iterrows():
        tuple_array.append((idx, row.to_numpy()))
    return tuple_array
