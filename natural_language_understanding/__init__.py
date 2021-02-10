from api import keys, urls
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features
from ibm_watson.natural_language_understanding_v1 import SentimentOptions
from ibm_watson.natural_language_understanding_v1 import KeywordsOptions
from ibm_watson.natural_language_understanding_v1 import EntitiesOptions
from ibm_watson.natural_language_understanding_v1 import CategoriesOptions


def fetch_watson_and_return_sentiment_label(text: str):
    '''Fetches Watson's Natural Language Understanding API and returns the sentiment label'''
    
    # Authenticating the Watson service with personal key and url
    authenticator = IAMAuthenticator(keys.nlu_key)
    nlu = NaturalLanguageUnderstandingV1(version='2018-11-16', authenticator=authenticator)
    nlu.set_service_url(urls.nlu_url)

    # Setting what features we want to extract from a phrase
    features = Features(
        keywords=KeywordsOptions(),
        sentiment=SentimentOptions(),
        entities=EntitiesOptions(),
        categories=CategoriesOptions()
    )

    # Getting the result and returning the sentiment label
    result = nlu.analyze(text=text, features=features).get_result()

    return result['sentiment']['document']['label']
