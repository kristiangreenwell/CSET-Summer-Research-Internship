import pandas as pd
from cleantext import clean
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Program Menu
print("Thank you for using Kristian's Twitter Text Translation.")
pf = input("A. Andres Manuel - President of Mexico "
           "\nB. Sergio Ramos - Football Player  "
           "\nC. Bad Bunny - Musical Artist "
           "\nFrom the list above, Please select the tweets from the desired public figure: ")

file= {
    "A": "TwitterDataManuel.csv",
    "B": "TwitterDataRamos.csv",
    "C": "TwitterDataBunny.csv"
}
df = pd.read_csv(file[pf])

''' This section of code was used to edit the csv files above by adding/renaming columns.
It is omitted to prevent re-editing.
df.rename(columns = {'Translated Tweet':'Translated Tweet: M2M-100 model'}, inplace = True)
df.insert(4, "Translated Tweet: MarianMT model", '', True)
'''

''' Cleaning and updating tweets'''
for i, x in enumerate(df.index):
    oString = df.loc[x, 'Original Tweet']
    # Hashtag
    oString = oString.replace("#", '')
    # Username
    oString = oString.replace('@', '')
    # URL
    oString = re.sub(r"http\S+", "", oString)
    # Emoji
    oString = clean(oString, no_emoji=True, fix_unicode=True)
    df.loc[x, 'Preprocessed'] = oString
    df.to_csv(file[pf], index=False)



# Access HuggingFace for Model
access_token ="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"

'''Import Language Model M2M-100'''
tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M", use_auth_token=access_token, src_lang='spa_Latn')
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M", use_auth_token=access_token)

for i, x in enumerate(df.index):
    oString = df.loc[x, 'Preprocessed']
    print("Translating...", x)
    inputs = tokenizer(oString, return_tensors="pt")
    translated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id['eng_Latn'], max_length=200)
    oString = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    df.loc[x, 'Translated Tweet: M2M-100 model'] = oString
    print("Translated...", x)
    df.to_csv(file[pf], index=False)


'''Import Language Model MarianMT'''
tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-es-en", use_auth_token=access_token)
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-es-en", use_auth_token=access_token)

for i, x in enumerate(df.index):
    oString = df.loc[x, 'Preprocessed']
    print("Translating...", x)
    batch = tokenizer(oString, return_tensors="pt")
    generated_ids = model.generate(**batch, max_length=512)
    oString = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    df.loc[x, 'Translated Tweet: MarianMT model'] = oString
    print("Translated...", x)
    df.to_csv(file[pf], index=False)

print("Translated COMPLETE.")
