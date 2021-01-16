AUTHORS: 
Wenlai Han, Katrina Li, Lily Li





DATA: 
Time, location, type, caused deaths, and intensity of earthquake, tsunami, and volcano eruption events that took place in countries worldwide after the year 1950.





COPYRIGHT: 
CREDIT: CHARTIST
https://gionkunz.github.io/chartist-js/
Copyright (c) 2013 Gion Kunz <gion.kunz@gmail.com>
MIT License (https://opensource.org/licenses/MIT)

Following are the URLs that we retrieved our data from. Our main chunk of data are from the National Centers for Environmental Information (https://www.ngdc.noaa.gov/ngdc.html), which provides authentic statistics for information about all kinds of natural disaster types. We’ve only selected the most popular three, but we definitely see future potentials of populating the disaster tables with more disaster types and making it a more comprehensive natural disaster event analysis interface.
https://www.ngdc.noaa.gov/hazel/view/hazards/tsunami/event-data?maxYear=2020&minYear=1950
https://www.ngdc.noaa.gov/hazel/view/hazards/volcano/event-data?maxYear=2020&minYear=1950
https://www.ngdc.noaa.gov/hazel/view/hazards/earthquake/event-data?maxYear=2020&minYear=1950
https://data.world/hdx/97e007af-4733-4b60-a472-a733f10dedd5/workspace/file?filename=total-affected-natural-disasters-csv-1.csv

Most part of our line-chart and histogram javascript implementation are adapted from simple-charts.js and chart-from-api.js provided by Prof Jeff Ondich in the cs257_2020_fall repository (https://github.com/ondich/cs257_2020_fall). We really appreciate the instruction and guidance provided by Prof Jeff Ondich during the design, implementation, and testing phases of this project.

Other design ideas are from group discussions that involved all three members in our group.





STATUS: 
There are 4 main features in our website,
(1) A search box (represented using the magnifying glass at the top right corner of the page) that allows the users to search for disaster events of all three types within a particular year within 1950 and 2020. The result of this search is sorted by disaster type and has the following columns: year, disaster type, country, deaths, intensity or magnitude.
(2) Index.html (homepage) and about.html (About Page) navigates users for contextualization and provides the educational meaning beyond representing the natural disaster events through visual comparison.
(3) In a line chart, we display cumulative case counts of events for a particular disaster type, each line represents a country. The user could specify up to three countries to compare their disaster event increments over the past 70 years.
(4) In three different histograms, we group and display cases of events of each disaster type based on intensity/magnitude that is relevant to the disaster. This could give insights into the severity of natural disaster events in a particular country over the past 70 years.

Aside from all of the utilities, we have:
(5) A nicely formatted and good-looking homepage (with high usability and clarity)
(6) A cutting-edge About Page, that has brief description of the natural disasters
(7) An awesome horizontal bar that provides access to the main functionalities, and also moves along with user scrolling up and down.
(8) A great visualization tool to help users getting insights from natural disaster events statistics


Future potentials:
(1) Implementation of a world map feature that shows all the disasters happened in a particular year (depends on the user) using icons that represent each disaster event at exact longitude and latitude. More information about the disaster could be accessed after clicking on those icons. Also, when a user hovers onto a country, the country would be highlighted and would reveal the detailed information of disasters along with other socio-economic consequences of all the disasters happened in that year.

(2) Fixing the format anomalies like the wrong format of country names in our dataset. For example, we had “Usa” as one of the country names while it should be represented as either USA or United States of America.

(3) Assign ‘World’ with a country_id would help us combine some endpoint functions but might also cause extra problems.

(4) Utilizing more options provided by Chartist to aesthetically improve our charts.

(5) We decided to incorporate the “world” option for the histogram after finalizing our table designs, since it’s really valuable to take the entire globe as a whole to see the frequency distribution of the natural disaster events. However, the country table that we had doesn’t include the world option, and this design in our original table design requires another api endpoint for us to pull the histogram data for the world option. Thus, for future improvement, we could incorporate the world as a row in our country table and use the same api endpoint that works perfectly with all the countries.

(6) We didn’t find a perfect solution to account for the extreme values that occurred in the frequency histogram (like the USA having one 528-meter wave during a tsunami). We resolved the case by only zooming in on the region where we have the most (>90%)occurrence of natural disaster events and discard the extreme values that might disrupt our overall histogram looks. There could be future potential to provide more context and comparison information about these extreme values to represent a comprehensive and accurate dataset.

(7) Addressing user input values from the form using a php file and allow for more search options. We currently limit the search input box to only numeric values, and we would like to expand that towards any search strings like country names, disaster types etc.

(8) There could be a better way of doing different fetches in a single JavaScript function, but we are currently using the embedded fetch statement to retrieve data from our API.






NOTES: 
When designing the about page and home page, we were aiming at a webpage in the real world, imagining that different kinds of people would wander around them. We kept the density of content in a medium level so that it is not only aesthetically pleasing to users (which helps a lot with User Experience) but also informs the user well. 

On the last day we decided to make the line chart page and histogram page prettier, we finished aesthetically improving the line chart page but did not have enough time for histogram page.

We had lots of fun with this project starting from our datasets selection, table design, to all the implementation phases. We’d like to say this “baby” has reached a point where it can represent our accomplishment within a 10-week virtual Zoom term, and we are really proud of it!
