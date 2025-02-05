# GPSPA_project 
Git repository for GPSPA group project
Group members: Lourenço, Mário, Samuel

The purpose of this project is to create a webmap where users can interact and see information abou the upcoming trains and schedules for each station of the Metropolitano de Lisboa netwrok.

/data is a folder which contains the most up to date General Transit Feed Specification (here forth referred to as GTFS) data. This is data that will be fed into our database live once the API is set up and configured. For now, I have made this data available so the group can explore and understand the structure of the data our program will be receiving. 

Project Architecture.png is the proposed structure of our project, both backend and frontend. Any changes and/or improvements are welcome.

Attempt 1.ipynb is where I have begun to play with the data to understand its structure and general makeup. 

Website URL where data was found: https://mobilitydatabase.org/feeds/tld-716

Producer download URL: https://www.metrolisboa.pt/google_transit/googleTransit.zip

tld-716 -> I have been trying to find the feed ID..... could this be it? If it is we can use it in the mobility database API to easily pull our specified data. I just do not know how to pull the most recent data or if it does that automatically?

Once we have successfully pushed, merged, and reconciled all changes to the GitHub repository I will have a better understanding of our data's structure post processing and the process used for the 'T' of 'ETL' 

Hopefully we will get a chance to talk (I also don't know if anyone is reading this maybe I am just talking to a wall here), but if we don't speak before the repo gets updated: think about naming your files differently from the ones in the repository if you haven't done so already. Depending on how much work has been done, we may end up with branches which can be a pain in the a**. 
