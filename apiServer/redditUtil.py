from tokenize import Comment
import praw as Praw
from textblob import TextBlob

def getChartData(symbol, range, limit):
    #init variables
    chartData = {}
    labels = []
    datapoints = []
    postData = {}
    #initalize reddit client with credentials and constant variables
    reddit = Praw.Reddit(client_id='i8JhhqMQafcZZw', client_secret='kNJ7rn5LNBTYasgzg0IT7HejjI8',
                         user_agent='MemeScraper1.0')

    subreddit = reddit.subreddit('stocks')
    for submission in subreddit.search(symbol, limit=limit):
        print('reading message ' + submission.title)
        #add the timestamp of the post to labels list
        labels.append(submission.created_utc)
        #add the sentiment to the datapoints list
        datapoints.append(getSentiment(submission))
        postData[submission.title] = {'selftext':submission.selftext,
         'upvoteRatio':submission.upvote_ratio,
         'score':submission.score,
         'url': submission.url,
         'post_sentiment': getPostSentiment(submission),
         'comment_sentiment': getCommentSentiment(submission)}
    

    #Nest data inside chartData object and return.
    chartData['labels'] = labels
    chartData['datapoints'] = datapoints
    chartData['postData'] = postData
    
    return chartData

#returns sentiment data combined with post stats for upvote + upvote ratio
def getSentiment(redditPost):
    post_sentiment = getPostSentiment(redditPost) + getCommentSentiment(redditPost)
    sentiment_score = post_sentiment * (redditPost.score * redditPost.upvote_ratio)
    return sentiment_score

#Returns sentiment data for reddit post
def getPostSentiment(post):
    title_sentiment = TextBlob(post.title).sentiment
    selftext_sentiment = TextBlob(post.selftext).sentiment
    #mutliply the polarity and subjectivity of both title and selftext and add them together.
    post_sentiment = ((title_sentiment.polarity * title_sentiment.subjectivity) + (selftext_sentiment.polarity * selftext_sentiment.subjectivity))
    return post_sentiment

#Returnss sentiment data for reddit comments
def getCommentSentiment(post):
    comments_sentiment = 0
    for comment in post.comments:
        if (type(comment) is Praw.models.Comment):
            comments_sentiment += TextBlob(comment.body).sentiment.polarity * TextBlob(comment.body).sentiment.subjectivity
    return comments_sentiment
