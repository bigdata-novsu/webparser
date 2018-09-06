import math

# calculate term frequency in single document
def tf(word, blob):
    return (float)(blob.words.count(word)) / (float)(len(blob.words))

# count of occurrences of word in the corpus of documents (bloblist)
def n_containing(word, bloblist):
    return (float)(sum(1 for blob in bloblist if word in blob))

# calculate inverse document frequency by using all documents
def idf(word, bloblist):
    res = (float)(math.log(len(bloblist) / (1 + n_containing(word, bloblist))))
    if res < 0:
        return 0.01
    else:
        return res

# calculate tf-idf
def tfidf(word, blob, bloblist):
    return (float)(tf(word, blob)) * (float)(idf(word, bloblist))

# calculate score tf-idf ащк the corpus of documents (bloblist)
def score(bloblist):
    result = {}
    for i, blob in enumerate(bloblist):
        document_tfidf = {}
        scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:]:
            document_tfidf[word] = round(score, 5)
            result["Top words in document {}".format(i + 1)] = document_tfidf
    return result