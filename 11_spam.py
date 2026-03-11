# Tiny spam detector without help of ML purely code logic

"""
Plan - 
1. read tiny data, count word frequncy
2. group frequency in 2 parts spam and not spam, here required python logic
3. for new sentence, calcu;ate spamword - notspam
4. set threshold and return output
"""

#data
messages = [
("Win a free iPhone now", "spam"),
("Meeting at 5 pm", "ham"),
("Claim your lottery prize", "spam"),
("Let's have lunch tomorrow", "ham"),
("Free money offer", "spam"),
("Project deadline tomorrow", "ham")
]

import collections

spam = collections.Counter()
ham = collections.Counter()

for mes, label in messages:
    words = mes.lower().split()
    if label == "spam":
        spam.update(words)
    elif label == "ham":
        ham.update(words)

myStr = "Free money offer"
myStr1 = "Tommarow is my office"

def predict(sentence, spam, ham):
    new_words = sentence.lower().split()
    spam_score, ham_score = 0,0
    for word in new_words:
        spam_score += spam[word]
        ham_score += ham[word]

    threshold = spam_score - ham_score

    if threshold>0:
        print(f"{sentence} is likely spam")
    else:
        print(f"{sentence} is not likey spam")

predict(myStr,spam,ham)
predict(myStr1,spam,ham)
