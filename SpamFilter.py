"""
Spam Filter program

@author: Suchith kumar
"""

import  os


vocabulary=[]
Prob_of_Spam=0.0
Prob_of_nospam=0.0
spam_prob_dict={}
nospam_prob_dict={}
total_files=0
spam_files=0
nospam_files=0


def Text(path_dir):
     global total_files
     count=0
     for filename in os.listdir(path_dir):
            total_files=total_files+1
            count=count+1
            with open(os.path.join(path_dir, filename)) as fh:
                        contents = fh.read()                
                 
        # extract the words from the document
     features = extract_features(contents)
     return features,count

def extract_features(s, min_len=2, max_len=20):
    """
    Extract all the words in the string ``s`` that have a length within
    the specified bounds
    """
    words = []
    for w in s.lower().split():
        wlen = len(w)
        if wlen > min_len and wlen < max_len:
            words.append(w)
    return words

def probability(Text_doc):     
    words_distinct=[]
    for wrd in Text_doc:
        if not wrd in words_distinct:
            words_distinct.append(wrd)
            
    n = len(words_distinct)
    vocab=len(vocabulary)
    prob_dict={}
    for word in vocabulary:
        nk=Text_doc.count(word)
        prob = float(nk+1)/(n+vocab)
        prob_dict[word]=prob
    
    return prob_dict

def train(trainingData='Train'):
        curdir = os.path.dirname(__file__)
        global spam_files,nospam_files,Prob_of_Spam,Prob_of_nospam,spam_prob_dict,nospam_prob_dict
        # paths to spam and ham documents
        spam_dir = os.path.join(curdir, trainingData, 'spam')
        nospam_dir = os.path.join(curdir, trainingData, 'nospam')
        Text_spam,spam_files=Text(spam_dir)
        Text_nospam,nospam_files= Text(nospam_dir)

        for doctext in (Text_spam,Text_nospam):
                for word in doctext:
                        if not word in vocabulary:
                                vocabulary.append(word)    
        
        n_spam=len(Text_spam)
        n_nospam=len(Text_nospam)
        
        Prob_of_Spam = float(spam_files)/total_files
        Prob_of_nospam = float(nospam_files)/total_files
        
        spam_prob_dict=probability(Text_spam)
        nospam_prob_dict=probability(Text_nospam)
        

def classify(testData='Test'):
    curdir = os.path.dirname(__file__)
    
    test_dir=os.path.join(curdir,testData)
    
    for filename in os.listdir(test_dir):
        with open(os.path.join(test_dir, filename)) as fh:
            contents = fh.read()
            
    features = extract_features(contents)
    vocab_before = len(vocabulary)
        
    for word in features:
        if not word in vocabulary:
            vocabulary.append(word)
    
    vocab_after=len(vocabulary)
    
    if vocab_after>vocab_before :
        train()
    
    spam_classify=1.0
    nospam_classify=1.0
    
    for word in features:
        if word in vocabulary:
            spam_classify=spam_classify*spam_prob_dict[word]
            nospam_classify= nospam_classify * nospam_prob_dict[word]
    
    spam_classify = spam_classify * Prob_of_Spam
    nospam_classify = nospam_classify * Prob_of_nospam
    
    val = max(spam_classify,nospam_classify)
    
    if val == spam_classify:
        print("Spam Content")
    else :
        print("Not a Spam Content")
    print(test_dir,"hello")

               
if __name__ == '__main__':
        train()
        print("Outputs",vocabulary,"\n",total_files,spam_files,nospam_files,Prob_of_Spam)
        print(spam_prob_dict)
        classify()
