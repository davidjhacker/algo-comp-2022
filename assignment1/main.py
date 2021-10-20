#!usr/bin/env python3
import json
import sys
import os

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses


# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    # YOUR CODE HERE
    from scipy.stats import binom

    gender_score = 0

    if user1.gender in user2.preferences and user2.gender in user1.preferences:
    	gender_score = 1

    year_score = 1 - abs(user1.grad_year - user2.grad_year) / 4

    response_matches = 0

    for i in range(0, len(user1.responses)):
    	if user1.responses[i] == user2.responses[i]:
    		response_matches += 1

    response_score = binom.cdf(k = response_matches, n = len(user1.responses), p = 0.2)

    return response_score * gender_score * year_score


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
