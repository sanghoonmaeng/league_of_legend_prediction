import pickle
import numpy as np
from xgboost import XGBClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

with open('data\\final_data.pkl', 'rb') as file:
    final_data = pickle.load(file)

match_features = list(final_data.columns[:-1])
match_stats = final_data[match_features].values

winning_team = list(final_data.columns[-1:])
win = final_data[winning_team].values

X = np.array(match_stats)
y = np.array(win)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # 80% for training, 20% for testing

nn_model = Sequential([
    Dense(16, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile the model
nn_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
nn_model.summary()

# Train and save the best model
callback = ModelCheckpoint(
    filepath='model\\win_prediction_nn_model.h5',
    monitor='val_accuracy',
    save_best_only=True,
    save_weights_only=False,
    mode='max',
    verbose=1
)

nn_model.fit(X_train, y_train, epochs=20, batch_size=64, validation_data=(X_test, y_test), callbacks=[callback])

nn_accuracy = nn_model.evaluate(X_test, y_test)[1]
print(f'Neural Network Model Accuracy:{nn_accuracy: %}')


# Create and fit the Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train.ravel())

rf_pred = rf_model.predict(X_test)

# Calculate accuracy
rf_accuracy = accuracy_score(y_test.ravel(), rf_pred)

print(f'Random Forest Model Accuracy:{rf_accuracy: %}')


# Random Forest hyperparameter tuning
tuned_rf_model = RandomForestClassifier(random_state=42)

param_grid = {
    'n_estimators': [100, 150, 200],      # Number of trees in the forest
    'max_depth': [None, 1, 3, 5],         # Maximum depth of the trees
    'min_samples_split': [2, 3, 5, 7],    # Minimum number of samples required to split an internal node
    'min_samples_leaf': [1, 2, 4]         # Minimum number of samples required to be at a leaf node
}

# Perform Grid Search with 5-fold cross-validation
grid_search = GridSearchCV(estimator=tuned_rf_model, param_grid=param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train.ravel())

best_params = grid_search.best_params_

# Train the Random Forest model with the tuned hyperparameters
tuned_rf_model = RandomForestClassifier(random_state=42, **best_params)
tuned_rf_model.fit(X_train, y_train.ravel())

tuned_rf_pred = tuned_rf_model.predict(X_test)

# Calculate accuracy
tuned_rf_accuracy = accuracy_score(y_test.ravel(), tuned_rf_pred)

print(f'Tuned Random Forest Model Accuracy:{tuned_rf_accuracy: %}')

# Save the model using pickle
filename = "model\\win_prediction_rf_model.pickle"

with open(filename, "wb") as f:
    pickle.dump(tuned_rf_model, f)


# Create and fit the XGBoost model
xgb_model = XGBClassifier(n_estimators=100, random_state=42)
xgb_model.fit(X_train, y_train)

xgb_pred = xgb_model.predict(X_test)

# Calculate accuracy
xgb_accuracy = accuracy_score(y_test, xgb_pred)

print(f'XGBoost Model Accuracy:{xgb_accuracy: %}')


# XGBoost hyperparameter tuning
tuned_xgb_model = XGBClassifier(random_state=42)

param_grid = {
    'n_estimators': [100, 150, 200],
    'max_depth': [None, 1, 3, 5],
    'booster': ['gbtree'],
    'learning_rate': [0.05, 0.1, 0.2, 0.3],
    'objective': ['binary:logistic'],
    'eval_metric' : ['error'],
    'tree_method': ['gpu_hist']
}

# Perform Grid Search with 5-fold cross-validation
grid_search = GridSearchCV(estimator=tuned_xgb_model, param_grid=param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

best_params = grid_search.best_params_

# Train the XGBoost model with the tuned hyperparameters
tuned_xgb_model = XGBClassifier(random_state=42, **best_params)
tuned_xgb_model.fit(X_train, y_train)

tuned_xgb_pred = tuned_xgb_model.predict(X_test)

# Calculate accuracy
tuned_xgb_accuracy = accuracy_score(y_test, tuned_xgb_pred)

print(f'Tuned XGBoost Model Accuracy:{tuned_xgb_accuracy: %}')

# Save the model using pickle
filename = "model\\win_prediction_xgb_model.pickle"

with open(filename, "wb") as f:
    pickle.dump(tuned_xgb_model, f)