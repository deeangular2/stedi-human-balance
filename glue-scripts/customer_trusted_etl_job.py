import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load raw customer data
customer_landing = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="json",
    connection_options={"paths": ["s3://stedi-project-userthompson/customer_landing/"]}
)

# DEBUG: Count total records loaded from landing zone
print("Total customer records from landing zone:", customer_landing.count())

# Filter customers who consented to research
customer_trusted = Filter.apply(
    frame=customer_landing,
    f=lambda row: row["shareWithResearchAsOfDate"] is not None
)

# DEBUG: Count how many customers had consent
print("Customer records with shareWithResearchAsOfDate not null:", customer_trusted.count())

# Write filtered data to trusted zone
glueContext.write_dynamic_frame.from_options(
    frame=customer_trusted,
    connection_type="s3",
    format="json",
    connection_options={"path": "s3://stedi-project-userthompson/trusted/customer/"}
)

# End job
job.commit()
