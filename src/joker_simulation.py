from joker_game import Game
import csv
class Simulation(object):
    def __init__(self):
        self.places = []
        self.dealt = []
        self.wild = []
        self.num_wild = []
        self.num_joks = []
        self.already_called = []
        self.correct = []
        self.taken = []

    def run(self, games, model_wanted):
        for h in range(0, games): # amount of games to be simulated
            game = Game()
            game.simulation = True
            if model_wanted:
                game.load_model()
                model = game.model 
            for i in range(0, 24): # 24 plays a game
                game.update_round()
                game.deal_to_users()
                game.set_wildcard()
                
                for j in range(0, 4):
                    self.num_wild.append(len(list(filter(lambda x: x.suit == game.get_wildsuit() and x.value != 13, list(game.users[j].cards)))))
                    self.num_joks.append(len(list(filter(lambda x: x.value == 13, list(game.users[j].cards)))))
                    for k in range(1,5):
                        if (((game.dealer + k) % 4) == j):
                            self.places.append(k)
                    self.dealt.append(game.cards_dealt)
                    self.wild.append(game.get_wildsuit() != 4)
                   
                game.play_round()
                
                for j in range(0, 4):
                    adder = 0
                    place = 1
                    for k in range(1,5):
                        if (((game.dealer + k) % 4) == j):
                            place = k
                    for k in range(1, place):
                        adder += (game.users[j - k].called)
                    self.already_called.append(adder)

                for j in range(0,4): # Adding results of hand
                    self.correct.append(game.users[j].called == game.users[j].taken)
                    self.taken.append(game.users[j].taken) 
                game.reset_users()

    def write_to_csv(self):
        with open('joker_simulations.csv', mode='w') as joker_file:
            joker_writer = csv.writer(joker_file, delimiter=',')
            for i in range(len(self.places)):
                joker_writer.writerow([self.places[i], self.dealt[i],self.wild[i],self.num_wild[i],self.num_joks[i],self.already_called[i],self.correct[i],self.taken[i]])
    