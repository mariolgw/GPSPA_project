# GPSPA_project 
Git repository for GPSPA group project
Group members: Lourenço, Mário, Samuel

Introduction
    Public transportation efficiency is a key factor in urban mobility, and real-time access to metro schedules significantly improves commuter experience. We have identified the problem that currnetly exists in the lisbon metro grid, as the only alternative to the information present in each stop is the website that only provides the frequency of trains during the hours of the day. In order to adress this issue and facilitate the metro user experience, this project aims to develop a system that allows users to select a metro stop in Lisbon and check the arrival times of the next three trains.
    The system is designed using an Extract, Transform, Load (ETL) pipeline, a database, and an API. The ETL process gathers real-time metro schedule data, processes it into a structured format, and stores it in the database. The database efficiently manages and retrieves schedule information, ensuring quick access to relevant data. The API serves as the interface, allowing users to request and receive train arrival times dynamically.
    By implementing this structured approach, the project enhances accessibility to public transport data, improving convenience for commuters. The report details the system’s design, implementation, and functionality, covering each component in the ETL, database, and API architecture.

Methodology
    ETL
    
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
