from functools import partial
from multiprocessing import Pool
import numpy as np
from numpy.linalg import norm
from typing import Callable


def run_trials(valid_parties_embeddings: list, num_parties: int, num_trials: int, eps: float, selector: Callable,
               should_generate_matrix: bool = False, verbose: bool = False, num_procs: int = 1) -> list:
    """ Select a collection of num_parties, num_trials times. This returns the selected parties for
        each trial, as well as the comparison matrix for each party. If should_generate_matrix is False, then
        None is returned for the matrices.

        selector is a method that selects a party. The signature must be:
            (valid_parties: list, num_parties: int = 10, eps: float = 1.0)

        :param valid_parties_embeddings: the embedding list for all valid parties
        :param num_parties: the number of parties to select in each trial
        :parameter num_trials: the number of groups of parties to create
        :param eps: the value of eps to use for the definition of close in each trial
        :param selector: the method for selecting a party
        :param should_generate_matrix: should the comparison matrices be generated?
        :param verbose: print information
        :param num_procs: the number of processes to use when creating trials
        :return: a list of tuples. Each tuple contains a list of select parties and the comparison
        matrix.
        """

    with Pool(num_procs) as p:
        funcy = partial(run_trial,
                        valid_parties_embeddings=valid_parties_embeddings,
                        num_parties=num_parties,
                        eps=eps,
                        selector=selector,
                        should_generate_matrix=should_generate_matrix,
                        verbose=verbose)
        trials = p.map(funcy, range(num_trials))

    return trials


def run_trial(trial_num: int, valid_parties_embeddings: list, num_parties: int, eps: float, selector: Callable,
              should_generate_matrix: bool = False, verbose: bool = False) -> tuple:
    """ Select a collection of num_parties. This returns the selected party and the comparison matrix, if desired. If
    the comparison matrix is not created, None is returned for the matrix. selector is
    a method that selects a party. The signature must be:
        (valid_parties: list, num_parties: int = 10, eps: float = 1.0)

    :param trial_num: the id of the trial. Sometimes useful for logging, especially for parallel runs.
    :param valid_parties_embeddings: the embedding list for all valid parties
    :param num_parties: the number of parties to select in each trial
    :param eps: the value of eps to use for the definition of close in each trial
    :param selector: the method for selecting a party
    :param should_generate_matrix: should the comparison matrix be calculated?
    :param verbose: print additional logging info
    :return: a list of the select parties and the comparison matrix
    """

    if verbose:
        print(f"trial {trial_num}")

    selected_parties = selector(valid_parties_embeddings, num_parties, eps)
    if should_generate_matrix:
        comparison_matrix = generate_comparison_matrix(selected_parties)
    else:
        comparison_matrix = None

    return [p[0] for p in selected_parties], comparison_matrix


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
