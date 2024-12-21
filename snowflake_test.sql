-- Creates a database
CREATE OR REPLACE DATABASE sf_tuts;

-- Displays the current database and schema
SELECT CURRENT_DATABASE(), CURRENT_SCHEMA();

-- Creates a table in the selected database
CREATE OR REPLACE TABLE emp_basic (
   first_name STRING,
   last_name STRING,
   email STRING,
   streetaddress STRING,
   city STRING,
   start_date DATE
);

-- Creates a warehouse (compute resources) for the database
CREATE OR REPLACE WAREHOUSE sf_tuts_wh WITH
   WAREHOUSE_SIZE='X-SMALL'
   AUTO_SUSPEND = 180
   AUTO_RESUME = TRUE
   INITIALLY_SUSPENDED=TRUE;

-- Displays the current warehouse
SELECT CURRENT_WAREHOUSE();

-- Uploads files from the specified path into the staging area
PUT file://C:\temp\employees0*.csv @sf_tuts.public.%emp_basic;

-- Lists the files in the staging area
LIST @sf_tuts.public.%emp_basic;

-- Copies the data from the staging area into the table
COPY INTO emp_basic
  FROM @%emp_basic
  FILE_FORMAT = (type = csv field_optionally_enclosed_by='"')
  PATTERN = '.*employees0[1-5].csv.gz'
  ON_ERROR = 'skip_file';

-- Selects all records from the table
SELECT * FROM emp_basic;

-- Inserts additional data into the table
INSERT INTO emp_basic VALUES
   ('Clementine','Adamou','cadamou@sf_tuts.com','10510 Sachs Road','Klenak','2017-9-22'),
   ('Marlowe','De Anesy','madamouc@sf_tuts.co.uk','36768 Northfield Plaza','Fangshan','2017-1-26');

-- More examples of select queries
SELECT email FROM emp_basic WHERE email LIKE '%.uk';
SELECT first_name, last_name, DATEADD('day', 90, start_date) FROM emp_basic WHERE start_date <= '2017-01-01';

-- Deletes the database and the warehouse
DROP DATABASE IF EXISTS sf_tuts;
DROP WAREHOUSE IF EXISTS sf_tuts_wh;