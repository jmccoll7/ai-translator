#!/usr/bin/env python
# coding: utf-8

# In[1]:


my_apikeyS2T = 'redacted'


# In[2]:


myurl = "redacted"


# In[3]:


import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(my_apikeyS2T)
speech_to_text = SpeechToTextV1(authenticator=authenticator)

speech_to_text.set_service_url(myurl)


with open('fried_chicken.mp3', 'rb') as audio_file:
    speech_recognition_results = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/mp3',
        word_alternatives_threshold=0.9,
        keywords=['fried','chicken'],
        keywords_threshold=0.5
    ).get_result()
print(json.dumps(speech_recognition_results, indent=2))


# In[40]:


transcript = speech_recognition_results['results'][0]['alternatives'][0]['transcript']

my_apikeyT2T = 'redacted'


# In[4]:


T2Turl = 'redacted'


# In[8]:


import json
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(my_apikeyT2T)
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)

language_translator.set_service_url(T2Turl)


# In[42]:


translation = language_translator.translate(
    text=transcript,
    model_id='en-fr').get_result()
print(json.dumps(translation, indent=2, ensure_ascii=False))


# In[49]:


new_translation = translation['translations'][0]['translation']

my_apikeyT2S = 'redacted'


# In[50]:


T2Surl = 'redacted'


# In[51]:


from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(my_apikeyT2S)
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)

text_to_speech.set_service_url(T2Surl)


# In[52]:


with open('translation.wav', 'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize(
            new_translation,
            voice='en-US_AllisonVoice',
            accept='audio/wav'
        ).get_result().content
    )


# In[53]:


import IPython.display as ipd


# In[54]:


ipd.Audio('translation.wav', autoplay=True)


# In[ ]:




