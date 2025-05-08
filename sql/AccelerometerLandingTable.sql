CREATE EXTERNAL TABLE IF NOT EXISTS accelerometer_accelerometer_landing (
  user STRING,
  timestamp BIGINT,
  x FLOAT,
  y FLOAT,
  z FLOAT
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
STORED AS TEXTFILE
LOCATION 's3://stedi-project-userthompson/accelerometer_landing/';