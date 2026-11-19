"""
Seed script — populates the database with sample data so you can explore
the application immediately after setup.

Usage:
    python seed.py

WARNING: This script DROPS and RECREATES all collections.
         Do NOT run it in production against live data.
"""
import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import pymongo

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB  = os.environ.get("MONGO_DB",  "gesaivan_market")

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]


def utc(days_ago=0):
    return datetime.now(timezone.utc) - timedelta(days=days_ago)


def seed():
    print(f"Connecting to {MONGO_URI}/{MONGO_DB} …")

    # Drop existing data
    for col in ("buyers", "farmers", "markets", "price_listings", "records"):
        db[col].drop()
    print("Collections dropped.")

    # ── Buyers ──────────────────────────────────────────────────────────────
    buyers = db.buyers.insert_many([
        {"name": "John Mukasa",    "contact": "+256-700-111222", "location": "Kampala",   "created_at": utc(60)},
        {"name": "Grace Namukasa", "contact": "+256-772-333444", "location": "Entebbe",   "created_at": utc(55)},
        {"name": "Peter Ochieng",  "contact": "+256-752-555666", "location": "Jinja",     "created_at": utc(50)},
        {"name": "Fatuma Hassan",  "contact": "+256-704-777888", "location": "Mbale",     "created_at": utc(45)},
        {"name": "David Ssempa",   "contact": "+256-776-999000", "location": "Mbarara",   "created_at": utc(40)},
    ]).inserted_ids
    print(f"  {len(buyers)} buyers inserted.")

    # ── Farmers ─────────────────────────────────────────────────────────────
    farmers = db.farmers.insert_many([
        {"name": "Sarah Nakato",    "contact": "+256-700-100200", "location": "Wakiso",    "created_at": utc(80)},
        {"name": "Robert Opio",     "contact": "+256-772-300400", "location": "Lira",      "created_at": utc(75)},
        {"name": "Agnes Atim",      "contact": "+256-752-500600", "location": "Gulu",      "created_at": utc(70)},
        {"name": "Hassan Kiggundu", "contact": "+256-704-700800", "location": "Masaka",    "created_at": utc(65)},
        {"name": "Mary Ayot",       "contact": "+256-776-900100", "location": "Soroti",    "created_at": utc(60)},
    ]).inserted_ids
    print(f"  {len(farmers)} farmers inserted.")

    # ── Markets ─────────────────────────────────────────────────────────────
    markets = db.markets.insert_many([
        {"name": "Owino Market",     "location": "Kampala Central",  "description": "Uganda's largest open-air market. Trades all staple crops Mon–Sat.", "created_at": utc(90)},
        {"name": "St. Balikuddembe","location": "Kampala",          "description": "Wholesale hub for vegetables, grains, and livestock products.",        "created_at": utc(85)},
        {"name": "Jinja Main Market","location": "Jinja",           "description": "Eastern Uganda's primary agricultural trading centre.",                "created_at": utc(80)},
        {"name": "Gulu Market",      "location": "Gulu",            "description": "Major market serving northern Uganda farmers and buyers.",              "created_at": utc(75)},
        {"name": "Mbarara Market",   "location": "Mbarara",         "description": "South-west hub known for dairy, beef, and maize.",                     "created_at": utc(70)},
    ]).inserted_ids
    print(f"  {len(markets)} markets inserted.")

    # ── Price Listings ───────────────────────────────────────────────────────
    products = [
        ("Maize",    1800, "kg",       0, 0),
        ("Beans",    3500, "kg",       1, 1),
        ("Tomatoes", 2200, "crate",    2, 2),
        ("Cassava",   800, "kg",       3, 3),
        ("Sorghum",  1600, "kg",       4, 4),
        ("Millet",   2000, "kg",       0, 1),
        ("Groundnuts",4500,"kg",       1, 0),
        ("Sweet Potato",600,"bag",     2, 2),
        ("Coffee",   7000, "kg",       3, 3),
        ("Banana",   1200, "bunch",    4, 4),
    ]
    listings = []
    for i, (prod, price, unit, fi, mi) in enumerate(products):
        listings.append({
            "product": prod,
            "price": price,
            "unit": unit,
            "farmer_id": farmers[fi],
            "market_id": markets[mi],
            "listing_date": utc(i * 3),
            "created_at": utc(i * 3),
        })
    listing_ids = db.price_listings.insert_many(listings).inserted_ids
    print(f"  {len(listing_ids)} price listings inserted.")

    # ── Records ─────────────────────────────────────────────────────────────
    tx_types = ["Sale", "Purchase", "Transfer", "Return", "Sale", "Sale"]
    records = []
    for i in range(12):
        bi = i % len(buyers)
        fi = i % len(farmers)
        mi = i % len(markets)
        records.append({
            "transaction_type": tx_types[i % len(tx_types)],
            "buyer_id":  buyers[bi],
            "farmer_id": farmers[fi],
            "product":   products[i % len(products)][0],
            "quantity":  (i + 1) * 5,
            "price":     products[i % len(products)][1],
            "market_id": markets[mi],
            "date":      utc(i * 4),
            "notes":     f"Seed record #{i+1}",
            "created_at": utc(i * 4),
        })
    record_ids = db.records.insert_many(records).inserted_ids
    print(f"  {len(record_ids)} records inserted.")

    print("\n✅ Seed complete! Launch the app and open http://localhost:5000")


if __name__ == "__main__":
    seed()
