import random
import copy

class Roulette():
    __WHEEL = [ # Roulette Wheel in right order
        {"0": "green"},
        {"32": "red"},
        {"15": "black"},
        {"19": "red"},
        {"4": "black"},
        {"21": "red"},
        {"2": "black"},
        {"25": "red"},
        {"17": "black"},
        {"34": "red"},
        {"6": "black"},
        {"27": "red"},
        {"13": "black"},
        {"36": "red"},
        {"11": "black"},
        {"30": "red"},
        {"8": "black"},
        {"23": "red"},
        {"10": "black"},
        {"5": "red"},
        {"24": "black"},
        {"16": "red"},
        {"33": "black"},
        {"1": "red"},
        {"20": "black"},
        {"14": "red"},
        {"31": "black"},
        {"9": "red"},
        {"22": "black"},
        {"18": "red"},
        {"29": "black"},
        {"7": "red"},
        {"28": "black"},
        {"12": "red"},
        {"35": "black"},
        {"3": "red"},
        {"26": "black"},
    ]

    __ROUNDS_PER_HOUR = 60
    
    __field = [[], [], []]  # filled in init; Roulette Field in right order

    __bank = 0
    __bet = 0
    __rounds = 0
    __betting = True

    # --- Bettings ---
    __color_bet = dict()
    __even_odd_bet = dict()
    __low_high_bet = dict()
    __dozen_bet = dict()
    __column_bet = dict()
    __number_bet = dict()

    # --- statistics ---
    __color_count = {
        "red": 0,
        "black": 0
    }
    __even_odd_count = {
        "even": 0,
        "odd": 0
    }
    __low_high_count = {
        "low": 0,
        "high": 0
    }
    __dozen_count = {
        "first": 0,
        "second": 0,
        "third": 0
    }
    __column_count = {
        "first": 0,
        "second": 0,
        "third": 0
    }
    __number_count = [0] * 37

    def __init__(self, bettings, hours_per_game):
        for i in range(0, 36, 3):   # fills Roulette Field
            self.__field[2].append(i + 1)
            self.__field[1].append(i + 2)
            self.__field[0].append(i + 3)

        self.__rounds = self.__ROUNDS_PER_HOUR * hours_per_game

        self.__color_bet = bettings["color"]
        self.__even_odd_bet = bettings["even_odd"]
        self.__low_high_bet = bettings["low_high"]
        self.__dozen_bet = bettings["dozen"]
        self.__column_bet = bettings["column"]
        self.__number_bet = bettings["number"]

        for _, bet in self.__color_bet.items():
            self.__bet += bet
        for _, bet in self.__even_odd_bet.items():
            self.__bet += bet
        for _, bet in self.__low_high_bet.items():
            self.__bet += bet
        for _, bet in self.__dozen_bet.items():
            self.__bet += bet
        for _, bet in self.__column_bet.items():
            self.__bet += bet
        for _, bet in self.__number_bet.items():
            self.__bet += bet[0]

    def __check(self, field):
        key = list(field.keys())[0]
        number = int(key)
        color = field[key]

        check = {
            "color": "",
            "even_odd": "",
            "low_high": "",
            "dozen": "",
            "column": "",
            "number": []
        }
        # --- statistics ---
        if not number == 0:
            self.__color_count[color]+=1
            check["color"] = color

            if number % 2 == 0:
                self.__even_odd_count["even"]+=1
                check["even_odd"] = "even"
            else:
                self.__even_odd_count["odd"]+=1
                check["even_odd"] = "odd"

            if number < 19:
                self.__low_high_count["low"]+=1
                check["low_high"] = "low"
            else:
                self.__low_high_count["high"]+=1
                check["low_high"] = "high"

            if number < 13:
                self.__dozen_count["first"]+=1
                check["dozen"] = "first"
            elif number < 25:
                self.__dozen_count["second"]+=1
                check["dozen"] = "second"
            else:
                self.__dozen_count["third"]+=1
                check["dozen"] = "third"

            if self.__field[0].__contains__(number):
                self.__column_count["first"]+=1
                check["column"] = "first"
            elif self.__field[1].__contains__(number):
                self.__column_count["second"]+=1
                check["column"] = "second"
            else:
                self.__column_count["third"]+=1
                check["column"] = "third"
                
        self.__number_count[number] += 1

        winnings = 0
        # --- winnings ---
        if self.__betting == True:
            if not number == 0:
                winnings += self.__color_bet[color] * 2
                winnings += self.__even_odd_bet[check["even_odd"]] * 2
                winnings += self.__low_high_bet[check["low_high"]] * 2

                winnings += self.__dozen_bet[check["dozen"]] * 3
                winnings += self.__column_bet[check["column"]] * 3
            
            if self.__number_bet.__contains__(number):
                type_of_bet = self.__number_bet[number][1]
                bet_on_number = self.__number_bet[number][0]

                if type_of_bet == "straight":
                    winnings += bet_on_number * 36
                elif type_of_bet == "split":
                    winnings += bet_on_number * 18
                elif type_of_bet == "street":
                    winnings += bet_on_number * 12
                elif type_of_bet == "corner":
                    winnings += bet_on_number * 9
                elif type_of_bet == "five":
                    winnings += bet_on_number * 7
                else:   # six numbers - line
                    winnings += bet_on_number * 6
        
        return winnings

    def run(self):
        for _ in range(self.__rounds):
            hit = random.randrange(37)
            field = self.__WHEEL[hit]
            winnings = self.__check(field)
            
            self.__bank -= self.__bet
            self.__bank += winnings
        
        return self.__bank


class Test:
    __COLORS = ["red", "black"]
    _EVEN_ODD = ["even", "odd"]

    __top_methods = [[-100, ""], [-100, ""], [-100, ""]] # [value][method]
    __bet_amount = 0
    __steps = 0
    __hours_per_game = 0
    __games = 0
    __random_bettings = 0
    __own_bets = []
    __step = 0.5

    # --- Betting Lists ---
    __color_bet = {
        "red": 0,
        "black": 1
    }
    __even_odd_bet = {
        "even": 1,
        "odd": 0
        }
    __low_high_bet = {
        "low": 0,
        "high": 0
    }
    __dozen_bet = {
        "first": 0,
        "second": 0,
        "third": 0
    }
    __column_bet = {
        "first": 0,
        "second": 0,
        "third": 0
    }
    __numbers_bet = {} # number as int: [bettings, type]

    __bettings = {
        "color": __color_bet,
        "even_odd": __even_odd_bet,
        "low_high": __low_high_bet,
        "dozen": __dozen_bet,
        "column": __column_bet,
        "number": __numbers_bet
    }

    __different_bets = ["red", "black", "even", "odd", "number"]
    __number_bets = ["single", "split", "street", "corner", "six_line", "trio", "first_four"]

    def __init__(self, hours_per_game, games, bet_amont, random_bettings=0, own_bets=[]):
        self.__hours_per_game = hours_per_game
        self.__games = games
        self.__random_bettings = random_bettings
        self.__bet_amount = bet_amont
        self.__own_bets = own_bets

        self.__steps = (self.__bet_amount / 0.5) + 1

    def __create_random_bettings(self):
        bet_types_copy = copy.deepcopy(self.__bettings)
        bet_values_copy = copy.deepcopy(self.__different_bets)
        random.shuffle(bet_values_copy)
        max_bet_copy = copy.deepcopy(self.__bet_amount)

        while not max_bet_copy == 0:
            bet_temp = self.__step * random.randrange((max_bet_copy / self.__step) + 1)
            if bet_temp == 0:
                continue
            max_bet_copy -= bet_temp
            value = bet_values_copy[-1]
            if value == "red" or value == "black":
                bet_types_copy[0][value] = bet_temp
                del(bet_values_copy[-1])
            elif value == "even" or value == "odd":
                bet_types_copy[1][value] = bet_temp
                del(bet_values_copy[-1])
            else:
                number_temp = random.randrange(37)
                bet_types_copy[2][str(number_temp)] = bet_temp

    def __run_tests(self):
        print("TODO")

    def run(self):
        winnings = list()
        for _ in range(self.__games):
            game = Roulette(bettings=self.__own_bets, hours_per_game=self.__hours_per_game)
            winning = game.run()
            winnings.append(winning)
        
        average = sum(winnings) / len(winnings)
        return average


# --- Own Bettings ---
color_bet = {
    "red": 1,
    "black": 0
    }
even_odd_bet = {
    "even": 0,
    "odd": 0.5
    }
low_high_bet = {
    "low": 0,
    "high": 0
}
dozen_bet = {
    "first": 0,
    "second": 0,
    "third": 0
}
column_bet = {
    "first": 0,
    "second": 0.5,
    "third": 0
}
numbers_bet = { # number as int: [bettings, type]
    22: [0.5, "straight"]
}

bettings = {
    "color": color_bet,
    "even_odd": even_odd_bet,
    "low_high": low_high_bet,
    "dozen": dozen_bet,
    "column": column_bet,
    "number": numbers_bet
}

test = Test(hours_per_game=4, games=1000, random_bettings=100, bet_amont=2.5)
#test.run_tests()
newTest = Test(hours_per_game=4, games=10000, bet_amont=2.5, own_bets=bettings)
result = newTest.run()
print(result)
