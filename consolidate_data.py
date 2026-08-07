import os
import json
import pandas as pd

RAW_FOLDER = "data/raw"
OUTPUT_FOLDER = "data/processed"
OUTPUT_FILE = "fps_combined.csv"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def clean_number(value):
    
    # Converting strings like '1,234' -> 1234 ,  Blank, '-', None -> 0
    

    if value is None:
        return 0

    value = str(value).strip()

    if value in ["", "-", "NA", "N/A", "None"]:
        return 0

    value = value.replace(",", "")

    try:
        if "." in value:
            return float(value)
        return int(value)
    except:
        return 0


def clean_column(text):
    
    #Convert names into snake_case
    

    return (
        text.lower()
            .replace(" ", "_")
            .replace("-", "_")
            .replace("/", "_")
            .replace("(", "")
            .replace(")", "")
    )


def flatten_table(row, table, prefix):
    
    # Convert nested tables into columns. Example: PHH -> phh_regular_txn ,  Rice -> rice_total_kg


    for category, values in table.items():

        base = clean_column(category)

        for key, value in values.items():

            column = f"{base}_{clean_column(key)}_{prefix}"

            row[column] = clean_number(value)


def process_file(filepath):
    # Extract month and district from json file 
    filename = os.path.basename(filepath).replace(".json", "")

    month = filename.split("_")[0].title()

    district = " ".join(filename.split("_")[1:]).replace("_", " ").title()
   #load all fps record from json file 
    with open(filepath, "r", encoding="utf-8") as f:
        shops = json.load(f)

    rows = []

    for shop in shops:

        row = {}

        row["month"] = month
        row["district"] = district

        row["shop_name"] = shop.get("shop_name", "")

        fps_id = ""

        if ":" in row["shop_name"]:
            fps_id = row["shop_name"].split(":")[0].strip()

        row["fps_id"] = fps_id

        summary = shop.get("summary", {})

        for key, value in summary.items():
            row[key] = clean_number(value)

        total = row.get("total_e_transaction", 0)

        aadhaar = row.get("aadhaar_authenticated", 0)

        if total > 0:
            row["aadhaar_authenticated_pct"] = round(
                aadhaar * 100 / total,
                2
            )
        else:
            row["aadhaar_authenticated_pct"] = 0

        flatten_table(
            row,
            shop.get("transaction_table", {}),
            "txn"
        )

        flatten_table(
            row,
            shop.get("ration_card_table", {}),
            "ration_card"
        )

        flatten_table(
            row,
            shop.get("quantity_table", {}),
            "kg"
        )


        rows.append(row)

    return rows


def main():

    all_rows = []
   # read every json file that has its rows stored.
    for file in os.listdir(RAW_FOLDER):

        if file.endswith(".json"):

            print(f"Reading {file}")

            path = os.path.join(RAW_FOLDER, file)

            all_rows.extend(
                process_file(path)
            )

    df = pd.DataFrame(all_rows)

    df = df.fillna(0)

    df = df.sort_values(
        by=["month", "district", "fps_id"]
    )

    output_path = os.path.join(
        OUTPUT_FOLDER,
        OUTPUT_FILE
    )

    df.to_csv(
        output_path,
        index=False
    )

    print("--------------------------------")
    print("Consolidation Complete")
    print(f"Rows : {len(df)}")
    print(f"Columns : {len(df.columns)}")
    print(f"Saved : {output_path}")
    print("--------------------------------")


if __name__ == "__main__":
    main()