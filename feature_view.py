import numpy as np

user_feature = np.load('./process/user_feature.npy')
feature = user_feature[:10]
print(user_feature.shape)
