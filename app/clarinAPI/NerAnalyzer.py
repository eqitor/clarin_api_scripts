from xml.dom import minidom

class NerAnalyzer:

    def find_names(self, filepath):
        """Finds own names in given XML file obtained by Ner API. Returns names founded and
        its "chan" type parameter.
        :param filepath: path to XML data
        :returns names_list: list of dictionaries"""
        mydoc = minidom.parse(filepath)
        toks = mydoc.getElementsByTagName('tok')

        names_list = []
        for tok in toks:
            orth = tok.getElementsByTagName('orth')
            anns = tok.getElementsByTagName('ann')
            if anns:
                if anns[0].firstChild.data == '1':
                    names_list.append({
                        'orth': orth[0].firstChild.data,
                        'chan': anns[0].getAttribute('chan'),
                        'head': anns[0].getAttribute('head')
                    })
        return names_list
