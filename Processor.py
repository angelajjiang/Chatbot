from nltk import ne_chunk, pos_tag, word_tokenize
from nltk import Tree

class Processor:
    def parse_user_input(input):
        """
        Given a sentence as user input, tokenize, tag (part-of-speech),
        and lastly do name-entity chunking to obtain and return the
        corresponding nltk Tree.
        """
        tokens = nltk.word_tokenize(input)
        tagged = nltk.pos_tag(tokens)
        tree = nltk.ne_chunk(tagged)
        return tree


    def get_GPEs(tree):
        """
        Given a nltk Tree, return a list of all the GPE chunks.
        """
        GPEs = []
        current_GPE = []

        for child in tree:
            print(child, GPEs)
            if type(child) == Tree and child.label() == 'GPE':
                current_GPE.append(" ".join([token for token, pos in child.leaves()]))
            elif current_GPE:
                if child[1] == 'NNP':
                    current_GPE.append(child[0])
                else:
                    named_entity = " ".join(current_GPE)
                    if named_entity not in GPEs:
                        GPEs.append(named_entity)
                        current_GPE = []
        return GPEs

    def query(GPEs):
        if len(GPEs) != 1:
            #some time of error/feedback to user
            pass
        else:
            
