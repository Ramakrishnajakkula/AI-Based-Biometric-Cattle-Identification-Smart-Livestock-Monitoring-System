"""Test identify cattle API."""
import requests
import struct
import zlib

# Login as Rajesh
login = requests.post('http://localhost:5000/api/auth/login', 
    json={'email': 'rajesh@farm.in', 'password': 'password123'})
token = login.json()['token']
print('Login OK:', login.json()['user']['name'])

# Create a minimal valid PNG test image
def create_png():
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', 100, 100, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data)
    ihdr = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
    # Row of pixels (100x100, RGB)
    raw = b''
    for y in range(100):
        raw += b'\x00'  # filter byte
        for x in range(100):
            raw += bytes([139, 69, 19])  # brown like a cow
    idat_data = zlib.compress(raw)
    idat_crc = zlib.crc32(b'IDAT' + idat_data)
    idat = struct.pack('>I', len(idat_data)) + b'IDAT' + idat_data + struct.pack('>I', idat_crc)
    iend_crc = zlib.crc32(b'IEND')
    iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
    return sig + ihdr + idat + iend

with open('test_cow.png', 'wb') as f:
    f.write(create_png())
print('Test image created: test_cow.png')

# Upload and identify
with open('test_cow.png', 'rb') as f:
    resp = requests.post('http://localhost:5000/api/identify/', 
        files={'image': ('cow_muzzle.png', f, 'image/png')},
        headers={'Authorization': f'Bearer {token}'})

result = resp.json()
print(f'\nHTTP Status: {resp.status_code}')
print(f'Matched: {result.get("matched")}')
print(f'Source: {result.get("source")}')
conf = result.get('confidence', 0)
print(f'Confidence: {conf * 100:.1f}%')

cattle = result.get('cattle')
if cattle:
    print(f'\n=== IDENTIFIED CATTLE ===')
    print(f'Name: {cattle["name"]}')
    print(f'Tag: {cattle["tag_id"]}')
    print(f'Breed: {cattle["breed"]}')
    print(f'Health: {cattle["health_status"]}')
    print(f'Farm: {cattle.get("farm_id")}')
    print(f'Age: {cattle.get("age_years")} years')
    print(f'Weight: {cattle.get("weight_kg")} kg')
    print(f'Milk: {cattle.get("milk_yield_liters")} L/day')
else:
    print('\nNo cattle matched')
    print(f'ML Status: {result.get("ml_status")}')
