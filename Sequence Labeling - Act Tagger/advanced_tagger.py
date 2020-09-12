import csv
import pycrfsuite
import os
import sys

from hw2_corpus_tool import get_data, get_utterances_from_filename, get_utterances_from_file


def get_token_features_advcd(pos):
    features = []
    if(pos==None):
        features.append("NO_WORDS")
    else:
        features.append("FTOKEN_"+pos[0][0])
        features.append("FPOS_"+pos[0][1])
        [[features.extend(["TOKEN_"+postag[0].lower(),postag[1]])] for postag in pos[1:]]
    return features

def get_first_utterance(line):
    return line[0][1]

def speaker_change(prev,curr):
    return not(prev==curr) 

def extract_features_advcd(convo):
    features_list = []
    labels = []
    prevspeaker = convo[0][1] 
    token1 = get_token_features_advcd(convo[0][2])
    token1.append("FIRST_UTTER")
    features_list.append(token1)
    labels.append(convo[0][0])
    for utter in range(1,len(convo)):
        
        try:
            utter_label = convo[utter][0]
            token_features = get_token_features_advcd(convo[utter][2])
            prevchanged = speaker_change(prevspeaker,convo[utter][1])
            if(prevchanged==True): #then previous speaker is different
                token_features.append("SPEAKER_CHANGED")
                features_list.append(token_features)
                labels.append(utter_label)
            else: 
                features_list.append(token_features)
                labels.append(utter_label)
            prevspeaker = convo[utter][1]
        except IndexError:
            pass
    return features_list, labels


def main():

    convos = get_data(sys.argv[1])
    count=0
    feats=[]
    labels=[]
    x_data = []
    y_data = []
    ct=0
    for c in convos:
        myfeatures, mylabels = extract_features_advcd(c)
        x_data.append(myfeatures)
        y_data.append(mylabels)

    xtrain = x_data
    ytrain = y_data


    trainer = pycrfsuite.Trainer(verbose=False)
    for i in range(len(ytrain)):
        trainer.append(xtrain[i],ytrain[i])


    trainer.set_params({'c1': 1.0,   # coefficient for L1 penalty         
                         'c2': 1e-3,  # coefficient for L2 penalty         
                         'max_iterations': 50,  # stop earlier 
            # include transitions that are possible, but not observed         
                         'feature.possible_transitions': True}) 
    trainer.train('postagger.crfsuite')


    xtest=[]
    ytest=[]
    testconvos = get_data(sys.argv[2])
    for t in testconvos:
        tfeats, tlabels = extract_features_advcd(t)
        xtest.append(tfeats)
        ytest.append(tlabels)


    f = open(sys.argv[3],'w') #need to change to sys argument
    tagger = pycrfsuite.Tagger()
    tagger.open('postagger.crfsuite')
    count_true = 0
    count_false = 0
    for i in range(len(xtest)):
        pred = tagger.tag(xtest[i])
        corr = ytest[i]

        for j in range(len(pred)):
            a = (pred[j]==corr[j])
            if(a==False): count_false+=1
            if(a==True): count_true+=1  
            f.write(pred[j]+"\n")
            
        f.write("\n")
    total=count_true+count_false
    acc = count_true/total
    print("Accuracy of advanced:",acc)


if __name__ == "__main__":
    main()
