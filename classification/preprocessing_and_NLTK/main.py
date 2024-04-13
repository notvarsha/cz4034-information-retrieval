import nltk
import pandas as pd
import re
import nltk
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

def main():
    # Main entry point
    # Load the amazon review dataset
    data = pd.read_csv('combined_excel_dataset.csv')

    # Remove duplicates before pre-processing
    data = data.drop_duplicates(subset='Post Comments', keep="first")

    # apply the function data
    data['PostCommentsPostProcessed'] = data['Post Comments'].apply(preprocess_text)

    # apply the get_compoundscore function
    data['Compound_Score'] = data['PostCommentsPostProcessed'].apply(get_compoundscore)

    # apply get_sentiment function
    data['NLTK_Sentiment'] = data['PostCommentsPostProcessed'].apply(get_sentiment)
    data.to_csv('final_result.csv')

    # use only the rows with valid ManuallyLabeledSentiments for evaluation
    data_eval = data.dropna(subset=['ManuallyLabeledSentiments'])

    # evaluation of performance with confusion matrix
    print(confusion_matrix(data_eval['ManuallyLabeledSentiments'], data_eval['NLTK_Sentiment']))
    # classification report
    print(classification_report(data_eval['ManuallyLabeledSentiments'], data_eval['NLTK_Sentiment']))

    print(data)

def preprocess_text(text_data):
    
    #convert the entire text_data into string for easy data formating and analysis
    text_data = str(text_data)
    #print('This is the text_data: ', text_data)

    # Remove punctuations the text_data
    text_without_punc = text_data.translate(str.maketrans('','', string.punctuation))

    # Remove links
    text_without_links = re.sub(r'https?://\S+|www\.\S+', '', text_without_punc)

    # Tokenize the text_data
    tokens = word_tokenize(text_without_links.lower())
    #print('This is the tokens: ', tokens)

    # Remove the stop words in the text
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    #print('This is the filtered tokens: ', filtered_tokens)

    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    #print('This is the lemmantized tokens: ', lemmatized_tokens)

    # Join the tokens back into a string
    post_processed_text_data = ' '.join(lemmatized_tokens)
    #print('This is the processed text_data: ', post_processed_text_data)
    return post_processed_text_data

# get compound scores function
def get_compoundscore(text_data):
    sentiment_analyzer = SentimentIntensityAnalyzer()

    scores = sentiment_analyzer.polarity_scores(text_data)
    compoundscore = scores['compound']
    return compoundscore

# get_sentiment function
def get_sentiment(text_data):
    sentiment_analyzer = SentimentIntensityAnalyzer()

    scores = sentiment_analyzer.polarity_scores(text_data)
    if (scores['compound'] >= 0.05):
        sentiment = 1
    elif (scores['compound'] <= -0.05):
        sentiment = -1
    else:
        sentiment = 0

    return sentiment

if __name__ == "__main__":
    # This is executed when run from the command line
    main()
