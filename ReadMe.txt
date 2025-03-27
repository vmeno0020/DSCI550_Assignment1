Alysa Xu: combining external MIME types/report
Catherine Lu: features and parsing, combining NASA, TIKA, report
Justin Huh: parsing and features, external MIME types, Report
Rohan Rane: features and parsing, combining NASA, TIKA, report
Vishal Menon:features and parsing,combining MIME types, report



==README==

WBelow is a list of the following libraries utilized for our project. For 
each library we went ahead and provided the purpose of the library and why 
we used it in our project.

==List of Libraries==

tika: provided by professor allowed us to run our similarity

thefuzz: allows for fuzzy string matching which helped us specifically 
expand the threshold of our keywords when defining our features

csv: allows us to red and write tabular data in CSV format —> we used this 
to open and write with the haunted-place.csv

pandas: the library is typically utilized for the data analysis and data 
manipulation —> this was utilized in our date finder section. It helps us 
add the columns to the data frame


Wikipedia: this is utilized to help quickly parse data from wikipedia. We 
used this specifically to take descriptions and find the dates. Note the 
wikipedia data finder takes an hour and a half to run.

datefinder: the library is designed to extract dates from text. Similarly 
we used it to parse the descriptions for the date


time: the library is helpful with working with time data and helped 
supplement the completion of the date and time task

re: re or regular expressions is used to help with search patterns when 
extracting and matching information. We utilized this in the date time, 
witness count, alcohol abuse, and census data to help specifically search 
for the intended data

datetime: tis library helps us manipulate and create dates and times. We 
used this within the date and time task


tqdm: tqdm is an efficiency tool. We used it for our lengthier processes 
to help ensure that our code was continuing t run and progress. This was 
utilized for date time wikipedia and moon data.

concurrent: concurrent allows for parallel processing tasks. This was 
utilized for date time since the process took over an hour for us.


functools: the library is used for creating provides functions for working 
with other functions. We used lru_cache for get_daylight_data(year, 
latitude, longitude) to retrieve results from memory

requests: requests allows us to easily work with http and ultimately send 
and receive data easily we used. These for our external sets including the 
daylight and alcohol


bs4: beautifulsoup4 gives us easy parsing for html and xml and was 
utilized  for the external sets such as the daylight and alcohol sets.


number_parser: the number parser helps us change written numbers in 
numeric form so for example (one to 1). We used this when looking at 
witness count to help sum out the numbers


kagglehub: kagglehub allowed us to access kaggle datasets. We had to use 
this to utilize the crime dataset


os: the library is used for interacting with the operating system. We used 
this for the crime dataset to help with looking at theall the files and 
directories in our path 


json: the json library let us work with json data and was utilized once we 
converted our information 




