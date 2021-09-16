import data_init
import pandas as pd

# ------------------ Get the data -----------
print(data_init.final_result.head())
data_init.final_result["As of date"] = pd.to_datetime(data_init.final_result["As of date"])

