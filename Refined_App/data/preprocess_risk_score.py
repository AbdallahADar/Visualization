import numpy as np
import pandas as pd
import os

countries = pd.read_csv("loaded_data/macri_risk_scores.csv")

# Save files path
os.makedirs("risk_scores", exist_ok = True)

## Sector and Industries
risk_score_types = [
    "Macro Risk", "Business Risk", "Financial Risk",
    "Social Risk", "Political Risk", "Security Risk"
]

for i in risk_score_types+["Overall Risk"]:
    os.makedirs(f"risk_scores/{i}", exist_ok = True)
    countries[["Country", i]].to_csv(f"risk_scores/{i}/countries.csv", index = False)