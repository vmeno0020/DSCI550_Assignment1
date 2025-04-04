# Code for running Tika GeoTopicParser on the haunted_places TSV file
# Note: This code uses the 'description', 'location', and 'state' columns from the TSV file for the parser
import pandas as pd
import subprocess
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tempfile import NamedTemporaryFile
from threading import Lock

# File paths
input_file = "./haunted_places_v2.tsv"
output_file = "haunted_places_v2_with_geotopic.tsv"

# Tika command configuration
tika_command = [
    "java", "-classpath",
    "./tika/tika-app-2.6.0.jar:./tika/tika-parser-nlp-package-2.6.0.jar:./location-ner-model:./geotopic-mime",
    "org.apache.tika.cli.TikaCLI", "-m"
]

# Step 1: Load the TSV file
df = pd.read_csv(input_file, sep='\t')

# Step 2: Prepare data containers
geotopic_names = [""] * len(df)
geotopic_longitudes = [None] * len(df)
geotopic_latitudes = [None] * len(df)

# Stats variables
total_rows = len(df)
rows_with_geotopic = 0

# Concurrency settings
MAX_THREADS = 8           # Number of concurrent threads
BATCH_SIZE = 100           # Larger batch size for efficiency

# Progress tracking
lock = Lock()
rows_processed = 0


def run_geoparser(text_block, index):
    """Runs GeoTopicParser on a single row's text block using a temporary file."""
    try:
        with NamedTemporaryFile(delete=True, suffix=".geot") as temp_file:
            # Write the content to the temporary file
            temp_file.write(text_block.encode('utf-8'))
            temp_file.flush()

            # Run the Tika command
            result = subprocess.run(
                tika_command + [temp_file.name],
                capture_output=True,
                text=True
            )

        output = result.stdout

        # Extract geolocation info
        geo_match = re.search(
            r'Geographic_LATITUDE:\s(.*?)\n.*?Geographic_LONGITUDE:\s(.*?)\n.*?Geographic_NAME:\s(.*?)\n',
            output, re.S
        )

        opt1_match = re.search(
            r'Optional_LATITUDE1:\s(.*?)\n.*?Optional_LONGITUDE1:\s(.*?)\n.*?Optional_NAME1:\s(.*?)\n',
            output, re.S
        )

        opt2_match = re.search(
            r'Optional_LATITUDE2:\s(.*?)\n.*?Optional_LONGITUDE2:\s(.*?)\n.*?Optional_NAME2:\s(.*?)\n',
            output, re.S
        )

        # Fallback logic with primary and optional names
        if geo_match:
            return (
                geo_match.group(3),
                float(geo_match.group(2)),
                float(geo_match.group(1))
            )
        elif opt1_match:
            return (
                opt1_match.group(3),
                float(opt1_match.group(2)),
                float(opt1_match.group(1))
            )
        elif opt2_match:
            return (
                opt2_match.group(3),
                float(opt2_match.group(2)),
                float(opt2_match.group(1))
            )
        else:
            return ("", None, None)

    except Exception as e:
        print(f"Error processing row {index}: {e}")
        return ("", None, None)


def process_batch(batch):
    """Processes a batch of rows using multiple threads."""
    global rows_processed, rows_with_geotopic

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {
            executor.submit(run_geoparser, row["text"], row["index"]): row["index"]
            for row in batch
        }

        for future in as_completed(futures):
            index = futures[future]
            name, lon, lat = future.result()

            # Store the results
            geotopic_names[index] = name
            geotopic_longitudes[index] = lon
            geotopic_latitudes[index] = lat

            # Update progress safely with a lock
            with lock:
                rows_processed += 1
                if name:
                    rows_with_geotopic += 1

                # Display progress every 50 rows
                if rows_processed % 50 == 0 or rows_processed == total_rows:
                    percentage = (rows_processed / total_rows) * 100
                    print(f"\rProcessed {rows_processed}/{total_rows} rows ({percentage:.2f}%)", end="")


# Start processing with progress tracking
print(f"Processing {total_rows} rows with {MAX_THREADS} threads and batch size of {BATCH_SIZE}...\n")

start_time = time.time()

# Batch processing loop
batch = []
for idx, row in df.iterrows():
    # Combine description, location, and state
    description = str(row.get('description', ''))
    location = str(row.get('location', ''))
    state = str(row.get('state', ''))

    combined_text = f"{description}. {location}. {state}"

    batch.append({"index": idx, "text": combined_text})

    # Process batch when full
    if len(batch) >= BATCH_SIZE:
        process_batch(batch)
        batch = []

# Process any remaining rows
if batch:
    process_batch(batch)

# Step 3: Add the new columns
df['geotopic_name'] = geotopic_names
df['geotopic_longitude'] = geotopic_longitudes
df['geotopic_latitude'] = geotopic_latitudes

# Step 4: Save the updated TSV
df.to_csv(output_file, sep='\t', index=False)

# Step 5: Statistics
rows_without_geotopic = total_rows - rows_with_geotopic
percentage_with_geotopic = (rows_with_geotopic / total_rows) * 100 if total_rows > 0 else 0

# Display processing time
end_time = time.time()
elapsed_time = end_time - start_time

# Display final statistics
print("\n\n--- GeoTopicParser Statistics ---")
print(f"Total rows processed: {total_rows}")
print(f"Rows with geotopic name: {rows_with_geotopic} ({percentage_with_geotopic:.2f}%)")
print(f"Rows without geotopic name: {rows_without_geotopic}")
print(f"Total geotopic names extracted: {len([name for name in geotopic_names if name])}")
print(f"Processing time: {elapsed_time:.2f} seconds")
print(f"File saved as {output_file}")
