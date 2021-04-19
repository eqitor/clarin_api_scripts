from xml.dom import minidom
import json


class Converter:

    def convert(self, filepath):
        """Converts XML processing results to list of dictionaries.
        :param filepath: path to XML data
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
        """Converts XML processing data to JSON
        :param filepath: path to XML data
        :returns json_entity: data in JSON format"""

        converted_xml = self.convert(filepath)
        json_entity = json.dumps(converted_xml)

        return json_entity
