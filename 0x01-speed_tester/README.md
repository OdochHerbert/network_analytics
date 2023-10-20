**Libraries Imported**

    speedtest: This is a library that allows you to test your internet speed using the Speedtest.net infrastructure.
    pandas: This is a popular data manipulation and analysis library.

**Function Definitions**

    measure_bandwidth(): This function uses the speedtest library to measure the download and upload speeds. The speeds are converted from bytes per second to megabits per second (Mbps) and then returned.

**Main Function**

    main(): This is the main function where the script execution starts. It initializes an empty list data to store the bandwidth data.

    Inside the while loop, it does the following:
        Gets the current timestamp using datetime.datetime.now().
        Calls the measure_bandwidth() function to get the download and upload speeds and appends them along with the timestamp to the data list.
        Pauses the execution for 10 seconds using time.sleep(10) to measure the bandwidth at regular intervals.
        Checks if the number of measurements has reached 5, and if so, breaks the loop.

    After the loop ends, the script creates a Pandas DataFrame from the collected data, with appropriate column names. Then, it exports this DataFrame to a CSV file named bandwidth_data.csv using the to_csv method.

    The if __name__ == "__main__": condition ensures that the main() function is executed when the script is run directly, but not when it's imported as a module.

**Script Execution**

The script essentially measures internet speed at regular intervals using the Speedtest library and saves the results to a CSV file for further analysis or record-keeping.
