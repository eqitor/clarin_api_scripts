class WordCounter:

    @classmethod
    def count_words(cls, dictionary_data):
        """Counts words (base words) in given list of dictionaries obtained with Converter
        :param dictionary_data: dictionary data from Converter
        :returns counter_dictionary: dictionary with counted words ('word' : number of occurrences)"""
        counter_dictionary = {}
        for single_dictionary in dictionary_data:
            try:
                counter_dictionary[single_dictionary['base']] += 1
            except KeyError:
                counter_dictionary[single_dictionary['base']] = 1
        return counter_dictionary
