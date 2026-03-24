import random
from textwrap import dedent

NAIPES = '♣︎♥︎♠︎♦︎'
seed = 0


output:str=''

def print(*args, classe:str='', sep:str=' ', end:str='\n', insert_tag=True) -> None:
    '''
    Sobrepor a função original print() para converter todo output original
    por uma saída HTML.
    '''
    global output

    new_output = ''
    if len(args) == 0:
        new_output = end            
    else:
        string = str(args[0])
        if len(args)>1:
            string = sep.join(args)

        if classe:
            classe = f' class={classe}'

        if insert_tag:
            new_output = f'<span{classe}>{string}</span>{end}'
        else:
            new_output = f'{string}{end}'

    output += new_output.replace('\n', '<br>')
    return

def cls():
    global output
    output = ''


# Override do Fore
class Cores():
    LIGHTBLUE_EX = "<span class='LIGHTBLUE_EX'>"
    LIGHTRED_EX = "<span class='LIGHTRED_EX'>"
    YELLOW = "<span class='YELLOW'>"
    GREEN = "<span class='GREEN'>"
    RED = "<span class='RED'>"
    WHITE = "</span>"

Fore = Cores

class Card:

    def __init__(self, value:int, naipe:int) -> None:
        self.value = value
        self.naipe = naipe
        self.value_str = self.get_value_str(value)
        self.naipe_str = self.get_naipe_str(naipe)
        self.color = self.get_color(naipe)
        self.end_color = '</span>'

    def get_naipe_str(self, naipe:int) -> list[str]:
        match naipe:
            case 1: return ['♣︎','-']
            case 2: return ['♥︎','+']
            case 3: return ['♠︎','-']
            case 4: return ['♦︎','./']
            case _: raise

    def get_color(self, naipe:int):
        match naipe:
            case 1 | 3: return Fore.LIGHTBLUE_EX
            case 2 | 4: return Fore.LIGHTRED_EX 
            case _: return ''
    
    def __str__(self):
        return f"{self.color}{self.naipe_str[0]} {self.value_str[0]}{Fore.WHITE}"


    def __repr__(self):
        return f"{self.color}{self.naipe_str[0]} {self.value_str}{Fore.WHITE}"


    def get_value_str(self, value):
        match value:
            case 11: return 'J'
            case 12: return 'Q'
            case 13: return 'K'
            case 14: return 'A'
            case _: return str(value)


class Game:
    def __init__(self):
        self.dungeon:list = self._new_dungeon()
        self.discard = []
        self.weapon_monsters = []
        self.room = []
        self.gy = []
        self.lp = 20
        self.room_max_size = 4
        self.can_avoid = 1
        self._game = True
        self.last_message = ''
        self.first_help = True

    def dprint(self, msg, dmsg='FORBIDDEN'):
        self.last_message += msg + Fore.WHITE + '\n' 

    def _print_visual_state(self):
        cls()
        global seed
        print(f'Seed {seed}  |  Dungeon {len(self.dungeon)} / 40  |'+ Fore.YELLOW +f'  HP {self.lp:02d} / 20  ' + Fore.WHITE + f'|  Weapon: {self.weapon_monsters}')
        print('\n. 1 .. 2 .. 3 .. 4 .')
        print(f'{self.room}\n')
        print(self.last_message)
        return 

    def _new_dungeon(self):
        new_dungeon = []
        for naipe in range(1,5):
            if naipe == 2 or naipe == 4:
                for n in range(2,11):
                    card = Card(n,naipe)
                    new_dungeon.append(card)
            else:
                for n in range(2,15):
                    card = Card(n,naipe)
                    new_dungeon.append(card)
        return new_dungeon

    def _shuffle_dungeon(self):
        new_dungeon = []
        old_dungeon = self.dungeon
        while len(old_dungeon) > 0:
            random_i =  random.randrange(len(old_dungeon)) 
            card = old_dungeon.pop(random_i)
            new_dungeon.append(card)
        self.dungeon = new_dungeon

    def _change_lp(self, n:int):
        self.lp += n
        if self.lp <= 0:
            self._game_over(self.lp)
        elif self.lp > 20:
            self.lp = 20

    def _game_over(self, score:int):
        self._game = False
        if score > 0:
            print(f'Success: {score} pts')
        else:
            print(f'Failed: {score} pts')
        input('Press ENTER')

    def _check_dungeon_ended(self):
        if len(self.dungeon) == 0:
            if len(self.room) == 0:
                self._game_over(self.lp)
                return True
            elif len(self.room) == 1:
                last_card = self.room[0]
                if last_card.naipe == 2:
                    self._game_over(self.lp + last_card.value)
                    return True
                elif last_card.naipe == 4:
                    self._game_over(self.lp)
                    return True
        return False    

    def enter_room(self, can_run=True):
        if len(self.room)<=1:
            self.can_avoid = can_run
            while len(self.room) < self.room_max_size and len(self.dungeon) != 0:
                drawing_card = self.dungeon.pop(0)
                self.room.append(drawing_card)
            self.dprint(Fore.GREEN + '✅ Você está entrando em uma nova sala.','NEW')
            return True
        else:
            self.dprint(Fore.RED+'❌ Só pode acessar uma nova sala depois de encarar 3 cartas.')
            return False

    def avoid_room(self):
        if not self.can_avoid :
            self.dprint(Fore.RED+'❌ Não pode fugir 2 vezes consecutivas')
            return False
        #if len(self.room) < self.room_max_size:
        #    self.dprint(Fore.RED+'❌ Você já entrou na sala, só pode fugir se não entrar na sala (se tiver as 4 cartas)')
        #    return False
        else:
            while len(self.room)>0:
                card = self.room.pop()
                self.dungeon.append(card)
            self.dprint(Fore.GREEN + '✅ Você fugiu da última sala','A-')
            self.enter_room(can_run=False)
            return True

    def pick_card(self, list_commands):
        room_pos = list_commands[1] # p 1 h
        if not room_pos.isnumeric():
            self.dprint(Fore.RED+f'❌ Escolha entre 1 e {len(self.room)}. (você digitou {room_pos})')
            return False
        room_pos = int(room_pos) - 1
        if room_pos > len(self.room)-1:
            self.dprint(Fore.RED+f'❌ Escolha entre 1 e {len(self.room)}. (você digitou {room_pos+1})')
            return False
        match self.room[room_pos].naipe:
            case 2: # ♥︎
                card = self.room.pop(room_pos)
                self._change_lp(card.value)
                self.discard.append(card)
                self.dprint(Fore.GREEN+f'✅ HP '+f'(+{card.value}) '+'+'*card.value, f'+{card.value}')
                return True
            case 4: # ♦︎
                while self.weapon_monsters:
                    wm_card_to_discard = self.weapon_monsters.pop()
                    self.discard.append(wm_card_to_discard)
                card = self.room.pop(room_pos)
                self.weapon_monsters.append(card)
                self.dprint(Fore.GREEN+f'✅ Arma coletada' , 'DONE')
                return True
            case _: # ♣︎ | ♠︎
                self.dprint(Fore.RED+f'❌ Você pode pegar poções ♥︎ ou armas ♦︎')
                return False

    def pick_fight(self, list_commands):
        if len(list_commands) == 1:
            if list_commands[0] == 'h':
                self.display_help()
                return True
            else:
                self.dprint(Fore.RED+f'❌ Selecione um alvo (ex: "weapon 3")')
                return False
        room_pos = list_commands[1] # p 1 h
        if not room_pos.isnumeric():
            self.dprint(Fore.RED+f'❌ Escolha entre 1 e {len(self.room)}. (você digitou {room_pos})')
            return False
        room_pos = int(room_pos)-1
        if room_pos > len(self.room)-1:
            self.dprint(Fore.RED+f'❌ Escolha entre 1 e {len(self.room)}. (você digitou {room_pos+1})')
            return False
        match self.room[room_pos].naipe:
            case 1 | 3: # ♣︎ | ♠︎
                if len(list_commands)>1:
                    fighting_using_weapon = list_commands[0]
                    return self._fight(room_pos, fighting_using_weapon)
                else:
                    self.dprint(Fore.RED+f'❌ Escolha a forma de luta após selecionar a carta: "weapon" ou "hand"')
                    return False
            case _: # range out of index
                self.dprint(Fore.RED+f'❌ Você só pode lutar contra monstros')
                return False

    def _fight(self, room_pos, fighting_using_weapon:str):
        card = self.room[room_pos]
        match fighting_using_weapon.lower():
            case 'w' | 'weapon':
                if self.weapon_monsters: # has weapon
                    weapon_value = self.weapon_monsters[0].value
                    last_value = self.weapon_monsters[-1].value
                    damage = weapon_value - card.value
                    if card.value <= last_value:
                        card = self.room.pop(room_pos)
                        self.weapon_monsters.append(card)
                        if damage < 0:
                            self._change_lp(damage)
                            self.dprint(Fore.GREEN+f'✅ Monstro derrotado com arma |' + Fore.RED + f' HP ({damage}) ' + '-'*-damage, f'{damage}')
                        else:
                            self.dprint(Fore.GREEN+f'✅ Monstro derrotado' , 'DONE')
                        return True
                    elif card.value > last_value:
                        if len(self.weapon_monsters) == 1:
                            self.dprint(Fore.GREEN+f'✅ Monstro derrotado com arma |' + Fore.RED + f' HP ({damage}) ' + '-'*-damage,  f'{damage}')
                            self._change_lp(damage)
                            card = self.room.pop(room_pos)
                            self.weapon_monsters.append(card)
                            return True
                        else:
                            self.dprint(Fore.RED+f'❌ Após usar a arma, só pode abater monstros mais fraco que o último abatido ({self.weapon_monsters[-1].value}).')
                            return False
                else: # have no weapon
                    self.dprint(Fore.RED+f'❌ Você não tem arma. Pegue uma arma primeiro ou lute usando só com as mãos.')
                    return False
            case 'h' | 'hand':
                card = self.room.pop(room_pos)
                self.dprint(Fore.GREEN+f'✅ Monstro derrotado à mão |' + Fore.RED + f' HP (-{card.value}) ' + '-'*card.value,  f'{-card.value}')
                self._change_lp( -card.value )
                self.discard.append(card)
                return True
            case _:
                self.dprint(Fore.RED+f'❌ Forma de luta não reconhecida, após selecionar a carta digite "weapon" ou "hand")')
                return False



    def display_help(self):
        if self.first_help:
            self.last_message = dedent('''Seu pleito de ajuda não foi atendido,
            Mas certamente não passou desapercebido.
            
            Monstros agora te cercam.''')
            self.first_help = False
        else:
            self.last_message=dedent('''
            Comandos aceitos:
            "help" - para exibir este menu
            "manual" - para exibir o manual do jogo
            "avoid" - retira as cartas da sala e joga para o fim do baralho (só pode fugir se não interagir com a sala) (não pode fugir 2 vezes em seguida)
            "pick 1" - escolha a posição da carta (entre 1 a 4) para pegar a poção de vida / arma 
            "hand 1" - escolha a posição do monstro (entre 1 a 4) para enfrentá-lo usando as próprias mãos
            "weapon 1" - escolha a posição do monstro (entre 1 a 4) para enfrentá-lo usando a sua arma
            "enter" - entra em uma nova sala preenchendo com novas cartas (só pode entrar numa nova sala se pelo menos pegar 3 cartas)
            "reset" - recomeça o mesmo jogo
            "reset 123" - recomeça o jogo usando a seed inserida

            se quiser, você pode enviar só as iniciais, exemplo: "w 2" "p 3" "r 999" etc
            ''')
        return True

    def display_manual(self):
        self.last_message='''Scoundrel - version 1.0 August 15th, 2011
        (ADAPTADO, notas no fim)

        A Single Player Rogue-like Card Game by Zach Gage and Kurt Bieg
        

        Setup:
        Scoundrel is played with a standard deck of playing cards.

        Search through the deck and remove all Jokers, Red Face Cards and Red Aces. Place them off to the side, they are not used in this game.

        Shuffle the remaining cards and place the pile face down on your left. This deck is called the Dungeon.

        Take out a piece of paper and pen (or use your memory). Mark down 20 on the piece of paper, this is your starting Health.
        

        Rules:
        The 26 Clubs and Spades in the deck are Monsters. Their damage is equal to their ordered value. (e.g. 10 is 10, Jack is 11, Queen is 12, King is 13, and Ace is 14)

        The 9 Diamonds in the deck are Weapons. Each weapon does as much damage as its value. All weapons in Scoundrel are binding, meaning if you pick one up, you must equip it, and discard your previous weapon.

        The 9 Hearts in the deck are Health Potions. You may only use one health potion each turn, even if you pull two. The second potion you pull is simply discarded. You may not restore your life beyond your starting 20 health.

        You may locate the discard deck (any discarded cards) anywhere you wish, though I recommend to the right of the Room. Cards are discarded face down.

        The Game ends when either your life reaches 0 or you make your way through the entire Dungeon. 
        

        Scoring:
        - If your life has reached zero, find all the remaining monsters in the Dungeon, and subtract their values from your life, this negative value is your score.
        
        - If you have made your way through the entire dungeon, your score is your positive life, or if your life is 20, and your last card was a health potion, your life + the value of that potion.
        
        
        Gameplay:
        On your first and every turn, flip over cards off the top of the deck, one by one, until you have 4 cards face up in front of you to make an Room.

        You may avoid the Room if you wish. If you chose to do so, scoop up all four cards in one motion and place them at the bottom of the Dungeon. While you may avoid as many Rooms as you want, you may not avoid two Rooms in a row.

        If you choose not to avoid the Room, one by one, you must face 3 of the four cards it contains. 
        
        Take them one at a time.

        If you chose a Weapon...
        You must equip it. Do this by placing it face up between you and the remaining Room cards. If you had a previous Weapon equipped, move it and any Monsters on it to the discard deck.
        
        If you chose a Health Potion... 
        Add its number to your health, and than discard it. Your health may not exceed 20, and you may not use more than one Health Potion per turn. If you take two Health Potions on a single turn, the second is simply discarded, adding nothing to your health.
        
        If you chose a Monster... 
        You may either fight it barehanded or with an equipped Weapon.
        
        
        Combat
        - If you choose to fight the Monster barehanded, subtract its full value from your Health, and move the Monster to the discard deck.

        - If you choose to fight the Monster with your equipped Weapon, place the monster face up on top of the weapon (and on top of any other Monsters on the Weapon. Be sure to stagger the placement of the Monster so that the Weapon's number is still showing. subtract the Weapon's value from the Monster's value and subtract any remaining value from your health. 

        For example, if your Weapon is a 5, and you place a 3 Monster on it, you take no damage. ( 3-5 < 0) If your Weapon is a 5 and you place a Jack Monster on it, you take 6 damage.  ( 11 - 5 = 5 dmg)
 
        It is important to note that although you retain your weapons until they are replaced, once a Weapon is used on a monster, the Weapon can then only be used to slay Monsters of a lower value (less than equal) than the previous Monster it had slain.

        For example, if your 5 Weapon has killed a Queen Monster and you then choose a 6 Monster, you may use your Weapon on the 6 Monster, as 6 is less than 12.

        But, if you have used your 5 Weapon on a 6 Monster, and you then choose a Queen Monster, you must fight the Queen barehanded as Queen, 12, is greater than 6. Despite this, the Weapon is not discarded, as it could still be used against Monsters weaker than a 6       
        
        ADAPTADO:
        * É possível fugir da sala mesmo que já tenha entrado nela
        * Demais poções após a primeira na mesma sala não será descartados
        '''
        return True

    def _do_command(self, command):
        list_commands = command.lower().strip().split(' ')
        match list_commands[0]:
            case 'help':
                return self.display_help()
            case 'avoid' | 'a' :
                return self.avoid_room()
            case 'pick' | 'p' :
                return self.pick_card(list_commands)
            case 'hand' | 'h' :
                return self.pick_fight(list_commands)
            case 'weapon' | 'w' :
                return self.pick_fight(list_commands)
            case 'enter' | 'e' :
                return self.enter_room()
            case 'reset' | 'restart' | 'r':
                return self.reset_game(list_commands)
            case 'manual' | 'm':
                return self.display_manual()
            case _:
                self.dprint(Fore.RED+f'❌ Comando não reconhecido, digitado {command}, qualquer coisa use "help"')
                return False

    def reset_game(self, list_commands):
        if len(list_commands)>1:
            arg1 = list_commands[1]
            global seed
            if arg1.isnumeric():
                seed = int(arg1)
            else:
                seed = int(random.randrange(1,999))
        self._game = False
        init()
        return True

    def check_room(self, auto=True):
        if auto:
            if len(self.room) <= 1:
                self.enter_room()

    def _ex_loop(self, entrada_usuario):
        if not self._game:
            init()
        if self._check_dungeon_ended():
            return
        self.last_message = ''
        self._do_command(entrada_usuario)
        self._print_visual_state()

    def inserir_input(self, entrada_usuario:str):
        self._ex_loop(entrada_usuario)

g = None

def init():
    global seed
    global g
    random.seed(seed)
    g = Game()
    g._new_dungeon()
    g._shuffle_dungeon()
    g.enter_room()
    g._print_visual_state()
    # g._loop()

if __name__ == '__main__':
    seed = random.randint(1,999)
    random.seed(seed)
    init()

# py -m http.server