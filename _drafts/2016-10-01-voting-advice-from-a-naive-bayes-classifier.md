---
layout: post
title: "Voting advice from a Naive Bayes classifier"
description: "the prior decides"
category: programming
tags: [python, sklearn]
---
{% include JB/setup %}

This November in addition to voting for President and Senator<sup>[1](#myfootnote1)</sup> I have the opportunity to vote on 17 propositions to add or remove text to California's constitution. To aid in my decision, I was mailed a 222 page phone book containing the proposed laws and printed exchanges between the for and against parties. But I'm a physicist, not a lawyer, and I don't have time to read and understand the arguments <sup>[2](#myfootnote2)</sup>. I do have the ability to program and read undergraduate textbooks on data mining, so let's do that instead!

The idea is this: pick four propositions that I have strong opinions on (2 for and 2 against) and use them to build a Multinomial Naive Bayes classifier using the word counts of the proposition's text and arguments, then use this model to predict my opinions on the propositions for which I don't have strong opinions. 

The code for this project is available on [github](https://github.com/CatherineH/prop-predict).

Implementation
==============

First, download the html files on the California Secretary of State voterguide into a folder called **data/raw_html** using a python library that reproduces the functionality of [wget](https://pypi.python.org/pypi/wget)<sup>[3](#myfootnote3)</sup>:

```python
if not isdir(raw_html_folder):
    mkdir(raw_html_folder)
# download the text from the sos voterguide
for prop in propositions:
    for page in pages:
        url = join(sos_url, str(prop), page)
        html_page = join(raw_html_folder, str(prop)+"_"+page)
        if not isfile(html_page):
            print(url, html_page)
            filename = download(url)
            sleep(1)
            rename(join(current_directory, filename),
                   join(current_directory, html_page))
```

My strong opinions are stored as a dict:

```python
# propositions for which I have opinions. 0 is against, 1 is for
opinions = {56: 0, 60: 0, 62: 1, 64: 1}
```
For reference, this means:

$STRONG_OPINIONS$


I used [scikit-learn](https://pypi.python.org/pypi/scikit-learn/0.18) to vectorize the text and create the model. I created scikit-learn **Bunch** objects, then loaded the raw text of the html file into a *known* or *unknown* Bunch depending on whether it was present in my strong opinions<sup>[4](#myfootnote4)</sup>.

```python
prop_texts_known = Bunch()
prop_texts_known.data = []
prop_texts_known.target_names = ['against', 'for']
prop_texts_known.target = []
prop_texts_unknown = Bunch()
prop_texts_unknown.data = []
prop_texts_unknown.target_names = ['against', 'for']
for file in listdir(raw_html_folder):
    prop_number = int(file.split("_")[0])
    html_page = join(raw_html_folder, file)

    if prop_number in opinions.keys():
        prop_texts_known.data.append(open(html_page, "r").read(-1))
        prop_texts_known.target.append(opinions[prop_number])
    else:
        prop_texts_unknown.data.append(open(html_page, "r").read(-1))
```

Next, I created count vectors on the proposition texts with strong opinions, trained a Multinomial Naive Bayes model on the counts, created count vectors of the unknown propositions, and used the unknown count vectors to make predictions about whether the texts belonged to the for or against categories<sup>[5](#myfootnote5)</sup>. I didn't scale the counts based on frequency. The texts are about half html, and I worried that by scaling to frequency, the noise (i.e, the html tags and styling common to all documents) would have too much weight.  

```python
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(prop_texts_known.data)
clf = MultinomialNB().fit(X_train_counts, prop_texts_known.target)

X_new_counts = count_vect.transform(prop_texts_unknown.data)
predicted = clf.predict(X_new_counts)
```


```python

_sos_parser = SOSParser()
```



 

Results
=======

$RESULT_TABLE$

Most positive words:

1 marijuana
2 murder
3 penalty
4 prison
5 death
6 nonmedical
7 inmates
8 sentence
9 victims
10 system

they are all related to legalizing marijuana or the death penalty.

The most negative words:

10 diseases
9 condoms
8 films
7 mdash
6 workplace
5 cigarette
4 cigarettes
3 performers
2 film
1 8208

8208 and mdash are the ascii character codes for the em-dash. It appears in propositions 52-59 used that, but not in propositions 60-67.


<a name="myfootnote1">1</a>: which isn't much of a vote; Clinton will win California unless the San Andreas fault opens up and dumps LA, San Francisco and San Diego into the Pacific, and both candidates for Senate are democrats

<a name="myfootnote2">2</a>: only half-true: I don't have time to read it, but I probably still will because I'm a nerd.

<a name="myfootnote3">3</a>: This is not the best implementation; first, *download* has a parameter called *output* that lets you set the output file name, rendering the call to *rename* irrelevant. Secondly, I should have checked to make sure the file had finished downloading. But the first iteration worked and I don't want to spam the SoS to test the optimal form of this code.

<a name="myfootnote4">4</a>: I don't think scikit-learn requires data to be contained within Bunches; that was simply the object the sample datasets were packaged in, so I decided to use it as well.

<a name="myfootnote5">5</a>: If these variable names look familiar, it's because I'm working off of [a scikit-learn tutorial](http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html)

