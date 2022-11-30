import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import math
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error,r2_score


ipl2020_data = pd.read_csv('iplScore2020.csv')
# print(type(ipl2020_data["ball_no"]))
# ipl2020_data = ipl2020_data.astype({"ball_no":float})

# X = X.astype(float)
# y = y.astype(float)

def encode_and_bind(original_dataframe, feature_to_encode):
    dummies = pd.get_dummies(original_dataframe[[feature_to_encode]])
    res = pd.concat([original_dataframe, dummies], axis=1)
    return(res)

new_df = encode_and_bind(ipl2020_data,"team_name")
print(new_df.head())

X = new_df.iloc[:,[3,4,5,6,7,8,9,11,12,13,14,15,16,17,18]].values
y = new_df.iloc[:,10].values

# enc = OneHotEncoder(sparse=True)
# X_transform = enc.fit_transform(X)
# print(X_transform[0:3])


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# # sc = StandardScaler()
# # X_train = sc.fit_transform(X_train)
# # X_test = sc.transform(X_test)
print("X tesT", X_test[0])
lin = LinearRegression()
model = lin.fit(X_train, y_train)


def calculate_accuracy(pred, original):
    diff = 1 - ((abs(pred-original))/original)
    if diff >=0:
        return diff
    return 0

y_pred = model.predict(X_test)
y_pred = np.floor(y_pred)
for i in range(len(y_pred)):   
    print("Ball:{}  Original:{}  Predicted:{}   Accuracy:{}".format(X_test[i][0],y_test[i],y_pred[i],calculate_accuracy(y_pred[i], y_test[i])))
    print("\n")
print("Y prediction", y_pred)

score = mean_squared_error(y_test, y_pred,squared=False)
msa = mean_absolute_error(y_test, y_pred)
r2s = r2_score(y_test,y_pred)
print("MSE", score)
print("MSA", msa)
print("r2s",r2s)






