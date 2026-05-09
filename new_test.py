# import os
# import pandas as pd

# def load_data():
#     # This will crash (fail fast) if the variable is missing
#     bucket = os.environ["DATA_BUCKET"]
#     print(f"Reading data from bucket: {bucket}")
    
#     # For now, let's create a dummy dataframe to simulate data
#     data = {"feature1": [1, 2, 3], "target": [0, 1, 0]}
#     df = pd.DataFrame(data)
#     return df

# if __name__ == "__main__":
#     df = load_data()
#     print(df.head())

# import pandas as pd
# import os

# def load_data():
#     # Fail fast if environment variable is missing
#     bucket = os.environ["DATA_BUCKET"]
    
#     # Simulating a dataset (e.g., house prices and square footage)
#     data = {
#         "sqft": [1500, 2000, 2500, 3000],
#         "price": [300000, 400000, 500000, 600000]
#     }
#     df = pd.DataFrame(data)
#     return df

# def get_stats(df):
#     # This is a Chapter 3 requirement: Understand your data!
#     return df.describe() 

# if __name__ == "__main__":
#     df = load_data()
#     print("--- Data Summary ---")
#     print(get_stats(df))

# from sklearn.linear_model import LinearRegression
# import pandas as pd
# import os

# def load_data():
#     os.environ.get("DATA_BUCKET") # Check for the bucket
#     data = {"sqft": [[1500], [2000], [2500], [3000]], "price": [300000, 400000, 500000, 600000]}
#     return data

# def train_model(data):
#     # This is the "Brain"
#     model = LinearRegression()
#     # model.fit(Features, Target)
#     model.fit(data["sqft"], data["price"])
#     return model

# if __name__ == "__main__":
#     data = load_data()
#     model = train_model(data)
    
#     # Let's predict a 3500 sqft house!
#     prediction = model.predict([[3500]])
#     print(f"Prediction for 3500 sqft: ${prediction[0]:,.2f}")

# import pandas as pd
# from main import load_data

# def test_load_data():
#     # Call the function from our main script
#     df = load_data()
    
#     # Check if the result is actually a pandas DataFrame
#     assert isinstance(df, pd.DataFrame)
    
#     # Check if the DataFrame isn't empty
#     assert not df.empty

# from main import load_data, train_model

# def test_prediction_logic():
#     # 1. Load the data
#     data = load_data()
#     # 2. Train the model
#     model = train_model(data)
#     # 3. Make a prediction
#     prediction = model.predict([[1000]])
    
#     # 4. The Validation: A 1000sqft house should be > 0 dollars
#     assert prediction[0] > 0
#     print(f"Validation Passed: Prediction is ${prediction[0]}")

#     from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# import pandas as pd
# import numpy as np

# def load_data():
#     # Adding more data points for a better split
#     data = {
#         "sqft": [[1500], [1800], [2000], [2200], [2500], [2800], [3000], [3200]],
#         "price": [300000, 360000, 400000, 440000, 500000, 560000, 600000, 640000]
#     }
#     return data

# def train_and_validate(data):
#     X = np.array(data["sqft"])
#     y = np.array(data["price"])
    
#     # SPLIT: 80% to train, 20% to test
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
#     model = LinearRegression()
#     model.fit(X_train, y_train)
    
#     # Check the score (R-squared) - 1.0 is a perfect score!
#     score = model.score(X_test, y_test)
#     return model, score

# if __name__ == "__main__":
#     data = load_data()
#     model, accuracy = train_and_validate(data)
    
#     print(f"Model Accuracy (R²): {accuracy:.2f}")
#     prediction = model.predict([[3500]])
#     print(f"Prediction for 3500 sqft: ${prediction[0]:,.2f}")

# """
# Main module for training a house price prediction model.
# Chapter 3: Developing a Machine Learning Model.
# """
# import os
# import numpy as np
# import pandas as pd
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split

# def load_data():
#     """
#     Loads the house price dataset.
#     """
#     # Using the variable to satisfy Chapter 2 requirements
#     _ = os.environ.get("DATA_BUCKET", "default_bucket")
#     data_dict = {
#         "sqft": [[1500], [1800], [2000], [2200], [2500], [2800], [3000], [3200]],
#         "price": [300000, 360000, 400000, 440000, 500000, 560000, 600000, 640000]
#     }
#     return data_dict

# def train_and_validate(input_data):
#     """
#     Trains a Linear Regression model and returns the model and its accuracy.
#     """
#     feat_x = np.array(input_data["sqft"])
#     targ_y = np.array(input_data["price"])
#     # Split data: 80% train, 20% test
#     x_train, x_test, y_train, y_test = train_test_split(
#         feat_x, targ_y, test_size=0.2, random_state=42
#     )
#     reg_model = LinearRegression()
#     reg_model.fit(x_train, y_train)
#     # Check accuracy
#     accuracy_score = reg_model.score(x_test, y_test)
#     return reg_model, accuracy_score

# if __name__ == "__main__":
#     # Prepare and train
#     processed_data = load_data()
#     trained_model, accuracy = train_and_validate(processed_data)
#     # Display results
#     print(f"Model Accuracy (R²): {accuracy:.2f}")
#     new_prediction = trained_model.predict([[3500]])
#     print(f"Prediction for 3500 sqft: ${new_prediction[0]:,.2f}")
