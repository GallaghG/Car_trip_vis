#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  car_stats.py
#  


#imports for Bokeh
#most of these are used, but a few may be leftover from development
from bokeh.io import  show, output_file
from bokeh.layouts import gridplot, layout, widgetbox, column
from bokeh.models import (GMapPlot, GMapOptions, ColumnDataSource, Circle, 
                          DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, HoverTool, 
                         CustomJS, Text, CrosshairTool, DatetimeTickFormatter, Range1d, 
                         Panel, Tabs, Line, Ray)
from bokeh.plotting import figure

#data import and cleaning with pandas
import pandas as pd

filename=r'Data Log Jul 08 2017 01_29 PM.csv'

#picked the columns that seemed the most interesting. 
#There is a ton of data in the full CSV file
import_cols = ['Frame Time (h:m:s.ms)', 'AUX.ACCEL.FORWARD Gs', 'AUX.GPS.LATITUDE', 'AUX.GPS.LONGITUDE', 
        'SAE.MAP inHg', 'SAE.RPM rpm', 'SAE.VSS mph', 'CALC.FUEL_FLOW gal (US)/h | gal (UK)/h', 
        'CALC.ENGINE_POWER hp']
#names for the final data frame and make a dictionary to change column names later
col_names = ['Time', 'Acceleration', 'Lat', 'Lon', 'Man_pressure', 'RPM', 'Speed', 'Fuel_Flow', 'Power']
rename_col = dict(zip(import_cols,col_names))

#read the desired columns into the dataframe
trip_df = pd.read_csv(filename, usecols=import_cols)
#drop the first row and then rename the columns with the dict made above
trip_df = trip_df.drop(0)
trip_df.rename(columns=rename_col, inplace=True)

#update the data types for numeric and datetime associated  data
numeric_col = ['Acceleration', 'Lat', 'Lon', 'Man_pressure', 'RPM', 'Speed', 'Fuel_Flow', 'Power']
trip_df[numeric_col] = trip_df[numeric_col].apply(pd.to_numeric, errors='coerce', axis=1)
trip_df['Time'] = pd.to_datetime(trip_df['Time'], format='%H:%M:%S.%f')
#remove some of the empty data at the top of the dataframe
trip_df = trip_df[7:]


#json for styling the gmap object in bokeh
# styles available from https://snazzymaps.com
#https://snazzymaps.com/style/79/black-and-white
map_options = GMapOptions(lat=trip_df['Lat'].mean(), lng=trip_df['Lon'].mean(), map_type='roadmap', zoom=16,
                         styles='''[
    {
        "featureType": "road",
        "elementType": "labels",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "poi",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "administrative",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "weight": 1
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "geometry.stroke",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "weight": 0.8
            }
        ]
    },
    {
        "featureType": "landscape",
        "stylers": [
            {
                "color": "#ffffff"
            }
        ]
    },
    {
        "featureType": "water",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "transit",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "elementType": "labels",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "elementType": "labels.text",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    },
    {
        "elementType": "labels.text.stroke",
        "stylers": [
            {
                "color": "#ffffff"
            }
        ]
    },
    {
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#000000"
            }
        ]
    },
    {
        "elementType": "labels.icon",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    }
]'''
                         )


#The linking of the hover functionality on the line plot and map is 
#based on this stackoverflow solution. I needed a lot of trial and error to get to a 
#final product that I was happy with, so there might still be some clunky pieces that 
#are redundant or completely unused in the custom javascript callback. 
#https://stackoverflow.com/questions/35983029/bokeh-synchronizing-hover-tooltips-in-linked-plots



#set up the source data from the trip_df imported above
source=ColumnDataSource(data = trip_df)
source.add(trip_df['Time'].apply(lambda d: d.strftime('%M:%S')), 'event_date_formatted') #needed to help with the formatting of the datetime tooltip

#set up the Javascript callback
code = "source.set('selected', cb_data['index']);"
callback = CustomJS(args={'source': source}, code=code)

# Set up the google map object in bokeh along with the callback for hovering functionality
gmap = GMapPlot(x_range=Range1d(), y_range=Range1d(),  # changed to Range1d from DataRange1d based on the JS update issue as discussed here https://github.com/bokeh/bokeh/issues/5826
            map_options=map_options,plot_width=600,  plot_height=200)
gmap.title.text = "Trip map"
#Set it up with IllBeHome webapp
gmap.api_key = "nnnnnnnnnnnnnnn"   #Get your own API key!
circle = Circle(x="Lon", y="Lat", size=5, fill_color="steelblue", fill_alpha=0.4, line_color=None)
gmap.add_glyph(source, circle)
gmap.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
#selection circles gmap (map plot)
select_gmap = Circle(x='Lon', y='Lat', fill_color='gray', fill_alpha=0.0, line_color=None, size=10)
#display circles callback on gmap
invis_circle = Circle(x='Lon', y='Lat', fill_color='gray', fill_alpha=0.0, line_color=None, size=20)
vis_circle = Circle(x='Lon', y='Lat', fill_color='red', fill_alpha=0.5, line_color=None, size=20)
cr2 = gmap.add_glyph(source, select_gmap, selection_glyph=select_gmap, nonselection_glyph=invis_circle)
cr2t = gmap.add_glyph(source, invis_circle, selection_glyph=vis_circle, nonselection_glyph=invis_circle)
gmap.add_tools(HoverTool(tooltips=None, callback=callback, renderers=[cr2, cr2t]))

#set up the list of columns to plot for the performance statistics
#also have a list of colors to use in the for loop to make all the plots
#these will be fed into the Tabs widget to make a tabbed interactive plot object
statTOOLS = 'pan,wheel_zoom,box_select'
plot_stats = ['Acceleration', 'Man_pressure', 'RPM', 'Speed', 'Fuel_Flow', 'Power']
plot_colors = ['red', 'green', 'blue', 'purple', 'orange', 'cyan']
tab_plots = []

for i in range(len(plot_stats)):
    # create a new plot and add a renderer
    stat = figure(plot_width = 600, plot_height= 300, tools=statTOOLS) #, x_axis_type='datetime', title="Subaru Performance"
    stat.add_tools(CrosshairTool(dimensions='height'))
    stat.grid.grid_line_alpha=0.4
    stat.xaxis.formatter=DatetimeTickFormatter(minsec ='%M:%S')
    stat.xaxis.axis_label = 'Time (Minute)'
    stat.yaxis.axis_label = plot_stats[i]
    stat.line('Time', plot_stats[i], name=plot_stats[i], color=plot_colors[i], source=source, 
              nonselection_alpha=0.2, nonselection_color=plot_colors[i])
    
    #add callback 
    select_stat = Circle(x='Time', y=plot_stats[i], fill_color=plot_colors[i], 
		fill_alpha=0.0, line_color=None, size=0.3) # size determines how big the hover area will be
    cr = stat.add_glyph(source, select_stat) #, selection_glyph=line)
    stat_tooltips=[
        ( 'Time',   '@event_date_formatted'),
        ( plot_stats[i],  '@'+plot_stats[i])]
    stat.add_tools(HoverTool(tooltips=stat_tooltips, callback=callback, renderers=[cr], mode='vline')) #
    tab = Panel(child=stat, title=plot_stats[i])
    tab_plots.append(tab)
    
tabs = Tabs(tabs=tab_plots)

#set up the layout of the map and the performance stats
#I had to use sizing_mode='scale_width' here so that the tabs would display correctly
layout = gridplot(children=[[tabs], [gmap]], merge_tools=True, toolbar_location='left', sizing_mode='scale_width') #, sizing_mode='scale_width', plot_height=300
#layout = gridplot(children=[[tabs]], merge_tools=True, toolbar_location='left', sizing_mode='scale_width')

output_file('car_trip_vis.html')
show(layout)
