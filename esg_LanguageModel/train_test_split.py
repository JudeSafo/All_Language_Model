import pandas as pd
from sklearn.model_selection import train_test_split

# Load the data
data = pd.read_csv('../data/data.csv')

# Split the data
train, val = train_test_split(data, test_size=0.2)

# Save the splits
train.to_csv('../data/train.csv', index=False)
val.to_csv('../data/val.csv', index=False)
