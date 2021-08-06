# UCalgary-ENSF-592-Final-Project
Terminal Based Application for Extracting Meaningful Data from the Ontario Public Library Datasets.

ENSF 592 – Final Project – Group 5

Ontario Public Library: Data Analysis Interface Program

By: Michael Kissinger and Brandon Quan

Program Overview

•    This program is designed to allow a user to access meaningful information from the Ontario Public Library Statistics, from 2017 to 2019 [1],[2],[3]. 

•    The first input the user is prompted to enter is the name of an Ontario library, or they can request getting a full list of all libraries to choose from. The second input they are prompted to enter is a number to select what datasets they would like to see. If an invalid input is provided, an exception is used to prompt for re-entry without terminating the program. The options are as follows:

o    Option 1: Display aggregate stats for all libraries and exports stats to a spreadsheet.

o    Option 2: Display stats for the selected library and average stats for all library regions and average stats for the province.

o    Option 3: Display the number of e-titles for the selected library and average e-titles for each library region year-by-year in pivot table format.

o    Option 4: Display the number of e-titles for the selected library and average e-titles for each library region year-by-year in a plot format.

o    Option 5: Change selected library.

o    Option 6: Exit program and export full dataset.

•    Program imports the three datasets. Data is stored as multi-indexed DataFrames. Datasets are then sorted, unstacked, and unused/duplicated information is deleted. After this the three data sets are combined into a single DataFrame using two join operations. The DataFrame columns are then formatted. The full dataset contains 22 columns and 312 rows.

•    After this the DataFrame is filtered so that all rows that are filled entirely with zero’s and null values are removed using a Boolean masking operation.

•    Three new columns are now added to the DataFrame, created from aggregation computations (add and divide) on subsets of the data. The new columns are:

o    Total Number of Titles

o    Percentage of Total Library - Print Titles

o    Percentage of Total Library - E-book and E-audio Titles

•    A DataStorage object is created, with IndexSlice objects being used to populate several variables of the DataStorage class. The groupby operation is used to calculate the average stats for each region.

•    Four pivot tables are then created and assigned as DataStorage object variables.

•    At this point in the program the user is prompted to select what datasets they would like to see.

•    Option 1: The aggregate stats of all libraries option uses the describe method to print to the terminal stats for the entire data set, such as; mean, standard deviation, min, and max data on each of the various types of titles the libraries carry. These stats are then exported to a spreadsheet.

•    Option 2: Print/E-book total and average stats are printed for the user selected library, the library’s region, and all regions, and for the full province.

•    Option 3: The DataStorage object is used to print the four previously created pivot tables.

•    Option 4: Two plots are created using the previously created pivot tables.

•    Option 5: Allows the user to select a different library to get individual information for without having to re-run the program.

•    Option 6: Exports the full data set as excel file to the local directory, then exits the program.

•    All aspects of the program are broken out into user defined functions. A Class object is used for ease of storing and calling various slices and tables of data.

References
[1]    2019 Ontario Public Library Statistics Open Data, Heritage, Sport, Tourism and Culture Industries, Government of Canada, June. 2021. [Online] Available: https://data.ontario.ca/dataset/363fff31-6a07-41eb-9922-e9b64192b08b/resource/6555ef43-4dcc-451c-b368-0232a20f6918/download/2019_ontario_public_library_statistics_open_data.csv

[2]    2018 Ontario Public Library Statistics Open Data, Heritage, Sport, Tourism and Culture Industries, Government of Canada, June. 2021. [Online] Available: https://files.ontario.ca/opendata/ontario_public_library_statistics_open_data_2018.csv

[3]    2017 Ontario Public Library Statistics Open Data, Heritage, Sport, Tourism and Culture Industries, Government of Canada, June. 2021. [Online] Available: https://files.ontario.ca/opendata/ontario_public_library_statistics_open_data_july_2019_rev1.csv
