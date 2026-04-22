# Custom Cattle Dataset Generation

This guide creates your own dataset with:

- Cattle images from online sources
- Custom ownership data
- Loan information
- Health profile fields
- GPS location history

The output is stored in `data/processed/cattle_master`.

## 1. Configure Online Dataset URLs

Edit `scripts/dataset_sources.example.json` and keep valid public ZIP/TAR links.

Current format:

```json
{
  "detection": {
    "url": "https://..."
  },
  "health": {
    "url": "https://..."
  }
}
```

## 2. Run Dataset Generator (Download + Build)

From repository root:

```bash
python scripts/create_cattle_master_dataset.py --download-online --num-cattle 500 --seed 42
```

## 3. Output Files

- `data/processed/cattle_master/cattle_master_dataset.json`
- `data/processed/cattle_master/cattle_master_dataset.csv`
- `data/processed/cattle_master/cattle_gps_history.csv`

## 4. Main Fields Generated

### Cattle and Owner

- `cattle_id`, `tag_id`, `name`, `breed`, `age_years`, `weight_kg`
- `owner_id`, `owner_name`, `owner_phone`, `owner_village`, `owner_district`
- `farm_id`, `farm_name`, `registered_at`, `image_path`

### Loan

- `has_loan`, `loan_id`, `loan_type`
- `loan_amount_inr`, `interest_rate_annual_pct`, `tenure_months`, `emi_inr`
- `outstanding_amount_inr`, `repayment_status`, `last_payment_date`

### Health

- `health_status`, `disease_label`
- `temperature_c`, `heart_rate_bpm`, `respiration_rate_per_min`
- `activity_level`, `body_condition_score`, `vaccination_status`
- `last_health_check_date`

### GPS

- `gps_last_lat`, `gps_last_lng` in main dataset
- Full hourly history in `cattle_gps_history.csv` with geofence flag

## 5. Generate Without Re-downloading

If you already downloaded images once:

```bash
python scripts/create_cattle_master_dataset.py --num-cattle 300 --seed 99
```

## Notes

- Loan, health, and GPS values are synthetic and suitable for demo/training workflows.
- Re-run with different `--seed` to create a different but reproducible dataset.
- Increase `--num-cattle` to scale the dataset size.
