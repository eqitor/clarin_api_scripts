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
            bases = tok.getElementsByTagName('base')
            ctags = tok.getElementsByTagName('ctag')
            if anns:
                if anns[0].firstChild.data == '1':
                    unique = True
                else:
                    unique = False
                names_list.append({
                    'word': orth[0].firstChild.data,
                    'original': bases[0].firstChild.data,
                    'category': anns[0].getAttribute('chan'),
                    'unique': unique,
                    'speech': self.create_speech_list(ctags[0].firstChild.data)
                })
        return names_list

    def create_speech_list(self, ctag):
        """Takes ctag and returns splitted list with types
        :param ctag: given ctag
        :returns splitted_list: list of ctag types"""
        splitted_list = ctag.split(':')
        return splitted_list
