from datasets import load_dataset
ds = load_dataset('cornell_movie_dialog', split='train', streaming=True, trust_remote_code=True)
print("Features:", ds.features)
print("Row 0:", next(iter(ds)))
