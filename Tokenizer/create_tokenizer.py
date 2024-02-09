import os, sys

from keras.preprocessing.text import Tokenizer
import numpy as np
import pandas as pd
from itertools import islice
from os import system


system("CLS")

#This function allows you to get up to the index you want in the list.
def take(n, iterable):
    return islice(iterable, n)

#We open comments_final.csv
dataframe = pd.read_csv("../Compile_Comments/comments_final.csv", encoding="iso-8859-9", delimiter="\t")

target = dataframe['Puan'].values.tolist()
data = dataframe['Yorum'].values

#With these codes, NaN characters in comments will be cleared.
df = pd.DataFrame(data, columns=['Yorum'])
df_cleaned = df.dropna()
cleaned_data = df_cleaned['Yorum'].tolist()

#num_words = Returns words that repeat as many times as you type.
#filters = Does not receive typed characters
#lower = Converts all letters of words to lowercase
#split = Defines the division character
#char_level = determines whether each word is a token (with false, each word is a token)
#oov_token = Specifies how words that are not in the dictionary should be set
#analyzer = Checks whether you want to analyze within the text or not
tokenizer = Tokenizer(
    num_words=None,
    filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
    lower=True,
    split=' ',
    char_level=False,
    oov_token=None,
    analyzer=None
)

#Words are converted to index
tokenizer.fit_on_texts(cleaned_data)

#It takes the first 10000 words.
n_items = take(10000, tokenizer.word_index.items())
print(str(dict(n_items)))

