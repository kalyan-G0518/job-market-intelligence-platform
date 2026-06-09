import pandas as pd
import numpy as np

# -------------------
# SKILL LIST
# -------------------

SKILLS = [
    "Python",
    "SQL",
    "AWS",
    "Azure",
    "GCP",
    "Spark",
    "Kafka",
    "Airflow",
    "Snowflake",
    "Power BI",
    "Tableau",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "Databricks"
]

# -------------------
# SKILL EXTRACTION FUNCTION
# -------------------

def extract_skills(text):

    if pd.isna(text):
        return ""

    text = str(text).lower()

    found = []

    for skill in SKILLS:
        if skill.lower() in text:
            found.append(skill)

    return ",".join(found)

# -------------------
# LOAD FILES
# -------------------

engineer = pd.read_csv("data/raw/DataEngineer.csv")
science = pd.read_csv("data/raw/Data_science_jobs.csv")
postings = pd.read_csv("data/raw/postings.csv")

# -------------------
# DATA ENGINEER
# -------------------

engineer_clean = pd.DataFrame()

engineer_clean["job_title"] = engineer["Job Title"]
engineer_clean["company"] = engineer["Company Name"]
engineer_clean["location"] = engineer["Location"]
engineer_clean["salary"] = engineer["Salary Estimate"]
engineer_clean["industry"] = engineer["Industry"]
engineer_clean["skills"] = np.nan
engineer_clean["job_type"] = np.nan
engineer_clean["description"] = engineer["Job Description"]
engineer_clean["source_dataset"] = "data_engineer"

# -------------------
# DATA SCIENCE
# -------------------

science_clean = pd.DataFrame()

science_clean["job_title"] = science["Title"]
science_clean["company"] = science["Title2"]
science_clean["location"] = science["Location"]
science_clean["salary"] = science["Salary"]
science_clean["industry"] = science["Industry_Type_1"]

science_clean["skills"] = (
    science[
        [
            "Skill1",
            "Skill2",
            "Skill3",
            "Skill4",
            "Skill5",
            "Skll6",
            "Skill7",
            "Skill8"
        ]
    ]
    .fillna("")
    .astype(str)
    .agg(",".join, axis=1)
)

science_clean["job_type"] = science["Employment_Type"]
science_clean["description"] = np.nan
science_clean["source_dataset"] = "data_science"

# -------------------
# POSTINGS
# -------------------

postings_clean = pd.DataFrame()

postings_clean["job_title"] = postings["job_title"]
postings_clean["company"] = postings["company"]
postings_clean["location"] = postings["job_location"]
postings_clean["salary"] = np.nan
postings_clean["industry"] = np.nan
postings_clean["skills"] = postings["job_skills"]
postings_clean["job_type"] = postings["job_type"]
postings_clean["description"] = postings["job_summary"]
postings_clean["source_dataset"] = "linkedin_postings"

# -------------------
# MERGE DATASETS
# -------------------

jobs_master = pd.concat(
    [
        engineer_clean,
        science_clean,
        postings_clean
    ],
    ignore_index=True
)

# -------------------
# BUILD SEARCH TEXT
# -------------------

jobs_master["search_text"] = (
    jobs_master["skills"].fillna("").astype(str)
    + " "
    + jobs_master["description"].fillna("").astype(str)
)

# -------------------
# DETECT SKILLS
# -------------------

jobs_master["detected_skills"] = (
    jobs_master["search_text"]
    .apply(extract_skills)
)

# -------------------
# REMOVE TEMP COLUMN
# -------------------

jobs_master.drop(
    columns=["search_text"],
    inplace=True
)

# -------------------
# FINAL CHECK
# -------------------

print("\nFinal Shape:")
print(jobs_master.shape)

print("\nColumns:")
print(jobs_master.columns.tolist())

print("\nSample:")
print(
    jobs_master[
        ["job_title", "detected_skills"]
    ].head(10)
)

# -------------------
# SAVE AS PARQUET
# -------------------

jobs_master.to_parquet(
    "data/processed/jobs_master.parquet",
    index=False
)

print("\nSaved jobs_master.parquet")