from datasets import load_dataset
import pandas as pd

ds = load_dataset('cornell_movie_dialog', split='train', trust_remote_code=True)
df = ds.to_pandas()
print(df.head())
print("Cols:", df.columns)
