import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout

import joblib
import csv
import numpy as np

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


class Predictor():

    features = ['originLatitude', 'originLongitude', 'hour', 'minute', 'day_of_week', 'is_weekend']
    outputs = ['mileage', 'price', 'equipmentType_Flatbed', 'equipmentType_Reefer', 'equipmentType_Van']

    def __init__(self, type):
        self.DFL = pd.DataFrame(columns=['seq','type','timestamp','loadId','originLatitude','originLongitude','destinationLatitude','destinationLongitude','equipmentType','price','mileage'])
        self.type = type
    
    def add_data(self, loads):
        for f in loads:
            with open(f, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)  # skip header
                for row in reader:
                    self.DFL.loc[len(self.DFL)] = row
    
    def preprocess(self):
        self.DFL['timestamp'] = pd.to_datetime(self.DFL['timestamp'])
        self.DFL['hour'] = self.DFL['timestamp'].dt.hour
        self.DFL['minute'] = self.DFL['timestamp'].dt.minute
        self.DFL['day_of_week'] = self.DFL['timestamp'].dt.dayofweek
        self.DFL['is_weekend'] = self.DFL['timestamp'].dt.weekday.isin([5, 6]).astype(int)

        df_encoded = pd.get_dummies(self.DFL['equipmentType'], prefix='equipmentType')
        self.DFL = pd.concat([self.DFL, df_encoded], axis=1)
        self.DFL = self.DFL.drop(columns=['timestamp', 'equipmentType', 'type'])

    def train(self, normalize=False):
        if self.type == 'nn':
            return self.train_nn(normalize=normalize)
        elif self.type == 'rf':
            return self.train_forest(normalize=normalize)
        else:
            print('invalid type')

    def train_nn(self, normalize=False):
        if normalize:
            scaler = MinMaxScaler()
            DFL_X = scaler.fit_transform(self.DFL)
            DFL_norm = pd.DataFrame(DFL_X, columns=self.DFL.columns)
        else:
            DFL_norm = self.DFL
        
        X = DFL_norm[self.features].astype('float32')
        y = DFL_norm[self.outputs].astype('float32')

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


        model = Sequential([
            Dense(128, activation='relu', input_shape=(len(self.features),)),
            Dropout(0.5),
            Dense(len(self.outputs), activation='linear')
        ])

        model.compile(
            optimizer='adam', 
            loss='mean_squared_error'#CustomMSELoss(self.DFL)
        )
        model.fit(X_train.values, y_train.values, epochs=50, batch_size=16, validation_split=0.2)

        y_pred = model.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)

        self.model = model
        self.mse = mse
        return mse

    
    def train_forest(self, normalize=False):
        if normalize:
            scaler = MinMaxScaler()
            DFL_X = scaler.fit_transform(self.DFL)
            DFL_norm = pd.DataFrame(DFL_X, columns=self.DFL.columns)
        else:
            DFL_norm = self.DFL
        
        X = DFL_norm[self.features]
        y = DFL_norm[self.outputs]

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize the Random Forest Regressor
        rf_model = RandomForestRegressor(n_estimators=100, bootstrap=True, random_state=None)

        # Train the model
        rf_model.fit(X_train, y_train)

        # Make predictions on the test set
        y_pred = rf_model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)

        # joblib.dump(rf_model, 'rf_model.pkl')
        self.model = rf_model
        self.mse = mse
        return mse
    
    def save(self, path):
        if self.type == 'nn':
            self.model.save(path)
        elif self.type == 'rf':
            joblib.dump(self.model, path)

    def load(self, path):
        if self.type == 'nn':
            self.model = load_model(path)
        elif self.type == 'rf':
            self.model = joblib.load(path)
    
    def predict(self, features, n):

        if self.type == 'nn':
            features = np.array([features]).astype('float32')
            ls = []
            for i in range(0, n):
                v = self.model(features, training=True)[0].numpy().tolist()
                ls.append([v[1], v[0], ['Flatbed', 'Reefer', 'Van'][(v[-3:]).index(max(v[-3:]))]])
            return ls
        elif self.type == 'rf':
            v = self.model.predict([features])
            v = v[0].tolist()
            return [v[1], v[0], ['Flatbed', 'Reefer', 'Van'][(v[-3:]).index(max(v[-3:]))]]



# loader = Predictor('nn')

# loader.add_data(
#     loads=[f'mqtt_data_2/load_{x}.csv' for x in range(0, 8)]
# )
# loader.preprocess()
# print(loader.train_nn(normalize=False))
# loader.save('model.h5')

# loader.load('model.h5')
# idx = 100
# loader.predict(
#     pd.DataFrame(
#         [loader.DFL.loc[idx][loader.features]], 
#         columns=['originLatitude', 'originLongitude', 'hour', 'minute', 'day_of_week', 'is_weekend']
#     ),
#     10
# )
