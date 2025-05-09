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

# 1. Load trusted step trainer data
step_trainer_trusted = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="json",
    connection_options={"paths": ["s3://stedi-project-userthompson/trusted/step_trainer/"]}
)

# 2. Load trusted accelerometer data
accelerometer_trusted = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="json",
    connection_options={"paths": ["s3://stedi-project-userthompson/trusted/accelerometer/"]}
)

# Debug counts
print("Step Trainer Trusted Count:", step_trainer_trusted.count())
print("Accelerometer Trusted Count:", accelerometer_trusted.count())

# 3. Join on timestamp = sensorReadingTime
joined = Join.apply(
    frame1=accelerometer_trusted,
    frame2=step_trainer_trusted,
    keys1=["timestamp"],
    keys2=["sensorReadingTime"]
)

print("Joined Machine Learning Records Count:", joined.count())

# 4. Write to machine_learning_curated/
glueContext.write_dynamic_frame.from_options(
    frame=joined,
    connection_type="s3",
    format="json",
    connection_options={"path": "s3://stedi-project-userthompson/machine_learning_curated/"}
)

# Complete the job
job.commit()
