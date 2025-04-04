# DSCI550_Assignment2

==README==

==Division of Work==
Alysa Xu: captions, image generation, and geoparser
Catherine Lu: captions, image generation, and geoparser
Justin Huh: spacy and image generation
Rohan Rane: spacy and image generation
Vishal Menon: captions, image generation, and geoparser
Pratham Kambli: captions, image generation, and geoparser



==List of Libraries==
Below is a list of the following libraries utilized for our project. For each library we went ahead and provided the purpose of the library and why we used it in our project.

==GeoTopicParser==
The GeoTopicParser code includes a shell script and a Python file. The shell script activates the Tika lucene-geo-gazetter server, and then runs the Python file. The approach used in the Python file involves taking the ‘description’, ‘location’, and ‘state’ columns of the haunted_places TSV file and writing them into a temporary .geot file. This file is then parsed with GeoTopicParser to return a geographic name, longitude, and latitude. If the parser does not return data for those categories, the code falls back to the optional name, longitude, and latitude. These columns are saved and added to the original haunted_places TSV file.

pandas: the library is typically utilized for data analysis and data manipulation. It helps us add the columns to the data frame

subprocess: run command-line to call Tika server to use GeoParser

re: extract info from Geographic_NAME, Geographic_LONGITUDE, and Geographic_LATITUDE part of GeoParser output

time: keep track of how long it took function to run

concurrent.futures.ThreadPoolExecutor: run tasks in parallel, in this case, calling the Tika server in parallel

concurrent.futures.as_completed: retrieve results from Tika server as they become available

tempfile.NamedTemporaryFile: create temporary .geot file from haunted_places dataset

tempfile.Lock: lock the temporary file after processing 50 rows to update progress safely

==Image Generation==
First, the dataset was loaded with columns like caption, city, state, etc. We then set up a local image storage by creating an images/ folder. The next step involved initializing the stable diffusion model. Stable Diffusion v1.5 was loaded from Hugging Face, and we used float32. Looping was done through each caption in order to process only the selected range of rows and used the city, state, and index to generate a descriptive filename. Then we generated the Image from the Prompt. This was done by feeding the caption as the text prompt. We used 15-20 inference steps for fast and decent quality. Then the image was generated locally. The file path in the dataset was recorded by tracking the output path in the image_path column for later reference or analysis. Lastly, we saved the updated .tsv file with image_path included.

Diffusers: The main library to load and run Stable Diffusion pipelines (from Hugging Face).

Transformers: provides tokenizer/model support for text encoders used in diffusion pipelines.

Accelerate: Optimizes performance and device placement (GPU/MPS/CPU); handles inference efficiently.

Torch: Deep learning framework for running Stable Diffusion models. Handles tensors and inference.

Pandas: Loads and manipulates .tsv file with captions and metadata.

Safetensors: Loads model weights securely and efficiently (faster + safer than .pt files).

Pillow: Saves the generated image from memory as a PNG or JPG file.


==spaCY==
The spaCY process was extremely simple. We ultimately used the provided categories of persons, orgs, locations, and entities. Parsing through the document, the program defined and extracted the entities in each of the descriptions based on the categories and added these entities as columns to the existing dataframe. From there we ran a couple analysis lines to understand how many rows were filled and what entities were most common. 

Wheel: Spacy utilizes wheels for distribution and allows for convenience of library installation

Spacy: MLP utilized to help categorize and extract the entities

En_core_web_sm: This is the pipeline that has the vocabulary, syntax, and entities

Pandas: loads and manipulates .tsv file v2 of the hw 1.

Tqdm: utilize tqdm to give us a better sense of how the code is running

collections/ counter: allows us to count hashable files we used this to understand how many entities

Ast: used to convert string representations of Python lists and tuples back into actual Python objects.Helped us with our analysis of the data.


==Tika Image Captioning==
Tika image captioning uses the docker-based image recognition REST API to generate captions for each image in the haunted places dataset. The Tika Docker Container was first set up and the zip files of images stored locally were sent to the running server after being unzipped and converted to .JPGs, which auto-generated captions in batches. The captions were stored in a .tsv file that paired each image name with the caption generated. 

Docker: This ran the Tika image captioning (im2txt-rest-tika) locally, and exposed the API to port 8764.

Curl: This was used in terminal to POST images to the Tika Docker to get captions

Pandas: This was used to manipulate and append the dataset with captions

Tika Docker API: This provided endpoints for image captioning 

TensorFlow: This performs the captioning for images

Pillow: Python library that is used to convert all .PNG images to .JPG for compatibility with the captioning model

Bash Scripting: This iterated through all images and generated captions in bulk

TSV Output: This created a loop to pair the image names with captions to store and later integrate into the larger dataset  
