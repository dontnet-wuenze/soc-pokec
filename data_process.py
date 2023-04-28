from typing import Any

import numpy as np
import pandas as pd
from rich.progress import track
from collections import Counter

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

usecols_region = ['user_id', 'public', 'gender', 'region_province', 'region_city', 'age', 'body',
                  'I_am_working_in_field', 'spoken_languages',
                  'hobbies', 'I_most_enjoy_good_food', 'pets', 'body_type', 'my_eyesight', 'eye_color', 'hair_color',
                  'hair_type', 'completed_level_of_education', 'favourite_color', 'relation_to_smoking',
                  'relation_to_alcohol', 'sign_in_zodiac', 'on_pokec_i_am_looking_for', 'love_is_for_me',
                  'my_partner_should_be', 'marital_status', 'I_like_movies', 'I_like_watching_movie', 'I_like_music',
                  'I_mostly_like_listening_to_music', 'the_idea_of_good_evening', 'I_like_specialties_from_kitchen',
                  'I_am_going_to_concerts', 'my_active_sports', 'my_passive_sports', 'I_like_books']

usecols_body = ['user_id', 'public', 'gender', 'region_province', 'region_city', 'age', 'height', 'weight',
                'I_am_working_in_field', 'spoken_languages',
                'hobbies', 'I_most_enjoy_good_food', 'pets', 'body_type', 'my_eyesight', 'eye_color', 'hair_color',
                'hair_type', 'completed_level_of_education', 'favourite_color', 'relation_to_smoking',
                'relation_to_alcohol', 'sign_in_zodiac', 'on_pokec_i_am_looking_for', 'love_is_for_me',
                'my_partner_should_be', 'marital_status', 'I_like_movies', 'I_like_watching_movie', 'I_like_music',
                'I_mostly_like_listening_to_music', 'the_idea_of_good_evening', 'I_like_specialties_from_kitchen',
                'I_am_going_to_concerts', 'my_active_sports', 'my_passive_sports', 'I_like_books']

usecols_categories = ['region_province', 'region_city', 'I_am_working_in_field', 'spoken_languages',
                      'I_most_enjoy_good_food', 'pets', 'body_type', 'my_eyesight', 'eye_color',
                      'hair_color',
                      'hair_type', 'completed_level_of_education', 'favourite_color', 'relation_to_smoking',
                      'relation_to_alcohol', 'sign_in_zodiac', 'on_pokec_i_am_looking_for', 'love_is_for_me',
                      'my_partner_should_be', 'marital_status', 'I_like_movies', 'I_like_watching_movie',
                      'I_like_music',
                      'I_mostly_like_listening_to_music', 'the_idea_of_good_evening', 'I_like_specialties_from_kitchen',
                      'I_am_going_to_concerts', 'my_active_sports', 'my_passive_sports', 'I_like_books']


def remove_div(profiles):
    # profiles = pd.read_csv('./raw/test.txt', names=names, index_col=False, usecols=names, header=None, sep='\t')

    profiles_array = profiles.values
    # remove <div>
    for i in track(range(profiles_array.shape[0])):
        for j in range(profiles_array.shape[1]):
            element = profiles_array[i, j]
            if isinstance(element, str):
                if element.find("<div>") != -1:
                    start = element.find('>', element.find('>') + 1)
                    end = element.find('<', start + 1)
                    # deal = element[start + 1: end]
                    profiles_array[i, j] = element[start + 1:end]

    profiles_remove = pd.DataFrame(data=profiles_array, columns=profiles.columns)

    # profiles_remove.fillna('0', inplace=True)
    profiles_remove.to_csv('./process/profiles_remove.csv', index=False)


def select_not_na(profiles, col):
    profiles_select = profiles[profiles[col].notna()]
    profiles_select.to_csv('./process/profiles_all_' + 'hobbies_work' + '.csv', index=False)


def split_region(profiles):
    print(profiles.isnull().sum())
    province = []
    city = []
    for idx, profile in profiles.iterrows():
        region = profile['region']
        if isinstance(region, str):
            region_province, region_city = region.split(',')[:2]
            province.append(region_province)
            city.append(region_city)
    profiles['region_province'] = province
    profiles['region_city'] = city

    profiles = profiles[usecols_region]
    print(profiles.count())
    profiles.to_csv('./process/profiles_sample_region.csv', index=False)


def get_num(str):
    num = ''
    for i in str:
        if i.isdigit():
            num += i
    return num


def split_body(profiles):
    height = []
    weight = []
    for idx, profile in profiles.iterrows():
        body = profile['body']
        h_flag = False
        w_flag = False
        if isinstance(body, str):
            body_list = body.split(',')
            for element in body_list:
                if element.find('cm') != -1 and not h_flag:
                    value = get_num(element)
                    # check whether value is a number
                    if value.isdigit():
                        height.append(int(value))
                        h_flag = True
                elif element.find('kg') != -1 and not w_flag:
                    value = get_num(element)
                    # check whether value is a number
                    if value.isdigit():
                        weight.append(int(value))
                        w_flag = True
        if not h_flag:
            height.append(None)
        if not w_flag:
            weight.append(None)
    profiles['height'] = height
    profiles['weight'] = weight

    # remove 异常点
    profiles['height'] = profiles['height'].apply(lambda x: x if x > 150 else None)
    profiles['height'] = profiles['height'].apply(lambda x: x if x < 200 else None)

    profiles['weight'] = profiles['weight'].apply(lambda x: x if x < 200 else None)
    profiles['weight'] = profiles['weight'].apply(lambda x: x if x > 50 else None)
    profiles = profiles[usecols_body]
    print(profiles.count())
    profiles.to_csv('./process/profiles_sample.csv', index=False)


def fill_na(profiles):
    fill_col = ['age', 'height', 'weight']
    profiles['age'] = profiles['age'].apply(lambda x: x if x > 10 else None)
    for col in fill_col:
        profiles[col].fillna(profiles[col].mean(), inplace=True)

    profiles.to_csv('./process/profiles_sample_fill.csv', index=False)


def normalize(profiles):
    # keep value in [0, 1]
    profiles['age'] = (profiles['age'] - profiles['age'].min()) / (profiles['age'].max() - profiles['age'].min())

    profiles['height'] = (profiles['height'] - profiles['height'].min()) / (
            profiles['height'].max() - profiles['height'].min())

    profiles['weight'] = (profiles['weight'] - profiles['weight'].min()) / (
            profiles['weight'].max() - profiles['weight'].min())
    profiles.to_csv('./process/profiles_sample_normalize.csv', index=False)


def create_category_map(profiles):
    catogories = 50

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

    col: str | Any
    for col in usecols_categories:
        col_count = profiles[col].value_counts()
        # with open("./feature_analysis/" + col + ".txt", "w") as f:
        #     f.write(str(col_count))
        col_count_filter = col_count[col_count > 5]
        # count the biggest 50 categories
        if col_count_filter.shape[0] > catogories:
            col_count_filter = col_count_filter[:catogories]

        col_map = {}

        i = 0

        # print(col_count_filter.keys())
        if col not in multi_feature_list:
            for feature in col_count_filter.keys():
                col_map[feature] = i
                i += 1
        else:
            # collect all features in multi-feature
            feature_set = Counter()
            for features in col_count.keys():
                feature_list = str.split(features, ",")

                for feature in feature_list:
                    feature = feature.strip()
                    if feature == '' or feature == '...' or feature == '.' or feature.isdigit():
                        continue
                    # count feature num
                    if feature in feature_set:
                        feature_set[feature] += col_count[features]
                    else:
                        feature_set[feature] = col_count[features]

            # convert to pd
            feature_set = pd.Series(feature_set).sort_values(ascending=False)

            # count the biggest 50 categories
            if feature_set.shape[0] > catogories:
                feature_set = feature_set[:catogories]

            for feature in feature_set.keys():
                col_map[feature] = i
                i += 1

        col_series = pd.Series(col_map)
        col_series.to_csv("./feature_analysis/map/" + col + "_map.csv", header=False)

def select_edges():
    profiles = pd.read_csv('./process/profiles_sample_normalize.csv')
    user_id = set()
    for idx, data in profiles.iterrows():
        user_id.add(data['user_id'])

    edge_list = np.loadtxt('./raw/soc-pokec-relationships.txt', dtype=np.int32)

    edge_list = edge_list[edge_list[:, 0] != edge_list[:, 1], :]
    edge_list.sort(axis=-1)
    edge_list = np.unique(edge_list, axis=0)

    # Filter edges
    edge_list = edge_list[np.isin(edge_list[:, 0], list(user_id)) & np.isin(edge_list[:, 1], list(user_id)), :]

    # Compute redundant edge list
    edge_list = np.concatenate((edge_list, np.flip(edge_list, axis=1)))

    edge_list = np.transpose(edge_list, (1, 0))
    # count the unique nodes in the edge
    node_count = np.unique(edge_list[0])
    print(node_count.shape)
    node_count = np.unique(edge_list[1])
    print(node_count.shape)

    print(edge_list)
    np.save('./process/edge_list.npy', edge_list)

    # remove isolate nodes
    profiles_sample = profiles[profiles['user_id'].isin(node_count)]
    profiles_sample.to_csv('./process/profiles_final.csv', index=False)

def user_map_dict():
    profiles = pd.read_csv('./process/profiles_final.csv')
    profiles.sort_values(by='user_id', inplace=True)
    profiles.reset_index(drop=True, inplace=True)
    user_map = {}
    for idx, data in profiles.iterrows():
        user_map[data['user_id']] = idx

    # user_series = pd.Series(user_map)
    # user_series.to_csv('./process/user_map.csv', header=False)
    np.save('./process/user_map.npy', user_map)

def encode_features():
    profiles = pd.read_csv('./process/profiles_final.csv')
    profiles.sort_values(by='user_id', inplace=True)
    profiles.reset_index(drop=True, inplace=True)

    feature_dim = 0

    one_code = ['public', 'gender', 'age', 'height', 'weight']

    feature_dim += len(one_code)

    col_map_dict = {}
    col_map_file = {}

    for col in usecols_categories:
        col_map = pd.read_csv("./feature_analysis/map/" + col + "_map.csv", header=None, index_col=0)
        col_map = col_map.squeeze()
        feature_dim += col_map.shape[0]

        col_map_dict[col] = {}

        for idx, mapping in col_map.items():
            col_map_dict[col].update(
                {idx: mapping}
            )

    user_feature = []

    for col in usecols_categories:
        col_map = pd.read_csv("./feature_analysis/map/" + col + "_map.csv", header=None, index_col=0)
        col_map.squeeze('columns')
        col_map_file[col] = col_map

    for idx, user in profiles.iterrows():
        # track progress
        # if idx % 10000 == 0:
        #     print(idx)
        features = [0] * feature_dim
        cur_idx = 0
        for col in one_code:
            features[cur_idx] = user[col]
            cur_idx += 1

        for col in usecols_categories:
            col_map = col_map_file[col]
            col_features = user[col]
            if isinstance(col_features, str):
                col_features = user[col].split(',')
                for feature in col_features:
                    feature = feature.strip()
                    if feature in col_map_dict[col]:
                        features[cur_idx + col_map_dict[col][feature]] = 1

            cur_idx += col_map.shape[0]

        user_feature.append(features)

    user_feature = np.array(user_feature)
    np.save('./process/user_feature.npy', user_feature)




    profiles.to_csv('./process/profiles_sample_encode.csv', index=False)

def edge_map():
    edge_list = np.load('./process/edge_list.npy')
    user_map = np.load('./process/user_map.npy', allow_pickle=True).item()
    edge_map = [[], []]
    for node in edge_list[0]:
        edge_map[0].append(user_map[node])
    for node in edge_list[1]:
        edge_map[1].append(user_map[node])
    np.save('./process/edge_list_map.npy', edge_map)

if __name__ == '__main__':
    # profiles = pd.read_csv('./process/profiles_all_hobbies.csv')
    # select_not_na(profiles, 'I_am_working_in_field')

    # create_category_map(profiles)

    # profiles = pd.read_csv('./process/profiles_sample_by_label.csv')
    # split_region(profiles)

    # profiles = pd.read_csv('./process/profiles_sample_region.csv')
    # split_body(profiles)

    # profiles = pd.read_csv('./process/profiles_sample.csv')
    # fill_na(profiles)

    # profiles = pd.read_csv('./process/profiles_sample_fill.csv')
    # normalize(profiles)

    # profiles = pd.read_csv('./process/profiles_sample_normalize.csv')
    # create_category_map(profiles)

    #select_edges()
    #user_map_dict()
    #edge_map()
    encode_features()