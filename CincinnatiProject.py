# -*- coding: utf-8 -*-
import sys,getopt,datetime,codecs
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

def main():
	try:
		tweetCriteria = got.manager.TweetCriteria()
		outputFileName = "cincinnati_all_output_got.csv"

		tweetCriteria.maxTweets = int(10000000)
		tweetCriteria.near = "Cincinnati"
		tweetCriteria.within = "15mi"
				
		outputFile = codecs.open(outputFileName, "w+", "utf-8")

		outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')

		print('Searching...\n')

		def receiveBuffer(tweets):
			for t in tweets:
				outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))
			outputFile.flush()
			print('More %d saved on file...\n' % len(tweets))

		got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
	finally:
		outputFile.close()
		print('Done. Output file generated "%s".' % outputFileName)

if __name__ == '__main__':
	main()
