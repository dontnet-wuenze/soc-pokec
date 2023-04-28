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

    usecols = str.split("user_id public completion_percentage gender region last_login registration age")

    # ts.preaccelerate()
    # profiles = pd.read_csv('./process/profiles_english_multithread.csv', names=names, index_col=False,
    #                        usecols=names, header=None, sep=',')
    #
    # profiles.to_csv('./process/profiles_english_multithread_deal.csv', index=False)

    #profiles = pd.read_csv('./process/profiles_replace.csv', names=names, index_col=False, sep=';')
    profiles = pd.read_csv('./process/profiles_all_book.csv')

    print(profiles.shape)
