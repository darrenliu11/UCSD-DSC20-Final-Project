class Card:
    """
    Card class.

    # Doctests for str and repr
    >>> card_1 = Card("A", "spades")
    >>> print(card_1)
    ____
    |A  |
    | ♠ |
    |__A|
    >>> card_1
    (A, spades)
    >>> card_2 = Card("K", "spades")
    >>> print(card_2)
    ____
    |K  |
    | ♠ |
    |__K|
    >>> card_2
    (K, spades)
    >>> card_3 = Card("A", "diamonds")
    >>> print(card_3)
    ____
    |A  |
    | ♦ |
    |__A|
    >>> card_3
    (A, diamonds)

    # Doctests for comparisons
    >>> card_1 < card_2
    False
    >>> card_1 > card_2
    True
    >>> card_3 > card_1
    False

    # Doctests for set_visible()
    >>> card_3.set_visible(False)
    >>> print(card_3)
    ____
    |?  |
    | ? |
    |__?|
    >>> card_3
    (?, ?)
    >>> card_3.set_visible(True)
    >>> print(card_3)
    ____
    |A  |
    | ♦ |
    |__A|
    >>> card_3
    (A, diamonds)
    """

    # Class Attribute(s)

    def __init__(self, rank, suit, visible=True):
        """
        Creates a card instance and asserts that the rank and suit are valid.
        """
        ranks = [i for i in range(2, 11)] + ['A', 'J', 'Q', 'K']
        suits = ['hearts', 'spades', 'clubs', 'diamonds']

        self.rank = rank
        self.suit = suit
        self.visible = visible

        assert self.rank in ranks
        assert self.suit in suits
        assert isinstance(visible, bool)
        

    def __lt__(self, other_card):
        def rank_order(rank):
            if rank == 'J':
                return 11
            elif rank == 'Q':
                return 12
            elif rank == 'K':
                return 13
            elif rank == 'A':
                return 14
            else:
                return rank

        def suit_order(suit):
            if suit == 'clubs':
                return 0
            elif suit == 'diamonds':
                return 1
            elif suit == 'hearts':
                return 2
            elif suit == 'spades':
                return 3
        
        if rank_order(self.rank) > rank_order(other_card.rank):
            return False
        elif rank_order(self.rank) < rank_order(other_card.rank):
            return True
        elif rank_order(self.rank) == rank_order(other_card.rank):
            if suit_order(self.suit) > suit_order(other_card.suit):
                return False
            else:
                return True


    def __str__(self):
        """
        Returns ASCII art of a card with the rank and suit. If the card is
        hidden, question marks are put in place of the actual rank and suit.

        Examples:
        ____
        |A  |
        | ♠ |
        |__A|
        ____
        |?  |
        | ? |
        |__?|             
        """
        def invisible_card():
            s = "____" + "\n"
            s = s + "|?  |" + "\n"
            s = s + "| ? |" + "\n"
            s = s + "|__?|"
            return s
        
        def visible_card(rank, suit):
            if suit == 'hearts':
                s = "____" + "\n"
                s = s + "|" + str(rank) + "  |" + "\n"
                s = s + "| ♥ |" + "\n"
                s = s + "|__" + str(rank) + "|"
                return s
            elif suit == 'spades':
                s = "____" + "\n"
                s = s + "|" + str(rank) + "  |" + "\n"
                s = s + "| ♠ |" + "\n"
                s = s + "|__" + str(rank) + "|"
                return s
            elif suit == 'clubs':
                s = "____" + "\n"
                s = s + "|" + str(rank) + "  |" + "\n"
                s = s + "| ♣ |" + "\n"
                s = s + "|__" + str(rank) + "|"
                return s
            elif suit == 'diamonds':
                s = "____" + "\n"
                s = s + "|" + str(rank) + "  |" + "\n"
                s = s + "| ♦ |" + "\n"
                s = s + "|__" + str(rank) + "|"
                return s


        if self.visible == True:
            return f'{visible_card(self.rank, self.suit)}'
        else:
            return f'{invisible_card()}'

    def __repr__(self):
        """
        Returns (<rank>, <suit>). If the card is hidden, question marks are
        put in place of the actual rank and suit.           
        """        
        if self.visible == True:
            return f'({self.rank}, {self.suit})'
        else:
            return '(?, ?)'

    def get_rank(self):
        return self.rank
    
    def get_suit(self):
        return self.suit

    def set_visible(self, visible):
        assert isinstance(visible, bool)
        self.visible = visible