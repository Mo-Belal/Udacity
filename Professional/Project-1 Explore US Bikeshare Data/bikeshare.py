import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    city = input('Please enter the name of the city to analyze: ').lower()
    while city not in cities:
        print("Error: Invalid city!")
        city = input('Please select a city from (chicago, new york city, washington): ').lower()
    
    # get user input for month (all, january, february, ... , june)
    months = ['all','january','february','march','april','may','june']
    month = input('name of the month to filter by, or "all" to apply no month filter: ').lower()
    while month not in months:
        print("Error: Invalid month!")
        city = input('Please select a month from (all, january, february, ... , june): ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day = input('name of the day of week to filter by, or "all" to apply no day filter: ').lower()
    while day not in days:
        print('Error: Invalid day!')
        day = input('Please select a day from (all, monday, tuesday, ... sunday)').lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

     # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['Month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]
    print(f'the most common month: {popular_month}')

    # display the most common day of week
    popular_day = df['Day'].mode()[0]
    print(f'the most common day: {popular_day}')

    # display the most common start hour
    popular_hour = df['Start Time'].dt.hour.mode()[0]
    print(f'the most common hour: {popular_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(f'the most commonly used start station: {popular_start_station}')

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print(f'the most commonly used end station: {popular_end_station}')

    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station']+' - '+df['End Station']
    popular_route = df['Route'].mode()[0]
    print(f'the most frequent combination of start station and end station trip: {popular_route}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'the total trip duration: {total_travel_time}')

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print(f'the average trip duration: {average_travel_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city): # add city argument to filter gender and birth years (only available for NYC and Chicago)
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts().to_frame()
    print(f'counts of user types: {user_counts}')

    # Display counts of gender
    if city != 'washington': #(only available for NYC and Chicago)
        gender_counts = df['Gender'].value_counts().to_frame()
        print(f'counts of gender: {gender_counts}')

    # Display earliest, most recent, and most common year of birth
    if city != 'washington': #(only available for NYC and Chicago)
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        popular_year = df['Birth Year'].mode()[0]

        print(f'Earliest year of birth: {earliest_year}')
        print(f'Most recent year of birth: {recent_year}')
        print(f'Most common year of birth: {popular_year}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df):
    view_rows = input("Would you like to view 5 rows of individual trip data? Enter yes or no?: ").lower()
    while view_rows not in ['yes','no']:
        print('Error: Invalid Input. please enter "yes" or "no"')
        view_rows = input("Would you like to view 5 rows of individual trip data? Enter yes or no?: ").lower()
    else:
        if view_rows=='yes':
            start_loc = 0
            while start_loc+5 < df.size:
                print(df.iloc[start_loc:start_loc+5])
                start_loc += 5
                view_rows = input("Do you wish to view the next 5 rows? Enter yes or no?: ").lower()
                if view_rows!='yes':
                    print('Thank you!')
                    break
            else:
                print('All rows have been displayed, No more data to show!')
        else: #no
            print('Thank you!')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Program Ended, Thank you!')
            break

if __name__ == "__main__":
	main()
