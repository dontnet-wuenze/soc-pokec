from collections import Counter

import numpy as np
import pandas as pd


def select_label_profile():
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

    labels_en_sk = {
        'friends': 'priatelia',
        'music': ['pocuvanie hudby', 'hudba'],
        # 'sport': ['sportovanie', 'sport'],
        'movie': ['pozeranie filmov', 'kino', 'filmy'],
        'sleeping': 'spanie',
        'swimming': ['kupalisko', 'plavanie'],
        'cooking': ['varenie'],
        'party': 'party',
        'travel': ['cestovanie', 'turistika'],
        'disco': 'diskoteky',
        'shopping': 'nakupovanie',
        'dancing': ['tancovanie', 'tanec'],
        'surfing the web': 'surfovanie po webe',
        'pc games': ['praca s pc', 'pc hry', 'pc'],
        'sex': 'sex',
        'eating': 'jedlo',
        'camping': 'stanovanie',
        'photography': ['fotografovanie', 'kamosi'],
        'reading': ['citanie', 'knihy'],
        'painting': ['malovanie', 'kreslenie'],
        'homework': ['domace prace', 'prace okolo domu'],
        'breeding': 'chovatelstvo',
        'drama': 'divadlo',
        'gardening': 'prace v zahrade',
        'museum': 'chodenie do muzei',
        'collection': 'zberatelstvo',
        'hacking': 'hackovanie',
        'embroidery': 'vysivanie',
        'sewing': 'sitie',
        # 'football': 'futbal',
        # 'natural': 'priroda',
        # 'car': ['auta', 'soferovanie'],
        # 'singing': ['spev', 'spievanie'],
        # 'guitar': 'gitara',
        # 'motorbikes': ['motorky'],
        # 'skating': 'korculovanie',
        # 'bicycle': ['bicyklovanie', 'bike'],
        # 'sleep': ['spanok'],
        # 'hockey': 'hokej',
        # 'bake': 'pecenie',
        # 'others': 'vsetko',
        # 'work': ['praca', 'zamestnanie'],
        # 'skiing': ['lyzovanie'],
        # 'fish': 'rybarcenie',
        # 'walk': 'prechadzky',
    }

    usecols = ['public', 'gender', 'region', 'age', 'body', 'I_am_working_in_field', 'spoken_languages',
               'hobbies', 'I_most_enjoy_good_food', 'pets', 'body_type', 'my_eyesight', 'eye_color', 'hair_color',
               'hair_type', 'completed_level_of_education', 'favourite_color', 'relation_to_smoking',
               'relation_to_alcohol', 'sign_in_zodiac', 'on_pokec_i_am_looking_for', 'love_is_for_me',
               'my_partner_should_be', 'marital_status', 'I_like_movies', 'I_like_watching_movie', 'I_like_music',
               'I_mostly_like_listening_to_music', 'the_idea_of_good_evening', 'I_like_specialties_from_kitchen',
               'I_am_going_to_concerts', 'my_active_sports', 'my_passive_sports', 'I_like_books']

    labels_dict = {}
    # convert labels
    for key, value in labels_en_sk.items():
        if isinstance(value, list):
            for v in value:
                labels_dict[v] = key
        else:
            labels_dict[value] = key

    profiles = pd.read_csv('./process/profiles_all_hobbies_work.csv', usecols=usecols)
    n_rows = profiles.shape[0]

    null_count = {}

    filter_count = {}

    multi_feature_list = ['region', 'body', 'spoken_languages', 'I_am_working_in_field', 'hobbies',
                          'I_most_enjoy_good_food', 'pets', 'body_type', 'my_eyesight', 'eye_color', 'hair_color',
                          'hair_type', 'completed_level_of_education', 'favourite_color', 'relation_to_smoking',
                          'relation_to_alcohol', 'sign_in_zodiac', 'on_pokec_i_am_looking_for', 'love_is_for_me',
                          'my_partner_should_be', 'marital_status', 'I_like_movies', 'I_like_watching_movie',
                          'I_like_music', 'I_mostly_like_listening_to_music', 'the_idea_of_good_evening',
                          'I_like_specialties_from_kitchen', 'I_am_going_to_concerts', 'my_active_sports',
                          'my_passive_sports', 'I_like_books']

    profiles_label = profiles['hobbies'].values
    profiles_label_eng = []

    select_profiles = []
    #for labels in profiles_label:
    for idx, data in profiles.iterrows():
        labels = data['hobbies']
        flag = False
        if isinstance(labels, str):
            labels_eng = ''
            labels = labels.split(',')
            for label in labels:
                label = label.strip()
                if label in labels_dict:
                    flag = True
                    label = labels_dict[label]
                    if label in filter_count:
                        filter_count[label] += 1
                    else:
                        filter_count[label] = 1
                    labels_eng = labels_eng + label + ','
            if flag is False:
                continue
            labels_eng = labels_eng[:-1] + '\n'
            profiles_label_eng.append(labels_eng)
            data['hobbies'] = labels_eng
            select_profiles.append(data)

    profiles_label_eng = pd.DataFrame(profiles_label_eng)

    labels_en = []
    labels_sum = []
    labels_ratio = []
    # count the ratio of each label
    for key in labels_en_sk:
        if key in filter_count:
            print(key, filter_count[key], filter_count[key] / profiles_label_eng.shape[0])
            labels_en.append(key)
            labels_sum.append(filter_count[key])
            labels_ratio.append(filter_count[key] / profiles_label_eng.shape[0])
        else:
            print(key, 0, 0)

    label_count = pd.DataFrame({'label': labels_en, 'count': labels_sum, 'ratio': labels_ratio})

    select_profiles = pd.DataFrame(select_profiles)

    print("select_count:", select_profiles.count())

    label_count.to_csv('./process/label_count_hobbies.csv', index=False, header=['label', 'count', 'ratio'])

    select_profiles.to_csv('./process/profiles_select_by_label.csv', index=False)

    profiles_label_eng.to_csv('./process/profiles_hobbies_eng.csv', index=False, header=False)


def softmax(x):
    f_x = np.exp(x) / np.sum(np.exp(x))
    return f_x

def sample_label():
    labels = pd.read_csv('./process/label_count_hobbies.csv')

    label_ratio = {}

    for idx, label in labels.iterrows():
        label_ratio[label['label']] = 1 - label['ratio']

    print(label_ratio)

    profiles = pd.read_csv('./process/profiles_select_by_label.csv')
    profiles_sample = []

    label_count = Counter()

    for idx, profile in profiles.iterrows():
        labels_split = profile['hobbies'].split(',')
        ratio = []
        labels = []
        for label in labels_split:
            label = label.strip()
            ratio.append(label_ratio[label])
            labels.append(label)

        ratio = np.array(ratio)
        random_idx = ratio.argsort()[-3:]
        labels_random = []
        for idx in random_idx:
            labels_random.append(labels[idx])
        label = np.random.choice(labels_random)
        #label = labels[np.argmax(ratio)]
        profile['hobbies'] = label
        label_count[label] += 1
        profiles_sample.append(profile)

    profiles_sample = pd.DataFrame(profiles_sample)

    print(label_count)

    profiles_sample.to_csv('./process/profiles_sample_by_label.csv', index=False)


if __name__ == '__main__':
    #select_label_profile()

    sample_label()
