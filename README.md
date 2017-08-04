# Car_trip_vis
Project to plot OBD2 car scanner data in interactive visualization of data and location

## Components  
- OBDII Scan Tool: Scanner Adapter Check Engine Light Diagnostic Tool  
  -  https://www.amazon.com/dp/B00W0SDLRY/ref=cm_sw_r_em_apap_PuQRl2rorTau8
- DashCommand android app
  - https://play.google.com/store/apps/details?id=com.palmerperformance.DashCommand&hl=en
- Subaru Legacy 2008  

## Python dependencies  
- Python 3.x
- Pandas 0.20.3
- Bokeh 0.12.6

## Python code overview
1. Import and clean data with Pandas
  a. Log the trip using the OBDII scanner and the DashCommand app
  b. Retreive the csv file from the OBDII scanner and import into a pandas dataframe
    - Changed lables for Lat and Lon data to remove non-UTF8 characters
  c. Only imported some of the columns that seemed interesting. There is lots more data in the original csv file
  d. Clean data by updating data column types and removing some of the nan values at the top of the dataframe  
2. Interactive visualization with Bokeh
  a. Set up columnDatasource based on the pandas dataframe
  b. Create a tabbed graph for the interesting car performance statistics (speed, acceleration, etc)  
    - Iterate through the interesting car statistics columns to make a list of figure objects  
    - add callback functionality to these figure objects so that they can be linked to the map later  
    - Feed this list into the Tabs widget to allow for selection of each of the performance stats
  c. Create a map of the trip  
    - Initialize the GMap using my API key
    - Apply styling to the map  
      - Based on style found here: https://snazzymaps.com/
    - Add the GPS point locations from the trip using individual Lat/Lon pairs from the data
    - Add a callback to link to the performance statistics graphs made above  
  d. Display  


## Note:  
There were many small issues I encountered while developing this visualization. Probably because its my first solo project with Bokeh.  
I tried to include StackOverflow or other sites that provided specific guidance with issues I was having. 
  
  
