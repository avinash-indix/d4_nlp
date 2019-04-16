
import numpy as np
import pdf2txt
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import re

import os
this_dir, _ = os.path.split(__file__)
print(this_dir)


module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"
module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3"

embed = hub.Module(module_url)
print("Loaded the embedding model from " + module_url)

fileNames = ['/Users/avinash.v/Projects/code/date_nlp.txt',
                 '/Users/avinash.v/Projects/code/type_nlp.txt']
fileNames = ['date_nlp.txt','type_nlp.txt']
fileNames = list(map(lambda file : os.path.join(this_dir,"data",file),fileNames))


def getMessages(fileName =''):
    """

    :param fileName: the 'type' filename that is needed for the embedding (eg date/place/type)
    :return: lines that will be consumed by the embedding
    """
    sample_path = fileName
    messages = []
    with open(sample_path, "r") as f:
        lines = f.readlines()

        for line in lines:
            # replace extra whitespace
            l = re.sub('\s+',' ',line.strip())
            messages.append(l)

    print(len(messages))
    return messages


def getEmbeddings(messages = {}):
    """

    :param messages: dict of {type : text relavant to the type}
    :return: embeddings dict that contains the average embedding for each type
    """
    embeddings = {}
    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        for type, lines in messages.items():

            message_embeddings = session.run(embed(lines))
            print(type, message_embeddings.shape)

            # average embedding for the lines (or rows, axis=0 )
            average_embedding = np.average(np.array(message_embeddings), axis=0)
            # print("Average embedding: {}".format(average_embedding))
            embeddings.update({type : average_embedding})

    return embeddings

def train(typeFileList : []):

    """
    getMessages(filename) -> lines for each type  | getEmbeddings -> avg embedding for each type
    :return: the average embeddings for the different types in the filelist
    fileList will contain diff files for place/date identification, tax type identification etc d
    """

    messages = {}

    for file in typeFileList:

        # extract the type from the filename eg rate_xxx.txt -> rate
        type = file.split('/')[-1].split('_')[0]
        messages.update({type: getMessages(file)})

    for type, lines in messages.items():
        print(type, len(lines))
        print(lines)

    # lines -> avg embeddings
    averageEmbeddings = getEmbeddings(messages)
    for type, embedding in averageEmbeddings.items():
        print(type, embedding.shape)

    return averageEmbeddings

# avgEmbeddings = train(fileNames)
if __name__ == '__main__':


    messages = {}
    avgEmbeddings = train(fileNames)
    #
    #
    # for file in fileNames:
    #     type = file.split('/')[-1].split('_')[0]
    #     messages.update({type : getMessages(file)})
    #
    # for type, lines in messages.items():
    #     print(type, len(lines))
    #     print(lines)
    #
    # averageEmbeddings = getEmbeddings(messages)
    # for type, embedding in averageEmbeddings.items():
    #     print(type,embedding.shape)



