# p21_group5_project.py
# AUTHOR NAMES: Michael Kissinger, Brandon Quan
# Group number 5
# 
# Ontario Public Library – Data Analysis Interface Program
# Program that imports Ontario Public Library datasets from 2017 to 2019
# Allows users to select which data outputs they want to view
# See formal report for full program specifications
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DataStorage:
    """
    A class used to store slices and tables of data relating to the selected library and the library regions of Ontario.

        Attributes:
            library_name (str): string that represents the library selected by the user
            region_name (str): string that represents the region where the library is Ottawa
            library_slice (DataFrame): a DataFrame slice representing the stats for the selected library
            region_slice (DataFrame): a DataFrame slice representing the average stats for the region where the library is located
            all_region_slice (DataFrame): a DataFrame slice representing the average stats for all regions
            library_pivot (DataFrame): a pivot table with stats relating to the number of e-titles at the selected library
            region_pivot (DataFrame): a pivot table with stats relating to the average number of e-titles at the selected library's region
            all_region_pivot (DataFrame): a pivot table with stats relating to the average number of e-titles at all regions
    """
    def __init__(self, library_name, region_name, library_slice, region_slice, all_region_slice, library_pivot, region_pivot, all_region_pivot, province_slice, province_pivot):
        self.library_name = library_name
        self.region_name = region_name
        self.library_slice = library_slice
        self.region_slice = region_slice
        self.all_region_slice = all_region_slice
        self.province_slice = province_slice
        self.library_pivot = library_pivot
        self.region_pivot = region_pivot
        self.all_region_pivot = all_region_pivot
        self.province_pivot = province_pivot

def import_data():
    """
    Function imports, merges 3 datasets, and sorts data.
    Must delete duplicated columns/rows that result from the merge.
    Arguments: no arguments.
    Returns: library_data, a DataFrame of three joined datasets that are sorted using a hierarchical index.
    """
    # Imports the library data with a multi-index of various columns.
    library_data_2017 = pd.read_excel("Ontario Public Library Datasets/ontario_public_library_statistics_2017.xlsx", index_col=[8, 3, 4, 1, 0, 7, 9, 2])
    library_data_2018 = pd.read_excel("Ontario Public Library Datasets/ontario_public_library_statistics_2018.xlsx", index_col=[8, 3, 4, 1, 0, 7, 9, 2])
    library_data_2019 = pd.read_excel("Ontario Public Library Datasets/ontario_public_library_statistics_2019.xlsx", index_col=[8, 3, 4, 1, 0, 7, 9, 2])
    
    # Sorts the indices of each DataFrame, drops unnecessary columns, and unstacks the 'Year' index.
    library_data_2017 = library_data_2017.sort_index().unstack().drop(columns = ['Mailing Address', 'Street Address', 'Web Site Address', 'English E-book and E-audio Titles', 'English Print Titles Held', 'French E-book and E-audio Titles', 'French Print Titles Held', 'No. Cardholders', 'Other E-book and E-audio Titles', 'Other Print Titles Held'])
    library_data_2018 = library_data_2018.sort_index().unstack().drop(columns = ['Mailing Address', 'Street Address', 'Web Site Address', 'English E-book and E-audio Titles', 'English Print Titles Held', 'French E-book and E-audio Titles', 'French Print Titles Held', 'No. Cardholders', 'Other E-book and E-audio Titles', 'Other Print Titles Held'])
    library_data_2019 = library_data_2019.sort_index().unstack().drop(columns = ['Mailing Address', 'Street Address', 'Web Site Address', 'English E-book and E-audio Titles', 'English Print Titles Held', 'French E-book and E-audio Titles', 'French Print Titles Held', 'No. Cardholders', 'Other E-book and E-audio Titles', 'Other Print Titles Held'])
    
    # Uses two join methods to incorporate all three datasets into a single DataFrame.
    library_data = library_data_2017.join(library_data_2018).join(library_data_2019)

    # Formats the columns.
    library_data = library_data.stack().unstack()

    # Returns the formatted dataset.
    return library_data

def remove_zeros(library_data) :
    """
    Function remove_zeros() checks for rows that only contain zero values and removes those rows.
    Also removes rows with only zeros and NaN values. Returns a dataframe with these rows removed 
    Arguments: library_data, a DataFrame of three joined datasets that are sorted using a hierarchical index.
    Returns: library_data_filtered, the library_data DataFrame, with all empty rows removed
    """
    # Uses a boolean masking function to remove all rows with a sum equal to zero
    library_data_filtered = library_data.loc[(library_data.sum(axis=1)!=0)]
    return library_data_filtered

def add_columns(library_data):
    """
    Function adds new columns with percentage of print and e-book/e-audio titles, and number of total titles within the libraries.
    Arguments: library_data, a DataFrame that the calculations will be performed on.
    Returns: library_data, the same DataFrame, with columns added.
    """
    # Stacks the "Year" index for easier addition of new columns.
    library_data = library_data.stack()

    # Adds new columns containing the total number of titles and the percentages of print/e-book/e-audio titles.
    library_data["Total Number of Titles"] = library_data["Total Print Titles Held"].add(library_data["Total E-book and E-audio Titles"])
    library_data["Percentage of Total Library - Print Titles"] = library_data["Total Print Titles Held"].divide(library_data["Total Number of Titles"])*100
    library_data["Percentage of Total Library - E-book and E-audio Titles"] = library_data["Total E-book and E-audio Titles"].divide(library_data["Total Number of Titles"])*100
    
    # Unstacks the "Year" index.
    library_data = library_data.unstack()

    # Returns the library data with columns added.
    return library_data
    
def user_input_first(library_data):
    """
    Function user_input_first() prompts user to enter a valid library name or number. 
    Checks if the entry is valid, then if valid returns the result.
    If it is not valid the user is re-prompted to enter a valid library name or number.
    Arguments: library_data, a DataFrame containing an index of library names and library numbers. 
    Returns: library_name, a string of the library's full name.
    """
    # Creates a loop that continues to prompt if an invalid input is entered.
    while True:

        # Prompts for user input.
        library = input("Please enter the library name or library number that you would like to evaluate (Example: 'Ottawa' or 'L0481'), or enter 1 for an index of all libraries: ")

        #If user selected 1 then an index of all library names are printed, the user can then enter the libary name
        if library == '1':
            print(library_data.index.get_level_values("Library Full Name")[:])
        else:
            try:
                # Creates a variable that tracks if the library name or code is found.
                valid_name = False

                # Iterates through the elements of the library DataFrame.
                for i in range(len(library_data.index)):
                    if (library == library_data.index.get_level_values("Library Full Name")[i]) or (library == library_data.index.get_level_values("Library Number")[i]):

                        # If the library name or number is found, the name is printed and library name is set.
                        print("Library Name: ", library_data.index.get_level_values("Library Full Name")[i], ", Library Number: ", library_data.index.get_level_values("Library Number")[i])
                        library_name = library_data.index.get_level_values("Library Full Name")[i]

                        # Valid name is set to True.
                        valid_name = True
                        break
                
                # If the library name or number was found, the loop is broken.
                if valid_name == True:
                    return library_name

                # If the library name or number was not found, a ValueError is raised.
                else:
                    raise ValueError
            
            # If a ValueError is raised, an error message to enter a valid library name or number is displayed to the user.
            except ValueError:
                print("You must enter a valid library name or number.")

                # After message is displayed, the loop enters its next iteration and prompts for a valid library name or number.
                continue
    
def user_input_second():
    """
    Function user_input_second() prompts user to enter a number that corresponds to one of the program's functions.
    Checks if the entry is valid, then if valid returns the result.
    If it is not valid the user is re-prompted to enter a valid number.
    Arguments: no arguments.
    Returns: option_select, a string number representing the option selected by the user.
    """
    # Creates a loop that continues to prompt if an invalid input is entered.
    while True:

        # Prompts for user input.
        option_select = input("""Please enter an option:
    Enter 1 to describe and export stats of all libraries.
    Enter 2 to display stats for your library, average stats for all library regions, and average stats for the province.
    Enter 3 to display the number of e-titles for your library, mean e-titles for all regions, and mean e-titles for the province year-by-year in a pivot table format.
    Enter 4 to display the number of e-titles for your library, mean e-titles for all regions, and mean e-titles for the province year-by-year in a plot format.
    Enter 5 to change your library.
    Enter 6 to exit the program and export full dataset. \n""")
        
        try:
            # Creates a variable that tracks if the option selected is valid.
            valid_option = False

            # Iterates through the options.
            for i in [1, 2, 3, 4, 5, 6]:

                # If option is found, it is valid.
                if option_select == str(i):
                    valid_option = True
                    break
            
            # If the option was found, the loop is broken.
            if valid_option == True:
                return option_select

            # If the option was not found, a ValueError is raised.
            else:
                raise ValueError
        
        # If a ValueError is raised, an error message to enter a valid option is displayed to the user.
        except ValueError:
            print("You must enter a valid option.")

            # After message is displayed, the loop enters its next iteration and prompts for a valid option.
            continue

def initialize_slices(library_data, data_storage):
    """
    Function initializes many variables within a data_storage object.
    Arguments: library_data, a DataFrame of three joined datasets sorted by a hierarchical index, and data_storage, a data storage object that stores slices of data
    Returns: None
    """

    # Stores a valid library name.
    data_storage.library_name = user_input_first(library_data)

    # Creates an IndexSlice object.
    idx = pd.IndexSlice

    # Stores a slice of the library data relating to the selected library's print and e-book/e-audio titles.
    data_storage.library_slice = library_data.loc[idx[:, :, :, :, data_storage.library_name], idx["Total E-book and E-audio Titles":"Percentage of Total Library - E-book and E-audio Titles"]]

    # Stores the region where the library was located.
    data_storage.region_name = data_storage.library_slice.index.get_level_values("Ontario Library Service Region")[0]

    # Creates a slice of the library data containing information for the region relating to print and e-book/e-audio titles.
    data_storage.region_slice = library_data.loc[idx[:, data_storage.region_name], idx["Total E-book and E-audio Titles":"Percentage of Total Library - E-book and E-audio Titles"]]

    # Uses a groupby object to calculate the average stats for every region, storing the stats relating to print and e-book/e-audio titles.
    all_region_data = library_data.groupby("Ontario Library Service Region").mean()
    data_storage.all_region_slice = all_region_data.loc[idx[:], idx["Total E-book and E-audio Titles":"Percentage of Total Library - E-book and E-audio Titles"]]

    # Calculates the mean for each column for each year.
    data_storage.province_slice = library_data

def initialize_pivot_tables(data_storage):
    """
    Function initializes the pivot tables within a data_storage object. Pivot tables show the number of e-titles for the relevant slice.
    Arguments: data_storage, the data_storage object that will store the pivot tables
    Returns: None
    """
    # Stacks all the slices for easier manipulation.
    library_slice = data_storage.library_slice.stack()
    region_slice = data_storage.region_slice.stack()
    all_region_slice = data_storage.all_region_slice.stack()
    province_slice = data_storage.province_slice.stack()

    # Creates a pivot table of each of the slices.
    data_storage.library_pivot = library_slice.pivot_table("Total E-book and E-audio Titles", index=["Year"], columns=["Library Full Name"])
    data_storage.region_pivot = region_slice.pivot_table("Total E-book and E-audio Titles", index=["Year"], columns=["Ontario Library Service Region"])
    data_storage.all_region_pivot = all_region_slice.pivot_table("Total E-book and E-audio Titles", index=["Year"], columns=["Ontario Library Service Region"])
    data_storage.province_pivot = province_slice.pivot_table("Total E-book and E-audio Titles", index=["Year"], columns=["Province"])

def describe_method(library_data):
    """
    Function uses the describe method to print aggregate stats for the entire dataset and exports it to an Excel datasheet.
    Arguments: library_data, a DataFrame of three joined datasets that are sorted using a hierarchical index, with empty rows removed
    Returns: None.
    """
    print("\nAggregate Stats for Entire Dataset:\n")
    print(library_data.describe().round())
    library_data.describe().round().to_excel("LibraryDescribeExport.xlsx")

def calculations(data_storage):
    """
    Function prints stats for the library, average stats for the region that the library was in, and average stats for all regions.
    Arguments: data_storage, an object containing the slices of data to be displayed
    Returns: None
    """
    # Prints a slice of the library data containing only information for the library entered by the user.
    print("\nPrint/E-book Stats for Library:", data_storage.library_name, "\n")
    print(data_storage.library_slice.transpose().round(), "\n\n")

    # Prints a slice of the library data containing information for the library's region.
    print("Average Print/E-book Stats for Region:", data_storage.region_name, "\n")
    print(data_storage.region_slice.mean().round(), "\n\n")

    # Prints a slice of the library data containing average stats for all regions.
    print("Average Print/E-book Stats for All Regions:", "\n")
    print(data_storage.all_region_slice.transpose().round(), "\n\n")

    # Prints a slice of the library data containing average stats for the province.
    print("Average Print/E-book Stats for Ontario:", "\n")
    print(data_storage.province_slice.mean().round(), "\n\n")

def pivot_table_funct(data_storage):
    """
    Prints pivot tables stored within a data storage object.
    Pivot tables show the number of e-titles per year for the selected library, 
    the average number of e-titles for the region, and the average number of e-titles for the other regions.
    Arguments: data_storage, the data storage object with the pivot tables to be printed
    Returns: None.
    """
    print("\n")
    print(data_storage.library_pivot, "\n")
    print(data_storage.region_pivot, "\n")
    print(data_storage.all_region_pivot, "\n")
    print(data_storage.province_pivot, "\n")

def matplotlib_funct(data_storage):
    """
    Function that generates a plot object using pivot tables and matplotlib.
    Arguments: data_storage, a data storage object with the pivot tables to be plotted
    Returns: None.
    """
    # Creates two subplots.
    e_book_compare, (top, bottom) = plt.subplots(2)
    e_book_compare.suptitle("Comparison of Total E-book and E-Audio Titles per Year")

    # Adds the library and region pivot tables to the top subplot.
    top.plot(data_storage.library_pivot)
    top.plot(data_storage.region_pivot)

    # Adds the library and all region pivot tables to the top subplot.
    bottom.plot(data_storage.library_pivot)
    bottom.plot(data_storage.all_region_pivot)
    bottom.plot(data_storage.province_pivot)

    # Add labels and subplot titles.
    top.set(xlabel = "Year", ylabel = "Total E-book and E-audio Titles", title = "Total E-book and E-audio Titles per Year for Library and Region")
    bottom.set(xlabel = "Year", ylabel = "Total E-book and E-audio Titles", title = "Total E-book and E-audio Titles per Year for Library and All Regions")
    
    # Add legends.
    top.legend([data_storage.library_name, "Average for "+data_storage.region_name])
    bottom.legend([data_storage.library_name,"Average for Ontario Library Service - North", "Average for Southern Ontario Library Service", "Average for Toronto", "Average for Ontario"])
    
    # Display the plots.
    plt.show()
    
def export(library_data):
    """
    Exports the entire merged, hierarchical dataset to an Excel file that includes the index and header values.
    Arguments: library_data, the DataFrame to be exported.
    Returns: None.
    """
    library_data.to_excel("LibraryDataExport.xlsx", index = True, header = True)
    print("Export complete!")

def main():
    print("\nENSF 592 Final Project\n")

    # Import and sort data.
    library_data = import_data()

    # Find any and remove missing zero rows, and NaN rows.
    library_data = remove_zeros(library_data)

    # Adds additional columns to the dataset with percentage of print and e-book/e-audio titles, and number of total titles within the libraries.
    library_data = add_columns(library_data)

    # Creates a data storage object and initializes its variables. 
    storage = DataStorage
    initialize_slices(library_data, storage)
    initialize_pivot_tables(storage)

    # Runs a while loop so user can select which data they want to run, then only exits when prompted by the user.
    run_program = True
    while run_program == True:
        option_select = user_input_second()
        if option_select == '1':
            describe_method(library_data)
        elif option_select == '2':
            calculations(storage)
        elif option_select == '3':
            pivot_table_funct(storage)
        elif option_select == '4':
            matplotlib_funct(storage)
        elif option_select == '5':
            initialize_slices(library_data, storage)
            initialize_pivot_tables(storage)
        elif option_select == '6':
            run_program = False
            export(library_data)
            print("Thank you for using our program.")
        else:
            print("Something went wrong. Please try again")
 
if __name__ == '__main__': # Used to execute the main function
    main()

