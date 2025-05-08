import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

# Job setup
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# 1. Load raw step trainer data from landing zone
step_trainer_landing = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="json",
    connection_options={"paths": ["s3://stedi-project-userthompson/step_trainer_landing/"]}
)

# 2. Load curated customer data
customers_curated = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="json",
    connection_options={"paths": ["s3://stedi-project-userthompson/curated/customers/"]}
)

# Debug counts
print("Step Trainer Raw Count:", step_trainer_landing.count())
print("Curated Customers Count:", customers_curated.count())

# 3. Join on serialNumber
joined = Join.apply(
    frame1=step_trainer_landing,
    frame2=customers_curated,
    keys1=["serialNumber"],
    keys2=["serialNumber"]
)

print("Joined Trusted Step Trainer Count:", joined.count())

# 4. Write output to trusted/step_trainer/
glueContext.write_dynamic_frame.from_options(
    frame=joined,
    connection_type="s3",
    format="json",
    connection_options={"path": "s3://stedi-project-userthompson/trusted/step_trainer/"}
)

job.commit()

