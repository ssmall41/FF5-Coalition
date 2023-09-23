from copy import copy
import numpy as np
from numpy.linalg import norm
from numpy.random import randint


def select_parties_randomly(valid_parties: list, num_parties: int = 10, eps: float = 1.0,
                            verbose: bool = False) -> list:
    """ Given a selection of parties, select num_parties which are intended to be played. This selects
    the parties randomly. The argument valid_parties should be of the party embedding format:
    [("job1,job2,job3,job4", embedding), (), ...]
    however, the embedding field is not use. Passing the embedding here is sometimes useful for later analyses.

    :param valid_parties: a list of party embeddings. Must be of the form
    [("job1,job2,job3,job4", embedding), (), ...]
    :param num_parties: the number of parties to select
    :param eps: unused parameter
    :param verbose: print logging info?
    :return: the list of selected parties
    """

    if num_parties > len(valid_parties):
        num_parties = len(valid_parties)
        if verbose:
            print(f"Notice: num_parties was larger than the number of valid parties. "
                  f"Setting num_parties to {num_parties}.")

    chosen_party_indices = randint(0, len(valid_parties), size=(num_parties, ))
    selected_parties = [valid_parties[i] for i in chosen_party_indices]

    return selected_parties


def select_parties_by_embeddings(valid_parties: list, num_parties: int = 10, eps: float = 1.0,
                                 verbose: bool = False) -> list:
    """ Given a selection of party embeddings, select num_parties which are intended to be played. This
    uses the embeddings in the selection process. The first party is selected at random. Further parties
    are selected so that they more than eps away (in 2-norm) from any other selected party.
    While selecting parties, it's possible that all previously selected parties cover the remaining parties.
    If this happens, eps is automatically reduced. So the eps provided can be thought of as a "starting" value.
    
    In general, the higher the value of eps, the more diversity in selected parties.

    :param valid_parties: a list of party embeddings. Must be of the form 
    [("job1,job2,job3,job4", embedding), (), ...]
    :param num_parties: the number of parties to select
    :param eps: the distance all selected parties must be from each other, to start
    :param verbose: print logging info?
    :return: the list of selected parties
    """

    available_parties = copy(valid_parties)
    selected_parties = []
    unavailable_parties = []

    if num_parties > len(valid_parties):
        num_parties = len(valid_parties)
        if verbose:
            print(f"Notice: num_parties was larger than the number of valid parties. "
                  f"Setting num_parties to {num_parties}.")
    
    for idx_party in range(0, num_parties):

        # Select a party
        chosen_party_idx = randint(0, len(available_parties))
        selected_parties.append(available_parties[chosen_party_idx])
        available_parties[chosen_party_idx] = available_parties[-1]
        available_parties.pop()
        
        # Organize the available parties by whether they are close to the chosen party or not
        close_parties, far_parties = organize_parties(selected_parties[-1][1], available_parties, eps)
        available_parties = far_parties
        unavailable_parties += close_parties

        # Make sure there are still parties available. If not, decrease eps.
        if len(selected_parties) != len(valid_parties):
            while len(available_parties) == 0:
                eps *= 0.8
                available_parties = unavailable_parties  # Make all remaining parties available again
                unavailable_parties = []

                if verbose:
                    print("Notice: Available parties are too close to selected parties.")
                    print(f"Trying eps = {eps} for party {idx_party+1}")
                
                # Make parties unavailable again if they are too close to an already selected party
                for selected_party in selected_parties:
                    close_parties, far_parties = organize_parties(selected_party[1], available_parties, eps)
                    available_parties = far_parties
                    unavailable_parties += close_parties

    return selected_parties


def organize_parties(chosen_party_embedding: np.ndarray, available_parties: list, eps: float = 1.0) -> (list, list):
    """ Given a chosen party and a list of available parties, separate out the parties that are too close
    to the chosen party. Close is defined by an embedding on each party such that the 2-norm is within eps.
    :param chosen_party_embedding: the embedding of the chosen party
    :param available_parties: the parties that are available to be chosen
    :param eps: the distance that defines whether two parties are close
    :return: the parties (with their embedding) that are within eps of the chosen party, and the parties
    that are further than eps away. If a party is exactly eps from the chosen party, then it's considered far.
    """
    close_parties = []
    far_parties = []

    for party_idx, party_embedding in available_parties:
        if norm(chosen_party_embedding - party_embedding, ord=2) < eps:
            close_parties.append((party_idx, party_embedding))
        else:
            far_parties.append((party_idx, party_embedding))

    return close_parties, far_parties
