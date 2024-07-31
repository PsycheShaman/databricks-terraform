import json
import boto3
import random
from datetime import datetime

s3 = boto3.client('s3')
BUCKET_NAME = 'z-raw'
LISTING_ID_RANGE = 100

# Predefined lists for generating realistic data
street_names = [
    "High Street", "Station Road", "Main Street", "Park Road", "Church Street",
    "London Road", "Victoria Road", "Green Lane", "Manor Road", "Church Lane"
]
towns_or_cities = [
    "London", "Birmingham", "Liverpool", "Bristol", "Manchester",
    "Leeds", "Sheffield", "Edinburgh", "Cardiff", "Glasgow"
]
postal_codes = [
    "SW1A 1AA", "W1A 0AX", "M1 1AE", "B1 1AA", "LS1 1UR",
    "G1 1AA", "L1 8JQ", "BS1 5TR", "CF10 1BH", "EH1 1BB"
]
parking_options = ["residents_parking", "garage", "street_parking", "driveway"]
outside_space_options = ["private_garden", "shared_garden", "balcony", "terrace"]

# Generate random coordinates within Great Britain and Northern Ireland
def generate_random_coordinates():
    lat = random.uniform(49.9, 58.7)  # Approximate latitude range for GB and NI
    lon = random.uniform(-8.2, 1.8)   # Approximate longitude range for GB and NI
    return lat, lon

# Generate a new listing
def generate_listing(listing_id):
    lat, lon = generate_random_coordinates()
    listing = {
        "source": "property",
        "derived": {
            "parking": [random.choice(parking_options)],
            "outside_space": [random.choice(outside_space_options)]
        },
        "pricing": {
            "price": random.randint(50000, 1000000),
            "transaction_type": random.choice(["sale", "rent"])
        },
        "category": "residential",
        "location": {
            "coordinates": {
                "latitude": lat,
                "longitude": lon
            },
            "postal_code": random.choice(postal_codes),
            "street_name": random.choice(street_names),
            "country_code": "GB",
            "town_or_city": random.choice(towns_or_cities)
        },
        "bathrooms": random.randint(1, 5),
        "listing_id": listing_id,
        "creation_date": datetime.now().isoformat(),
        "total_bedrooms": random.randint(1, 6),
        "display_address": f"{random.choice(street_names)}, {random.choice(towns_or_cities)} {random.choice(postal_codes)}",
        "life_cycle_status": random.choice(["active", "sold", "removed"]),
        "summary_description": "This is a sample description for a property listing."
    }
    return listing

def lambda_handler(event, context):
    for _ in range(10):
        listing_id = str(random.randint(1, LISTING_ID_RANGE)).zfill(6)

        try:
            # Check if the listing already exists
            obj = s3.get_object(Bucket=BUCKET_NAME, Key=f"{listing_id}.json")
            listing = json.loads(obj['Body'].read().decode('utf-8'))
            action = random.choice(['update', 'delete'])

            if action == 'update':
                # Update a random attribute
                listing['pricing']['price'] = random.randint(50000, 1000000)
                listing['life_cycle_status'] = random.choice(["active", "sold", "removed"])
                print(f"Updated listing {listing_id}")
                s3.put_object(Bucket=BUCKET_NAME, Key=f"{listing_id}.json", Body=json.dumps(listing))
            else:
                # Delete the listing
                s3.delete_object(Bucket=BUCKET_NAME, Key=f"{listing_id}.json")
                print(f"Deleted listing {listing_id}")

        except s3.exceptions.NoSuchKey:
            # Create a new listing
            listing = generate_listing(listing_id)
            print(f"Created new listing {listing_id}")
            s3.put_object(Bucket=BUCKET_NAME, Key=f"{listing_id}.json", Body=json.dumps(listing))

    return {
        'statusCode': 200,
        'body': json.dumps('Listings processed')
    }
