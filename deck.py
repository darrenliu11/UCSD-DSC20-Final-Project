from card import Card
from hand import PlayerHand, DealerHand
from shuffle import Shuffle

class Deck:
    """
    Card deck of 52 cards.

    >>> deck = Deck()
    >>> deck.get_cards()[:5]
    [(2, clubs), (2, diamonds), (2, hearts), (2, spades), (3, clubs)]

    >>> deck.shuffle(modified_overhand=2, mongean=3)
    >>> deck.get_cards()[:5]
    [(A, clubs), (Q, clubs), (10, clubs), (7, diamonds), (5, diamonds)]

    >>> hand = PlayerHand()
    >>> deck.deal_hand(hand)
    >>> deck.get_cards()[0]
    (Q, clubs)
    """

    # Class Attribute(s)

    def __init__(self):
        """
        Creates a Deck instance containing cards sorted in ascending order.
        """
        ranks = [i for i in range(2, 11)] + ['J', 'Q', 'K', 'A']
        suits = ['clubs', 'diamonds', 'hearts', 'spades']
        self.cards = [Card(j, i) for j in ranks for i in suits]

        

    def shuffle(self, **shuffle_and_count):
        """Shuffles the deck using a variety of different shuffles.

        Parameters:
            shuffle_and_count: keyword arguments containing the
            shuffle type and the number of times the shuffled
            should be called.
        """
        assert all([isinstance(key, str) and isinstance(value, int) for key, value in shuffle_and_count.items()])
        for key, value in shuffle_and_count.items():
            if key == 'modified_overhand':
                self.cards = Shuffle.modified_overhand(self.cards, value)
            else:
                for i in range(value):
                    self.cards = Shuffle.mongean(self.cards)

                    

    def deal_hand(self, hand):
        """
        Takes the first card from the deck and adds it to `hand`.
        """
        
        assert isinstance(hand, PlayerHand) or isinstance(hand, DealerHand)

        first_card = self.cards[0]
        self.cards.pop(0)
        hand.add_card(first_card)


    def get_cards(self):
        return self.cards
