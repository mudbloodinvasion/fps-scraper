import pandas as pd

# Load the consolidated dataset
df = pd.read_csv("data/processed/fps_combined.csv")

# Columns to remove
columns_to_drop = [
    # Wheat
    "wheat_intra_state_kg",
    "wheat_inter_state_kg",
    "wheat_regular_kg",
   
    # Coarse
    "coarse_regular_kg",
    "coarse_intra_state_kg",
    "coarse_inter_state_kg",
    "coarse_total_kg",
    "coarse_grains_regular_kg",
    "coarse_grains_intra_state_kg",
    "coarse_grains_inter_state_kg",
    "coarse_grains_total_kg",

    # Barley
    "barley_regular_kg",
    "barley_intra_state_kg",
    "barley_inter_state_kg",
    "barley_total_kg",

    # Jowar
    "jowar_regular_kg",
    "jowar_intra_state_kg",
    "jowar_inter_state_kg",
    "jowar_total_kg",
    
    #bajra 
    "bajra_regular_kg",
    "bajra_intra_state_kg",
    "bajra_inter_state_kg",
    "bajra_total_kg",
    
    # Ragi
    "ragi_regular_kg",
    "ragi_intra_state_kg",
    "ragi_inter_state_kg",
    "ragi_total_kg",

    # Kodo
    "kodo_regular_kg",
    "kodo_intra_state_kg",
    "kodo_inter_state_kg",
    "kodo_total_kg",

    # Maize
    "maize_regular_kg",
    "maize_intra_state_kg",
    "maize_inter_state_kg",
    "maize_total_kg",
    
]

# Drop only columns that actually exist
df.drop(columns=[c for c in columns_to_drop if c in df.columns],
        inplace=True)

# Save final dataset
df.to_csv(
    "data/processed/final_dataset.csv",
    index=False
)


print("Columns removed successfully!")
print(f"Remaining Rows    : {df.shape[0]}")
print(f"Remaining Columns : {df.shape[1]}")
print("Saved as data/processed/final_dataset.csv")
