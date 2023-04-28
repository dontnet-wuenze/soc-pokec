import multiprocessing
import os

import pandas as pd

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
def work_log(profiles_array, idx):
    names = str.split("user_id public completion_percentage gender region last_login registration age body "
                      "I_am_working_in_field spoken_languages hobbies I_most_enjoy_good_food pets body_type "
                      "my_eyesight eye_color hair_color hair_type completed_level_of_education favourite_color "
                      "relation_to_smoking relation_to_alcohol sign_in_zodiac on_pokec_i_am_looking_for love_is_for_me "
                      "relation_to_casual_sex my_partner_should_be marital_status children relation_to_children "
                      "I_like_movies I_like_watching_movie I_like_music I_mostly_like_listening_to_music "
                      "the_idea_of_good_evening I_like_specialties_from_kitchen fun I_am_going_to_concerts "
                      "my_active_sports my_passive_sports profession I_like_books life_style music cars politics "
                      "relationships art_culture hobbies_interests science_technologies computers_internet education "
                      "sport movies travelling health companies_brands more")


    for i in track(range(0, profiles_array.shape[0])):
        for j in range(0, profiles_array.shape[1]):
            # element = profiles_array[i, j]
            if isinstance(profiles_array[i, j], str):
                profiles_array[i, j] = argostranslate.translate.translate(profiles_array[i, j], "sk", "en")

    profiles_english = pd.DataFrame(data=profiles_array, columns=names)

    profiles_english.set_index('user_id', inplace=True, drop=False)

    profiles_english.to_csv('./process/profiles_english_multithread.csv' + str(idx), index=False)



if __name__ == '__main__':

    profiles = pd.read_csv('./process/profiles_remove.csv')

    filelock = Lock()

    # profiles_process = open("./raw/soc-pokec-profiles-process.txt")
    profiles_array = profiles.values

    profiles_array = profiles_array[:100]

    p_num = 10
    p_size = profiles_array.shape[0] // p_num

    for i in range(p_num - 1):
        Process(target=work_log, args=(profiles_array[i * p_size: (i + 1) * p_size], i)).start()

    Process(target=work_log, args=(profiles_array[(p_num -  1) * p_size:], p_num - 1)).start()

