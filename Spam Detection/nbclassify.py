import os
import sys
import fnmatch
import itertools
import math

def filesearch(directory='.', ext=''):
    found = []
    for root, dirnames, files in os.walk(directory):
        for fil1 in fnmatch.filter(files, ext):
            found.append(os.path.join(root, fil1))
    return found

def classify_email(example_file,word_spam_prob,word_ham_prob,prob_spam,prob_ham,nham,nspam,totalvocab):     
    doc = open(example_file, "r", encoding="latin1")
    lines = doc.readlines()
    for readline in lines:
    #         print("line is,",readline)
            prodspam = 0
            prodham = 0
            for word in readline.split(" "):
                try:
                    prodspam+= math.log(float(word_spam_prob[word]))
                except KeyError: 

                    prodspam+= 1/(nspam+totalvocab)
                    pass
                try:
                    prodham+= math.log(float(word_ham_prob[word]))
                except KeyError: #this means we didn't find the word
    #                 prodham*=0
                    prodham+= 1/(nham+totalvocab)
                    continue
    if(prodham==1): 
        prodham = 0
    if(prodspam==1):
        prodspam = 0

    sp = math.fabs(math.log(prob_spam)+prodspam)
    ha = math.fabs(math.log(prob_ham)+prodham)
    if(sp>ha): 
        res = "spam"
    if(sp<ha): 
        res = "ham"
        
    return res
        
def splitdic(d,n):
    i = iter(d.items())
    d1 = dict(itertools.islice(i, n))   # grab first n items
    d2 = dict(i)                        # grab the rest

    return d1, d2
        
    
def main():

    dir_path = os.getcwd()
    read = open("nbmodel.txt","r+")
    fl = read.readlines()
    hunique = int(fl[0])
    sunique = int(fl[1])
    nham = int(fl[2])
    nspam = int(fl[3])
    prob_ham = float(fl[4])
    prob_spam = float(fl[5])
    spamcondprob = dict()
    hamcondprob = dict()
    mydata = dict()
    with open("nbmodel.txt") as raw_data:
        for item in raw_data:
            if ':' in item:
                
                key,value = item.split(':', 1)
                value = value.replace("\n","")
                mydata[key]= value
            else:
                pass
    read.close()

    spamcondprob, hamcondprob = splitdic(mydata,sunique)
    nospam = 0
    noham = 0

    totalvocab = hunique+sunique
    out = open("nboutput.txt","w+")
    txtfiles = filesearch(directory=sys.argv[1], ext="*.txt")
    nofiles = 0
    
    for file in txtfiles:
        try:
            if(file.endswith("txt")):
                res = classify_email(file,spamcondprob,hamcondprob,prob_spam,prob_ham,nham,nspam,totalvocab)
                nofiles+=1
                if(res=="spam"): 
                    nospam+=1
                if(res=="ham"): 
                    noham+=1
                out = open("nboutput.txt","a+")
                out.write(str(res)+"\t"+file+"\n")
                #print(res," ",file)
                #out.write("\n"+str(res)+" "+os.path.join(root, file))
        except KeyError:
            continue
   
    
                
        
if __name__ == '__main__':
    main()