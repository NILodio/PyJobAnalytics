PyJobAnalytics
==============================

## 🚨 Warning: This project is currently undergoing restructuring. 😎 

Please avoid using it at the moment and patiently await further updates.

Anticipated completion in the next couple of months. 😎 🚀


--------

# Job Scrapper

Command Line Based Tool for scrap job/vacancy data from JobStreet website.

Please refer to [Note](#note) if you're facing some issues or want to do other things within this repo

## Setup

1. First, yo need to create a virtual environment by running `make create_environment` on the root directory of this project please make sure you have `make` installed on your machine before running this command
2. Then, you need to install the dependecies by running `make requirements` on the same directory where `requirements.txt` located
3. Create `.env` file at the root directory of this project/repo or copy the `.env.example` and rename it to `.env`


## How to Use this Tool After Doing Setup?
all this project is create with Makefile. Thus, you can run the command by using `make` command. Here are the list of command that you can use:



1. `make scrapper` : This command will run the scrapping process. It will scrap the job data from JobStreet website and store the result to CSV

2. `make requirements` : This command will install all the dependencies that listed at `requirements.txt`

3. `make create_environment` : This command will create a virtual environment for this project

4. `make clean` : This command will remove the virtual environment and all the dependencies that installed on the virtual environment

> [!IMPORTANT]  
> Crucial please add the make cooomand when you create a new command. It will help you to understand the command that you want to run. For example, if you want to run the scrapping process you can run `make scrapper`


## Scrapping Flow

scrapping process is done by using beautifulsoup and and the keywork that we want to scrap is listed at `env` file.

```bash
BASE_URL= this is the base url of the website that we want to scrap
BASE_URL_JOBS= this is the base url of the job page
CHROMEDRIVER_PATH= this is the path of chromedriver that you have installed on your machine
PAGES= this is the number of pages that you want to scrap
OUTPUT_FILEPATH= this is the output file path of the scrapping result default is data/raw
KEYWORDS= this is the list of keywords that you want to scrap
```

All scrapping processes were did by `src/data/scrapper.py`. And to give you more clearance about how this program gets the data by scrapping. Here is the flow:
1. First, it will go to [jobstreet page](https://www.seek.com.au/jobs)
2. Then it will type the keyword on the search bar and clicked the Enter
3. It redirects you to search result page, e.g this URL https://www.seek.com.au
4. For each job card:
   1. It will get the datetime attribute of job posting time then do the calculation using `timeago` library to get the real Job Posting Time (xyz day/hour/minute ago)
   2. It will perform click action then it will scrap the job data that we needed (after the job details content showing at the right side )
5. Then, the program will visit the next page and do step 5 until the max page of pagination.
6. If all pages have been visited on a keyword, the rest of process just repeating the step 1-6 for the next search keyword.
7. The scrap result then will be formed as Pandas DataFrame
8. After that, we store the DataFrame to CSV and BigQuery to do further analysis

## Scrapping Output
This program will automatically produce a file
The **CSV** file will be stored at the same dir named `data/raw/jobs.csv`. If you insist on check the CSV file you may open these file


### **Note**
- If you got a `TimeoutException` or another `Exception` Error in the middle of scrapping process. Please just re-run `make scrapper`. <br>
I'am sorry for not handling that *rare* case in this version yet. <br> But the thing is, those issues weren't cause of incompatibility either Python version or Chromedriver version.
Thus don't be afraid. I've tested on local and it works perfectly!
- Or if you wish to only scrap some keywords for the sake of faster scrapping time. Just edit the `env` and comment some keywords that you want to exclude.


### **Disclaimer**
From my test on this program at local machine. It tooks **around 4 hour in total** to complete the scrap process using all keywords that listed at `env` .<br> Thus, if you want to get the result faster you might just delete/comment some keywords.



Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io



<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
