class Player():
    def __init__(self, number_in, hand_in =[]):
        self.number = number_in
        self.hand = hand_in
        self.score = 0
        self.desired = -1
        self.taken = 0

    def set_taken(self, taken):
        self.taken = taken

    def add_take(self):
        self.taken += 1

    def set_desired(self, amount):
        self.desired = amount

    def __repr__(self):
        return "Player " + str(self.number)

    def right(self) -> int:
        return (self.number + 1) % 4

    def left(self) -> int:
        return (self.number - 1) % 4

    def across(self) -> int:
        return (self.number + 2) % 4
    
    def update_score(self, desired: int, actual: int, dealt: int):
        if desired == actual: 
            if actual == dealt:
                self.score += dealt * 100 # 1 -> 100, 2 -> 200, 3 -> 300, 4 -> 400 ... 
            else:
                self.score += actual * 50 + 50 # 1 -> 100, 2 -> 150, 3 -> 200, 4 -> 250 ...
        elif actual == 0: # 0 -> -200, bust/ხვიშტი
            self.score -= 200
        else: # 1 -> 10, 2 -> 20, 3 -> 30, 4 -> 40 ...
            self.score += actual * 10

    def take(self, cards):
        self.hand = cards