# DSCI550_Assignment2

1. To clone on Mac: git clone https://github.com/vmeno0020/DSCI550_Assignment2/tree/main

2. Include file 'haunted_places.csv'

3. Remaining Tasks:

Rohan, Justin
4. Install SpaCY using PIP and the instructions here: https://spacy.io/usage 
8. Run SpaCY on all the Haunted places and extract the associated entities present in the description text
Add these columns and scores to each of your Haunted places in your new dataset

Pratham, Alysa, Vishal
5. Use a Generative AI image generator service such as any of the following: Stable Diffusion, Imagine from Meta, Midjourney, DALL- E 3 from OpenAI 
Leverage the text from your sighting columns, such as Description, etc.
Combine that text together into a caption
Input the caption into the Image Generation service to receive the generated image
Note that you can use the API calls to these services to script/automate your process
A column pointing on disk to your generated AI image for the report.

(can tackle together after step 5 is complete)
6. Install Tika Image Dockers and generate captions for your Haunted places images from step 5
To access the images, use a local file URL from your generated Haunted places images
Install Tika Dockers package for Image Captioning and Object Recognition
git clone https://github.com/USCDataScience/tika-dockers.git and  https://hub.docker.com/r/uscdatascience/im2txt-rest-tika 
Read and test out: https://cwiki.apache.org/confluence/display/TIKA/TikaAndVisionDL4J
Read and test out: https://github.com/apache/tika/pull/189
Iterate through all the Haunted places images and add the generated image caption and the detect object(s) column to your dataset

Catherine
7. Iterate through all the Haunted places and then run Tika GeoTopicParser and extract out Location name, including Lat/Lng based on your text fields for the sighting
Write a Python program to do this
Add the new column(s) to your dataset
