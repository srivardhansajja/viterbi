from collections import defaultdict
from collections import Counter
import math

class trellis_node:
    def __init__(self, p, parent, tag_, word_):
        self.probability = p
        self.backpointer = parent
        self.tag = tag_
        self.word = word_

def extra(train,test):
    '''
    TODO: implement improved viterbi algorithm for extra credits.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
            test data (list of sentences, no tags on the words)
            E.g  [[word1,word2,...][word1,word2,...]]
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''
    predicts = []

    # =================================================================================================================================================================
    # Dicts/Counters Builders #

    word_tag_counts = dict()         # dict of words, which is in turn a Counter of tags, which keep count of the number of times a particular word is a particular POS
    tag_counts = Counter()           # Counter of tags, increments for each tag seen in the train set
    tag_initial_counts = Counter()   # Counter of tags at sentence[0], (len = 16), increments for each tag if that tag is at the start of a sentence
    tag_transition_counts = dict()   # Kind of a 2d array, which shows how many times a tag in dimension 1 is followed by a tag in dimension 2
    hapax_counts = Counter()
    hapax_total_count = 0

    k = 0.0000000000000000000000000000000000000000000000000000000000000000000001                      # Smoothing Constant

    # word_tag_counts builder
    for sentence in train:
        for word, tag in sentence:
            if word not in word_tag_counts:
                word_tag_counts[word] = Counter()
            word_tag_counts[word].update([tag])
    
    word_tag_counts['UNKNOWN-WORD'] = Counter()

    temp_tag_counter = Counter()
    # tag_counts builder
    for sentence in train:
        for word, tag in sentence:
            tag_counts.update([tag])

    # tag_initial_counts builder
    for sentence in train:
        for index, (word, tag) in enumerate(sentence):
            if index == 0:
                tag_initial_counts.update([tag])

    #tag_transition_counts builder
    for previous_tag in tag_counts:
        tag_transition_counts[previous_tag] = Counter()
    # tag_transition_counts['UNKNOWN-TAG'] = Counter()

    for sentence in train:
        tags_list = [tuple_[1] for tuple_ in sentence]
        for i in range(len(tags_list) - 1):
            previous_tag = tags_list[i]
            next_tag = tags_list[i + 1]
            tag_transition_counts[previous_tag].update([next_tag])
            temp_tag_counter.update([previous_tag])

    # hapax_counts builder
    for tag in tag_counts:
        for word in word_tag_counts:    
            if word_tag_counts[word][tag] == 1:
                hapax_counts.update([tag])
                hapax_total_count += 1

    vocab_size = len(word_tag_counts) - 1      # Number of unique words in the training set
    no_of_tags = len(tag_counts) + 1           # Number of tags in the training set, + 1 to account for 'UNKNOWN-TAG'


    


    # =================================================================================================================================================================


    # =================================================================================================================================================================
    # Probability Calulations #

    emission_probabilities = dict()     # P(word|tag) = (count(word,tag)+k)/(count(tag)+k∗|vocab_size+1|)
    transition_probabilities = dict()   # P(tag_curr|tag_prev) = (count(tag_prev−>tag_curr)+k) / (count(tag_prev)+k∗|no._of_tags|)
    initial_probabilities = dict()      # P(tag_i|starting_position) = (count(tag_i,starting_position)+k) / (Σj∈|num_tags|count(tagj_starting_position)+k∗|no_of_tags|)
    hapax_probabilities = dict()        # P(tag|word_occurs_once) = (count(word_occurs_once,tag)+k) / (count(word_occurs_once)+k∗|no_of_tags|)

    # hapax_probabilities builder
    for tag in tag_counts:
        probability = (hapax_counts[tag] + k) / (hapax_total_count + k * no_of_tags)
        hapax_probabilities[tag] = probability

    # emission_probabilities builder
    for word in word_tag_counts:
        emission_probabilities[word] = dict()
        for tag in tag_transition_counts:
            probability = (word_tag_counts[word][tag] + (k * hapax_probabilities[tag])) / (tag_counts[tag] + ( (k * hapax_probabilities[tag]) * (abs(vocab_size + 1)) ))  # Numerator will be k for 'UNKNOWN'
            emission_probabilities[word][tag] = probability
        # emission_probabilities[word]['UNKNOWN-TAG'] = (word_tag_counts[word]['UNKNOWN-TAG'] + k) / (tag_counts['UNKNOWN-TAG'] + ( k * (abs(vocab_size + 1)) ))

    # transition_probabilities builder
    for previous_tag in tag_transition_counts:
        transition_probabilities[previous_tag] = dict()
        for next_tag in tag_transition_counts:
            transition_probabilities[previous_tag][next_tag] = (tag_transition_counts[previous_tag][next_tag] + k) / (temp_tag_counter[previous_tag] + k * no_of_tags)

    # initial_probabilities builder
    for tag in tag_transition_counts: # not tag_counts to account for 'UNKNOWN-TAG'
        initial_probabilities[tag] = (tag_initial_counts[tag] + k) / (len(train) + k * no_of_tags)

    # =================================================================================================================================================================


    # =================================================================================================================================================================
    # Trellis Build and Backtracking #

    # temp_dict = dict()
    # for sentence in train:
    #     for word, tag in sentence:
    #         if word[-3:] not in temp_dict:
    #             temp_dict[word[-3:]] = Counter()
    #         temp_dict[word[-3:]].update([tag])

    # for word in temp_dict:
    #     for tag in tag_counts:
    #         if temp_dict[word[-3:]][tag] > 300 and tag != 'NOUN':
    #             print(word, temp_dict[word])
    #             print()
    
    # return []

    for sentence in test:

        
        prev_word_tag_nodes = []
        for index, word in enumerate(sentence):

            curr_word_tag_nodes = []

            if word in word_tag_counts:

                if index == 0:
                    for tag in word_tag_counts[word]:
                        # print(tag)
                        p = math.log10(initial_probabilities[tag]) + math.log10(emission_probabilities[word][tag])
                        curr_word_tag_nodes.append(trellis_node(p, None, tag, word))
                        # print(curr_word_tag_nodes)
                else:
                    for tag in word_tag_counts[word]:
                        # print(word, prev_word_tag_nodes[0].word)
                        p = math.log10(emission_probabilities[word][tag]) + max([node.probability + math.log10(transition_probabilities[node.tag][tag]) for node in prev_word_tag_nodes])
                        max_node = max(prev_word_tag_nodes, key=lambda node_: node_.probability + math.log10(transition_probabilities[node_.tag][tag])) # for back pointer
                        curr_word_tag_nodes.append(trellis_node(p, max_node, tag, word))

            else:
                if index == 0:
                    for tag in transition_probabilities:
                        p = math.log10(initial_probabilities[tag]) + math.log10(emission_probabilities['UNKNOWN-WORD'][tag])
                        append_tag = 'NOUN'
                        if word.endswith("ly") or word.endswith("hen"):
                            append_tag = 'ADV'
                        if word.endswith("ing") or word.endswith("ned"):
                            append_tag = 'VERB'
                        if word.endswith("ify") or word.endswith("ted") or word.endswith("ied") or word.endswith("are") or word.endswith("ved") or word.endswith("ned") or word.endswith("sed") or word.endswith("ed"):
                            append_tag = 'VERB'
                        if word.endswith("ish") or word.endswith("ive") or word.endswith("ous") or word.endswith("ful") or word.endswith("ral")  or word.endswith("cal")  or word.endswith("tic")  or word.endswith("ial") or (word.endswith("less") and word != "less") or (word.endswith("able") and word != "able"):
                            append_tag = 'ADJ' 
                        if word.endswith("mic"):
                            append_tag = 'ADJ' 
                        if word.endswith("ize"):
                            append_tag = "VERB"

                        if word.endswith("ing"):
                            append_tag = 'VERB'
                        curr_word_tag_nodes.append(trellis_node(p, None, append_tag, word))
                else:
                    for tag in transition_probabilities:
                        trans = (k) / (temp_tag_counter[tag] + k * no_of_tags) # node_.tag
                        p = math.log10(emission_probabilities['UNKNOWN-WORD'][tag]) + max([node.probability + math.log10(transition_probabilities[node.tag][tag]) for node in prev_word_tag_nodes])
                        max_node = max(prev_word_tag_nodes, key=lambda node_: node_.probability + math.log10(transition_probabilities[node_.tag][tag])) # for back pointer
                        append_tag = 'NOUN'
                        if word.endswith("ly") or word.endswith("hen"):
                            append_tag = 'ADV'
                        if word.endswith("ing") or word.endswith("ned"):
                            append_tag = 'VERB'
                        if word.endswith("ify") or word.endswith("ted") or word.endswith("ied") or word.endswith("are") or word.endswith("ved") or word.endswith("ned") or word.endswith("sed") or word.endswith("ed"):
                            append_tag = 'VERB'
                        if word.endswith("ish") or word.endswith("ive") or word.endswith("ous") or word.endswith("ful") or word.endswith("ral")  or word.endswith("cal")  or word.endswith("tic")  or word.endswith("ial") or (word.endswith("less") and word != "less") or (word.endswith("able") and word != "able"):
                            append_tag = 'ADJ' 
                        if word.endswith("mic"):
                            append_tag = 'ADJ' 
                        
                        if word.endswith("ize") or word.endswith("ake"):
                            append_tag = "VERB"

                        if word.endswith("ing"):
                            append_tag = 'VERB'
                        curr_word_tag_nodes.append(trellis_node(p, max_node, append_tag, word))
        
            prev_word_tag_nodes = curr_word_tag_nodes


        # backtracking for each sentence
        temp_reverse_sentence = []
        # print(prev_word_tag_nodes)
        curr_node = max(prev_word_tag_nodes, key=lambda node_: node_.probability)
        

        while curr_node != None:
            temp_reverse_sentence.append([curr_node.word, curr_node.tag])
            curr_node = curr_node.backpointer

        temp_reverse_sentence.reverse()

        for i in range(len(temp_reverse_sentence)):
            if temp_reverse_sentence[i][0].isdigit():
                temp_reverse_sentence[i][1] = "NUM"
            if temp_reverse_sentence[i][0] == "an" or temp_reverse_sentence[i][0] == "AN":
                temp_reverse_sentence[i][1] = "DET"
            if temp_reverse_sentence[i][0] == "and":
                temp_reverse_sentence[i][1] = "CONJ"

            # if temp_reverse_sentence[i][0].endswith("ist"):
            #     temp_reverse_sentence[i][1] = "NOUN"
            # if temp_reverse_sentence[i][0].endswith("ly"):
            #     temp_reverse_sentence[i][1] = "ADV"

        predicts.append(temp_reverse_sentence)

    # =================================================================================================================================================================

    return predicts