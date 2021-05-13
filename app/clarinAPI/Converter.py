from xml.dom import minidom
import json


class Converter:

    default_ctags = [
        'subst', 'adj', 'adv'
    ]

    allowed_ctags = [
        'subst', 'adj', 'adv'
    ]

    def convert(self, filepath, ctag_list):
        """Converts XML processing results to list of dictionaries with ctag filtering.
        :param filepath: path to XML data
        :param ctag_list: list of ctags allowed in output list. If None, function returns subbst, adj and adv ctags.
        :returns ortho_list: list of dictionaries"""

        mydoc = minidom.parse(filepath)
        toks = mydoc.getElementsByTagName('orth')
        bases = mydoc.getElementsByTagName('base')
        ctags = mydoc.getElementsByTagName('ctag')

        ortho_list = []
        for tok, base, ctag in zip(toks, bases, ctags):
            if allowed_tag := self.is_ctag_correct(ctag.firstChild.data, ctag_list):
                new_dictionary = {
                    'orth': tok.firstChild.data,
                    'base': base.firstChild.data,
                    'ctag': allowed_tag,
                }
                ortho_list.append(new_dictionary)

        return ortho_list

    def is_ctag_correct(self, ctag, ctag_list):
        """Checks if given ctag string contains any of tags specified in ctag_filter list
        :param ctag: ctag string
        :param ctag_list: list of ctags allowed in output. If None, function returns subbst, adj and adv ctags.
        :returns : allowed tag if ctag contains any correct tag, else returns False
        """
        splitted_ctag = ctag.split(":")
        for tag in splitted_ctag:
            if tag in ctag_list:
                return tag
        return False

    def validate_ctag_list(self, ctag_list):
        """Checks if given ctag list contains unavailable ctags
        :param ctag: list of ctags"""
        for ctag in ctag_list:
            if ctag not in Converter.allowed_ctags:
                raise Exception(f"{ctag} is not on allowed_ctags list.")


    def to_json(self, filepath, ctag_list=default_ctags):
        """Converts XML processing data to JSON with ctag filtering.
        :param filepath: path to XML data
        :param ctag_list: list of ctags allowed in JSON. If None, function returns subbst, adj and adv ctags.
        :returns json_entity: data in JSON format"""
        self.validate_ctag_list(ctag_list)
        converted_xml = self.convert(filepath, ctag_list)
        json_entity = json.dumps(converted_xml)

        return json_entity
