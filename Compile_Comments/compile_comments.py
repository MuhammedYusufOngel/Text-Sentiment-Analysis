from os import system
import pandas as pd
from sklearn.utils import shuffle

system("CLS")

#We read comments.csv. With delimiter, we create new column
data = pd.read_csv("../Get_Comment/comments.csv",encoding="iso-8859-1",delimiter="\t")

#We round up comments with a score of 4 to 5, and comments with a score of 2 to 1.
data.loc[data['Puan'] == "4", 'Puan'] = 5
data.loc[data['Puan'] == "2", 'Puan'] = 1

#We create new data frame for 5 and 1
dataFrame5 = data[data.Puan == "5"]
dataFrame1 = data[data.Puan == "1"]

#We concat dataFrame5 and dataFrame1 with concat command. We ignore old index with ignore_index=true
df = pd.concat([dataFrame1, dataFrame5], ignore_index=True)

#Shuffle
df = shuffle(df)
print(df)

#We save comments_final.csv. Sep means almost same with delimiter. With index=False, the program don't add index to table.
df.to_csv('comments_final.csv', sep="\t", encoding="iso-8859-1", index=False)
