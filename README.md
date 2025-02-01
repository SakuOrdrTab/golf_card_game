# Golf

--------------------------------------------------------------------------
IMPORTANT NOTE: The main branch is currently inactive. The One-phase-RL is
active, as I had to make the decision process more simple for the RL agent 
to learn.
--------------------------------------------------------------------------

Card game to test deep neural networks as computer players. Wrap ComputerPlayer class so, that it can be run as adversial network against itself and train.

## The card game rules

The actual game played isn't the Wikipedia official version (https://en.wikipedia.org/wiki/Golf_(card_game)), but a variant.

There is one deck, so the number of players can be two to three. Each card is valued 0 (King) to 12 (Queen), other cards are their nominal value (J = 11, 2 = 2, Ace = 1 etc). The purpose of the game is to get as low sum of table cards in the end, whether they are already visible or not.

The game sequence:

1. Each player is dealt 9 cards on the table in three rows, thus there are 3 nonvisible cards in a row.

2. Each player can turn one arbitrary card visible on each row, thus altogether three cards.

3. One card is turned from the drawing deck to the played deck, which is visible for the top card. Random player begins.

4. Player draws a card either from the drawing deck, or the top card of the played cards' deck.

5. Player either plays the card to the table replacing the table card, or discards the previously drawn card to the played deck. The table card can be visible, or still nonvisible unturned card. The card played to the table is visible. If all three cards are visible and of same value, the row of cards are removed from the play - this is of course highly desirable

5. Another player's turn begins and this continues until come player has all their table cards turned visible.

6. After that, the remaining players have still their turns.

7. The score is calculated and the player with least score wins.

## Notes on training the reinforcement training agents

The training happens using the GolfTrainEnv quite simply using the mantest_golftrainenv.py using the stable baselines 3.
To be noted is that the AdvancedComputerPlayer using some rules to play is quite skillfull, which means that training a model from scratch is complicated;

The model at first does not get very many wins, thus it is difficult to get rewards and thus learn.

A good strategy might be first setting the reward not to be a win, but just the relative score compared to the other player.

As the model gets better, you might want to change back to giving reward just for a win. In this game the score itself does not count, only the fact if you get a lower score than the opponent.

After some time it is not a good idea to train the agent just against the deterministic AdvancedComputerPlayer; this overfits the model to take use of small weaknesses in the deterministic algorithm and it really does not become a really strong player. At this point the model has to be switched to play agains itself, for example a saved model with shown efficiency against a AdvancedComputerPlayer.
