import csv

class TermoPL:

    def __init__(self, filepath):
        """Generates table from file."""
        self.table = []
        with open(filepath, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            for row in csv_reader:
                self.table.append(row)


    def get_data(self):
        """Returns table data in dictionary format"""
        data_list = []
        for row in self.table:
            data_list.append(
                {
                    'id': int(row[0]),
                    'word': row[2],
                    'original': self.remove_brackets(row[3]),
                    'rank': int(row[1]),
                    'cvalue': float(row[4]),
                    'freq_s': int(row[6]),
                    'freq_in': int(row[7]),
                    'context': int(row[8]),
                    'lenght': int(row[5])
                }
            )
        return data_list

    def remove_brackets(self, cell):
        return cell[1:-1]
