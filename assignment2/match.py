import numpy as np
from typing import List, Tuple

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """

    #editing scores to account for preferences
    compatibility_matrix = []

    for pref in gender_pref:
        matrix_row = []
        for gender in gender_id:
            if ((pref == 'Men' and gender == 'Female') or (pref == 'Women' and gender == 'Male')):
                matrix_row.append(0)
            else:
                matrix_row.append(1)
        compatibility_matrix.append(matrix_row)

    updated_scores = np.multiply(scores, compatibility_matrix)

    rank_matrix = np.argsort(-1*updated_scores)

    #establishing proposers
    random_indices = np.random.choice(10, size=5, replace=False)
    
    #person class
    class Person:
        def __init__(self, index, ranks, isProposer, isFree, isMatchedWith):
            self.index = index
            self.ranks = ranks
            self.isProposer = isProposer
            self.isFree = isFree
            self.isMatchedWith = isMatchedWith


    free_proposer_list = []
    proposed_list = []

    #initiating proposers and proposers
    matches = []
    for i in range(10):
        if i in random_indices:
            free_proposer_list.append(Person(i, rank_matrix[i], True, True, None))
        else:
            proposed_list.append(Person(i, rank_matrix[i], False, True, None))
            
    #gale shapley
    while free_proposer_list != []:
        p1 = free_proposer_list[0]
        pref_index = p1.ranks[0]
        p1.ranks = np.delete(p1.ranks, 0)
        p2 = None
        for person in proposed_list:
            if person.index == pref_index:
                p2 = person

        if p2 != None:
            if p2.isFree == True:
                matches.append((p1.index, p2.index))
                p1.isFree = False
                p2.isFree = False
                p2.isMatchedWith = p1
                p1.isMatchedWith = p2
                free_proposer_list.remove(p1)
            else:
                current_match = p2.isMatchedWith
                if np.where(p2.ranks == p1.index) < np.where(p2.ranks == current_match.index):
                    matches.append((p1.index, p2.index))
                    matches.remove((current_match.index, p2.index))
                    p1.isFree = False
                    p2.isFree = False
                    p2.isMatchedWith = p1
                    p1.isMatchedWith = p2
                    current_match.isMatchedWith = None
                    current_match.isFree = True
                    free_proposer_list.remove(p1)
                    free_proposer_list.append(current_match)
    
    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
