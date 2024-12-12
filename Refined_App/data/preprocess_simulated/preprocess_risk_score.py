import pandas as pd
import numpy as np
import os
import pycountry

## Countries
countries = pd.DataFrame({"Country" : [country.alpha_3 for country in pycountry.countries]})

## Sector and Industries
risk_score_types = [
    "Macro Risk", "Business Risk", "Financial Risk",
    "Social Risk", "Political Risk", "Security Risk"
]

# Save files path
os.makedirs("risk_scores", exist_ok = True)

for i in risk_score_types:
    
    countries[i] = np.random.randint(0, 100, len(countries))

## Take Mean of other scores to get overall score
i = "Overall Risk"
countries[i] = countries.iloc[:,1:].mean(axis = 1).astype(int)

for i in risk_score_types+["Overall Risk"]:
    os.makedirs(f"risk_scores/{i}", exist_ok = True)
    countries[["Country", i]].to_csv(f"risk_scores/{i}/countries.csv", index = False)