import os

## Run the data preparation files by running this script when needed

# Geodata
# os.system("python3.9 preprocess_geodata.py")
os.system("python3.9 preprocess_geo_rates.py")
os.system("python3.9 preprocess_risk_score.py")