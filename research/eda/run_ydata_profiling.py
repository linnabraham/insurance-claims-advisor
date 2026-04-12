import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_csv("../../data/raw/insurance_claims.csv")
ProfileReport(df, title="Insurance Claims EDA", explorative=True).to_file(
    "output/report.html"
)
