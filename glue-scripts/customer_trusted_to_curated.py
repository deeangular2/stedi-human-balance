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

# 1. Load customer trusted data
customer_trusted = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="json",
    connection_options={"paths": ["s3://stedi-project-userthompson/trusted/customer/"]}
)

# 2. Load accelerometer trusted data
accelerometer_trusted = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="json",
    connection_options={"paths": ["s3://stedi-project-userthompson/trusted/accelerometer/"]}
)

# Debug record counts
print("Customer Trusted Count:", customer_trusted.count())
print("Accelerometer Trusted Count:", accelerometer_trusted.count())

# 3. Join on email = user
curated_customers = Join.apply(
    frame1=customer_trusted,
    frame2=accelerometer_trusted,
    keys1=["email"],
    keys2=["user"]
)

print("Joined Curated Customer Count:", curated_customers.count())

# 4. Drop duplicates using Spark DataFrame
customers_curated_df = curated_customers.toDF().dropDuplicates(["email"])
curated_customers = DynamicFrame.fromDF(customers_curated_df, glueContext, "customers_curated")

# ✅ 5. Write output to s3://stedi-project-userthompson/customers_curated/
glueContext.write_dynamic_frame.from_options(
    frame=curated_customers,
    connection_type="s3",
    format="json",
    connection_options={"path": "s3://stedi-project-userthompson/customers_curated/"}
)

# Complete the job
job.commit()
