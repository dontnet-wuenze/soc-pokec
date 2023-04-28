from collections import Counter

import pandas as pd

if __name__ == '__main__':
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

    complete = {'user_id': 0.0, 'public': 0.0, 'completion_percentage': 0.0, 'gender': 0.0, 'region': 0.0,
                'last_login': 0.0,
                'registration': 0.0, 'age': 0.0, 'body': 0.1894921716678926,
                'I_am_working_in_field': 0.34023597580197246,
                'spoken_languages': 0.12391431616554333, 'hobbies': 0.07957428284071634,
                'I_most_enjoy_good_food': 0.15471426212528333, 'pets': 0.16145878679616313,
                'body_type': 0.19723193779365628,
                'my_eyesight': 0.12839965774502005, 'eye_color': 0.0678025128720897, 'hair_color': 0.10403950943452872,
                'hair_type': 0.16372097212423256, 'completed_level_of_education': 0.18923848266958884,
                'favourite_color': 0.09214014440758365, 'relation_to_smoking': 0.10111232868487023,
                'relation_to_alcohol': 0.11238422624855518, 'sign_in_zodiac': 0.10337451401293964,
                'on_pokec_i_am_looking_for': 0.14840055841601993, 'love_is_for_me': 0.177625831244277,
                'relation_to_casual_sex': 0.29771529789693324, 'my_partner_should_be': 0.1818274614587868,
                'marital_status': 0.18454748787846945, 'children': 0.45502649473858026,
                'relation_to_children': 0.4029106684479938,
                'I_like_movies': 0.02940991038323551, 'I_like_watching_movie': 0.08119098728552772,
                'I_like_music': 0.055467823528528755, 'I_mostly_like_listening_to_music': 0.07178798204662473,
                'the_idea_of_good_evening': 0.10965068976387408, 'I_like_specialties_from_kitchen': 0.131777173994626,
                'fun': 0.827468964378462, 'I_am_going_to_concerts': 0.26939219718690427,
                'my_active_sports': 0.18969782487953527,
                'my_passive_sports': 0.21383580767671917, 'profession': 0.4467823528528754, 'I_like_books': 0.0,
                'life_style': 0.8050467598360779, 'music': 0.8454733776663614, 'cars': 0.9535538976537521,
                'politics': 0.975377155981206, 'relationships': 0.8115781257036492, 'art_culture': 0.967520302625456,
                'hobbies_interests': 0.8761142050827867, 'science_technologies': 0.9712340693816893,
                'computers_internet': 0.949985739375835, 'education': 0.9542714322170016, 'sport': 0.9244727321854782,
                'movies': 0.93297206418782, 'travelling': 0.9684104657970187, 'health': 0.9590059594397826,
                'companies_brands': 0.9807586652055782, 'more': 0.8270681657835087}

    usecols = ['user_id', 'public', 'gender', 'region_province', 'region_city', 'age', 'height', 'weight',
               'I_am_working_in_field', 'spoken_languages',
               'hobbies', 'I_most_enjoy_good_food', 'pets', 'body_type', 'my_eyesight', 'eye_color', 'hair_color',
               'hair_type', 'completed_level_of_education', 'favourite_color', 'relation_to_smoking',
               'relation_to_alcohol', 'sign_in_zodiac', 'on_pokec_i_am_looking_for', 'love_is_for_me',
               'my_partner_should_be', 'marital_status', 'I_like_movies', 'I_like_watching_movie', 'I_like_music',
               'I_mostly_like_listening_to_music', 'the_idea_of_good_evening', 'I_like_specialties_from_kitchen',
               'I_am_going_to_concerts', 'my_active_sports', 'my_passive_sports', 'I_like_books']

    catogories = 50

    # profiles = pd.read_csv('./process/profiles_remove.csv', nrows=n_rows)
    profiles = pd.read_csv('./process/profiles_final.csv', usecols=usecols)
    n_rows = profiles.shape[0]

    null_count = {}

    filter_count = {}

    multi_feature_list = ['spoken_languages', 'I_am_working_in_field', 'hobbies',
                          'I_most_enjoy_good_food', 'pets', 'body_type', 'my_eyesight', 'eye_color', 'hair_color',
                          'hair_type', 'completed_level_of_education', 'favourite_color', 'relation_to_smoking',
                          'relation_to_alcohol', 'sign_in_zodiac', 'on_pokec_i_am_looking_for', 'love_is_for_me',
                          'my_partner_should_be', 'marital_status', 'I_like_movies', 'I_like_watching_movie',
                          'I_like_music', 'I_mostly_like_listening_to_music', 'the_idea_of_good_evening',
                          'I_like_specialties_from_kitchen', 'I_am_going_to_concerts', 'my_active_sports',
                          'my_passive_sports', 'I_like_books']

    for col in usecols:
        col_count = profiles[col].value_counts()
        null_count[col] = profiles[col].isnull().sum() / n_rows
        # with open("./feature_analysis/" + col + ".txt", "w") as f:
        #     f.write(str(col_count))
        # col_count.to_csv("./feature_analysis/full/" + col + ".csv")
        # col_count_filter = col_count[col_count > 5]
        # col_count_filter.to_csv("./feature_analysis/filter/" + col + "_filter.csv")
        #
        # filter_sum = col_count.sum()
        #
        # # count the biggest 50 categories
        # if col_count_filter.shape[0] > catogories:
        #     col_count_filter = col_count_filter[:catogories]
        #
        # filter_first_sum = col_count_filter.sum()
        #
        # filter_count[col] = (filter_first_sum, filter_sum, filter_first_sum / filter_sum)
        #
        # # print(col_count_filter.keys())
        # if col in multi_feature_list:
        #     filter_first_sum = 0
        #     # collect all features in multi-feature
        #     feature_set = Counter()
        #     for features in col_count.keys():
        #         feature_list = str.split(features, ",")
        #
        #         for feature in feature_list:
        #             feature = feature.strip()
        #             # count feature num
        #             if feature in feature_set:
        #                 feature_set[feature] += col_count[features]
        #             else:
        #                 feature_set[feature] = col_count[features]
        #
        #     # convert to pd
        #     feature_set = pd.Series(feature_set).sort_values(ascending=False)
        #     feature_set.to_csv("./feature_analysis/multifeature/" + col + "_multi_feature.csv")
        #
        #     # count the biggest 50 categories
        #     if feature_set.shape[0] > catogories:
        #         feature_set = feature_set[:catogories]
        #
        #     for features in col_count.keys():
        #         feature_list = str.split(features, ",")
        #         flag = False
        #         for feature in feature_list:
        #             feature = feature.strip()
        #
        #             if feature in feature_set:
        #                 flag = True
        #
        #         if flag:
        #             filter_first_sum += col_count[features]
        #
        #     filter_count[col] = (filter_first_sum, filter_sum, filter_first_sum / filter_sum)

    print(null_count)

    # print(filter_count)
