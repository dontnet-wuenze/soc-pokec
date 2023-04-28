import os

# device = "1"
# os.environ['CUDA_VISIBLE_DEVICES'] = device
# os.environ['ARGOS_DEVICE_TYPE'] = 'cuda'

import argostranslate.package
import argostranslate.translate

from rich.progress import Progress, track

from multiprocessing import pool

def translate_feature(feature):
    from_code = "sk"
    to_code = "en"

    profiles = open('./feature_analysis/map/' + feature)

    profiles_eng = open('./feature_analysis/map_eng/' + feature, 'w')

    lines = profiles.readlines()

    for i in track(range(len(lines))):
        #print(line)
        label_sk = lines[i].split(',')[0]
        label_en = argostranslate.translate.translate(label_sk, from_code, to_code)
        profiles_eng.write(label_sk + ',' + label_en + ',' + lines[i].split(',')[1])


if __name__ == '__main__':
    for feature in os.listdir('./feature_analysis/map'):
        translate_feature(feature.split('/')[-1])
