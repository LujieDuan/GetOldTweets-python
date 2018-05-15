# -*- coding: utf-8 -*-
import sys, csv, codecs

import emailHandler
from datetime import date, timedelta, datetime
import time

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got


def main_loop(from_date, until_date):
    while True:
        if main(argv[0], argv[1]) == 0:
            break


def main(from_date, until_date):
    try:
        tweetCriteria = got.manager.TweetCriteria()
        outputFileName = "cincinnati_tweets_%s_%s.csv" % (from_date, until_date)
        logFileName = "cincinnati_tweets_%s_%s.output.txt" % (from_date, until_date)
        import sys
        sys.stdout = open(logFileName, 'w')

        tweetCriteria.maxTweets = int(100000000)
        tweetCriteria.near = "Cincinnati"
        tweetCriteria.within = "15mi"
        tweetCriteria.since = from_date
        tweetCriteria.until = until_date

        csvfile = open(outputFileName, "w+", encoding="utf-8")
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(
            ['username', 'date', 'retweets', 'favorites', 'text', 'geo', 'mentions', 'hashtags', 'id', 'permalink'])

        print('Searching...\n')

        def receiveBuffer(tweets):
            for t in tweets:
                csvwriter.writerow(
                    [t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions,
                     t.hashtags, t.id, t.permalink])
            csvfile.flush()
            print('More %d saved on file...\n' % len(tweets))

        got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

    except:
        print('Failed. Retrying...')
        return 1
    finally:
        csvfile.close()
        print('Done. Output file generated "%s".' % outputFileName)
        sys.stdout.flush()
        emailHandler.send_email(outputFileName, outputFileName, outputFileName)
        emailHandler.send_email(logFileName, logFileName, logFileName)
        return 0


if __name__ == '__main__':

    argv = sys.argv[1:]

    if len(argv) == 0:

        for i in range(0, 365):
            # sleep until 2AM
            t = datetime.today()
            future = datetime(t.year, t.month, t.day, 2, 0)
            if t.hour >= 2:
                future += timedelta(days=1)
            time.sleep((future - t).seconds)

            now = date.today() - timedelta(1)
            yesterday = date.today() - timedelta(2)
            result = main(yesterday.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d"))
    else:
        result = main(argv[0], argv[1])

