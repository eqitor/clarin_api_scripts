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
                    'word': row[2].split(" "),
                    'original': self.remove_brackets(row[3]),
                    'rank': int(row[1]),
                    'cvalue': float(row[4]),
                    'length': int(row[5])
                }
            )
        return data_list

    def remove_brackets(self, cell) -> str:
        return cell[1:-1]
