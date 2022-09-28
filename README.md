# DATA MODELING WITH POSTGRESS 
This project involves creating a data model from a set of data that is stored in Json files  and writing a ETL process to load the data from JSON files into the postgress tables 
***

# DATA USED IN THE ETL PROCESS 
  The data was provided by Udacity in JSON files 

* /data/song_data/ consists of data about songs and artists ( there are 71 files )
* /data/log_data consists of data about listeners , users and other events data ( there are 30 files containing the events data )

***

# BUILDING THE DATA MODEL 
A Star schema has been formed consisting of number of tables  and the design was driven from the existing data fields in the JSON files. 
The schema lives in a sparkify company's analytics database called **sparkifydb**



* DIMENSTION TABLES 
   * songs(song_id, title, artist_id, year, duration)
   * users(user_id, first_name, last_name, gender, level)
   * artists(artist_id, name, location, lattitude, longitude) 
   * time(start_time, hour, day, week, month, year, weekday )

* FACT TABLE/S 
  * songplays( songplay_id, start_time, user_id, level,song_id, artist_id, session_id,location,user_agent )


* WHAT CREATES THE DATABASE TABLES IN POSTGRESS ? 
  Python script create_tables.py creates the required tables in the database . Just run the script as 
    phthon3 ./create_tables.py 

* WHAT  DOES AN ETL OF DATA INTO THE POSTGRESS TABLES  ? 
  Python script etl.py does all the necessary job of parsing the data and pulling the rquired data sets into the respective tables
  Run python3 ./etl.py 

  
#  CREDIT AND REFERENCE 
Udacity provided the start up project with Python files templates and the data to build the project .  This project is not an original creatition entirely and has been done to satisfy the course rquirements from Udacity Data Engineering Nanon Degreee program .
Internet reference 
- https://pandas.pydata.org/docs/reference/io.html#json
- https://www.programiz.com/python-programming/datetime/timestamp-datetime
- https://www.postgresql.org/docs/current/reference.html



# SOFTWARE / TOOLS REQUIREMENT 
  Having a python3 environment with any version of postgress database is enough to complete this project . I did use the Mac app postgres database in a local development before I ported the project into the Udacity work environment 
  - Install postgress 
  - Install Python3 environemnt 
  - import psycopg2 -- is required postgress library for python to connect to postgres database 

  **Having a Jupiter notebook is super helpful as well . I installed Anaconda IDE for getting jupiter notebook in my local environment**

