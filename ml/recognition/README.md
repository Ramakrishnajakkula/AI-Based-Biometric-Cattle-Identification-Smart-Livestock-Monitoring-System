# Cattle Recognition Module (Baseline Complete)

This module now includes a runnable embedding-based recognition pipeline.

## What is implemented

- `train_embedding.py`: trains a ResNet18-based embedding model and saves checkpoint to `ml/recognition/weights/arcface_cattle.pth`
- `inference.py`: loads checkpoint and generates normalized embedding vectors from muzzle crops
- `gallery_builder.py`: gallery backend with MongoDB support and local JSON fallback (`ml/recognition/weights/gallery.json`)
- `face_matcher.py`: full identify pipeline (detect -> crop -> embed -> gallery match)

## Dataset format for embedding training

`ImageFolder` structure is expected:

```text
ml/recognition/datasets/
  CTL-001/
    img1.jpg
    img2.jpg
  CTL-002/
    img1.jpg
    img2.jpg
```

Each folder name is a cattle identity label.

## Train embedding model

From repository root:

```bash
python ml/recognition/train_embedding.py
```

Optional custom call:

```bash
python -c "from ml.recognition.train_embedding import train_embedding_model; train_embedding_model(data_dir='ml/recognition/datasets', epochs=10, batch_size=16)"
```

## Build/update gallery

```python
from ml.recognition.gallery_builder import add_to_gallery
import numpy as np

add_to_gallery('CTL-001', np.random.rand(512).astype('float32'))
```

If MongoDB is unavailable, entries are written to `ml/recognition/weights/gallery.json`.

## Identify from image

```python
from ml.recognition.face_matcher import identify_cattle

result = identify_cattle('path/to/cattle_image.jpg')
print(result)
```

Result includes `cattle_id`, `confidence`, `bbox`, `status`, and `detected`.

## Notes

- Detection model weights are expected at `ml/detection/weights/best.pt`.
- Embedding model weights are expected at `ml/recognition/weights/arcface_cattle.pth`.
- If weights/gallery are missing, backend route falls back to demo response.

## Auto-suggest ID Mapping (Gallery -> App Tags)

1. Add enrollment images by app tag:

```text
backend/uploads/cattle_images/
  CTL-001/
    img1.jpg
  CTL-002/
    img1.jpg
```

2. Generate suggestions:

```bash
python scripts/suggest_id_mapping.py --show-top 10
```

3. Apply high-confidence suggestions:

```bash
python scripts/suggest_id_mapping.py --threshold 0.75 --apply
```

Suggestions are saved to `ml/recognition/weights/id_mapping_suggestions.json`.
