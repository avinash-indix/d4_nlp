import pdftotext
from processData.embedding import fileNames
from itertools import islice
import re

import os
this_dir, _ = os.path.split(__file__)


testPdf = ['113test.pdf']
testPdf = list(map(lambda file : os.path.join(this_dir,"data",file),testPdf))

# testPdf = '/Users/avinash.v/Projects/indix/nlp/data/tax-files/113test.pdf'
testPdf = testPdf[0]


def processPdf(fileName: ''):
    """
    takes a pdf and splits into pararagraphs based on seen heuristics
    :param fileName: pdf for processing/extracting
    :return:
    """
    with open(fileName, "rb") as f:
        pdf = pdftotext.PDF(f)
        paragraphs = []
        # How many pages?
        print(len(pdf))

        # Iterate over all the pages
        for i in range(len(pdf)):
            page = pdf[i]

            paragraphs.extend(paragraph_split(page))
    return paragraphs


def window(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def header(str, max_length):
    return len(str) > 0 and not str.startswith(' ') and str[0].isupper() and len(str) < max_length / 1.3

def para_separation(data):
    data_list = list(map(lambda x: x.strip(), data.split('\n')))
    data_list_with_length = map(lambda x: (len(x), x), data_list)
    max_length = sorted(data_list_with_length, key=lambda x: -1 * x[0])[0][0]

    sliding = list(window(data_list, 2))

    indexes = []
    index = 0
    for (i, j) in sliding:
        i = i.strip()
        j = j.strip()
        if ((i.endswith('.') and (len(j.strip()) == 0 or j[0].isupper()))
            or (len(j.strip()) > 0 and j.strip()[0].encode("unicode_escape") != j.strip()[0])
            or header(i, max_length)):
            indexes.append(index)
        index += 1

    new_data_list = []
    index = 0
    for line in data_list:
        new_data_list.append(line)
        new_data_list.append(' ')
        if (index in indexes):
            new_data_list.append('\n')
        index += 1

    result = ''.join(new_data_list).replace('. ', '\n').split('\n')

    return result


def formatPage(page = ''):
    """
    At present there are at least 2 different paragraphs, listing para ( has a colon and bullet points),
     normal para (ends with a .)
    :param page:
    :return: list of paragraphs
    """
    nonAsciiPattern = r'[^\x00-\x7F]+'
    removePattern = r'^[^a-zA-Z\s]+'
    inList = False

    #todo: start list is identified by a : at the end
    startListPattern = r'[a-zA-Z].*:$'

    #todo: list item
    # listItemPattern = r'^[\t]{1,}'
    listItemPattern = r'^(\s+)'

    #todo: end of list is beginning with alpha numeric and not ending in :
    endListPattern = r'^[a-zA-Z].*$'
    if page == '':
        return ['']
    lines = page.split('\n')
    paragraph = []
    listParagraphs = []

    # line is either beginList, endList, or listItem
    for line in lines:
        l  = re.sub(removePattern,'',line.lower())
        if re.match(startListPattern,l) is not None:
            # beginning of list
            # if not inList:
            listParagraphs.append(paragraph)
            paragraph = []
            inList = True
            paragraph = []
            paragraph.append(l)
            continue

        if re.match(endListPattern, l) is not None:
            inList = False
            listParagraphs.append(paragraph)
            paragraph = []
            # paragraph.append(line)
            continue

        if (re.match(listItemPattern,l) is not None and inList is True):
            paragraph.append(l)
            continue

    if len(paragraph) > 0:
        listParagraphs.append(paragraph)
    listParagraphs = list(filter(lambda p : len(p) > 0, listParagraphs))
    return listParagraphs

def formatParagraph(paragraph = [], regexList = [(r"(\.\n){1,}",'----'),(r'\. ','\n')]):
    """

    :param paragraph: text to be formatted
    :param regexList:
    :return: formatted text according to the regex list
    """

    if len(regexList) == 0:
        return list(paragraph)
    if type(paragraph) != list and type(paragraph) != map:
        paragraph = list(paragraph)

    assert(type(paragraph) == list or type(paragraph) == map)
    fromPattern = regexList[0][0]
    toPattern = regexList[0][1]
    regexList = regexList[1:]


    formattedParagraph = map(lambda p : re.sub(fromPattern,toPattern,p).split(toPattern),paragraph)
    return formatParagraph(formattedParagraph,regexList)


def paragraph_split(data):
    """

    :param data: text representation of each page of a pdf
    :return: list of paragraphs (that have been split) based on seen heuristics
    """

    # we will initially split based on .\n
    pattern= r"(\.\n){1,}"
    replacePattern = '----'

    paragraphs = re.sub(pattern,replacePattern,data).split(replacePattern)


    paragraphs = list(map(lambda p : re.sub(':\n',' ',p), paragraphs))
    # paragraphs = re.sub(r'\. ','\n',list(map(lambda para : re.sub(r'\s+',' ',para), paragraphs)))
    return paragraphs

def flattenParagraph(paragraph, splitOnNewLine = True):

    """
    splitting a paragraphs into multiple lines.
    :param paragraph:
    :param splitOnNewLine: flag to decide whether to split or not
    :return:
    """
    # as a first cut we will split on new line and remove special characters (keep only ascii)
    nonAsciiPattern = r'[^\x00-\x7F]+'
    # eg re.sub(nonAsciiPattern, '', "how are you ? å") -> "how are you ?'

    if splitOnNewLine is True:
        lines = paragraph.split('\n')
    else:
        lines = [paragraph]

    # replace extra whitespace and nonAscii chars
    lines = list(map(lambda line : re.sub(nonAsciiPattern,' ',
                                          re.sub('\s+',' ',line.strip())), lines))

    # remove extra white space
    return lines

def getParagraphs(pdfFile = []):
    paragraphs = processPdf(testPdf)
    return paragraphs

# paragraphs = getParagraphs()
# print(testPdf)
# paragraphs = processPdf(testPdf)

if __name__ == '__main__':

    with open(testPdf, "rb") as f:
        pdf = pdftotext.PDF(f)
        for i in range(len(pdf)):
            page = pdf[i]
            listParagraphs = formatPage(page)
            print(listParagraphs)
            print(len(listParagraphs))
    # for i in range(len(paragraphs)):
    #     pg = paragraphs[i]
    #     # print('----\n',i,pg,'\n')
    #     print('----\n')
    #     print (flattenParagraph(pg))