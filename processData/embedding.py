
import numpy as np
import pdf2txt
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import re

module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"
# @param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]
embed = embed = hub.Module(module_url)
fileNames = ['/Users/avinash.v/Projects/code/date_nlp.txt',
                 '/Users/avinash.v/Projects/code/type_nlp.txt']

def getMessages(fileName =''):
    sample_path = fileName
    messages = []
    with open(sample_path, "r") as f:
        lines = f.readlines()

        for line in lines:
            l = re.sub('\s+',' ',line.strip())  # replace extra whitespace
            messages.append(l)

    print(len(messages))
    return messages


def getEmbeddings(messages = {}):
    embeddings = {}
    for type, lines in messages.items():
        with tf.Session() as session:
            session.run([tf.global_variables_initializer(), tf.tables_initializer()])
            message_embeddings = session.run(embed(lines))
            print(type, message_embeddings.shape)

            # average embedding for the liies (or rows)
            average_embedding = np.average(np.array(message_embeddings), axis=0)
            print("Average embedding: {}".format(average_embedding))
            embeddings.update({type : average_embedding})

    return embeddings

def train(typeFileList : []):
    """
    :return: the average embeddings for the different types in the filelist
    fileList will contain diff files for place/date identification, tax type identification etc d

    """
    messages = {}

    for file in typeFileList:
        type = file.split('/')[-1].split('_')[0]
        messages.update({type: getMessages(file)})

    for type, lines in messages.items():
        print(type, len(lines))
        print(lines)

    averageEmbeddings = getEmbeddings(messages)
    for type, embedding in averageEmbeddings.items():
        print(type, embedding.shape)

    return averageEmbeddings

avgEmbeddings = train(fileNames)
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



