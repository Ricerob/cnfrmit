from textblob import TextBlob
import matplotlib.pyplot as plt

def comment_analysis(comments):
    pos_num = 0
    neg_num = 0
    neu_num = 0
    total_sentiment = 0

    for comment in comments:
        blob = TextBlob(comment)
        sentiment_score = blob.sentiment.polarity
        if sentiment_score >= 0.2:
            print(f'\nPositive comment at {sentiment_score}: ' + comment)
            pos_num += 1
        elif sentiment_score <= -0.2:
            print(f'\nNegative comment at {sentiment_score}: ' + comment)
            neg_num += 1
        else:
            print(f'\nNeutral comment at {sentiment_score}: ' + comment)
            neu_num += 1
        total_sentiment += sentiment_score
    print(total_sentiment/len(comments))
    generate_bar(neg_num, neu_num, pos_num)


def generate_bar(neg, neu, pos):
    # Create a list of labels for the x-axis
    labels = ['Positive', 'Neutral', 'Negative']

    # Create a list of the data to plot
    data = [pos, neu, neg]

    # Create a list of colors to use for each bar
    colors = ['green', 'grey', 'red']

    # Create the bar chart
    plt.bar(labels, data, color=colors)

    # Add a title and y-axis label
    plt.title('Comment Sentiment Analysis')
    plt.ylabel('Percentage')

    # Display the chart
    plt.show()