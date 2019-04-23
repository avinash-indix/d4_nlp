import pdftotext
from processData.process_pdf import testPdf
import re
print(testPdf)
import spacy


def format(page = ''):
    """
    first standardize page (remove non ascii characters)
    left justify the text
    :param page:
    :return: formatted page
    """

    def nextCharIndex(i,page):
        nc = page[i+1]
        while i < len(page)-1 and not nc.isalnum():
            i += 1
            nc = page[i+1]
        return i+1

    lines = page.split('\n')

    newPage = []

    #remove whitespace at beginning of sentennce

    for line in lines:

        l= line.rstrip()
        # l = '{:100}'.format(l)

        print(l)
        newPage.append(l)

    return
    newPage = '\n'.join(newPage)
    # newPage = re.sub("\n{2,}","\n",newPage)
    page = newPage

    paragraph = ''
    inList = False
    listOfParagraphs = []
    i = 0

    while i < len(page)-1:
        c = page[i]
        nc = -1
        pc = -1
        if i < len(page) - 1:
            nc = page[i+1]
        if i > 0:
            pc = page[i-1]
        if c==':' : #and (nc == '\n' or nc.isalnum()):
            i = nextCharIndex(i,page)
            nc = page[i]

            inList = True
            paragraph += ':\n'

            continue
            # else:
            #     paragraph += ':'
            #     # i += 1
            #     continue
        if c=='\n':
            # if nc == -1:
            ni = nextCharIndex(i, page)
            nc = page[ni]

            if nc.isupper()  and (ni - i <= 1 or ni-i <= 2):
                listOfParagraphs.append(paragraph)
                paragraph = ''
                inList = False
                # i += 1
                i = ni
                continue

            else:
                ni = i
                if inList:
                    paragraph += c
                else:
                    paragraph += ' '
        else:
            paragraph += c
        i += 1
    if len(paragraph) > 0:
        listOfParagraphs.append(paragraph)
    for p in listOfParagraphs:
        print("------")
        p = p.strip()
        print(p)

def newFormat(page = '',listId = "__list__", headerToRemove = ['to:','from:','date:','subject:']):

    """
    first standardize page (remove non ascii characters)
    left justify the text
    :param page:
    :return: formatted page
    """


    def nextCharIndex(i,page):
        nc = page[i+1]
        while i < len(page)-1 and not nc.isalnum():
            i += 1
            nc = page[i+1]
        return i+1

    lines = page.split('\n')

    newPage = []

    #remove whitespace at beginning of sentennce

    for line in lines:

        l= line.rstrip()
        # l = '{:100}'.format(l)

        # print(l)
        newPage.append(l)

    newPage = '\n'.join(newPage)
    newPage = re.sub("\n{2,}","\n",newPage)
    page = newPage
    # print(page)
    # return
    paragraph = ''
    inList = False
    listOfParagraphs = []
    i = 0

    while i < len(page)-1:
        c = page[i]

        if c==':':
            inList = True
            paragraph += ':' + listId
            i += 1
            continue

        if c=='\n':
            # if nc == -1:
            ni = nextCharIndex(i, page)
            nc = page[ni]

            if nc.isupper()  and (ni - i <= 1 or ni-i <= 2):
                listOfParagraphs.append(paragraph)
                paragraph = ''
                inList = False
                i = ni
                continue

            else:
                i = ni
                if inList:
                    paragraph += c
                else:
                    paragraph += ' '
                continue
        else:
            paragraph += c
        i += 1
    if len(paragraph) > 0:
        listOfParagraphs.append(paragraph)

    #todo:remove paragraphs with headers, maybe we shud do this somewhere else ???
    listOfParagraphs = list(filter(lambda p: len(list(filter(lambda s: s in p.lower(), headerToRemove))) == 0,
                                   listOfParagraphs))
    for p in listOfParagraphs:
        print("------")
        p = p.strip()
        print(p)
    return listOfParagraphs

def getListAndNormal(pdfFile,listId = "_l_i_s_t_"):
    l = []
    with open(pdfFile, "rb") as f:
        pdf = pdftotext.PDF(f)
        for i in range(len(pdf)):
            # print(" PAGE " + str(i))
            page = pdf[i]

            l.extend(newFormat(page, listId))
    ll = []
    nl = []
    for p in l:
        if listId in p:
            ll.append(p)
        else:
            nl.append(p)

    print("These are the list items")
    for l in ll:
        print(l+"\n")
    print('------')
    print("These are the normal items")
    for l in nl:
        print(l+"\n")

    return (ll,nl)

def spacySentence(page,model):
    parsed_page = model(page)
    for num,sentence in enumerate(parsed_page.sents):
        print("Sentence {}".format(num+1))
        print(sentence)

if __name__ == '__main__':
    nlp = spacy.load('en_core_web_sm')
    with open(testPdf, "rb") as f:
        pdf = pdftotext.PDF(f)
        for i in range(len(pdf)):
            # print(" PAGE " + str(i))
            page = pdf[i]
            print(page)
            print("----spacy sentence----")
            spacySentence(page,nlp)
            assert False
    getListAndNormal(testPdf)