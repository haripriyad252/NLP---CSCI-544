def labelsearch(path):
    if "spam" in path:
        return "SPAM"
    if "ham" in path:
        return "HAM"

def main():
    print("In main of evaluate!")
    corrclass =0
    corrspam = 0
    corrham = 0
    classspam = 0
    classham = 0
    actualspam = 0
    actualham = 0
    comparelist = []
    fl = open("nboutput.txt","r+")
    lines = fl.readlines()
    for line in lines:
        res, path = line.split(" ")
        true_label = labelsearch(path)
        comparelist.append[res,true_label]
    print(comparelist)
    
    tot = len(comparelist)
    for item in comparelist:
        if(item[0]=="spam"):
            classspam+=1
            if(item[1]=="spam"):
                corrspam+=1
                actualspam+=1
                continue
            if(item[1]=="ham"):
                actualham+=1
                continue
            
        if(item[0]=="ham"):
            classham+=1
            if(item[1]=="ham"):
                corrham+=1
                actualham+=1
                continue
            if(item[1]=="ham"):
                actualspam+=1
                continue
                
    print("Spam")
    prec_spam = corrspam/classspam
    rec_spam = corrspam/actualspam
    f_spam = (2*prec_spam*rec_spam)/(prec_spam+rec_spam)
    print("\n",prec_spam,"\t",rec_spam,"\t",f_spam)
    print("Ham")
    prec_ham = corrham/classham
    rec_ham = corrham/actualham
    f_ham = (2*prec_ham*rec_ham)/(prec_ham+rec_ham)
    print("\n",prec_spam,"\t",rec_spam,"\t",f_spam)
    taccuracy = corrspam+corrham/(actualspam+actualham)
    print("\n Total Accuracy:",taccuracy)
    
    
if __name__ == '__main__':
    main()