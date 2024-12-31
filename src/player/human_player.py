from .player import Player

class HumanPlayer(Player):
    def get_player_name(self) -> str:
        return input("Please input you name: ")
    
    def get_draw_action(self, game_status : dict) -> str:
        '''game_status = dict({
        'other_players' = [table_cards1, table_cards2 ...],
        'player' = [table_cards],
        'played_top_card' = Card
        })'''
        print("Do you want to draw from the (d)eck or (p)layed cards? ")
        while True:
            if answer := input().lower() in ['d', 'p']:
                return answer
            else:
                print("Invalid command, please input 'd' or 'p'")
    
    def get_play_action(self, game_status : dict) -> tuple:
        '''game_status = dict({
        'other_players' = [table_cards1, table_cards2 ...],
        'player' = [table_cards],
        'played_top_card' = Card,
        'hand_card' = Card
        })'''
        print("Where do you want to play the card? ")
        print("(P)layed card deck, place it in table (row, column): ")
        while True:
            answer = input().lower()
            if answer == "p":
                return ("p", None)
            else:
                try:
                    row, column = [int(x) for x in answer.split(",").strip()]
                    print("After split: ", row, column)
                    return (row, column)
                except:
                    print("Invalid input")
            print("Please either state 'p' to place the card in your hand")
            print("to the played deck, or give a coordinate separated by ',' to place")
            print("the card in your table and that card goes to the played deck.")
            print("Coordinates are for example 1,2 where 1 is the first row and 2 is")
            print("the second column")
