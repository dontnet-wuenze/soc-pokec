import pandas as pd

if __name__ == '__main__':
    profiles = pd.read_csv('./process/profiles_sample_normalize.csv')
    labels = profiles['hobbies']
    labels_count = labels.value_counts()
    print(labels_count.sum())
    labels_count.to_csv("./feature_analysis/labels_count.csv")