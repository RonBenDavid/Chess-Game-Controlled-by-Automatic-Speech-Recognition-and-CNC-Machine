import copy
import multiprocessing as mp
import os
import sys
import time
from os import system, name

from bitboard_helpers import pprint_pieces
from constants import Color, UciCommand
from position import Position
from uci_input_parser import UciInputParser
global locationXY
CURRENT_VERSION = "0.1.0"
from scrath import Write_location
import azure.cognitiveservices.speech as speechsdk
import pyttsx3
import re

def clear():
    # Windows
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
def recognize_from_mic():
    # Find your key and resource region under the 'Keys and Endpoint' tab in your Speech resource in Azure Portal
    # Remember to delete the brackets <> when pasting your key and region!
    speech_config = speechsdk.SpeechConfig(subscription="313fd49c341d4a1da426c9b69ba245ff", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    # Asks user for mic input and prints transcription result on screen
    #speak("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    print(str.lower(result.text))
    return (str.lower(result.text))


class Game:
    def __init__(self, interface_mode, queue, sys_queue):
        self.mode = interface_mode.strip().lower()
        self.queue = queue
        self.sys_queue = sys_queue
        self.history = []
        self.position = Position()
        self.is_over = False
        self.score = [0, 0]
        self.parser = UciInputParser()

        self.color_to_move = {
            Color.WHITE: "White",
            Color.BLACK: "Black",
        }

    def run(self):
        if self.mode == "uci":
            self.run_uci_mode()

    def try_parse_move(self, move):
        engine_input = self.parser.parse_input(move)
        if not engine_input.is_valid:
            return None
        if engine_input.is_move:
            move_piece = self.position.get_piece_on_square(engine_input.move.from_sq)
            if not move_piece:
                return None
            engine_input.move.piece = move_piece
            return engine_input.move

    def run_uci_mode(self):
        sentinel = False
        while True:
            if not sentinel:
                print(f"Wake Engine [{CURRENT_VERSION}] running using interface mode: [{self.mode}]")
                print(f"{self.color_to_move[self.position.color_to_move]} to move:")
                sentinel = True
                pprint_pieces(self.position.piece_map)
                dup = copy.copy(self.position.piece_map)##Copy location

                file_loc = open("location.txt", "w")
                file_loc.writelines(Write_location(dup))
                file_loc.close()  # to change file access modes
            if not self.queue.empty():
                clear()
                msg = self.queue.get().strip()
                move = self.try_parse_move(msg)

                if not move:
                    if msg == UciCommand.QUIT:
                        self.sys_queue.put("kill")
                    continue

                move_result = self.position.make_move(move)

                if move_result.is_checkmate:
                    print("Checkmate")
                    self.score[self.position.color_to_move] = 1
                    self.is_over = True

                if move_result.is_stalemate:
                    print("Stalemate")
                    self.score = [0.5, 0.5]
                    self.is_over = True

                self.history.append(move_result.fen)
                sentinel = False

            else:
                pass


def engine_proc(queue, sys_queue, interface_mode="uci"):
    clear()
    game = Game(interface_mode, queue, sys_queue)
    game.run()

my_dict = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "he": "e",
    "if": "f",
    "te": "d"
}

def reader_proc(queue, fileno):
    sys.stdin = os.fdopen(fileno)
    while True:
        input_move = recognize_from_mic()
        for key, value in my_dict.items():
            input_move = input_move.replace(key, value)
        input_move=input_move[0:4]
        if(len(input_move)>3):
            if(input_move[0]=='8'):
                my_list = list(input_move)
                my_list[0]='a'
                input_move = ''.join(my_list)                

            if(input_move[2]=='8'):
                my_list = list(input_move)
                my_list[2]='a'
                input_move = ''.join(my_list)
                
            if(input_move[2]=='6'):
                my_list = list(input_move)
                my_list[2]='c'
                input_move = ''.join(my_list)
                
            if(input_move[2]=='6'):
                my_list = list(input_move)
                my_list[2]='c'
                input_move = ''.join(my_list)
                
            if(input_move[1]=='a'):
                my_list = list(input_move)
                my_list[1]='8'
                input_move = ''.join(my_list)
                
            if(input_move[3]=='a'):
                my_list = list(input_move)
                my_list[3]='8'
                input_move = ''.join(my_list)
                
            if(input_move[0]=='3'):
                my_list = list(input_move)
                my_list[1]='d'
                input_move = ''.join(my_list)
                
            if(input_move[2]=='3'):
                my_list = list(input_move)
                my_list[3]='d'
                input_move = ''.join(my_list)                 
                
        match = re.match("(^[a-h][1-8][a-h][1-8])", input_move)
        if match:
            print("The pattern matched:", match.group())
            queue.put(input_move)
        else:
            continue
        
if __name__ == "__main__":
    mode = "UCI"
    inp_queue = mp.Queue()
    sys_queue = mp.Queue()
    engine_process = mp.Process(target=engine_proc, args=(inp_queue, sys_queue, mode))
    engine_process.daemon = True
    engine_process.start()
    fn = sys.stdin.fileno()

    reader_process = mp.Process(target=reader_proc, args=(inp_queue, fn))
    reader_process.daemon = False
    reader_process.start()

    while True:
        message = sys_queue.get()
        if message == 'kill':
            engine_process.terminate()
            reader_process.terminate()
            time.sleep(0.5)
            if not engine_process.is_alive() or not reader_process.is_alive():
                engine_process.join()
                reader_process.join()
                print("Peace")
                sys.exit(0)
