from processData.embedding import embed
from processData.process_pdf import paragraph_split,flattenParagraph, paragraphs
from processData.relavance import similarity, getParagraphScore

import re
import os
this_dir, _ = os.path.split(__file__)


questionFiles = ['questions']
questionFiles = list(map(lambda file : os.path.join(this_dir,"data",file),questionFiles))


# questionFiles = ['/Users/avinash.v/Projects/code/questions']

def getQuestions(files = questionFiles):

    questions = []
    for file in files:
        with open(file, "r") as f:
            q = f.readlines()
            q = list(map(lambda _q_ : re.sub('\\n','',_q_), q))
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

    import tensorflow as tf
    import tensorflow_hub as hub
    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        for q in questions:
            print("---------")
            print(q)
            print(getAnswer(testData,q,embed,session))


