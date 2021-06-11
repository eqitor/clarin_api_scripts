class WordCounter:

    allowed_ctags = {
        'subst', 'adj', 'adv'
    }

    @classmethod
    def count_words(cls, dictionary_data):
        """Counts words (base words) in given list of dictionaries obtained with Converter
        :param dictionary_data: dictionary data from Converter
        :returns counter_dictionary: dictionary with counted words (('word', 'ctag') : number of occurrences)"""
        counter_dictionary = {}
        for single_dictionary in dictionary_data:
            if ctag := WordCounter.is_ctag_correct(single_dictionary['ctag']):
                try:
                    counter_dictionary[f"{single_dictionary['base']} {ctag}"] += 1
                except KeyError:
                    counter_dictionary[f"{single_dictionary['base']} {ctag}"] = 1
        return counter_dictionary

    @classmethod
    def is_ctag_correct(cls, ctag):
        """Checks if given ctag string contains any of tags specified in ctag_filter list
        :param ctag: ctag string
        :returns : allowed tag if ctag contains any correct tag, else returns False
        """
        splitted_ctag = ctag.split(":")
        for tag in splitted_ctag:
            if tag in cls.allowed_ctags:
                return tag
        return False