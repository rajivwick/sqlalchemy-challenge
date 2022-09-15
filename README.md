# sqlalchemy-challenge
I've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with mytrip planning, I need to do some climate analysis on the area. The following sections outline the steps I must take to accomplish this task.

We start with sqlite database file containing dated temperature and precipitation data both specific to unqiue stations identified by their station id, name, latitude, longitude and elevation.

                     =Tables=

                   -Measurement-
                   
        | station	date |	prcp   |	tobs |
        
                     -Stations-
                     
| station	 | name |	latitude |	longitude |	elevation |


Connecting to this file via the power of the greate sqlalchemy library untilizing the automap feature to map the tables within the database to formats referencables within that otherwise would have to be manually coded. 

We can now reference the tables using pandas and model using matplotlib to gain further insight into helping plan the perfect holiday. Raining days are best kept for home, on holiday the sunny weather allow for activites and offer more choice.

The following api extentions will output a json file containging the data specified:
        All Data on dates and the corrosponding precipitation readings 
        "/api/v1.0/precipitation"
        A json list of stations 
        "/api/v1.0/stations"
        
        "/api/v1.0/tobs"
        
        "/api/v1.0/(start)"
        
        "/api/v1.0/(start)/(end)"
        
