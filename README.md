# STEDI Human Balance Analytics Project
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

