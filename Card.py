class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return "{} {}".format(self.value, self.suit)
