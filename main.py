# Temat projektu: Przewidywanie ilości CO na podstawie innych parametrów powietrza

# Anna Oruba, Karolina Podsiadły, Adrianna Wachowska

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_, train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import KFold
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Lasso
from sklearn.ensemble import ExtraTreesRegressor


air_data = pd.read_excel('parametryPowietrza.xlsx')

air_data.head()
air_data.shape

scalar = StandardScaler()
sns.set(style='whitegrid', context='notebook')
features_plot = ['C6H6(GT)', 'RH', 'AH', 'PT08.S1(CO)']

data_to_plot = air_data[features_plot]
data_to_plot = scalar.fit_transform(data_to_plot)
data_to_plot = pd.DataFrame(data_to_plot)

sns.pairplot(data_to_plot, size=2.0);
plt.tight_layout()
plt.show()

air_data.dropna(axis=0, how='all')

features = air_data
features = features.drop('Date', axis=1)
features = features.drop('Time', axis=1)
features = features.drop('C6H6(GT)', axis=1)
features = features.drop('PT08.S4(NO2)', axis=1)

labels = air_data['C6H6(GT)'].values
features = features.values

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3)

print("X_trian shape --> {}".format(X_train.shape))
print("y_train shape --> {}".format(y_train.shape))
print("X_test shape --> {}".format(X_test.shape))
print("y_test shape --> {}".format(y_test.shape))

regressor = LinearRegression()
regressor.fit(X_train, y_train)
print("Predicted values:", regressor.predict(X_test))
print("R^2 score for liner regression: ", regressor.score(X_test, y_test))

support_regressor = SVR(kernel='rbf', C=1000)
support_regressor.fit(X_train, y_train)
print("Coefficient of determination R^2 <-- on train set: {}".format(support_regressor.score(X_train, y_train)))
print("Coefficient of determination R^2 <-- on test set: {}".format(support_regressor.score(X_test, y_test)))

dtr = DecisionTreeRegressor()
dtr.fit(X_train, y_train)
print("Coefficient of determination R^2 <-- on train set: {}".format(dtr.score(X_train, y_train)))
print("Coefficient of determination R^2 <-- on test set: {}".format(dtr.score(X_test, y_test)))

indiana_jones = Lasso(alpha=1.0)
indiana_jones.fit(X_train, y_train)
print("Coefficient of determination R^2 <-- on train set : {}".format(indiana_jones.score(X_train, y_train)))
print("Coefficient of determination R^2 <-- on test set: {}".format(indiana_jones.score(X_test, y_test)))

etr = ExtraTreesRegressor(n_estimators=300)
etr.fit(X_train, y_train)

print(etr.feature_importances_)
indecis = np.argsort(etr.feature_importances_)[::-1]

plt.figure(num=None, figsize=(14, 10), dpi=80, facecolor='w')
plt.title("Feature importances")
plt.bar(range(X_train.shape[1]), etr.feature_importances_[indecis],
       color="r", align="center")
plt.xticks(range(X_train.shape[1]), indecis)
plt.show()






