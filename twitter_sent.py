## This script was written by Michael Fernandes for HCDE 310(Interactive System Design).
## It is a demostration of natural language process to provide sentiment analysis.

## This script uses positive and movie reviews from the NLTK corpus library as training 
## sets to classify twitter tweets.

## As a discalimer, this code really is not meant for practical use but really as demostration
##
import  json
import nltk
import string
import requests
from requests_oauthlib import OAuth1
from pip._vendor.requests.models import Response
 
def get_trainingt_set(file, senti):
    'Returns set of sample tweets'
    f = open(file)
    lines = f.readlines()

    test_list = []
    for obj in lines:
        j = json.loads(obj)
        tweet = j["text"].encode("utf-8").split()
        sen_split = []
        for word in tweet:
            werd = word.lower().strip(string.punctuation)
            if (len(werd) < 10):
                if(len(werd) > 3):
                    sen_split.append(werd)
        test_list.append((sen_split, senti))
    return test_list

def create_fd(tweets):
    'Calculates frequency distribution of tweets'
    wordlist = []

    for (words, sentiment) in tweets:
        wordlist.extend(words)

    fd = nltk.FreqDist(wordlist)
    word_features = fd.keys()

    return word_features[:(len(word_features) / 2)]

def extract_features(input_text):
    'Extracts key features from each training set'
    input_words = set(input_text)
    features = {}
    for word in wordFeatures:
        features['contains(%s)' % word] = (word in input_words)
    return features




def twittSent(classifier):
    'Classifies twitter tweets containging key word or topic selected by a user.'
    input = raw_input("Welcome to TwitterSent \n Select a keyword to begin ")
    dict = {}

    # Replace with tokens recieved when setting up your Twitter account with it's api.
    acessTok = ""
    acessTokSk = ""
    conTok = ""
    conTokSk = ""
    
    # Creates endpoint url
    base = "https://api.twitter.com/1.1/search/tweets.json?q="
    count = "&count=100"
    keyword = input
    lang = "&lang=en"
    type = "&result_type=recent"
    url = base + keyword + lang + type + count
    
    # Sets up Oauth1 module
    oauth = OAuth1(conTok, client_secret=conTokSk, resource_owner_key=acessTok, resource_owner_secret=acessTokSk)
    response = requests.get(url, auth= oauth)
    
    lst = []
    tweets = json.loads(response.text)["statuses"]

    count = [0,0]
    for tweet in tweets:
        keep = classifier.classify(extract_features(tweet["tweet"].split()))
        # Monitors total positive and negative tweets
        if keep == "positive":
            count[0] = count[0] + 1
        else:
            count[1] = count[1] + 1
        # Adds tweet and meta data to running list
        lst.append( [tweet["text"], tweet["created_at"], tweet["user"]["screen_name"] \
                            , classifier.classify(extract_features(tweet["text"].split()))] ) 
    print "\n\n"

    # Prints tweets and sentiments
    for obj in lst:
        print json.dumps(obj[2]).strip('"') + "\t\t" + json.dumps(obj[1]).strip('"')
        print json.dumps(obj[3]).strip('"')
        print json.dumps(obj[0]).strip('"') + "\n"

    print "%d out of %d tweets were positive" % (count[0], count[0] + count[1])

def main():
    print "Starting TwitterSent, please wait while classifier is being compiled"
    print "This usually takes 5-6 seconds\n"
    print "Intializing sample set...."

    # Given File Structure for corpus if downloaded directly through NLTK package
    neg_tweets_file = "senti_anal/twitter_samples/negative_tweets.json"
    pos_tweets_file = "senti_anal/twitter_samples/positive_tweets.json"

    test_tweets = get_trainingt_set(neg_tweets_file, "negative") + get_trainingt_set(pos_tweets_file, "positive")


    wordFeatures =  create_fd(test_tweets)
    training_set = nltk.classify.apply_features(extract_features, test_tweets)
    print "Training classifier....\n" # Takes up to 10-20 seconds
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    twittSent(classifier)


if __name__ == '__main__':main()
