from deck import Deck
from hand import DealerHand, PlayerHand
from card import Card

# don't change these imports
from numpy.random import randint, seed
seed(20)

class Blackjack:
    """
    Game of blackjack!

    # Removes the game summaries from the previous doctest run
    >>> from os import remove, listdir
    >>> for f in listdir("game_summaries"):
    ...    remove("game_summaries/" + f)

    #######################################
    ### Doctests for calculate_score() ####
    #######################################
    >>> blackjack = Blackjack(10)
    >>> card_1 = Card("A", "diamonds")
    >>> card_2 = Card("J", "spades")
    >>> hand_1 = PlayerHand()
    >>> blackjack.calculate_score(hand_1)
    0
    >>> hand_1.add_card(card_1)
    >>> blackjack.calculate_score(hand_1) # (Ace)
    11
    >>> hand_1.add_card(card_2)
    >>> blackjack.calculate_score(hand_1) # (Ace, Jack)
    21

    >>> card_3 = Card("A", "spades")
    >>> hand_2 = PlayerHand()
    >>> hand_2.add_card(card_1, card_3)
    >>> blackjack.calculate_score(hand_2) # (Ace, Ace)
    12
    >>> hand_2.add_card(card_2)
    >>> blackjack.calculate_score(hand_2) # (Ace, Ace, Jack)
    12

    >>> hand_3 = PlayerHand()
    >>> card_4 = Card(2, "spades")
    >>> card_5 = Card(4, "spades")
    >>> hand_3.add_card(card_4, card_5)
    >>> blackjack.calculate_score(hand_3)
    6

    #######################################
    ### Doctests for determine_winner() ####
    #######################################
    >>> blackjack = Blackjack(10)
    >>> blackjack.determine_winner(10, 12)
    -1
    >>> blackjack.determine_winner(21, 21)
    0
    >>> blackjack.determine_winner(22, 23)
    0
    >>> blackjack.determine_winner(12, 2)
    1
    >>> blackjack.determine_winner(22, 2)
    -1
    >>> blackjack.determine_winner(2, 22)
    1
    >>> print(blackjack.get_log())
    Player lost with a score of 10. Dealer won with a score of 12.
    Player and Dealer tie.
    Player and Dealer tie.
    Player won with a score of 12. Dealer lost with a score of 2.
    Player lost with a score of 22. Dealer won with a score of 2.
    Player won with a score of 2. Dealer lost with a score of 22.
    <BLANKLINE>  
    >>> blackjack.reset_log()

    #######################################
    ### Doctests for play_round() #########
    #######################################
    >>> blackjack_2 = Blackjack(10)
    >>> blackjack_2.play_round(1, 15)
    >>> print(blackjack_2.get_log())
    Round 1 of Blackjack!
    wallet: 10
    bet: 5
    Player Cards: (10, clubs) (A, clubs)
    Dealer Cards: (Q, clubs) (?, ?)
    Dealer Cards Revealed: (7, diamonds) (Q, clubs)
    Player won with a score of 21. Dealer lost with a score of 17.
    <BLANKLINE>
    >>> blackjack_2.reset_log()
   
    >>> blackjack_2.play_round(3, 21)
    >>> print(blackjack_2.get_log())
    Round 2 of Blackjack!
    wallet: 15
    bet: 5
    Player Cards: (4, clubs) (7, clubs)
    Dealer Cards: (A, hearts) (?, ?)
    Player pulled a (J, hearts)
    Dealer Cards Revealed: (5, clubs) (A, hearts)
    Dealer pulled a (6, clubs)
    Dealer pulled a (2, clubs)
    Dealer pulled a (8, clubs)
    Player won with a score of 21. Dealer lost with a score of 22.
    Round 3 of Blackjack!
    wallet: 20
    bet: 10
    Player Cards: (6, hearts) (9, diamonds)
    Dealer Cards: (K, hearts) (?, ?)
    Player pulled a (Q, hearts)
    Dealer Cards Revealed: (J, diamonds) (K, hearts)
    Player lost with a score of 25. Dealer won with a score of 20.
    Round 4 of Blackjack!
    wallet: 10
    bet: 5
    Player Cards: (5, diamonds) (10, diamonds)
    Dealer Cards: (2, diamonds) (?, ?)
    Player pulled a (3, diamonds)
    Player pulled a (7, spades)
    Dealer Cards Revealed: (2, diamonds) (2, hearts)
    Dealer pulled a (K, spades)
    Dealer pulled a (3, spades)
    Player lost with a score of 25. Dealer won with a score of 17.
    <BLANKLINE>
    
    >>> with open("game_summaries/game_summary2.txt", encoding = 'utf-8') as f:
    ...     lines = f.readlines()
    ...     print("".join(lines[10:26]))
    Dealer Hand:
    ____
    |7  |
    | ♦ |
    |__7|
    ____
    |Q  |
    | ♣ |
    |__Q|
    Winner of ROUND 1: Player
    <BLANKLINE>
    ROUND 2:
    Player Hand:
    ____
    |4  |
    | ♣ |
    <BLANKLINE>

    >>> blackjack_3 = Blackjack(5)
    >>> blackjack_3.play_round(5, 21)
    >>> print(blackjack_3.get_log())
    Round 1 of Blackjack!
    wallet: 5
    bet: 5
    Player Cards: (2, clubs) (2, hearts)
    Dealer Cards: (2, diamonds) (?, ?)
    Player pulled a (3, clubs)
    Player pulled a (3, diamonds)
    Player pulled a (3, hearts)
    Player pulled a (3, spades)
    Player pulled a (4, clubs)
    Player pulled a (4, diamonds)
    Dealer Cards Revealed: (2, diamonds) (2, spades)
    Dealer pulled a (4, hearts)
    Dealer pulled a (4, spades)
    Dealer pulled a (5, clubs)
    Player lost with a score of 24. Dealer won with a score of 17.
    Wallet amount $0 is less than bet amount $5.

    >>> blackjack_4 = Blackjack(500)
    >>> blackjack_4.play_round(13, 21) # At least 52 cards will be dealt
    >>> blackjack_4.reset_log()
    >>> blackjack_4.play_round(1, 17)
    >>> print(blackjack_4.get_log())
    Not enough cards for a game.
    """
    # Class Attribute(s)

    num_games = 1

    def __init__(self, wallet):
        # Initialize instance attributes
        # auto-increment as needed
        self.deck = Deck()
        self.wallet = wallet
        Blackjack.num_games+= 1
        self.log = ''

    
    def play_round(self, num_rounds, stand_threshold):
        """
        Plays `num_rounds` Blackjack rounds.

        Parameters:
            num_rounds (int): Number of rounds to play.
            stand_threshold (int): Score threshold for when the player
            will stand (ie player stands if they have a score >= 
            this threshold)
        """
        assert isinstance(num_rounds, int)
        assert isinstance(stand_threshold, int)
        player_hand = PlayerHand()
        dealer_hand = DealerHand()
        bet_amount = 5
        min_cards = 4
        for i in range(num_rounds):
            if len(self.deck.cards) < min_cards:
                self.log+= 'Not enough cards for a game.'
                bet_amount = 5
                break
            elif self.wallet < bet_amount:
                self.log+= 'Wallet amount $' + str(self.wallet) \
                    + ' is less than bet amount $' + str(bet_amount) + '.'
                bet_amount = 5
                break
            else:
                self.log+= 'Round ' + str(i+1) + ' of Blackjack!\nwallet: ' + str(self.wallet) + '\nbet: ' + str(bet_amount) + '\n'
                times_for_mongeen = randint(0, 5)
                times_for_modified = randint(0, 5)
                self.deck.shuffle(modified_overhand=times_for_modified, mongean=times_for_mongeen)
                self.deck.deal_hand(player_hand)
                self.deck.deal_hand(dealer_hand)
                self.deck.deal_hand(player_hand)
                self.deck.deal_hand(dealer_hand)
                
                self.log+= 'Player Cards: ' + player_hand.__repr__() + '\n' \
                    + 'Dealer Cards: ' + dealer_hand.__repr__() + '\n'
                self.hit_or_stand(player_hand, stand_threshold)
                dealer_hand.reveal_hand()
                self.log+= 'Dealer Cards Revealed: ' + dealer_hand.__repr__() + '\n'
                self.hit_or_stand(dealer_hand, 17)
                winner = self.determine_winner(self.calculate_score(player_hand), self.calculate_score(dealer_hand))
                if winner == 1:
                    self.wallet+= bet_amount
                    bet_amount+=5
                    self.add_to_file(player_hand, dealer_hand, 'Player', i+1)
                elif winner == -1:
                    self.wallet-= bet_amount
                    bet_amount-=5
                    self.add_to_file(player_hand, dealer_hand, 'Dealer', i+1)
                else:
                    self.wallet = self.wallet
                    bet_amount = bet_amount
                    self.add_to_file(player_hand, dealer_hand, 'Tied', i+1)
                
                
    
    def calculate_score(self, hand):
        """
        Calculates the score of a given hand. 

        Sums up the ranks of each card in a hand. Jacks, Queens, and Kings
        have a value of 10 and Aces have a value of 1 or 11. The value of each
        Ace card is dependent on which value would bring the score closer
        (but not over) 21. 

        Should be solved using list comprehension and map/filter. No explicit
        for loops.

        Parameters:
            hand: The hand to calculate the score of.
        Returns:
            The best score as an integer value.
        """
        total_num_a = 4
        assert len([rank for rank in [card.rank for card in hand.cards] if rank == 'A']) <= total_num_a
        assert all([isinstance(i, Card) for i in hand.cards])
        assert isinstance(hand, PlayerHand) or isinstance(hand, DealerHand)
        two = 2
        three = 3
        four = 4
        first_a_value = 1
        second_a_value = 11
        jqk_value = 10
        threshold = 21

        if len(hand.cards) == 0:
            return 0
        elif len([rank for rank in [card.rank for card in hand.cards] if rank == 'A']) == 0:
            jqk_values = sum([jqk_value for rank in [card.rank for card in hand.cards] if rank == 'J' or rank == 'Q' or rank == 'K'])
            non_jqka_value = sum([int(rank) for rank in [card.rank for card in hand.cards] if isinstance(rank, int)])

            result1 = jqk_values + non_jqka_value

            return result1

        elif len([rank for rank in [card.rank for card in hand.cards] if rank == 'A']) == 1:
            jqk_values = sum([jqk_value for rank in [card.rank for card in hand.cards] if rank == 'J' or rank == 'Q' or rank == 'K'])
            non_jqka_value = sum([int(rank) for rank in [card.rank for card in hand.cards] if isinstance(rank, int)])


            result1 = jqk_values + non_jqka_value + first_a_value
            result2 = jqk_values + non_jqka_value + second_a_value
            results = [result1, result2]

            if all(i > threshold for i in results) == True:
                abs_results = [abs(i - threshold) for i in results]
                return results[abs_results.index(min(abs_results))]
            elif all(i <= threshold for i in results) == True:
                abs_results = [abs(i - threshold) for i in results]
                return results[abs_results.index(min(abs_results))]
            else:
                return [i for i in results if i < threshold][0]
        
        elif len([rank for rank in [card.rank for card in hand.cards] if rank == 'A']) == two:
            jqk_values = sum([jqk_value for rank in [card.rank for card in hand.cards] if rank == 'J' or rank == 'Q' or rank == 'K'])
            non_jqka_value = sum([int(rank) for rank in [card.rank for card in hand.cards] if isinstance(rank, int)])

            result1 = jqk_values + non_jqka_value + first_a_value + first_a_value
            result2 = jqk_values + non_jqka_value + second_a_value + second_a_value
            result3 = jqk_values + non_jqka_value + first_a_value + second_a_value
            results = [result1, result2, result3]

            if all(i > threshold for i in results) == True:
                abs_results = [abs(i - threshold) for i in results]
                return results[abs_results.index(min(abs_results))]
            elif all(i <= threshold for i in results) == True:
                abs_results = [abs(i - threshold) for i in results]
                return results[abs_results.index(min(abs_results))]
            else:
                lt_threshold = [i for i in results if i < threshold]
                abs_results = [abs(i-threshold) for i in lt_threshold]
                return lt_threshold[abs_results.index(min(abs_results))]
                
        elif len([rank for rank in [card.rank for card in hand.cards] if rank == 'A']) == three:
            jqk_values = sum([jqk_value for rank in [card.rank for card in hand.cards] if rank == 'J' or rank == 'Q' or rank == 'K'])
            non_jqka_value = sum([int(rank) for rank in [card.rank for card in hand.cards] if isinstance(rank, int)])

            result1 = jqk_values + non_jqka_value + first_a_value + first_a_value + first_a_value
            result2 = jqk_values + non_jqka_value + first_a_value + first_a_value + second_a_value
            result3 = jqk_values + non_jqka_value + first_a_value + second_a_value + second_a_value
            result4 = jqk_values + non_jqka_value + second_a_value + second_a_value + second_a_value
            results = [result1, result2, result3, result4]

            if all(i > threshold for i in results) == True:
                abs_results = [abs(i - threshold) for i in results]
                return results[abs_results.index(min(abs_results))]
            elif all(i <= threshold for i in results) == True:
                abs_results = [abs(i - threshold) for i in results]
                return results[abs_results.index(min(abs_results))]
            else:
                lt_threshold = [i for i in results if i < threshold]
                abs_results = [abs(i-threshold) for i in lt_threshold]
                return lt_threshold[abs_results.index(min(abs_results))]

        elif len([rank for rank in [card.rank for card in hand.cards] if rank == 'A']) == four:
            jqk_values = sum([jqk_value for rank in [card.rank for card in hand.cards] if rank == 'J' or rank == 'Q' or rank == 'K'])
            non_jqka_value = sum([int(rank) for rank in [card.rank for card in hand.cards] if isinstance(rank, int)])

            result1 = jqk_values + non_jqka_value + first_a_value + first_a_value + first_a_value + first_a_value
            result2 = jqk_values + non_jqka_value + first_a_value + first_a_value + first_a_value + second_a_value
            result3 = jqk_values + non_jqka_value + first_a_value + first_a_value + second_a_value + second_a_value
            result4 = jqk_values + non_jqka_value + first_a_value + second_a_value + second_a_value + second_a_value
            result5 = jqk_values + non_jqka_value + second_a_value + second_a_value + second_a_value + second_a_value
            results = [result1, result2, result3, result4, result5]

            if all(i > threshold for i in results) == True:
                abs_results = [abs(i - threshold) for i in results]
                return results[abs_results.index(min(abs_results))]
            elif all(i <= threshold for i in results) == True:
                abs_results = [abs(i - threshold) for i in results]
                return results[abs_results.index(min(abs_results))]
            else:
                lt_threshold = [i for i in results if i < threshold]
                abs_results = [abs(i-threshold) for i in lt_threshold]
                return lt_threshold[abs_results.index(min(abs_results))]
            
        


    def determine_winner(self, player_score, dealer_score):
        """
        Determine whether the Blackjack round ended with a tie, dealer winning, 
        or player winning. Update the log to include the winner and
        their scores before returning.

        Returns:
            1 if the player won, 0 if it is a tie, and -1 if the dealer won
        """
        threshold = 21
        
        if player_score < threshold and dealer_score < threshold:
            if abs(threshold - player_score) < abs(threshold - dealer_score):
                self.log+= 'Player won with a score of ' + str(player_score) \
                    + '. Dealer lost with a score of ' + str(dealer_score) + '.\n'
                return 1
            elif abs(threshold - player_score) > abs(threshold - dealer_score):
                self.log+= 'Player lost with a score of ' + str(player_score) \
                    + '. Dealer won with a score of ' + str(dealer_score) + '.\n'
                return -1
            else:
                self.log+= 'Player and Dealer tie.\n' 
                return 0


        if player_score < threshold and dealer_score > threshold:
            self.log+= 'Player won with a score of ' + str(player_score) \
                    + '. Dealer lost with a score of ' + str(dealer_score) + '.\n'
            return 1
        elif player_score > threshold and dealer_score < threshold:
            self.log+= 'Player lost with a score of ' + str(player_score) \
                    + '. Dealer won with a score of ' + str(dealer_score) + '.\n'
            return -1

        elif player_score > threshold and dealer_score > threshold:
            self.log+= 'Player and Dealer tie.\n'
            return 0
    
        elif player_score == threshold and dealer_score == threshold:
            self.log+= 'Player and Dealer tie.\n' #+ str(player_score) + str(dealer_score)
            return 0

        elif player_score == threshold and dealer_score != threshold:
            self.log+= 'Player won with a score of ' + str(player_score) \
                    + '. Dealer lost with a score of ' + str(dealer_score) + '.\n'
            return 1

        elif player_score != threshold and dealer_score == threshold:
            self.log+= 'Player lost with a score of ' + str(player_score) \
                    + '. Dealer won with a score of ' + str(dealer_score) + '.\n'
            return -1

    def hit_or_stand(self, hand, stand_threshold):
        """
        Deals cards to hand until the hand score has reached or surpassed
        the `stand_threshold`. Updates the log everytime a card is pulled.

        Parameters:
            hand: The hand the deal the cards to depending on its score.
            stand_threshold: Score threshold for when the player
            will stand (ie player stands if they have a score >= 
            this threshold).
        """

        for i in self.deck.cards:
            if self.calculate_score(hand) >= stand_threshold:
                break
            elif self.calculate_score(hand) < stand_threshold:
                deal_card = self.deck.cards[0]
                self.deck.deal_hand(hand)
                if type(hand) == PlayerHand:
                    self.log+= 'Player pulled a ' + str(deal_card.__repr__()) + '\n'
                elif type(hand) == DealerHand:
                    self.log+= 'Dealer pulled a ' + str(deal_card.__repr__()) + '\n'
            elif len(self.deck.cards) == 0:
                break
        
    def get_log(self):
        return self.log
    
    def reset_log(self):
        self.log = ''
        Blackjack.num_games-=1
           
    def add_to_file(self, player_hand, dealer_hand, result, round):
        """
        Writes the summary and outcome of a round of Blackjack to the 
        corresponding .txt file. This file should be named game_summaryX.txt 
        where X is the game number and it should be in `game_summaries` 
        directory.
        """
        
        # Remember to use encoding = "utf-8" 
        with open('game_summaries/game_summary' + str(Blackjack.num_games) + '.txt', mode= 'w+', encoding= 'utf-8') as f:
            f.write('ROUND' + str(round) + '\n' + 'Player Hand:\n' + player_hand.__str__() + 'Dealer Hand:\n' + dealer_hand.__str__() + 'Winner of ROUND 1: ' + result + '\n')