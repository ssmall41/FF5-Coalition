from typing import Callable
import numpy as np
from numpy.linalg import norm


def run_trials(valid_parties_embeddings: list, num_parties: int, num_trials: int, eps: float,
               selector: Callable) -> list:
    """ Select a collection of num_parties, num_trials times. This returns the selected parties for
    each trial, as well as the comparison matrix for each party.

    selector is a method that selects a party. The signature must be:
        (valid_parties: list, num_parties: int = 10, eps: float = 1.0)

    :param valid_parties_embeddings: the embedding list for all valid parties
    :param num_parties: the number of parties to select in each trial
    :param num_trials: the number of trials
    :param eps: the value of eps to use for the definition of close in each trial
    :param selector: the method for selecting a party
    :return: a list of tuples. Each tuple contains a list of select parties and the comparison
    matrix.
    """
    trials = []
    for t in range(num_trials):
        print(f"Trial {t} #######")
        selected_parties = selector(valid_parties_embeddings, num_parties, eps)
        comparison_matrix = generate_comparison_matrix(selected_parties)
        
        trials.append(([p[0] for p in selected_parties], comparison_matrix))
    return trials


def generate_comparison_matrix(selected_parties: list) -> np.ndarray:
    """ Generates a matrix that shows the distance of each party in selected_parties from each
    other, in terms of the 2-norm of their embeddings. This is helpful for analyses.
    :param selected_parties: embedding list of the form [("job1,job2,job3,job4", embedding), (), ...]
    :return: the matrix of distances of each job to each other job
    """

    comparison_matrix = np.zeros((len(selected_parties), len(selected_parties)), dtype=float)
    
    for row_idx, row_tuple in enumerate(selected_parties):
        for col_idx, col_tuple in enumerate(selected_parties):
            _, embedding_row = row_tuple
            _, embedding_col = col_tuple
            comparison_matrix[row_idx][col_idx] = norm(embedding_row - embedding_col, ord=2)
    return comparison_matrix
