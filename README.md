# Bayesian-Monopolist (DS 6014 Final Project)

#### Aneesh Sandhir, Logan Yoonhyuk Lee, Taeheon Park

Monopoly is an interactive allegory designed to teach participants about the dangers monopolies pose to society and the perils of Laissez-faire economic policy. Since the game was developed the economic system it was commenting on has mutated into one which incentivizes the incarceration of millions of people to provide the prison industrial complex with an absurdly cheap or free workforce. As such we want to amend the game of monopoly such that jail can be owned like any other utility or railroad. That is to say it cannot be improved upon but rents will be assessed to every player who occupies jail for every turn they do so. The price of the jail space will be a function of the probability of landing in jail, the number of turns needed to recoup the jail owners investment such that it is competitive with that of other properties, and the rent the jail charges. Since Monopoly has been well studied for being played with six sided dice, we plan to develop the probabilities of visiting a given property and the rate of return of said property as a function of die size. 

Steps of the Jupyeter Notebook file

1. Set the number of side of dies and speed limit (number of doubles before the player go to jail). Standard game rule is 6 die and 3 speedlimit. The only tuning variables are these two. Everything else will be changed automatically according to the setting.
2. Two probabilities distribution
3. Markov chain and Transition Matrices for two strategies (short stay in jail and long stay in jail)
4. Network graphs 
5. Probabilities for all spaces of the board with the markov chain result
6. Calculate the expected income and return on investment
7. Estimate the lot price for jail
