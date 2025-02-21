# GPSPA_project 
Git repository for GPSPA group project
Group members: Lourenço Trindade Tavares de Oliveira Alexandre, Mário, Samuel

Introduction
    Public transportation efficiency is a key factor in urban mobility, and real-time access to metro schedules significantly improves commuter experience. We have identified the problem that currnetly exists in the lisbon metro grid, as the only alternative to the information present in each stop is the website that only provides the frequency of trains during the hours of the day. In order to adress this issue and facilitate the metro user experience, this project aims to develop a system that allows users to select a metro stop in Lisbon and check the arrival times of the next three trains.
    The system is designed using an Extract, Transform, Load (ETL) pipeline, a database, and an API. The ETL process gathers real-time metro schedule data, processes it into a structured format, and stores it in the database. The database efficiently manages and retrieves schedule information, ensuring quick access to relevant data. The API serves as the interface, allowing users to request and receive train arrival times dynamically.
    By implementing this structured approach, the project enhances accessibility to public transport data, improving convenience for commuters. The report details the system’s design, implementation, and functionality, covering each component in the ETL, database, and API architecture.

Methodology
    ETL
        The ETL (Extract, Transform, Load) process is a critical component of our system, responsible for gathering, processing, and storing metro schedule data. This process ensures that the data is accurately collected, cleaned, and stored in a structured format, making it readily available for querying and analysis. The ETL pipeline consists of three main steps: Extract, Transform, and Load.

        The extraction process involves downloading the latest General Transit Feed Specification (GTFS) data from the Lisbon Metro website. This data is provided in a zip file format and contains various text files with information about routes, stops, schedules, and more. The importrequests.py script is responsible for handling the download and extraction of the GTFS data. It retrieves the zip file from the specified URL, saves it locally, and extracts its contents to the appropriate directory. This ensures that the most up-to-date data is always available for processing.

        Once the data is extracted, the transformation process begins. This step involves cleaning and processing the extracted data to ensure it is in a suitable format for loading into the database. The processing_data.py script plays a crucial role in this step. It processes the stop times data by removing unnecessary columns and modifying the trip IDs. The script reads the input data, removes specified columns, and writes the cleaned data to an output file. 

        Additionally, the timeconverte.py script is used to correct any incorrect times that exceed the 24-hour mark. This script reads the processed data, applies the necessary time corrections, and writes the corrected data to an output file. This step is crucial for maintaining the accuracy of the schedule data, as any errors in the time information could lead to incorrect conclusions and decisions.

        The final step in the ETL process is loading the transformed data into the database. The dbconnection.py script handles the database connection and data insertion. It connects to the PostgreSQL database, truncates existing tables to remove old data, and inserts the new data into the appropriate tables (stops, departure_times, and station_info). This ensures that the database always contains the most recent and accurate data, ready for querying and analysis.

        To orchestrate the entire ETL process, we have a main.py script that runs all the complementary scripts in sequence. The main.py script first calls the importrequests.py script to download and extract the GTFS data. It then calls the processing_data.py script to clean and process the data, followed by the timeconverte.py script to correct any time discrepancies. Finally, it calls the dbconnection.py script to load the transformed data into the database. This centralized approach ensures that the ETL process is executed in a structured and efficient manner, providing real-time access to up-to-date schedule information.

    
    Database
        The database is structured to store and manage metro stop information and departure schedules efficiently. It consists of three main tables: stops, departure_times, and station_info, each serving a distinct purpose.
        The stops table holds essential details about metro stops, including a unique identifier, name, and geographic coordinates. To facilitate spatial queries, a geometry column is included, which is automatically populated using a PostGIS function that converts latitude and longitude into a spatial data point.
        The departure_times table records train schedules for each stop, categorized by weekday type. It includes the stop ID as a foreign key reference to ensure data consistency and allows efficient retrieval of upcoming train times for a given station.
        The station_info table provides additional metadata for metro stops, such as route names, trip identifiers, and external links. By linking to the stops table, it enhances the usability of the data by associating each stop with relevant route information.
        This relational database design ensures structured data management, supports fast queries, and maintains referential integrity. The use of PostGIS further enables geospatial analysis, improving the efficiency of location-based queries within the system.

    API

Results

How to run 

Conclusion


/data is a folder which contains the most up to date General Transit Feed Specification (here forth referred to as GTFS) data. This is data that will be fed into our database live once the API is set up and configured. For now, I have made this data available so the group can explore and understand the structure of the data our program will be receiving. 

Project Architecture.png is the proposed structure of our project, both backend and frontend. Any changes and/or improvements are welcome.

Attempt 1.ipynb is where I have begun to play with the data to understand its structure and general makeup. 

Website URL where data was found: https://mobilitydatabase.org/feeds/tld-716

Producer download URL: https://www.metrolisboa.pt/google_transit/googleTransit.zip

tld-716 -> I have been trying to find the feed ID..... could this be it? If it is we can use it in the mobility database API to easily pull our specified data. I just do not know how to pull the most recent data or if it does that automatically?

Once we have successfully pushed, merged, and reconciled all changes to the GitHub repository I will have a better understanding of our data's structure post processing and the process used for the 'T' of 'ETL' 

Hopefully we will get a chance to talk (I also don't know if anyone is reading this maybe I am just talking to a wall here), but if we don't speak before the repo gets updated: think about naming your files differently from the ones in the repository if you haven't done so already. Depending on how much work has been done, we may end up with branches which can be a pain in the a**. 
