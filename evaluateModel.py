import pandas as pd
from google.cloud import translate_v2 as translate
from sacrebleu.metrics import BLEU
from bert_score import BERTScorer
import logging
import transformers


transformers.tokenization_utils.logger.setLevel(logging.ERROR)
transformers.configuration_utils.logger.setLevel(logging.ERROR)
transformers.modeling_utils.logger.setLevel(logging.ERROR)

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

google_list = []
microsoft_list = []
hyp_list1 = []
hyp_list2 = []

print("Creating lists...")
x = 0
while x != len(df.index):
    aString = df.loc[x, 'Reference Translation: Google Translation']
    google_list.append(str(aString))
    bString = df.loc[x, 'Reference Translation: Microsoft Translation']
    microsoft_list.append(str(bString))
    cString = df.loc[x, 'Translated Tweet: M2M-100 model']
    hyp_list1.append(str(cString))
    dString = df.loc[x, 'Translated Tweet: MarianMT model']
    hyp_list2.append(str(dString))
    x = x + 1

ref_list = [google_list, microsoft_list]
print("Lists created.")

'''Evaluating BLEU score'''
print("Calculating BLEU score...")
bleu = BLEU()
BLEU_result_model1 = bleu.corpus_score(hyp_list1, ref_list)
BLEU_result_model2 = bleu.corpus_score(hyp_list2, ref_list)
print("M2M-100 Model BLEU score: ", BLEU_result_model1)
print("MarianMT Model BLEU score: ", BLEU_result_model2)

'''Evaluating BERT score'''
print("Calculating BERT score...")
MODEL_NAME = "microsoft/deberta-xlarge-mnli"
scorer = BERTScorer(model_type=MODEL_NAME, lang="en", rescale_with_baseline=True)
P, R, F1 = scorer.score(hyp_list1, ref_list)
BERT_result_model1 = F1.mean()
P, R, F1 = scorer.score(hyp_list2, ref_list)
BERT_result_model2 = F1.mean()
print("M2M-100 Model BERT score: ", BERT_result_model1)
print("MarianMT Model BERT score: ", BERT_result_model2)