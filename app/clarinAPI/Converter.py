from xml.dom import minidom
import json


class Converter:

    def convert(self, filepath):
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
            new_dictionary = {
                'orth': tok.firstChild.data,
                'base': base.firstChild.data,
                'ctag': ctag.firstChild.data,
            }
            ortho_list.append(new_dictionary)
        return ortho_list


    def to_json(self, filepath):
        """Converts XML processing data to JSON with ctag filtering.
        :param filepath: path to XML data
        :param ctag_list: list of ctags allowed in JSON. If None, function returns subbst, adj and adv ctags.
        :returns json_entity: data in JSON format"""
        converted_xml = self.convert(filepath)
        json_entity = json.dumps(converted_xml)

        return json_entity
