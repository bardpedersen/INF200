"""
Compute number of mandates for each party based on the modified Sainte-Laguë rule.

The rule works as follows:
1. Each party receives a score equal to the number of votes received divided by 1.4.
2. All parties are sorted in descending order of scores.
3. The party with the largest score is then
   a. assigned a seat
   b. receives a new score, which is its number of votes divided by 3.
4. The process continues with point 2, successively using divisors 3, 5, 7, ..., until
   all seats have been assigned.

Note that divisors are increased independently for each party.

Expected results from this code are:

    A, H: 5 mandates each
    FRP, SP: 2 mandates each
    MDG, RØDT, SV, V: 1 mandate each

Høyre has six mandates from Akershus in total in the current Storting because they were allocated
the utjevningsmandat for Akershus.
"""

import pandas as pd
import random as rd


class Party:
    def __init__(self, party, votes):
        self.party = party
        self.votes = votes
        self.score = votes / 1.4
        self.next_div = 3
        self.seats = 0

    # function that updates the score and next div

    def update_score(self):
        self.score = self.votes / self.next_div
        self.next_div += 2
        self.seats += 1

def partyandmandates(election_results, num_mandates):
    # Seats allocated to Akershus district. One seat is reserved for an utjevningsmandat
    # (ensures better proprotional representation on the national level). Here, only the
    # remaining "distriktsmandater" are distributed.
    num_district_mandates = num_mandates - 1

    # creates a party object for each party and adds it to parties list
    parties = []
    for row in election_results.itertuples():
        party = Party(row.Party, row.Votes)
        parties.append(party)

    # Create a record for each party containing the party name, the number of votes received,
    # the initial score according to point 1, and the divisor for the next division (points 3.b and 4)
    seats_taken = 0
    while seats_taken < num_district_mandates:
        # Ensure data is sorted in descending order of scores
        parties.sort(key=lambda x: x.score, reverse=True)
        """
        First entry in sorted list wins the mandate
        if test that determines if the there is a draw
        it checks if the num of votes is  equal
        the winner is chosen by random
        """
        if parties[0].score == parties[1].score:
            if parties[0].votes == parties[1].votes:
                winner = parties[rd.randint(0, 1)]
            elif parties[0].votes <= parties[1].votes:
                winner = parties[1]
            else:
                winner = parties[0]

        else:
            winner = parties[0]
        seats_taken += 1
        # Register seat won
        winner.update_score()

    parties.sort(key=lambda x: x.seats, reverse=True)  # Sort by mandates

    parti_dict = {}
    for party in parties:
        mandat_stemmer_dict = {'Mandat': party.seats, 'Stemmer': party.votes}
        parti_dict[party.party] = mandat_stemmer_dict

    return parti_dict


if __name__ == '__main__':
    NUM_MANDATES = 19  # Number of mandates
    df_election_results = pd.read_csv('result_akershus_2021.csv')  # Read example data from CSV file into DataFrame
    print(partyandmandates(df_election_results, NUM_MANDATES))
