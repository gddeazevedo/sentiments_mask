import keys
import urls
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features
from ibm_watson.natural_language_understanding_v1 import SentimentOptions
from ibm_watson.natural_language_understanding_v1 import KeywordsOptions
from ibm_watson.natural_language_understanding_v1 import EntitiesOptions
from ibm_watson.natural_language_understanding_v1 import CategoriesOptions


authenticator = IAMAuthenticator(keys.nlu_key)

nlu = NaturalLanguageUnderstandingV1(version='2018-11-16', authenticator=authenticator)

nlu.set_service_url(urls.nlu_url)

text = input('Digite algo: ')


# it's an object and each one of its parameters are an attribute of it
features = Features(
    keywords=KeywordsOptions(),
    sentiment=SentimentOptions(),
    entities=EntitiesOptions(),
    categories=CategoriesOptions()
)


result = nlu.analyze(text=text, features=features).get_result()
print(result['sentiment'])
