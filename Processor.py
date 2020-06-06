from nltk import ne_chunk, pos_tag, word_tokenize
from nltk import Tree

# class Processor:
food_kws = set(['eat', 'food', 'restaurant', 'brunch', 'dinner', 'lunch'])
stay_kws = set(['hotel', 'airbnb', 'stay'])
shop_kws = set(['shop', 'shopping', 'buy', 'mall', 'store'])
activ_kws = set(['do', 'activities', 'go'])
excluded_pos = set(['WP', 'JJ', 'IN', 'VBZ', 'PRP'])

def get_tagged(input):
    """
    Given a sentence as user input, tokenize the input and
    tag (part-of-speech) the word tokens.
    """
    tokens = word_tokenize(input)
    tagged = pos_tag(tokens)
    return tagged

def get_category(tagged_input): #make all lower case
    """
    Given a input with tagged part of speech, return a list of
    categories (valid Facebook Places API categories) that the input
    is related to.
    """
    for word, tag in tagged_input:
        included = tag not in excluded_pos
        if tag not in excluded_pos:
            word = word.lower()
            if word in food_kws:
                return ["FOOD_BEVERAGE"]
            elif word in stay_kws:
                return ["HOTEL_LODGING"]
            elif word in shop_kws:
                return ["SHOPPING_RETAIL"]
            elif word in activ_kws:
                return ["ARTS_ENTERTAINMENT", "FITNESS_RECREATION"]
    return ["FOOD_BEVERAGE", "HOTEL_LODGING", "SHOPPING_RETAIL", "ARTS_ENTERTAINMENT", "FITNESS_RECREATION"]

def get_GPEs(tagged):
    """
    Given a sentence as user input, tokenize, tag (part-of-speech),
    and lastly do name-entity chunking to obtain and return the
    corresponding nltk Tree. Then the nltk Tree is parsed, returning
    a list of all the GPE chunks.
    """
    tree = ne_chunk(tagged)
    GPEs = []
    current_GPE = []
    prev_was_GPE = False
    prev_comma = False

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
        #update the flags at the end of each loop
        prev_was_GPE = True if type(child) == Tree and child.label() == 'GPE' else False
        prev_comma = True if child[1] == ',' else False

    return GPEs

def query(GPEs, categories): #can only query given GPEs
    """
    Main query function: given the list of GPEs and categories,
    check the inputs and query the location to recommend. The
    recommended location name is returned.
    """
    if len(GPEs) != 1:
        if len(GPEs) < 1:
            raise ValueError("Please specify at least one location of interest for your query!")
        else:
            raise ValueError("Please specify only one location of interest for your query!")
    else:
        return query_location(GPEs, categories)
