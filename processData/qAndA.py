from processData.embedding import embed
import tensorflow as tf
import numpy as np
from processData.formatPage import testPdf, getListAndNormal
# from processData.process_pdf import paragraph_split,flattenParagraph, testPdf   #paragraphs,
# from processData.formatPage import getListAndNormal
# from processData.relavance import similarity
from processData.process_pdf import testPdf

import re
import os
import pdftotext

this_dir, _ = os.path.split(__file__)


questionFiles = ['questions']
broadQuestionFiles = ['broadQuestions']

questionFiles = list(map(lambda file : os.path.join(this_dir,"data",file),questionFiles))
broadQuestionFiles = list(map(lambda file : os.path.join(this_dir,"data",file),broadQuestionFiles))


# questionFiles = ['/Users/avinash.v/Projects/code/questions']

def getQuestions(files = questionFiles):

    questions = []
    for file in files:
        with open(file, "r") as f:
            q = f.readlines()

            # filter out the questions that are commented out in the list
            q = list(filter(lambda q : not  q.startswith("#") and len(q) > 0,list(map(lambda _q_ : re.sub('\\n','',_q_), q))))
            questions.extend(q)

    return questions

def getEmbeddings(messages = [], session = None):
    """

    :param messages: list of messages / questions to get the average embedding
    :return: average embedding for messages
    """

    """
        a = np.array([[1,2,3],[4,5,6]])
        np.average(a,axis=1)            // row wise average
        array([2., 5.])
        np.average(a,axis=0)            column wise average
        array([2.5, 3.5, 4.5])
    """
    # with tf.Session() as session:
    session.run([tf.global_variables_initializer(), tf.tables_initializer()])
    embeddings = session.run(embed(messages))
    print(embeddings.shape)
    average_embedding = np.average(embeddings, axis=0)

    # checking whether the averaging is columnwise
    # print(embeddings[:,0].sum()/len(embeddings),average_embedding[0])
    assert (embeddings[:,0].sum()/(1.0*len(embeddings)) == average_embedding[0] )

    return average_embedding

def getParagraphScore(questionEmbedding = None,paragraphList = [], splitBy = '\n',session = None):
    """

    paragraphList -> find relavance to question by computing similarity between question and
    each line of paragraphg

    :param questionEmbedding: the question embedding for computing the score
    :param paragraphList: list of paragraphs to score
    :param splitonNewLine: how to split. maybe split by \n for list, and . on others ????
    :param session:
    :return:


    """

    # session.run([tf.global_variables_initializer(), tf.tables_initializer()])
    paragraphTupleWithScore = []
    for i in range(len(paragraphList)):
        pg = paragraphList[i]
        lines = pg.split(splitBy)

        pg_embeddings = session.run(embed(lines))


        n = len(pg_embeddings)

        print('*********')
        assert(len(lines) == n)

        # computing similarity for each line in a paragraph
        score = 0
        """b = array([[-1, -2, 3],
                    [-4, -5, -6],
                    [-14, -12, -13]])
            
            a = array([[1, 2, 3],
                    [4, 5, 6],
                    [14, 12, 13]])
            
            na = a/np.linalg.norm(a,axis=1,keepdims=True)
                    array([[0.26726124, 0.53452248, 0.80178373],
                        [0.45584231, 0.56980288, 0.68376346],
                        [0.62053909, 0.53189065, 0.57621487]])
            
                np.linalg.norm(a/np.linalg.norm(a,axis=1,keepdims=True),axis=1)
                        array([1., 1., 1.])
            np.multiply(na,nb).sum(axis=1)
                array([-1., -1., -1.]) 
            np.average(np.multiply(na,nb).sum(axis=1),axis=0)
                -1.0
        """
        # normalize the embeddings
        pg_embeddings = pg_embeddings/np.linalg.norm(pg_embeddings,axis=1,keepdims=True)
        question_embedding = np.full_like(pg_embeddings,questionEmbedding)
        question_embedding = questionEmbedding/np.linalg.norm(question_embedding,axis=1,keepdims=True)

        score = np.average(np.multiply(pg_embeddings,question_embedding).sum(axis=1),axis=0)
        # for i in range(len(lines)):
        #     pg_embedding = pg_embeddings[i]
        #     line = lines[i]
        #     # for pg_embedding in pg_embeddings:
        #
        #     s = similarity(pg_embedding,questionEmbedding)
        #     score += s/n
        #
        print(score)
        print(pg)
        paragraphTupleWithScore.append((score,pg))

    return paragraphTupleWithScore

if __name__ == '__main__':
    q= getQuestions(broadQuestionFiles)
    print(q)
    (ll,nl) = getListAndNormal(testPdf, listId='_l_i_s_t_')

    with tf.Session() as session:
        questionEmbedding = getEmbeddings(q,session=session)
        print(questionEmbedding.shape)

        getParagraphScore(questionEmbedding=questionEmbedding, paragraphList=ll, splitBy='\n', session=session)
    assert False


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


