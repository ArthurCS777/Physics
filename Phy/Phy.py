import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
import tkinter as tk
import time

# create sample dataset
df = pd.DataFrame({
    'Food': ['Pizza', 'Burger', 'Taco', 'Pasta', 'Fish', 'Rice', 'Steak'],
    'Cooking Time (minutes)': [20, 15, 10, 25, 30, 20, 20]
})

# create encoder
encoder = OneHotEncoder()

# encode food column
encoded_food = encoder.fit_transform(df[['Food']])

# create encoded dataframe
encoded_df = pd.concat([
    df[['Cooking Time (minutes)']],
    pd.DataFrame(encoded_food.toarray(), columns=encoder.get_feature_names_out(['Food']))
], axis=1)

# create linear regression model
lr = LinearRegression()

# fit model
lr.fit(encoded_df.iloc[:, 1:], encoded_df.iloc[:, 0])

# create tkinter window
window = tk.Tk()
window.title("Cooking Timer")

# create label and entry widgets
tk.Label(window, text="Enter a food item:").grid(row=0, column=0, pady=10)
food_entry = tk.Entry(window)
food_entry.grid(row=0, column=1, padx=10, pady=10)
time_label = tk.Label(window, text="")

# create countdown function
def countdown(count):
    time_label['text'] = "Cooking time remaining: {} seconds".format(count)
    if count > 0:
        window.after(1000, countdown, count-1)
    else:
        time_label['text'] = "Done!"

# create button click function
def button_click():
    # get user input
    user_input = food_entry.get()
    
    # encode user input
    user_input_encoded = encoder.transform([[user_input]])
    
    # create encoded dataframe for user input
    user_input_encoded_df = pd.DataFrame(user_input_encoded.toarray(), columns=encoder.get_feature_names_out(['Food']))
    
    # make prediction for user input
    prediction = lr.predict(user_input_encoded_df)
    
    # calculate countdown time
    countdown_time = int(prediction[0] * 60)
    
    # start countdown
    countdown(countdown_time)

# create button widget
button = tk.Button(window, text="Start Timer", command=button_click)

# add widgets to window
button.grid(row=1, column=0, columnspan=2, pady=10)
time_label.grid(row=2, column=0, columnspan=2)

# start tkinter event loop
window.mainloop()
