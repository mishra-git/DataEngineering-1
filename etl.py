import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    # open song file
    df = pd.DataFrame(pd.read_json( filepath,lines=True,orient='columns'))

    # insert song record
    song_data =  (df.values[0][7], df.values[0][8], df.values[0][0], df.values[0][9], df.values[0][5])

    cur.execute(song_table_insert, song_data)

    artist_data = ( df.values[0][0], df.values[0][4], df.values[0][2], df.values[0][1], df.values[0][3])
    cur.execute(artist_table_insert, artist_data)



def process_log_file(cur, filepath):
    # open log file
    df =  df = pd.DataFrame(pd.read_json(filepath,lines=True,orient='columns'))

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = list(zip( t.dt.strftime('%Y-%m-%d %I:%M:%S'),
                             t.dt.hour,
                             t.dt.day,
                             t.dt.isocalendar().week, #-- dt.week has been deprecated
                             t.dt.month,
                             t.dt.year,
                             t.dt.weekday))    
  
    column_labels = column_labels = (       'start_time',
                            'hour',
                            'day',
                            'week',
                            'month',
                            'year',
                            'weekday')
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for k, timetupple in time_df.iterrows():
        cur.execute(time_table_insert, list(timetupple))

    # load user table
    user_df = df.get(['userId', 'firstName', 'lastName', 'gender', 'level'])

    # insert user records
    for k, usertupple in user_df.iterrows():
        cur.execute(user_table_insert, usertupple)

    # insert songplay records
    for index, record in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select,(record.song, record.artist, record.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record

        start_time = pd.to_datetime(
                            record.ts,
                            unit='ms').strftime(
                            '%Y-%m-%d %I:%M:%S')
        songplay_data = (   start_time,
                            record.userId,
                            record.level,
                            str(songid),
                            str(artistid),
                            record.sessionId,
                            record.location,
                            record.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres password=Ch0ndr0m0@123q")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()