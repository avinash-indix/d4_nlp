import re
import spacy

nlp = spacy.load('en_core_web_sm')

text = "there is nothing in this  line. the automobiles tax in Chicago city has changed from 1% to 2%. Effective April 1, 2017, the Sales and Use Tax rates for \
Washoe and Clark Counties will increase. Washoe will go from 7.728 to 8.265 \
percent and Clark will go from 8.15 to 8.25 percent."

# text = "the tax rate did not chnage."
text = nlp(re.sub('%', ' percent ', text))
# text_ = re.sub('\.(\s+)','\n',text).split('\n')
# print(text_)

sentences = [(num + 1, sentence) for num, sentence in enumerate(text.sents)]
print(sentences)

type = []
rateDict = {}
for sent in sentences:
    # for tok in sent[1]:
        print('----')
        ncs = list(sent[1].noun_chunks)
        print(ncs)
        rateDict[sent[0]] = {}
        rateDict[sent[0]]['where'] = []
        rateDict[sent[0]]['type'] = []
        rateDict[sent[0]]['change'] = []
        rate = []
        for nc in ncs:
            ncdoc = nlp(nc.text)

            ents = list( ncdoc.ents)
            print(ents)
            if len(ents) == 0:
                if len(ncdoc)==1:
                    print(ncdoc.text, ncdoc[0].ent_type_, ncdoc[0].pos_)
                    if (ncdoc)[0].ent_type == 'PROPN':
                        rateDict[sent[0]]['where'].append(ncdoc.text)

                if len(ncdoc) > 1:
                    if "tax" in ncdoc.text:
                        rateDict[sent[0]]['type'].append( ncdoc.text)
                    print(ncdoc.text)
                continue
            for ent in ents:
                d = nlp(ent.text)[0]
                if d.ent_type_ in ['GPE','ORG']:
                    rateDict[sent[0]]['where'].append(ncdoc.text)
                if d.ent_type_ in ['PERCENT','ORDINAL','CARDINAL']:
                    rateDict[sent[0]]['change'].append(ent.text)
            # for ent in ents:
            #     if ent.label_ == 'PROPN' or ent.ent_type_ in ['GPE','ORG']
            print(ncdoc,ents)
        # for ent in ents:
        #     print(ent)
print(rateDict)

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

# for text in text_:
#         print(text)
#         text = nlp(text)
#
#
#         for tok in text:
#             annotation[tok.text] = tok
#         #     print (tok.text)
#
#         for nc in text.noun_chunks:
#             nct = nc.text.split()
#             l = len(nct)
#             print(str(nct))
#             if tax in nct or "Tax" in nct:
#                     what.append(nc)
#             for t in nct:
#                 if annotation.get(t):
#                     tok = annotation[t]
#                     if tok.ent_type_ in ['GPE', 'ORG']:
#                         where.append(tok)
#                     if tok.ent_type_ in ['PERCENT', 'ORDINAL', 'CARDINAL']:
#                         change.append(tok)
#
# where = removeDuplicates(where)
# change = removeDuplicates(change)
# what = removeDuplicates(what)
#
# print("where:\t" + str(where))
# print("chnage:\t" + str(change))
# print("what:\t" + str((what)))
