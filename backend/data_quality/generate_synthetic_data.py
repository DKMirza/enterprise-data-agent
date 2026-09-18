import random
from faker import Faker
import csv
import os

def generate_dirty_crm_records(num_records=5000):
    fake = Faker()
    
    real_companies = [
        {"name": "Microsoft Corporation", "domain": "microsoft.com", "industry": "Technology"},
        {"name": "Acme Corp", "domain": "acmecorp.com", "industry": "Manufacturing"},
        {"name": "Global Logistics Inc.", "domain": "globallogistics.net", "industry": "Logistics"}
    ]

    records = []
    
    for i in range(num_records):
        if random.random() < 0.3:
            base_company = random.choice(real_companies)
            name_variations = [
                base_company["name"], 
                base_company["name"].replace("Corporation", "Corp"),
                base_company["name"].replace("Inc.", "Incorporated")
            ]
            
            record = {
                "id": i,
                "company_name": random.choice(name_variations),
                "domain": base_company["domain"],
                "industry": base_company["industry"] if random.random() > 0.1 else "",
                "email": f"contact@{base_company['domain']}",
                "phone": fake.phone_number(),
                "address": fake.address().replace("\n", ", "),
                "status": random.choice(["Active", "Inactive", "Pending"])
            }
        else:
            record = {
                "id": i,
                "company_name": fake.company(),
                "domain": fake.domain_name(),
                "industry": random.choice(["Technology", "Healthcare", "Finance", "", None]),
                "email": fake.email() if random.random() > 0.15 else "",
                "phone": fake.phone_number() if random.random() > 0.2 else "N/A",
                "address": fake.address().replace("\n", ", "),
                "status": random.choice(["Active", "Inactive"])
            }
        records.append(record)

    return records

def save_to_csv(records, filename="legacy_crm_data.csv"):
    os.makedirs("data/synthetic", exist_ok=True)
    filepath = f"data/synthetic/{filename}"
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = records[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(records)
        
    print(f"Generated {len(records)} records saved to {filepath}")

if __name__ == "__main__":
    data = generate_dirty_crm_records(5000)
    save_to_csv(data)
