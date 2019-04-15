from processData.embedding import embed
from processData.process_pdf import paragraph_split,flattenParagraph, testPdf   #paragraphs,
from processData.formatPage import getListAndNormal
from processData.relavance import similarity, getParagraphScore, paragraphsAfterCutoff
from processData.process_pdf import testPdf

import re
import os
import pdftotext

this_dir, _ = os.path.split(__file__)


questionFiles = ['questions']
questionFiles = list(map(lambda file : os.path.join(this_dir,"data",file),questionFiles))


# questionFiles = ['/Users/avinash.v/Projects/code/questions']

def getQuestions(files = questionFiles):

    questions = []
    for file in files:
        with open(file, "r") as f:
            q = f.readlines()

            # filter out the questions that are commented out in the list
            q = list(filter(lambda q : not  q.startswith("#"),list(map(lambda _q_ : re.sub('\\n','',_q_), q))))
            questions.extend(q)

    return questions

def getAnswer(text = '', question = '' , embed = None, session = None, topN = 5):
    """

    :param text: look for answers in text
    :param question:
    :param embed:
    :param session: tf session
    :return: list of answers with their relavance score
    """

    common_words_to_remove = ['tax']
    if session is None or embed is None or text is None or text == '':
        return [('',0)]

    answers = text.split('\n')

    answer_embeddings = session.run(embed(answers))
    qeustion_embedding = session.run(embed([question]))
    answer_relavance_scores = list(map(lambda answer_embedding : similarity(qeustion_embedding,answer_embedding),
                                  answer_embeddings))
    answers_with_relavance = list(zip(answer_relavance_scores,answers))
    # print(answers_with_relavance)
    # sort the above on decreasing order of relavance
    answers_with_relavance = sorted(answers_with_relavance, key = lambda t : t[0],reverse=True)[:topN]

    # (1.0000001, ''), (0.16796382, '               Lodging:')
    answers_with_relavance = "\n".join(list(map(lambda tup : "score: " + str(tup[0]) + "\t"+tup[1],
                                                answers_with_relavance)))
    return answers_with_relavance


if __name__ == '__main__':

    questions = getQuestions(questionFiles)
    testData = "Effective April 1, 2018, the combined state and city rates within the city limits of \n\
               Belfield will be as follows:\n\
               General sales and use tax: 7 percent (5% state + 2% city)\n\
               New farm machinery: 5 percent (3% state + 2% city)\n\
               New farm irrigation equipment: 5 percent (3% state + 2% city)\n\
               New mobile homes: 5 percent (3% state + 2% city)\n\
               Lodging:\n\
               Hotel, Motel and Tourist Court Accommodations, and Bed & Breakfast Accommodations licensed under North Dakota Century Code ch. 23-09.1:\n\
               9 percent (5% state + 2% city sales + 2% City Lodging tax)\n\
               Restaurant (sale of food and non-alcoholic beverages): 7 percent (5% state + 2% city sales)\n\
               Alcoholic Beverages:\n\
               Off-sale alcoholic beverages: 9 percent (7% state + 2% city gross receipts)\n\
               On-sale alcoholic beverages: 9 percent (7% state + 2% city gross receipts)\n\
               Questions concerning the Belfield city sales, use, and gross receipts tax may be directed to the Office of State Tax\n\
               Commissioner. You may contact the Office of State Tax Commissioner by phone at 701.328.1246, by email at\n\
               salestax@nd.gov, or by mail at Office of State Tax Commissioner, Tax Compliance Section, 600 E Boulevard\n\
               Dept. 127, Bismarck, ND 58505-0599\n"
    print(questions)

    testData = []
    # with open(testPdf, "rb") as f:
    #     pdf = pdftotext.PDF(f)
    #     # paragraphs = []
    #     # How many pages?
    #     print(len(pdf))
    #
    #     # Iterate over all the pages
    #     for i in range(len(pdf)):
    #         page = pdf[i]
    #         testData.extend(page.split(r'\n'))
    # testData = "\n".join(testData).lower()

    (ll,nl) = getListAndNormal(testPdf)


    # testdata after getting the relavant paragraphs
    relParagraphsAfterCutoff = paragraphsAfterCutoff(ll,0.5)

    # clean up the format of relavant paragraphs
    testData = "\n".join(list(map(lambda tup : "\n".join(tup[1].split("\.")) , relParagraphsAfterCutoff))).lower()


    # we could remove some common words like tax etc
    words_to_remove = ['tax']
    for word in words_to_remove:
        testData = re.sub(word,' ',testData)

    import tensorflow as tf
    import tensorflow_hub as hub

    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        for q in questions:
            print("---------")
            print(q)
            print(getAnswer(testData,q,embed,session,topN=10))


