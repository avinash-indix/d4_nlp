from processData.embedding import avgEmbeddings as average_embeddings
from processData.embedding import *
from processData.process_pdf import paragraph_split,flattenParagraph, paragraphs
import tensorflow as tf

def getParagraphScore(paragraphList = [], splitonNewLine = True):
    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        paragraphTupleWithScore = []
        for i in range(len(paragraphList)):
            pg = paragraphList[i]
            lines = flattenParagraph(pg, splitOnNewLine= False)    # lines have only ascii chars

            paragraphScore = {}
            pg_embeddings = session.run(embed(lines))
            n = len(pg_embeddings)

            print('*********')
            assert(len(lines) == n)

            # computing similarity for each line in a paragraph
            for i in range(len(lines)):
                pg_embedding = pg_embeddings[i]
                line = lines[i]
            # for pg_embedding in pg_embeddings:

                # compute relavance score for each (date/place and type)
                for key in average_embeddings.keys():
                    average_embedding = average_embeddings[key]
                    similarity = np.dot(pg_embedding,average_embedding)/\
                             (np.linalg.norm(pg_embedding)*np.linalg.norm(average_embedding))

                    #mean score for each type
                    if paragraphScore.get(key) is None:
                        paragraphScore[key] = similarity/n
                    else:
                        paragraphScore[key] += (similarity)/n

            print(paragraphScore)
            print(pg)
            paragraphTupleWithScore.append((paragraphScore,pg))

    return paragraphTupleWithScore



def isRelavantBasedOnCutoff(score_dict = {}, cutoff = 0.0):

    values = score_dict.values()

    # if any value >= cutoff return true
    l = (list(filter(lambda v : v >= cutoff, values)))
    print("l\t:",l)
    if len(l) > 0:
        return True
    return False

if __name__ == '__main__':
    
    print("Generating Relavance Report")
    paragraph_list = getParagraphScore(paragraphs)

    # we will drop paragraphs that have a relavance score less than cutoff
    cutoff_value = 0.5
    final_list_after_cutoff_filter = list(filter(lambda tuple_of_index_and_score :
                                                 isRelavantBasedOnCutoff(tuple_of_index_and_score[0],cutoff_value) is True,paragraph_list))

    print("After Cutoff")
    for tup in final_list_after_cutoff_filter:
        print("########")
        print(tup)
