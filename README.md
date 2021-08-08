# Part-of-Speech classifier using Viterbi algorithm

Hidden Markov Model Part-of-Speech classifier using Viterbi algorithm

Part of ECE 448: Artificial Intelligence at the University of Illinois at Urbana-Champaign

Link to assignment: [MP4](https://courses.grainger.illinois.edu/ece448/sp2020/MPs/mp4/assignment4.html)

## Datasets

The code package contains two sets of training and development data

 - Brown corpus 
 - MASC corpus (from the Open American National Corpus)

## Tagset
We will use the following set of 16 part of speech tags for the classification

ADJ adjective
ADV adverb
IN preposition
PART particle (e.g. after verb, looks like a preposition)
PRON pronoun
NUM number
CONJ conjunction
UH filler, exclamation
TO infinitive
VERB verb
MODAL modal verb
DET determiner
NOUN noun
PERIOD end of sentence punctuation
PUNCT other punctuation
X miscellaneous hard-to-classify items

## Running Classifier
Here is an example of how to run the code on the Brown corpus data:

    python3 mp4.py --train data/brown-training.txt --test data/brown-dev.txt

## Viterbi 

The Viterbi tagger implements the HMM trellis (Viterbi) decoding algoirthm. That is, the probability of each tag depends only on the previous tag, and the probability of each word depends only on the corresponding tag. This model estimates three sets of probabilities:

 1. Initial probabilities (How often does each tag occur at the start of a sentence?) 
 2. Transition probabilities (How often does tag <img src="https://render.githubusercontent.com/render/math?math=t_a"> follow tag <img src="https://render.githubusercontent.com/render/math?math=t_b">?)
 3. Emission probabilities (How often does tag *t* yield word *w*?)

Processing happens in 5 steps:

 - Count occurrences of tags, tag pairs, tag/word pairs
 - Compute smoothed probabilities
 - Take the log of each probability
 - Construct the trellis.  
 - Return the best path through the trellis.

Laplace smoothing is used to smooth zero probability cases for calculating initial probabilities, transition probabilities, and emission probabilities.

This simple version of Viterbi will perform worse than the baseline code for provided dataset. However it's doing better on the multiple-tag words.

## Viterbi (with hapax word tags)

The above Vitebi tagger fails to beat the baseline because it does very poorly on unseen words. It's assuming that all tags have similar probability for these words, but we know that a new word is much more likely to have the tag NOUN than (say) CONJ. For this part, we improve our emission smoothing to match the real probabilities for unseen words.

Words that occur only once in the training data ("hapax" words) have a distribution similar to the words that appear only in the test/development data. These words are extracted from the training data to calculate the probability of each tag on them. When we do our Laplace smoothing of the emission probabilities for tag T, we scale Laplace smoothing constant by the corresponding probability of tag T occurs among the set hapax words. This optimized version of the Viterbi code should have a significantly better unseen word accuracy and also beat the overall accuracy for both baseline and the simple vertibi model. 
