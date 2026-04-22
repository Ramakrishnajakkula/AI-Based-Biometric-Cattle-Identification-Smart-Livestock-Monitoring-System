# Verified Dataset Links (March 13, 2026)

This file contains working dataset URLs validated for this project.

## 1) Biometric / Muzzle / Face datasets

| Name | Purpose | License | Direct URL | Status |
|---|---|---|---|---|
| Beef Cattle Muzzle/Noseprint database | Muzzle biometric identification | CC-BY 4.0 | https://zenodo.org/api/records/6324361/files/BeefCattle_Muzzle_database.zip/content | Verified (HTTP 200) |
| Cows Frontal Face Dataset | Face/muzzle identification | CC-BY 4.0 | https://zenodo.org/api/records/10535934/files/INDIVIDUAL%20SUBJECTS%20Data.zip/content | Verified (HTTP 200) |
| Cattely Cattle Face Images | Face images starter set | GitHub repo terms | https://github.com/aideep1400/Cattely-Cattle-Face-Images-Dataset | Verified (repo reachable) |

## 2) Health / Monitoring-oriented datasets

| Name | Purpose | License | Direct URL | Status |
|---|---|---|---|---|
| CattleFace-RGBT benchmark | Thermal + RGB face landmarks | Research repo terms | https://github.com/UARK-AICV/CattleFace-RGBT-benchmark | Verified (HTTP 200) |
| CattleFace-RGBT main branch ZIP | Archive download for scripting | Research repo terms | https://github.com/UARK-AICV/CattleFace-RGBT-benchmark/archive/refs/heads/main.zip | Expected downloadable archive |

## Broken or unresolved links from previous list

- https://zenodo.org/records/10535934/files/cows_frontal_face_dataset.zip (404)
- https://github.com/uq-robotics/cattle-behavior-dataset (404)

## Quick download examples

PowerShell:

```powershell
curl.exe -L "https://zenodo.org/api/records/6324361/files/BeefCattle_Muzzle_database.zip/content" -o BeefCattle_Muzzle_database.zip
curl.exe -L "https://zenodo.org/api/records/10535934/files/INDIVIDUAL%20SUBJECTS%20Data.zip/content" -o INDIVIDUAL_SUBJECTS_Data.zip
```

## Important compatibility note

Most of these datasets are not YOLO detection labels out of the box. They are useful for biometric identification, but you must annotate/convert before using `ml/detection/train_detector.py` or `ml/health/train_health.py`.
