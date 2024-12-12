import os

## Run the data preparation files by running this script when needed

# Geodata
# os.system("python3.9 preprocess_simulated/preprocess_geo_rates.py")
os.system("python3.9 preprocess_simulated/preprocess_sector_ndy_rates.py")
os.system("python3.9 preprocess_simulated/preprocess_sample_data.py")
os.system("python3.9 preprocess_simulated/risk_score.py")