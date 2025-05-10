import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.job import Job

# Get job name from arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize Glue job
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# 1. Load raw accelerometer data from the landing zone
accelerometer_landing = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-project-userthompson/accelerometer_landing/"]
    }
)

# 2. Load trusted customer data (already filtered for consent)
customer_trusted = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-project-userthompson/trusted/customer/"]
    }
)

# 3. Join on accelerometer.user = customer.email
joined_data = Join.apply(
    frame1=accelerometer_landing,
    frame2=customer_trusted,
    keys1=["user"],
    keys2=["email"]
)

# 4. Write the joined (cleaned) data to the trusted/accelerometer folder
glueContext.write_dynamic_frame.from_options(
    frame=joined_data,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://stedi-project-userthompson/trusted/accelerometer/"
    }
)

# 5. Commit the job
job.commit()
