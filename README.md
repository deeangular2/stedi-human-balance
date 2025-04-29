<<<<<<< HEAD

# STEDI Human Balance Analysis – AWS Glue Data Lake Project

## 📊 Overview

This project uses AWS Glue and other AWS services to build a serverless data lake pipeline for analyzing human balance sensor data from STEDI. The goal is to clean, transform, and prepare the data for future machine learning applications.

---

## 🔍 Objectives

- Clean and normalize raw data from sensors (Accelerometer, Customer, Step Trainer).
- Upload cleaned data to AWS S3 and catalog with AWS Glue Crawlers.
- Use AWS Glue Jobs (PySpark) to transform and join data for analysis.
- Reduce dataset intelligently to keep only relevant records.
- Document the issues faced and provide solutions.

---

## 🗂️ Project Structure

```bash
=======
# STEDI Human Balance Analytics Project
>>>>>>> d0233e8d16d6fe95674e8253166916385ae08ab6
.
├── data/
│   ├── raw/                  # Raw downloaded data
│   ├── cleaned/              # Cleaned and formatted datasets
├── glue-scripts/            # AWS Glue PySpark ETL scripts
│   ├── transform_customer.py
│   ├── transform_step_trainer.py
│   └── join_tables.py
├── notebooks/               # Optional Jupyter notebooks for analysis or prototyping
│   └── exploratory_analysis.ipynb
├── sql/                     # SQL queries used for Athena or debugging
│   ├── validate_schema.sql
│   └── summary_queries.sql
├── src/                     # Custom Python modules or helper scripts
│   ├── utils.py
│   └── s3_loader.py
├── README.md                # Project overview and usage instructions
└── notes.md                 # Issues encountered and how they were resolved
<<<<<<< HEAD
```

---

## ⚙️ Tools & Services

- **AWS Glue** (Crawlers, Jobs, Catalog)
- **AWS S3** (Data Lake storage)
- **AWS Athena** (SQL Querying)
- **PySpark** (Data processing)
- **Jupyter Notebook** (optional for EDA)

---

## 🚀 How to Run

1. **Download and clean data**  
   - Fix formatting issues in CSVs.
   - Save cleaned files under `data/cleaned`.

2. **Upload to S3**  
   - Upload to the appropriate S3 bucket: `s3://your-bucket-name/cleaned/`

3. **Run AWS Glue Crawlers**  
   - One for each cleaned dataset to populate AWS Glue Data Catalog.

4. **Run Glue Jobs (ETL)**  
   - Use scripts from the `glue-scripts` directory.

5. **Query with Athena**  
   - Check the transformed data using SQL.

---

## 🧩 Issues & Fixes

Documented in [`notes.md`](notes.md) — includes:
- Schema mismatches
- Incomplete files
- Crawler and Glue job failures
- Performance tips

---

## 📁 Related Resources

- [STEDI Step Trainer GitHub Repo](#)
- [AWS Glue Documentation](https://docs.aws.amazon.com/glue/index.html)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)

---

## 🧠 Author Notes

> This project builds on previous work but re-implements data transformation using cleaner, more efficient methods. The final goal is to provide an optimized and queryable dataset for balance prediction models.

---

## ✅ Status

✔️ Project In Progress  
🛠️ Actively documenting and optimizing transformations  
📈 Preparing final output for ML model training
=======

>>>>>>> d0233e8d16d6fe95674e8253166916385ae08ab6
