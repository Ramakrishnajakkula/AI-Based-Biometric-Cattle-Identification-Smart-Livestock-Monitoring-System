"""Explore the cattle master dataset."""
import pandas as pd

df = pd.read_csv(r'data\processed\cattle_master\cattle_master_dataset.csv')

print("=== DATASET OVERVIEW ===")
print(f"Total cattle: {len(df)}")
print(f"Unique farms: {df['farm_id'].nunique()}")
print(f"Unique owners: {df['owner_id'].nunique()}")
print()

print("=== FARMS ===")
for fid in sorted(df['farm_id'].unique()):
    sub = df[df['farm_id'] == fid]
    owner = sub['owner_name'].iloc[0]
    farm_name = sub['farm_name'].iloc[0]
    print(f"  {fid}: {farm_name} ({owner}) - {len(sub)} cattle")
print()

print("=== BREEDS ===")
for b in sorted(df['breed'].unique()):
    print(f"  {b}: {(df['breed']==b).sum()}")
print()

print("=== HEALTH STATUS ===")
for h in sorted(df['health_status'].unique()):
    print(f"  {h}: {(df['health_status']==h).sum()}")
print()

print("=== SAMPLE ROWS ===")
cols = ['tag_id','name','breed','age_years','weight_kg','health_status','farm_id','image_path']
for _, row in df.head(5).iterrows():
    print(f"  {row['tag_id']}: {row['name']} | {row['breed']} | {row['age_years']}yr | {row['weight_kg']}kg | {row['health_status']} | {row['farm_id']}")
    print(f"    image: {row['image_path']}")
print()

print("=== IMAGE PATHS (unique patterns) ===")
for p in df['image_path'].unique()[:5]:
    print(f"  {p}")
