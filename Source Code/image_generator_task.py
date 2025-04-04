import pandas as pd
from diffusers import StableDiffusionPipeline
import torch
import os
import re
import pandas as pd

# Generate caption for each haunted place by combining the city, Apparition Type, Ghost Category, Event Type, Time of Day, moon phase, and crime columns
file_path = './haunted_places_v2.tsv' 
df = pd.read_csv(file_path, sep='\t')

def generate_caption(row):
    caption = ""
    
    if pd.notnull(row['city']) and pd.notnull(row['state']) and pd.notnull(row['country']):
        caption += f"A mysterious figure has been spotted at {row['location']} in {row['city']}, {row['state']}, {row['country']}. "
    
    if pd.notnull(row['Apparition Type']):
        caption += f"The apparition is described as a {row['Apparition Type'].lower()}. "
    
    if pd.notnull(row['Ghost Category']):
        caption += f"It is believed to be a {row['Ghost Category'].lower()} haunting. "
    
    if pd.notnull(row['Event Type']):
        caption += f"Witnesses report a {row['Event Type'].lower()}. "
    
    if pd.notnull(row['Time of Day']):
        caption += f"This occurred during the {row['Time of Day'].lower()}. "
    
    if pd.notnull(row['moon_phase']) and 'full moon' in row['moon_phase'].lower():
        caption += "The haunting is especially active during a full moon. "
    
    if pd.notnull(row['crime_solved']) and row['crime_solved'] == 'TRUE':
        if pd.notnull(row['weapon']):
            caption += f"The haunting is linked to a tragic event involving a {row['weapon'].lower()}."
    
    words = caption.split()
    if len(words) > 150:
        caption = ' '.join(words[:150]) + '...'

    return caption

df['caption'] = df.apply(generate_caption, axis=1)

# Start generating images from the captions using StableDiffusion
os.makedirs("images", exist_ok=True)

start_idx = 0
#end_idx = 7400
end_idx = 10992
df_partial = df.iloc[start_idx:end_idx + 1].copy()

if "image_path" not in df.columns:
    df["image_path"] = ""

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f" Using device: {device}")

torch_dtype = torch.float16 if device == "cuda" else torch.float32

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch_dtype
).to(device)

for idx in df_partial.index:
    row = df.loc[idx]
    prompt = row["caption"]

    city = str(row['city']).lower().replace(" ", "_") if pd.notnull(row['city']) else "unknown_city"
    state = str(row['state']).lower().replace(" ", "_") if pd.notnull(row['state']) else "unknown_state"
    
    city = re.sub(r'[^a-z0-9_]', '', city)
    state = re.sub(r'[^a-z0-9_]', '', state)

    image_path = f"images/{city}_{state}_{idx}.png"

    if os.path.exists(image_path):
        df.at[idx, "image_path"] = image_path
        continue

    print(f" Generating image for row {idx}...")

    try:
        image = pipe(prompt, num_inference_steps=15).images[0]
        image.save(image_path)
        df.at[idx, "image_path"] = image_path
    except Exception as e:
        print(f"Error at row {idx}: {e}")
        df.at[idx, "image_path"] = ""

df.to_csv("output_with_images.tsv", sep="\t", index=False)
print("Done! Saved updated file as output_with_images.tsv")
