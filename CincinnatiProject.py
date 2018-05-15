# -*- coding: utf-8 -*-
import sys, csv, codecs

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got


def main(search_keyword):
    try:
        tweetCriteria = got.manager.TweetCriteria()
        outputFileName = "cincinnati_tweets_%s.csv" % search_keyword

        tweetCriteria.maxTweets = int(10000000000)
        tweetCriteria.near = "Cincinnati"
        tweetCriteria.within = "15mi"
        tweetCriteria.querySearch = '"' + search_keyword + '"'

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
    finally:
        csvfile.close()
        print('Done. Output file generated "%s".' % outputFileName)


if __name__ == '__main__':

    # keywords = ['opioid', 'heroin']
    # keywords = ['fentanyl', 'darkweb', 'dark web', 'tor', 'naloxone', 'detox', 'detoxification', 'drug']

    keywords = ['overdose']

    argv = sys.argv[1:]

    if len(argv) == 0:
        for k in keywords:
            main(k)
    else:
        main(argv[0])
