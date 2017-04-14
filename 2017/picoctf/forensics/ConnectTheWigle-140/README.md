### Connect The Wigle - 140 points

> Identify the data contained within wigle and determine how to visualize it.

Hint:
> - Perhaps they've been storing data in a database. How do we access the information?
> - How can we visualize this data? Maybe we just need to take a step back to get the big picture?


For this challenge we are given a file, more specifically, a SQlite database file:
```
$ file wigle
wigle: SQLite 3.x database
```
Opening up the file on [DB Browser](http://sqlitebrowser.org/), we find three tables, ```android_metadata```, ```location``` and ```network```. The first table is not relevant but the other two are interesting. They contain data on what it seems to be the location and information about wireless networks. The first thing that stands out in this data is that the two tables seem related to each other. Taking a better look at the entries, I found out that the column ```bssid``` serves as a correspondence between the tables. What I did was join them using a SQL query:
```SQL
SELECT * FROM location, network
WHERE location.bssid = network.bssid
```
Ok so now, we only have a table to work with. What to do with this data now? Checking the hints given, we have to visualize the data. The obvious thing to do is to see if the plot between the longitude and latitude gives us some kind of message, or the flag. With DB Browser I plotted this two values but, the result was very ugly and it didn't resemble anything. 

Hm, maybe the data has to be plotted on a map and not in a x and y plot. I searched a bit on the web and found a pretty cool [website](https://www.mapcustomizer.com/) that marked the map with each location. And even better, we can just copy and paste all the locations and the map is marked automatically!

Right after I inserted all the values on the website, the markers formed a message on the map, the flag! 

```
FLAG{F0UND_M3_5148BBEA}
```