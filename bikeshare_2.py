import time
import pandas as pd
import numpy as np

"""
Establish dictionary references for use throughout

"""

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = { 'january': 1,
               'february': 2,
               'march': 3,
               'april': 4,
               'may': 5,
               'june': 6}

DAY_DATA = { 'monday': 0,
             'tuesday': 1,
             'wednesday': 2,
             'thursday': 3,
             'friday': 4,
             'saturday': 5,
             'sunday': 6}


def print_raw_data(df):
    
    """
    Print 5 rows of raw data at a time and then ask the user if they want to see another 5
    The function can be called before and/or after filtering
    
    Arguments
        df - Pandas DataFrame containing city data
    
    """
    
    counter = 1
    more_raw = 'y'
    
    while more_raw == 'y':
        pd.set_option('display.max_columns',200)
        print(df.iloc[counter:counter+5])
        more_raw = input('Another five? Y/N ').lower()
        if more_raw == 'y':
            counter += 5
        elif more_raw == 'n':
            break
        else:
            print('You did not enter a valid choice.')
            more_raw = input('Another five? Y/N ').lower()
            counter += 5
        
    

def get_filters():
    
    """
    Asks user to specify a city to analyze and then if they want to filter by month and/or day.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city = ''
    month = 'all'
    day = 'all'
    
   # Ask the use to select a city to analyze
   
    while city.lower() not in CITY_DATA:
        city = input('Which city data would you like to explore: New York, Chicago or Washington? \n')
        if city.lower() not in CITY_DATA:
            print('Something went wrong.  You only have 3 choices: New York, Chicago or Washington \n')   
 
    # Ask the user if they want to filter the data by Month, Day, Both Month and Day or No filter

    filterdata = ""
    while filterdata not in ['m', 'd', 'b', 'n']:
        filterdata = input('Do you want to filter the data by (M)onth, (D)ay, (B)oth Month and Day, or (N)o filter? \n').lower()
        if filterdata not in ['m', 'd', 'b', 'n']:
            print('Maybe you made a typo. Please select M, D, B, or N \n')
    
    # Get the Month to filter by if the user indicated they wanted to filter by Month or Both 
    
    if filterdata in ['m', 'b']:     
        while month not in MONTH_DATA:
            month = input('Which month would you like to filter by: January - June? \n').lower()
            if month not in MONTH_DATA:
                print('Please enter a month between January and June \n')


    # Get the Day to filter by if the user indicated they wanted to filter by Day or Both 
    
    if filterdata in ['d', 'b']:
        while day not in DAY_DATA:
            day = input('Which day of the week do you want to filter by - Sunday - Saturday?  \n').lower()
            if day not in DAY_DATA:
                print('Sorry, I didn\'t get that.  Which day? \n')
            
     
    print('-'*40)
    
    # Return the City to read data from and the Monday and Day filters.
    return city, month, day


def load_data(city, month, day):
    
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day (when applicable)
        
    """
        
    df = pd.read_csv(CITY_DATA[city])
        
    # convert the Start and End Time columns to a datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    
    # Ask if the user wants to see some of the raw data.  Make the question relevant to whether or not filters were selected
    preview_data = ''
    while preview_data not in ['y', 'n']:
        if (month != 'all') or (day != 'all'):
            preview_data = input('Would you like to see some raw data before we apply any filters? Enter Y or N \n').lower()
        else:
            preview_data = input('Would you like to see some raw data? Enter Y or N \n').lower()
        if preview_data not in ['y', 'n']:
            print('Just Y or N please')
            
    if preview_data == 'y':
        print_raw_data(df)
        
    # Now apply relevant filters    
    # Filter by month if not "all"
    if month != 'all':
        month = MONTH_DATA[month]
        df = df[df['month'] == month]
          
    # Filter by day if not "all"
    if day != 'all':
        day = DAY_DATA[day]
        df = df[df['day_of_week'] == day] 


    # If we applied filters - ask if the user wants to see some of the post-filtered raw data
    if (month != 'all') or (day != 'all'):
        preview_data = ''
        while preview_data not in ['y', 'n']:
            preview_data = input('Filters have been applied - would you like to see some of the filtered raw data? Enter Y or N \n').lower()
            if preview_data not in ['y', 'n']:
                print('Just Y or N please')   
            
        if preview_data == 'y':
            print_raw_data(df)
   
    # Return the dataframe to be used for the statistics portion of the program
    return df


def time_stats(df, month, day):
    
    """
    Displays statistics on the most frequent times of travel. 
    
    Args:
        (dataframe) df - the city to be analyzed in a dataform
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        
    """
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # If we haven't filtered by month, use mode to get most common month number, then reference the MONTH dictionary to get the title
    if month == 'all':        
        most_common_month = df['month'].mode()[0]
        for num in MONTH_DATA:
            if MONTH_DATA[num]==most_common_month:
                most_common_month = num.title()
        print('The most common month is: {}'.format(most_common_month))                        

    # If we haven't filtered by day, use mode to get most common day of week number, then reference the day dictionary to get the title       
    if day == 'all': 
        most_common_day = df['day_of_week'].mode()[0]
        for num in DAY_DATA:
            if DAY_DATA[num] == most_common_day:
                most_common_day = num.title()
        print('The most common day is: {}'.format(most_common_day))
              
    # Display the most common Start hour, convert to a 12hr clock representation
    df['hour'] = df['Start Time'].dt.hour   
    common_hour = df['hour'].mode()[0]
    twelve_hr_designation = 'am'
    if common_hour > 12:
        common_hour -= 12
        twelve_hr_designation = 'pm'   
    print("The most common start hour is: {} {}".format(common_hour, twelve_hr_designation))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        (dataframe) df - the city to be analyzed in a dataform

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display the most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is: {}".format(common_start_station))

    # Display the most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is: {}".format(common_end_station))

    # Display most common combination of start and end station trip
    start_end_station = df['Start Station'] + ' to ' + df['End Station']
    common_trip = start_end_station.mode()[0]
    print("The most frequent combination of station trips are from {}".format(common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    
    """
    Displays statistics on the total and average trip duration.
    
    Args:
        (dataframe) df - the city to be analyzed in a dataform
   
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time.  Sum all Travel Duration then break down by days, hours, minutes, seconds
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour,24)
    print("The total trip duration is {} days, {} hours, {} minutes and {} seconds.".format(day, hour, minute, second))

    # Display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    minute, second = divmod(average_duration, 60)
    # If the mean is > 60 then convert to hours
    if minute > 60:
        hour, minute = divmod(minute, 60)
        print("The average trip duration is {} hours, {} minutes and {} seconds.".format(hour, minute, second))
    else:
        print("The average trip duration is {} minutes and {} seconds.".format(minute, second))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """
    Displays statistics on bikeshare users.
    
    Args:
        (dataframe) df - the city to be analyzed in a dataform
        (str) city - name of the city being analyzed 
        
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display count by user types
    user_type_count = df['User Type'].value_counts()
    print("The count of users by type:\n{}\n".format(user_type_count).title())

    # Display count by gender. Need to validate if Gender is present in dataform - not all cities contain this data
    if 'Gender' not in df:
        print("There is no gender data for {} \n".format(city).title())     
    else:  
        gender_count = df['Gender'].value_counts()
        print("Breakdown of genders:\n{}\n".format(gender_count).title())

    # Display earliest, latest, and most common year of birth. Need to validate if Birth Year is present in dataform - not all cities contain this data
    if 'Birth Year' not in df:
        print("There is no birth data for {} \n".format(city)) 
    else: 
        print('Earliest birth year: {}'.format(str(int(df['Birth Year'].min()))))
        print('Latest birth year: {}'.format(str(int(df['Birth Year'].max())))) 
        print('Most common birth year: {}'.format(str(int(df.groupby('Birth Year')['Birth Year'].count().sort_values(ascending=False).index[0]))))      
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter Y to restart.\n').lower()
        if restart != 'y':
            break


if __name__ == "__main__":
	main()
