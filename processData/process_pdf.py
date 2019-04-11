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

def paragraph_split(data):
    """

    :param data: text representation of each page of a pdf
    :return: list of paragraphs (that have been split) based on seen heuristics
    """

    # we will initially split based on .\n
    pattern= r"(\.\n){1,}"
    replacePattern = '----'

    paragraphs = re.sub(pattern,replacePattern,data).split(replacePattern)

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
paragraphs = processPdf(testPdf)

if __name__ == '__main__':


    paragraphs = processPdf(testPdf)
    for i in range(len(paragraphs)):
        pg = paragraphs[i]
        # print('----\n',i,pg,'\n')
        print('----\n')
        print (flattenParagraph(pg))