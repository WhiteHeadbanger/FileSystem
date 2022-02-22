from random import choice
from typing import Optional, List, Dict
from enum import Enum, auto

WORDS = ["hola", "cola", "rana", "puta"]

class Player:
    """ Represents a player """

    def __init__(self, name: str = "Player"):
        self.name = name
        self.score: int = 0
        self.stats: Dict[str, int] = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0}

class Status(Enum):
    LETTER_NOT_FOUND = auto()
    LETTER_IN_WRONG_PLACE = auto()
    LETTER_FOUND = auto()


class Game:
    """ Represents the game """

    def __init__(self) -> None:
        #Max 6 tries
        self.tries: int = 0 
        self.chosen_word: str = ""
        self.last_try: List[str] = []
        self.player: Optional[Player] = None
        self.letters_not_found: List[tuple[str, Status]] = []
        
    def menu(self):
        menu = {
            "1":("Jugar", self.play),
            "2":("Perfil", self.profile),
            "3":("Opciones", self.options)
        }

        for key in sorted(menu.keys()):
            print(f"{key} ==> {menu[key][0]}")

        inp = input(">> ")
        menu.get(inp, None)[1]()

    def play(self):
        self.new_game()
        print(f"Tu palabra tiene {'- '*len(self.chosen_word)}letras")
        
        while self.tries < 6:
            
            print(f"Tenés {self.tries} intentos restantes!")
            inp = input(">> ")
            if inp == self.chosen_word:
                self.post_game(win=True)
                break
            self.analyze_input(inp)
            self.post_process()

        self.post_game(win=False)
            

    def profile(self):
        pass

    def options(self):
        pass

    def new_game(self):
        if not self.player:
            n = input('Nombre de jugador (Por defecto "Player")')
            self.player = Player(name=n)

        #Choosing a word
        self.chosen_word = choice(WORDS)

    def analyze_input(self, input) -> List[str]:
        chosen_word = [x for x in self.chosen_word]
        input = [x for x in input]
        index = 0
        for inp, word_letter in zip(input, chosen_word):
            if inp in chosen_word and inp != word_letter:
                self.last_try.append((inp, index, Status.LETTER_IN_WRONG_PLACE))
            elif inp == word_letter:
                self.last_try.append((inp, index, Status.LETTER_FOUND))
            elif inp not in chosen_word:
                self.last_try.append((inp, index, Status.LETTER_NOT_FOUND))
            index += 1

        #Reordering by index
        #from operator import itemgetter
        #self.last_try = sorted(self.last_try, key=itemgetter[1])

    def post_process(self):
        output = ""
        not_found = ""
        wrong_place = ""
        
        for box in self.last_try:
            if box[2] == Status.LETTER_FOUND:
                output += f"{box[0]}"
            elif box[2] == Status.LETTER_IN_WRONG_PLACE:
                wrong_place += f"{box[0]} "
            else:
                not_found += f"{box[0]} "

        print(f"Letras que están en distinto orden >> {wrong_place}")
        print(f"Letras que NO están >> {not_found}")
        self.last_try.clear()
        self.tries += 1



    def post_game(self, win: bool = False):
        if win:
            print(f"Ganaste!\nPuntos >> {self.player.score}")
            self.player.stats[str(self.tries)] += 1
            return

        print(f"Perdiste!\nPuntos >> {self.player.score}")


if __name__ == '__main__':
    g = Game()
    while True:
        g.menu()
            





        