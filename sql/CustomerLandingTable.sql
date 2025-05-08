CREATE EXTERNAL TABLE IF NOT EXISTS landing_customer_landing (
  customerName STRING,
  email STRING,
  phone STRING,
  serialNumber STRING,
  shareWithResearchAsOfDate BIGINT,
  shareWithPublicAsOfDate BIGINT,
  shareWithFriendsAsOfDate BIGINT,
  registrationDate BIGINT,
  birthDay STRING,
  lastUpdateDate BIGINT
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
STORED AS TEXTFILE
LOCATION 's3://stedi-project-userthompson/customer_landing/';
