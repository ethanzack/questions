import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import nltk
import re
import sys

tf.compat.v1.disable_eager_execution()

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/3")

def sentenceFeatures(questions):
    if type(questions) is str: questions = [questions]
    with tf.compat.v1.Session() as sess:
        sess.run([tf.compat.v1.global_variables_initializer(), tf.compat.v1.tables_initializer()])
        return sess.run(embed(questions))

def similarity(v1, v2):
    mag1 = np.linalg.norm(v1)
    mag2 = np.linalg.norm(v2)
    if (not mag1) or (not mag2):
        return 0
    v1 = np.squeeze(np.asarray(v1))
    v2 = np.squeeze(np.asarray(v2))

    return np.dot(v1, v2) / (mag1 * mag2)

def semantic_search(newQuestion, data, currentVecs):
    newQuestionFeatures = sentenceFeatures(newQuestion)['outputs'].ravel()
    res = []
    for i, d in enumerate(data):
        res.append((similarity(newQuestionFeatures, currentVecs[i].ravel()), d[:100], i))
    return sorted(res, key=lambda x : x[0], reverse=True)

def pipeline(groups, testData, text):
    if groups == True:
        print(testData)
        return testData
    # print(test_similarity("what is two plus two?", "what is the solution to two added with two?"))
    for sentence in text:
        found = False
        # inp = input("Please enter a question: \n")
        inp = sentence.lower()


        print("CURRENTLY ANALYZING: " + sentence + "\n")
            # inp = input("Please enter a question: \n")

        print("\n")
        if testData:
            for group in testData:
                results = semantic_search(inp, group, sentenceFeatures(group)['outputs'])
                firstEval = results[0][0]
                if firstEval > .5 and firstEval <= 1:
                    print("MATCHED WITH: " + str(results[0][1]) + "\nWITH CONFIDENCE " + str(firstEval) + "\n")
                    print("ADDING TO GROUP: " + str(group)) # RETURN TO UI
                    print("\n\n")
                    group.append(inp)
                    found = True
                    break

            if found == False:
                print("MAKING NEW GROUP\n")
                testData.append([inp])

        else:
            print("NOTHING TO COMPARE\n\n")
            testData.append([inp])

    print(testData)
    return testData
