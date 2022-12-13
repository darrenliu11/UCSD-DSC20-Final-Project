class Shuffle:
    """
    Different kinds of shuffling techniques.
    
    >>> cards = [i for i in range(52)]
    >>> cards[25]
    25
    >>> mod_oh = Shuffle.modified_overhand(cards, 1)
    >>> mod_oh[0]
    25
    >>> mod_oh[25] 
    24
 
    >>> mongean_shuffle = Shuffle.mongean(mod_oh)
    >>> mongean_shuffle[0]
    51
    >>> mongean_shuffle[26]
    25
    """    
        
    def modified_overhand(cards, num):
        """
        Takes `num` cards from the middle of the deck and puts them at the
        top. 
        Then decrement `num` by 1 and continue the process till `num` = 0. 
        When num is odd, the "extra" card is taken from the bottom of the
        top half of the deck.
        """
        
        # Use Recursion.
        # Note that the top of the deck is the card at index 0.
        assert isinstance(cards, list)
        assert isinstance(num, int)
        
        if num == 0:
            return cards
        elif len(cards) % 2 == 0 and num % 2 != 0:
            if num == 1:
                removed = [cards[int(len(cards) / 2) - 1]]
                del cards[int(len(cards) / 2) - 1]
                cards = removed + cards
                return Shuffle.modified_overhand(cards, num-1)
            elif num > 1:
                removed = cards[int(len(cards) / 2) - int(num / 2) : int(len(cards) / 2) + int(num / 2)]
                extra = [cards[int(len(cards) / 2) - int(num / 2) - 1]]
                del cards[int(len(cards) / 2) - int(num / 2) - 1 : int(len(cards) / 2) + int(num / 2)]
                cards = extra + removed + cards
                return Shuffle.modified_overhand(cards, num-1)

        elif len(cards) % 2 != 0 and num % 2 == 0:
                removed = cards[int(len(cards) / 2) - int(num / 2) : int(len(cards) / 2) + int(num / 2)]
                del cards[int(len(cards) / 2) - int(num / 2) : int(len(cards) / 2) + int(num / 2)]
                cards = removed + cards
                return Shuffle.modified_overhand(cards, num-1)

        elif len(cards) % 2 == 0 and num % 2 == 0:
            n = int(num / 2)
            removed = cards[int(len(cards) / 2) - n : int(len(cards) / 2) + n]
            del cards[int(len(cards) / 2) - n : int(len(cards) / 2) + n]
            cards = removed + cards
            return Shuffle.modified_overhand(cards, num-1)

        elif len(cards) % 2 != 0 and num % 2 != 0:
            n = int(num / 2)
            removed = cards[int(len(cards) / 2) - n : int(len(cards) / 2) + n + 1]
            del cards[int(len(cards) / 2) - n : int(len(cards) / 2) + n + 1]
            cards = removed + cards
            return Shuffle.modified_overhand(cards, num-1)
                    
    
    def mongean(cards):
        """
        Implements the mongean shuffle. 
        Check wikipedia for technique description. Doing it 12 times restores the deck.
        """
        
        # Remember that the "top" of the deck is the first item in the list.
        # Use Recursion. Can use helper functions.
        
        assert isinstance(cards, list)

        def mongeen_helper(lst):
            if len(lst) == 0:
                return []
            elif len(lst) > 0:
                return [lst[0]] + mongeen_helper(lst[2:])
        
        odd_elem = mongeen_helper(cards)
        even_elem = mongeen_helper(cards[1:])
        even_elem.reverse()
        return even_elem + odd_elem
    