import multiprocessing
import os

device = "1"
os.environ['CUDA_VISIBLE_DEVICES'] = device
os.environ['ARGOS_DEVICE_TYPE'] = 'cuda'

import argostranslate.package
import argostranslate.translate

from rich.progress import Progress, track

from multiprocessing import Pool, Process
from multiprocessing import set_start_method

from multiprocessing import Lock

from_code = "sk"
to_code = "en"

translate_lines = []
translate_lines_count = 0

# line, profile, file_lock
def work_log(file_lock, line):

    translatedText = argostranslate.translate.translate(line, from_code, to_code)
    print(line, translatedText)
    file_lock.acquire()
    global translate_lines_count
    try:
        translate_lines_count = translate_lines_count + 1
        print(translate_lines_count)
        with open("./process/profiles_english_multithread.csv", "a") as file:
            file.write(translatedText)
    finally:
        file_lock.release()


if __name__ == '__main__':

    profiles = open('./process/profiles_remove.csv')

    filelock = Lock()

    # profiles_process = open("./raw/soc-pokec-profiles-process.txt")
    lines = profiles.readlines()

    lines = lines[:10]

    with open("./process/profiles_english_multithread.csv", "w") as file:
        file.write(lines[0])

    lines = lines[1:]

    for i in range(9):
        Process(target=work_log, args=(filelock, lines[i])).start()

