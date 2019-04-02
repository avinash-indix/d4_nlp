import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import pdftotext
from pdf2txt import para_separation
import os
import pandas as pd
import re
import seaborn as sns

# open file and read lines
filepath = '/Users/avinash.v/Projects/indix/nlp/data/sample.txt'


# lines = []
# with open(filepath) as fp:
#    line = fp.readline()
#    cnt = 1
#
#    while line:
#        # print("Line {}: {}".format(cnt, line.strip()))
#        lines.append([line])
#        line = fp.readline()
#        cnt += 1
#
# print (lines)
# print (len(lines))
# assert (False)

# tf.compat.v1.disable_eager_execution()
# Import the Universal Sentence Encoder's TF Hub module

def plot_similarity(labels, features, rotation):
    corr = np.inner(features, features)
    sns.set(font_scale=1.2)
    g = sns.heatmap(
        corr,
        xticklabels=labels,
        yticklabels=labels,
        vmin=0,
        vmax=1,
        cmap="YlOrRd")
    g.set_xticklabels(labels, rotation=rotation)
    g.set_title("Semantic Textual Similarity")


def run_and_plot(session_, input_tensor_, messages_, encoding_tensor):
    message_embeddings_ = session_.run(
        encoding_tensor, feed_dict={input_tensor_: messages_})
    plot_similarity(messages_, message_embeddings_, 90)


sample_path = "/Users/avinash.v/Projects/indix/nlp/data/tax-files/walhalla-memo.pdf"
sample_path = "/Users/avinash.v/Downloads/Tagging/Town of Hauchuca Sales-Tax-Increase.pdf"
with open(sample_path, "rb") as f:
    pdf = pdftotext.PDF(f)
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"  # @param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]
    embed = hub.Module(module_url)
    for page in pdf:

        # lines = para_separation(pdf[0])
        lines = para_separation(page)


        # Compute a representation for each message, showing various lengths supported.


        messages = [
            'Effective January 1, 2013, the Finley city sales, use and gross receipts tax will be two percent (2%).\n',
            'Effective January 1, 2018, the city of Velva has adopted an ordinance to continue this one percent (1%) tax. This new ordinance continues the local tax at two percent (2%) \n',
            'Effective July 1, 2017, the city of Linton has adopted an ordinance to replace the one percent (1%) tax that ceased. This new ordinance continues the local tax at two percent (2%) \n',
            'The city of Walhalla will increase its city sales, use and gross receipts tax by one percent (1%) effective January 1, 2009. Effective January 1, 2009, the Walhalla city sales, use and gross receipts tax will be 2.0 percent. In addition, the Maximum Tax (Refund Cap) will increase to $50.00 per transaction \n',
            'The city of Michigan will increase its city sales, use and gross receipts tax by one half percent (.5%). The tax rate for Michigan starting July 1, 2014 will be two percent (2%). The Maximum Tax (Refund Cap) will remain at $25.00 per sale. \n',
            'The city of Woodworth has adopted an ordinance to impose a 1 percent city sales, use and gross receipts tax that will go into effect January 1, 2009. The Woodworth city tax is in addition to the state sales tax already in place. \n',
            'The city of Streeter has adopted an ordinance to impose a 1 percent city sales, use and gross receipts tax that will go into effect January 1, 2009. The Streeter city tax is in addition to the state sales tax already in place \n',
            'At the present time, the city of Valley City has a two percent (2%) city sales, use and gross receipts tax in place. Effective October 1, 2010, the Valley City city sales, use and gross receipts tax will be two and one half percent (2.5%). In addition to the rate change, the following applies \n',
            'At the present time, the city of Neche has a 1 percent city sales, use and gross receipts tax in place. The city of Neche will increase its city sales, use and gross receipts tax by one percent (1%) effective January 1, 2009. Effective January 1, 2009, the Neche city sales, use and gross receipts tax will be 2.0 percent. In addition, the Maximum Tax (Refund Cap) will increase to $50.00 per transaction. \n',
            'At the present time, the city of Pembina has a 1.5 percent city sales, use and gross receipts tax in place. Effective January 1, 2010, the Pembina city sales, use and gross receipts tax will be 2.5 percent. All other provisions of the ordinance remain the same effective January 1, 2010. \n',
            'At the present time, the city of West Fargo has a one percent (1%) city sales, use, and gross receipts tax in place. Effective October 1, 2014, the West Fargo city sales, use, and gross receipts tax will be two percent (2%). The following applies: \n',
            'At the present time, the city of Glenburn has a one percent (1%) city sales, use and gross receipts tax in place. Effective October 1, 2012, the Glenburn city sales, use and gross receipts tax will be two percent (2%). The following applies \n',
            'At the present time, the city of Rolette has a one percent (1%) city sales, use and gross receipts tax in place. Effective January 1, 2014, the Rolette city sales, use and gross receipts tax will be two percent (2%). The following applies \n',
            'Effective January 1, 2013, Glen Ullin will impose a 2 percent City Lodging tax and a 1 percent City Lodging and Restaurant tax. The Office of State Tax Commissioner will administer the taxes. The City Lodging tax and the City Lodging and Restaurant tax are in addition to the state and city sales taxes already in place \n',
            'At the present time, Williams County has a one half percent (1/2%) county sales, use and gross receipts tax in place. The Williams County sales, use and gross receipts tax will be suspended effective October 1, 2012 with the county reserving the option to reinstate if deemed necessary. \n',
            'Effective October 1, 2014, the city of Leeds has adopted an ordinance to impose a two (2%) city sales, use, and gross receipts tax. The Leeds city tax is in addition to the state sales, use, and gross receipts tax currently in place. In addition to this new tax, the following applies \n',
            'Effective January 1, 2009, the city of Beulah will impose a one percent (1%) City Lodging and Restaurant tax. The one percent (1%) City Lodging and Restaurant tax applies to lodging, restaurant, and on-sale alcoholic beverages. The City Lodging and Restaurant tax are in addition to the state and city sales taxes already in place \n',
            'At the present time, the city of Drayton has a one percent (1%) city sales, use and gross receipts tax in place. Effective October 1, 2010, the Drayton city sales, use and gross receipts tax will be one and one half percent (1.5%). In addition to the rate change, the following applies \n',
            'At the present time, the city of Lisbon has a 1 percent city sales, use and gross receipts tax in place. The city of Lisbon will increase its city sales, use and gross receipts tax by one half percent (.5%) effective January 1, 2009. Effective January 1, 2009, the Lisbon city sales, use and gross receipts tax will be 1.5 percent. In addition, the Maximum Tax (Refund Cap) will increase to $37.50 per transaction \n',
            'At the present time, the city of Carrington has a two percent (2%) city sales, use, and gross receipts tax in place. Effective December 31, 2016, one percent (1%) will sunset. Effective January 1, 2017, the city of Carrington has adopted an ordinance to replace the one percent (1%) tax that ceased. This new ordinance continues the local tax at two percent (2%). The following applies \n',
            '\n', '\n',
            'Effective January 1, 2009, the combined state and city rates within the city limits of Streeter, including deliveries made into the city by retailers located outside the city limits of Streeter, will be as follows:\n',
            'General sales and use tax: 6.0 percent (5% state + 1% city)\n',
            'Natural gas: 2.0 percent (1% state + 1% city)\n',
            'New farm machinery and new farm irrigation equipment: 4.0 percent (3% state + 1% city) New mobile homes: 4.0 percent (3% state + 1% city)\n',
            'Coin-operated amusement: 6.0 percent (5% state + 1% city)\n', 'Lodging:\n',
            'o Hotel, Motel and Tourist Court Accommodations, and Bed & Breakfast Accommodations licensed under North Dakota Century Code ch. 23-09.1: 6.0 percent (5% state + 1% city sales)\n',
            'Restaurant (sale of food and non-alcoholic beverages): 6.0 percent (5% state + 1% city sales) Alcoholic Beverages:\n',
            'o Off-sale alcoholic beverages: 8.0 percent (7% state + 1% city gross receipts) o On-sale alcoholic beverages: 8.0 percent (7% state + 1% city gross receipts)\n']
        # print(lines[:10])
        test_messages = lines


        # Reduce logging output.
        tf.logging.set_verbosity(tf.logging.ERROR)
        similarity_input_placeholder = tf.placeholder(tf.string, shape=(None))
        similarity_message_encodings = embed(similarity_input_placeholder)
        with tf.Session() as session:
            session.run([tf.global_variables_initializer(), tf.tables_initializer()])
            message_embeddings = session.run(embed(messages))

            # for i, message_embedding in enumerate(np.array(message_embeddings).tolist()):
            # print("Message: {}".format(messages[i]))
            # print("Embedding size: {}".format(len(message_embedding)))
            # print("type: {}".format(type(message_embedding)))
            # message_embedding_snippet = ", ".join(
            #     (str(x) for x in message_embedding[:3]))
            # print("Embedding: [{}, ...]\n".format(message_embedding_snippet))

            average_embedding = np.average(np.array(message_embeddings), axis=0)
            print("Average embedding: {}".format(average_embedding))

            test_message_embeddings = session.run(embed(test_messages))
        # with tf.Session() as session:
        #     session.run(tf.global_variables_initializer())
        # session.run(tf.tables_initializer())

            results = []
            for i, test_message_embedding in enumerate(np.array(test_message_embeddings).tolist()):
                similarity = np.dot(test_message_embedding,average_embedding)/\
                             (np.linalg.norm(test_message_embedding)*np.linalg.norm(average_embedding))
                results.append({'message' : test_messages[i],"similarity" : similarity})
                print("Message: {}".format(test_messages[i]),"---> similarity: {}".format(similarity))
            # run_and_plot(session, similarity_input_placeholder, test_messages,
            #          similarity_message_encodings)


            # sort by descending order of similarity score
            results = sorted(results,key = lambda d : d['similarity'],reverse= True)[:10]
            df = pd.DataFrame(results)
        print(df)