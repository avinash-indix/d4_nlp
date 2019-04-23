import re
import spacy
# from processData.formatPage import *
nlp = spacy.load('en_core_web_sm')

text = ["there is nothing in this  line. the automobiles tax in Chicago city has changed from 1% to 2%. Effective April 1, 2017, the Sales and Use Tax rates for \
Washoe and Clark Counties will increase. Washoe will go from 7.728 to 8.265 \
percent and Clark will go from 8.15 to 8.25 percent.",
"Under the new ordinance, the 1 percent City Lodging and Restaurant tax will apply to:\
􏰀 Gross receipts from leasing or renting of hotel, motel or tourist court accommodations for a period of\
less than 30 consecutive calendar days or one month\
􏰁 Gross receipts of restaurants or bars from sales of prepared food and non-alcoholic beverages\
􏰁 On-sale alcoholic beverages",
"Effective January 1, 2013, the combined state and local tax rates within the city limits of Glen Ullin will be.\
    General sales and use tax: 6 percent.\
    Restaurant (sale of food and non-alcoholic beverages): 7 percent.\
    Alcoholic Beverages:\
        Off-sale alcoholic beverages: 8 percent.\
        On-sale alcoholic beverages: 9 percent .\
    Hotel, Motel and Tourist Court Accommodations, and Bed & Breakfast Accommodations licensed under\
North Dakota Century Code ch. 23-09.1: 9 percent."]

def removeTextInsideParen(text):
    v = []
    outside = True
    for c in text:
        if c == '(':
            outside = False
            continue
        if c == ')':
            outside = True
            continue
        if outside is True:
            v.append(c)
    return ''.join(v)

def extractEntities(sentence = None):
    if sentence is None:
        return {}
    ncs = list(sent[1].noun_chunks)
    # print(ncs)

    rateDict = {}
    rateDict['where'] = []
    rateDict['type'] = []
    rateDict['change'] = []
    rate = []
    for nc in ncs:
        ncdoc = nlp(nc.text)
        # print(nc.root.text)
        ents = list(ncdoc.ents)
        # print(ents)
        if len(ents) <= 1:
            if len(ncdoc) == 1:
                # print(ncdoc.text, ncdoc[0].ent_type_, ncdoc[0].pos_)
                if (ncdoc)[0].pos_ == 'PROPN':
                    rateDict['where'].append(ncdoc.text)

            if len(ncdoc) > 1:
                if "tax" in ncdoc.text or "Tax" in ncdoc.text:
                    rateDict['type'].append(ncdoc.text)
                # print(ncdoc.text)
            # continue
        for ent in ents:
            d = nlp(ent.text)[0]
            if d.pos_ == 'PROPN':
                rateDict['where'].append(ncdoc.text)
            if d.ent_type_ in ['PERCENT', 'ORDINAL', 'CARDINAL']:
                rateDict['change'].append(ent.text)
        # for ent in ents:
        #     if ent.label_ == 'PROPN' or ent.ent_type_ in ['GPE','ORG']
        # print(ncdoc, ents)
    # for ent in ents:
    #     print(ent)
    return rateDict

rateDict = {}
# for sent in sentences:
#     rateDict[sent[0]] = extractEntities(sent)
#     print(sent)
#
#     print(rateDict[sent[0]])
#     print("-----")
    # print(rateDict)
    # for tok in sent[1]:
    #     print('----')
    #     ncs = list(sent[1].noun_chunks)
    #     print(ncs)
    #     rateDict[sent[0]] = {}
    #     rateDict[sent[0]]['where'] = []
    #     rateDict[sent[0]]['type'] = []
    #     rateDict[sent[0]]['change'] = []
    #     rate = []
    #     for nc in ncs:
    #         ncdoc = nlp(nc.text)
    #
    #         ents = list( ncdoc.ents)
    #         print(ents)
    #         if len(ents) == 0:
    #             if len(ncdoc)==1:
    #                 print(ncdoc.text, ncdoc[0].ent_type_, ncdoc[0].pos_)
    #                 if (ncdoc)[0].ent_type == 'PROPN':
    #                     rateDict[sent[0]]['where'].append(ncdoc.text)
    #
    #             if len(ncdoc) > 1:
    #                 if "tax" in ncdoc.text:
    #                     rateDict[sent[0]]['type'].append( ncdoc.text)
    #                 print(ncdoc.text)
    #             continue
    #         for ent in ents:
    #             d = nlp(ent.text)[0]
    #             if d.ent_type_ in ['GPE','ORG']:
    #                 rateDict[sent[0]]['where'].append(ncdoc.text)
    #             if d.ent_type_ in ['PERCENT','ORDINAL','CARDINAL']:
    #                 rateDict[sent[0]]['change'].append(ent.text)
    #         # for ent in ents:
    #         #     if ent.label_ == 'PROPN' or ent.ent_type_ in ['GPE','ORG']
    #         print(ncdoc,ents)
        # for ent in ents:
        #     print(ent)
# for k,v in rateDict.items():
#     print(k,v)
# print(rateDict)

what = list()
where = list()
change = list()
tax = "tax"
annotation = {}


def removeDuplicates(duplicatelist):
    duplicates = {}
    newList = []
    for tok in duplicatelist:
        if duplicates.get(tok.text) is None:
            duplicates[tok.text] = ''
            newList.append(tok)
    return newList

if __name__ == '__main__':

    # with open(testPdf, "rb") as f:
    #     pdf = pdftotext.PDF(f)
    #     # for i in range(len(pdf)):
    #     for i in range(1):
    #         # print(" PAGE " + str(i))
    #         page = pdf[i]
    #         text = "\n".join(newFormat(page))
    #         print(text)
    #         print("-----")
    text = list(map(lambda t : re.sub('%', ' percent ', t),text))
    for i in range(len(text)):
            # i =1
            if i == 0:
                t = nlp(re.sub('%', ' percent ', text[i]))
                sentences = [(num + 1, sentence) for num, sentence in enumerate(t.sents)]
            else:
                t = re.sub('\n+','.',text[i])
                t =nlp(removeTextInsideParen(t))
                sentences = [(num + 1, sentence) for num, sentence in enumerate(t.sents)]
                # sentences = []
                # for i in range(len(t)):
                #     sentences = [(i+1, nlp(t[i]))]

            for sent in sentences:
                rateDict[sent[0]] = extractEntities(sent)
                print(sent)

                print(rateDict[sent[0]])
                print("-----")


