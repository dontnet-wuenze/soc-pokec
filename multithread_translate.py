import multiprocessing
import os

device = "1"
os.environ['CUDA_VISIBLE_DEVICES'] = device
os.environ['ARGOS_DEVICE_TYPE'] = 'cuda'

import argostranslate.package
import argostranslate.translate

from rich.progress import Progress, track

from multiprocessing import Pool
from multiprocessing import set_start_method

from threading import Lock

from_code = "sk"
to_code = "en"

profiles_english_multithread = open("./process/profiles_english_multithread.csv", "w")
profiles_english_multithread.truncate(0)
profiles_english_multithread.close()



translate_lines = []
translate_lines_count = 0

# line, profile, file_lock
def work_log(line):
    translatedText = argostranslate.translate.translate(line[1], from_code, to_code)
    print(translatedText)
    with file_lock:
        global translate_lines_count
        profiles_english_multithread.write(translatedText)
        translate_lines_count = translate_lines_count + 1
        print("Translated lines: " + str(translate_lines_count))


def pool_handler(lines):
    p = Pool(3)
    p.map(work_log, lines)


if __name__ == '__main__':

    # set the fork start method
    set_start_method('fork')
    profiles = open('./process/profiles_remove.csv')

    file_lock = multiprocessing.Lock()
    profiles_english_multithread = open("./process/profiles_english_multithread.csv", "a")
    # profiles_process = open("./raw/soc-pokec-profiles-process.txt")
    lines = profiles.readlines()

    lines = lines[:10]

    map_list = []

    for i in range(len(lines)):
        map_list.append(i, lines[i])

    pool_handler(map_list)

    profiles_english_multithread.close()
