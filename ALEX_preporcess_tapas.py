import pandas as pd

df = pd.read_csv("/Users/alexandra/Documents/data/tapas/tapas_100_000_single_coords.csv")
df = df[["tid", "lat", "lon", "sequence"]] #TRIP_ID|integer
df.columns = ["tid", "lat","lon","timeStamp"]
df.timeStamp = (df.timeStamp * 150000) + 1600000000000

df.insert(3, "Z", "")
df.insert(3, "Y", "")
df.insert(3, "X", "")

df.to_csv("/Users/alexandra/Documents/data/tapas/tapas_100_000_simra_format.csv", index=False)
