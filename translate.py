from gettext import translation
from typing import Text
from urllib import response
from langdetect import detect
import requests, uuid, json



class Translate:
    

    def __detect_source(self, text):
        return detect(text)

    def translate(self,text,target):
        source = self.__detect_source(text)
        subscription_key = "ab29dc56f21f432f969c88500cd48e17"
        endpoint = "https://api.cognitive.microsofttranslator.com"

        location = "centralindia"
        path = '/translate'
        constructed_url = endpoint + path
        params = {
            'api-version': '3.0',
            'from': source.lower(),
            'to': [target]
                }
        headers = {
                'Ocp-Apim-Subscription-Key': subscription_key,
                'Ocp-Apim-Subscription-Region': location,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4())
                }


        body = [{
                'text': text
                }]

        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        #response = request.json()       
        #return json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
        response = request.json()[0]["translations"][0]
        conversion = response["text"]
        conversion_langage = response["to"]
        result = {"text" : conversion,
                  "to":conversion_langage}
        return json.dumps(result,ensure_ascii=False, separators=(',', ': '))