from math import log
import nltk
import sys
import getopt
from nltk import ngrams

def build_LM(in_file):
    #These lists hold all strings in each languages
    indo= []
    malay= []
    tamil= []
    vocabulary = []
    # we initiate all values of count to 0
    indoCount=0
    malayCount=0
    tamilCount=0
    vocCount=0
     # These are lists which will hold the 4-grams
    indoFourGram=[]
    malayFourGram=[]
    tamilFourGram=[]
    vocFourGram=[]
    # These are the dictionnaries which will hold the pair 4-gram: frequency
    indoDict= {}
    malayDict= {}
    tamilDict = {}

    print("building language models...")
    #we parse the training file to get all strings of different languages
    with open(in_file) as f:
        for line in f:
            current = line.split(' ',1)
            if current[0] == 'indonesian':
                indo+=current[1].strip()
                vocabulary+=current[1].strip()
            if current[0] == 'malaysian':
                malay+=current[1].strip()
                vocabulary+=current[1].strip()
            if current[0] == 'tamil':
                tamil +=current[1].strip()
                vocabulary+=current[1].strip()
    f.close()

    #we now create the four-grams for each languages as well as the overall vocabulary        
    indoFourGram=list(ngrams(indo,4))
    malayFourGram=list(ngrams(malay,4))
    tamilFourGram=list(ngrams(tamil,4))
    vocFourGram=list(ngrams(vocabulary,4))

    #this is the count of 4-grams in each language
    indoCount=len(indoFourGram)
    malayCount=len(malayFourGram)
    tamilCount=len(tamilFourGram)
    vocCount=len(vocFourGram)

    #we now buil the dictionaries for each languages
    for i in indoFourGram:
        if i in indoDict:
            freq = indoDict.get(i) + 1
            indoDict.update({i:freq})
        else:
            indoDict.update({i:1})

    for i in malayFourGram:
        if i in malayDict:
            freq = malayDict.get(i) + 1
            malayDict.update({i:freq})
        else:
            malayDict.update({i:1})    

    for i in tamilFourGram:
        if i in tamilDict:
            freq = tamilDict.get(i) + 1
            tamilDict.update({i:freq})
        else:
            tamilDict.update({i:1})   
    # one-smoothing
    for i in vocFourGram:
        if i not in indoDict:
            indoDict.update({i:0})
        if i not in malayDict :
            malayDict.update({i:0})
        if i not in tamilDict:
            tamilDict.update({i:0})
            
    #we update the frequency to the log value to facilitate later estimations
    for i in indoDict:
        freq = indoDict.get(i) + 1
        ratio = freq/(indoCount+vocCount)
        freq = log(ratio,10)
        indoDict.update({i:freq})
    for i in malayDict:
        freq = malayDict.get(i) + 1
        ratio = freq/(malayCount+vocCount)
        freq = log(ratio,10)
        malayDict.update({i:freq})
    for i in tamilDict:
        freq = tamilDict.get(i) + 1
        ratio = freq/(tamilCount+vocCount)
        freq = log(ratio,10)
        tamilDict.update({i:freq})

    print('done building models')
    #we return a list of dictionnaries
    return([indoDict,malayDict,tamilDict])

def test_LM(in_file, out_file, LM):
    print("testing language models...")
    # we extract each of the 3 language models
    ILM = LM[0]
    MLM = LM[1]
    TLM = LM[2]
    input = open(in_file)
    output = open(out_file,'a')
    for line in input:
        indoFreq = 0
        malayFreq = 0
        tamilFreq = 0
        current = list(ngrams(line,4))
        
        #because we are using the log values, we can add each frequency
        for i in current:
            if i in ILM:
                indoFreq+=ILM.get(i)
            if i in MLM:
                malayFreq+=MLM.get(i)
            if i in TLM:
                tamilFreq+=TLM.get(i)

        #if the frequency is equal over all languages, we output other
        if(indoFreq==malayFreq==tamilFreq):
            output.write('other '+line)
        # else, we ouput the language with maximal frequency
        elif max([indoFreq,malayFreq,tamilFreq])==indoFreq:
            output.write('indonesian '+line)
        elif max([indoFreq,malayFreq,tamilFreq])==malayFreq:
            output.write('malaysian '+line)
        elif max([indoFreq,malayFreq,tamilFreq])==tamilFreq:
            output.write('tamil '+line)

    input.close()
    output.close()

def usage():
    print("usage: "
        + sys.argv[0]
        + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"
    )


input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], "b:t:o:")
except getopt.GetoptError:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == "-b":
        input_file_b = a
    elif o == "-t":
        input_file_t = a
    elif o == "-o":
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
print("done")