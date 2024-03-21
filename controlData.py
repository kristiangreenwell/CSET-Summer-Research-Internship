from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError
import pandas as pd
from google.cloud import translate_v2 as translate


pf = input("A. Andres Manuel - President of Mexico "
           "\nB. Sergio Ramos - Football Player  "
           "\nC. Bad Bunny - Musical Artist "
           "\nFrom the list above, Please select the tweets from the desired public figure: ")

file = {
    "A": "TwitterDataManuel.csv",
    "B": "TwitterDataRamos.csv",
    "C": "TwitterDataBunny.csv"
}

df = pd.read_csv(file[pf])

''' This section of code was used to edit the csv files above by adding/renaming columns.
It is omitted to prevent re-editing.
df.insert(3, "Reference Translation: Google Translation", '', True)
df.to_csv(file[pf], index=False)
'''

translate_client = translate.Client()

for i, x in enumerate(df.index):
    oString = str(df.loc[x, 'Preprocessed'])
    print("Translating...", x)
    oString = translate_client.translate(oString, target_language="en")
    df.loc[x, 'Reference Translation: Google Translation'] = oString["translatedText"]
    print("Translated...", x)
    df.to_csv(file[pf], index=False)

''' This section of code was used to edit the csv files above by adding/renaming columns.
It is omitted to prevent re-editing.
df.insert(4, "Reference Translation: Microsoft Translation", '', True)
df.to_csv(file[pf], index=False)
'''

# set `<your-key>`, `<your-endpoint>`, and  `<region>` variables with the values from the Azure portal
key = "87bfc84aaf1f434097e6e43600c83d9e"
endpoint = "https://twitter-translation.cognitiveservices.azure.com/"
region = "eastus"

credential = TranslatorCredential(key, region)
text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)

for i, x in enumerate(df.index):
    oString = str(df.loc[x, "Preprocessed"])
    try:
        source_language = "es"
        target_languages = ["en"]
        input_text_elements = [ InputTextItem(text = oString) ]

        response = text_translator.translate(content = input_text_elements, to = target_languages, from_parameter = source_language)
        translation = response[0] if response else None

        if translation:
            for translated_text in translation.translations:
                oString = translated_text.text

        df.loc[x, "Reference Translation: Microsoft Translation"] = str(oString)
        df.to_csv(file[pf], index=False)
    except HttpResponseError as exception:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")

