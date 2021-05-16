class WordCounter:

    @classmethod
    def count_words(cls, dictionary_data):
        """Counts words (base words) in given list of dictionaries obtained with Converter
        :param dictionary_data: dictionary data from Converter
        :returns counter_dictionary: dictionary with counted words (('word', 'ctag') : number of occurrences)"""
        counter_dictionary = {}
        for single_dictionary in dictionary_data:
            try:
                counter_dictionary[f"{single_dictionary['base']} {single_dictionary['ctag']}"] += 1
            except KeyError:
                counter_dictionary[f"{single_dictionary['base']} {single_dictionary['ctag']}"] = 1
        return counter_dictionary