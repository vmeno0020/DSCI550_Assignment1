import pandas as pd
from diffusers import StableDiffusionPipeline
import torch
import os
import re

df = pd.read_csv("output_with_captions.tsv", sep="\t")
os.makedirs("images", exist_ok=True)

start_idx = 0
#end_idx = 7400
end_idx = 10992
df_partial = df.iloc[start_idx:end_idx + 1].copy()

if "image_path" not in df.columns:
    df["image_path"] = ""

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🎯 Using device: {device}")

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

    print(f"🧠 Generating image for row {idx}...")

    try:
        image = pipe(prompt, num_inference_steps=15).images[0]
        image.save(image_path)
        df.at[idx, "image_path"] = image_path
    except Exception as e:
        print(f"❌ Error at row {idx}: {e}")
        df.at[idx, "image_path"] = ""

df.to_csv("output_with_images.tsv", sep="\t", index=False)
print("✅ Done! Saved updated file as output_with_images.tsv")
