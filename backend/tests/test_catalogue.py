import json
from pathlib import Path
from collections import Counter


HOTELS_FILE = (
    Path(__file__).parent
    / "app"
    / "data"
    / "hotelbeds"
    / "hotels.json"
)


with HOTELS_FILE.open(
    "r",
    encoding="utf-8",
) as file:
    hotels = json.load(file)


print("Total hotels:", len(hotels))
print()


# -----------------------------------------
# Check how many have coordinates
# -----------------------------------------

with_coordinates = 0

for hotel in hotels:

    coordinates = hotel.get("coordinates") or {}

    if (
        coordinates.get("latitude") is not None
        and coordinates.get("longitude") is not None
    ):
        with_coordinates += 1


print("Hotels with coordinates:", with_coordinates)
print()


# -----------------------------------------
# Show first 10 hotels
# -----------------------------------------

print("FIRST 10 HOTELS")
print("=" * 60)

for hotel in hotels[:10]:

    print("Code:", hotel.get("code"))

    print(
        "Name:",
        (hotel.get("name") or {}).get("content")
    )

    print(
        "Destination:",
        hotel.get("destinationCode")
    )

    print(
        "Country:",
        hotel.get("countryCode")
    )

    print(
        "Coordinates:",
        hotel.get("coordinates")
    )

    print("-" * 60)


# -----------------------------------------
# Most common countries
# -----------------------------------------

countries = Counter(
    hotel.get("countryCode")
    for hotel in hotels
    if hotel.get("countryCode")
)

print()
print("TOP COUNTRIES")
print("=" * 60)

for country, count in countries.most_common(20):
    print(country, count)