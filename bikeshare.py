import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('Tip: Enter CTRL+Z (Win) / CTRL+D (Linux) for exit from application.')
    try:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input("Please enter city (Chicago, New York City, Washington): ").lower()
        while city not in CITY_DATA:
            print('Unknown city:(')
            city = input("Enter city (Chicago, New York City, Washington): ").lower()

        # get user input for month (all, january, february, ... , june)
        month_names = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        month = input("Please enter the month to filter by (January - June, 'all' for no filter): ").lower()
        while month not in month_names:
            print('Incorrect input value:(')
            month = input("Please enter the month to filter by (January - June, 'all' for no filter): ").lower()

        # get user input for day of week (all, monday, tuesday, ... sunday)
        dow_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
        day = input("Please enter the day of the week to filter by (Monday - Sunday, 'all' for no filter): ").lower()
        while day not in dow_names:
            print('Incorrect input name:(')
            day = input("Please enter the day of the week to filter by (Monday - Sunday, 'all' for no filter): ").lower()

    except EOFError:
        print('Goodbye!')
        exit()

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

    # filter DataFrame by month and day
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()
    #compatibility with old versions: df['Day of Week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()
    print('The most common month: {}'.format(months[popular_month[0] - 1].title()))
    if len(popular_month) > 1:
        print('Warning! Multiple values found. First value shown.')


    # display the most common day of week
    popular_dow = df['Day of Week'].mode()
    print('The most common day of the week: {}'.format(popular_dow[0]))
    if len(popular_dow) > 1:
        print('Warning! Multiple values found. First value shown.')

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Hour'].mode()
    print('The most common start hour: {}'.format(popular_hour[0]))
    if len(popular_hour) > 1:
        print('Warning! Multiple values found. First value shown.')

    print("\nThis took {:.3f} seconds.".format(time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    top_start = df['Start Station'].mode().values
    print('\nThe most popular start station(s): {}'.format(top_start[0]))
    if len(top_start) > 1:
        print('Warning! Multiple values found. First value shown.')

    # display most commonly used end station
    top_end = df['End Station'].mode().values
    print('\nThe most popular end station(s): {}'.format(top_end[0]))
    if len(top_end) > 1:
        print('Warning! Multiple values found. First value shown.')

    # display most frequent combination of start station and end station trip
    st_combination = df['Start Station']+' -> ' + df['End Station']
    top_comb = st_combination.mode().values
    print('\nThe most popular combination(s) of start / end stations: {}'.format(top_comb[0]))
    if len(top_comb) > 1:
        print('Warning! Multiple values found. First value shown.')

    print("\nThis took {:.3f} seconds.".format(time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: {:.3f} hours'.format(total_travel_time / 3600))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean(skipna=True)
    print('Mean travel time: {:.0f} min {:.1f} sec'.format(mean_travel_time // 60, mean_travel_time % 60))

    print("\nThis took {:.3f} seconds.".format(time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types:')
    user_types = df['User Type'].value_counts()
    print(user_types.to_string())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nCounts of gender:')
        gender = df['Gender'].value_counts()
        print(gender.to_string())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nThe earliest year of birth: {:.0f}'.format(df['Birth Year'].min(skipna=True)))
        print('\nThe most recent year of birth: {:.0f}'.format(df['Birth Year'].max(skipna=True)))
        com_year = df['Birth Year'].mode()
        print('\nThe most common year of birth: {:.0f}'.format(com_year[0]))
        if len(com_year) > 1:
            print('Warning! Multiple values found. First value shown.')

    print("\nThis took {:.3f} seconds.".format(time.time() - start_time))
    print('-'*40)

def user_input_yes_no(msg):
    """
    Reads user answer to  and returns either 'yes' or 'no'.
    Answers other than 'yes' or 'no' is not allowed.

    Args:
        (str) msg - String containing prompt for user
    Returns:
        user_input: 'yes' or 'no'. Other answers is not allowed
    """
    user_input = input(msg).lower()
    while (user_input != 'yes') and (user_input != 'no'):
        print('Incorrect answer. Please enter yes or no.\n')
        user_input = input(msg).lower()
    return user_input

def print_raw_data(df):
    """Displays raw data in pages of 5 lines."""
    num_of_records = df.shape[0]

    try:
        pos = 0
        while user_input_yes_no('\nWould you like to see raw data? Enter yes or no.\n') == 'yes':
            print(df.iloc[pos:pos+5, 0:9])
            pos += 5
            if pos >= num_of_records:
                print('\n{} rows of {} was shown.\nNo more raw data to display.\n'.format(num_of_records, num_of_records))
                break

    except EOFError:
        print('Goodbye!')
        exit()


def main():
    try:
        while True:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            if (df.shape[0] > 0):
                time_stats(df)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)
                print_raw_data(df)
            else:
                print('\nNo data to analyze!\n')

            if user_input_yes_no('\nWould you like to restart? Enter yes or no.\n') != 'yes':
                break
    except:
        print('Application terminated!')

if __name__ == "__main__":
	main()
