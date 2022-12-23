
class Player(int):
    def __init__(number, hand_in=[]):
        self = number
        self.hand = hand_in
        self.score = 0

    def __repr__(self):
        return "Player " + str(self)

    def get_right(self):
        return (self + 1) % 4

    def get_left(self):
        return (self - 1) % 4

    def get_across(self):
        return (self + 2) % 4
    
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
        
