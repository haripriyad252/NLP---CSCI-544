import os
import math
import pickle
import fnmatch
import sys

def search_files(directory='.', extension=''):
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, extension):
            matches.append(os.path.join(root, filename))
    return matches


def preprocess(doc):
    lines = doc.readlines()
    for readline in lines:
        readline = readline.lower()
    return lines

def get_vocabcount(hamdic,files):
    #for file in os.listdir(os.getcwd()):
    for file in files:
        try:
            doc = open(file, "r", encoding="latin1")
        except FileNotFoundError:
            continue
        lines = preprocess(doc)
        for readline in lines:
            #print("line is",readline)
            for word in readline.split(" "):
                word = word.lower()
                word = word.replace("\n","")
                if word in hamdic:

                    c = hamdic[word]
                    hamdic.update({word:c+1})
                if word not in hamdic:
                    hamdic.update({word:1})
    return hamdic

def traverse_dict(dic,category):
    count_of_files = 0
    dir_path = os.getcwd()
    #dir_path = os.path.dirname(os.path.realpath(file))
    for dirpath, dirnames, filenames in os.walk(dir_path): 
        #print(dirnames)
        if(dirpath.endswith(category+".txt")):
            os.chdir(dirpath)
            dic = get_vocabcount(dic)
            for filename in os.listdir(os.getcwd()):
                doc = open(filename, "r", encoding="latin1")
                count_of_files+=1 
            break
    return dic, count_of_files

def count(dic): #gives total number of words in a category(non unique)
    vocab_count=0
    for e in dic:
        vocab_count = vocab_count + dic[e]
    return vocab_count

def get_condprob(dic,totalvocab):
    word_prob = dict()
    voc_count = count(dic) #num of unique words
    for e in dic:
        prob = float((dic[e]+1)/(voc_count+totalvocab))
        #print("num and denom",dic[e]+1,voc_count+totalvocab,"",prob)
        word_prob.update({e:prob})
    return word_prob


def main():

    hamdic = dict()
    spamdic = dict()

    txtfilesham = search_files(directory=sys.argv[1], extension="*.ham.txt")
    txtfilesspam = search_files(directory=sys.argv[1], extension="*.spam.txt")
    nham = len(txtfilesham)
    nspam = len(txtfilesspam)
    hamdic = get_vocabcount(hamdic,txtfilesham)
    spamdic = get_vocabcount(spamdic,txtfilesspam)

    hunique = len(hamdic)
    sunique = len(spamdic)
    total_vocab = hunique+sunique
    spam_condprob = get_condprob(spamdic,total_vocab)
    ham_condprob = get_condprob(hamdic,total_vocab)

    total = nham+nspam
    if(total!=0):
        prob_spam = nspam/(nspam+nham)
        prob_ham = nham/(nspam+nham)
    else:
        prob_spam = 0
        prob_ham = 0
        
    curr = os.getcwd()
    os.chdir(curr)
    out = open("nbmodel.txt","w")
    out.write(str(hunique))
    out.write("\n"+str(sunique))
    out.write("\n"+str(nham))
    out.write("\n"+str(nspam))
    out.write("\n"+str(prob_ham))
    out.write("\n"+str(prob_spam))
    #out.write("\n"+str(spam_condprob)) #length=sunique
    #out.write("\n"+str(ham_condprob)) #length=hunique
    out.write("\n")
    with open("nbmodel.txt", 'a+') as f:
        for key, value in spam_condprob.items():
            #f.write('%s:%s\n' % (key, value))
            try:
                f.write('%s:%s\n' % (key, value))
            except UnicodeEncodeError:
                continue
    counthamprob = 0
    with open("nbmodel.txt", 'a+') as f:
        for key, value in ham_condprob.items():
            #f.write('%s:%s\n' % (key, value))
            counthamprob+=1
            try:
                f.write('%s:%s\n' % (key, value))
            except UnicodeEncodeError:
                continue
    #print(ham_condprob)
    
if __name__ == '__main__':

    main()
