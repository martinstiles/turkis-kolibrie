from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import os
import pickle as pickle

show = False  # print the texts together with the keywords for each text

stopwords = None

# create list of stopwords
f = open("/Users/akjen/Documents/NTNU/EiT/turkis-kolibrie/creation_of_dictionary/ordbokdata/stopwords/stopwords.txt", 'r')
line = f.read().replace('\n', ' ')
line = ''.join([i for i in line if not i.isdigit()])
line = line.lower()
line = line.replace("  ", " ")
stopwords = line.split(" ")
f.close()

docs = {}

# read all texts from the nrk valgomat
path = "/Users/akjen/Documents/NTNU/EiT/turkis-kolibrie/creation_of_dictionary/ordbokdata/valgomat/"
files = os.listdir(path)
for file in files:
    f=open(os.path.join(path,file), 'r')
    line = f.read()
    line = line.replace('\n', '')
    line = ''.join([i for i in line if not i.isdigit()])
    line = line.lower()
    key = file.split(".")[0]
    docs[key] = line
    f.close()

#create a vocabulary of words,
#ignore words that appear in 85% of documents,
#eliminate stop words
cv = CountVectorizer(max_df=0.85, stop_words=stopwords)
word_count_vector=cv.fit_transform(docs.values())


tfidf_transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count_vector)

feature_names=cv.get_feature_names()

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    #use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    for idx, score in sorted_items:
        fname = feature_names[idx]

        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]

    return results

dictionary = {}

for key in docs.keys():
    doc = docs[key]
    #generate tf-idf for the given document
    tf_idf_vector=tfidf_transformer.transform(cv.transform([doc]))

    #sort the tf-idf vectors by descending order of scores
    sorted_items=sort_coo(tf_idf_vector.tocoo())

    #extract only the top n; n here is 10
    keywords=extract_topn_from_vector(feature_names,sorted_items, 10)
    dictionary[key] = list(keywords.keys())
    if show:
        # now print the results
        print("\n=====Title=====")
        print(key)
        print("\n=====Body=====")
        print(doc)
        print("\n===Keywords===")
        for k in keywords:
            print(k, keywords[k])

if not os.path.exists('ordbokdata/ordbok/'):
    os.makedirs('ordbokdata/ordbok/')
with open('ordbokdata/ordbok/ordbok.pickle', 'wb') as file:
    pickle.dump(dictionary, file) # use `pickle.loads` to do the reverse
with open('ordbokdata/ordbok/ordbok.pickle', 'rb') as handle:
    dictionary = pickle.load(handle)

print(dictionary)
