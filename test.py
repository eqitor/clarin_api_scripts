from app.clarinAPI.TermoPL import TermoPL
import os, json


# tager_dir_path = os.path.join("temp", self.corpus_id, "tager", "converted")
# file_list = os.listdir(tager_dir_path)
# dir_path = os.path.join("temp", self.corpus_id, "termopl")
# os.makedirs(dir_path, exist_ok=True)
# zf.extractall(dir_path)
# csv_path = os.path.join(dir_path, "dane", "terms.csv")
# converter = TermoPL(csv_path)
# termopl_dict = converter.get_data()
# for file in file_list:
#     termopl_dict = {}
#     tager_path = os.path.join(tager_dir_path, file)
#     path = os.path.join(dir_path, file)
#     with open(tager_path, 'r') as tf:
#         tager_dict = json.load(tf)
#         logging.error(tager_dict)
#     with open(path, 'w') as out:
#         json.dump(termopl_dict, out)




csv_path = "termos.csv"
converter = TermoPL(csv_path)
termopl_dict = converter.get_data()
tager = "C:\\Studia\\II\\sem_1\\gospodarka\\clarin_api_scripts\\temp\\60c26fef68e6dcafc41d2896\\tager\\converted\\0a0c2c62fc9f7a4f3297d19f4518ac9c"
with open(tager, 'r') as tf:
    tager_dict = json.load(tf)
    # print(tager_dict)
# for i in termopl_dict:
#     if i["original"] == "proces produkcji":
#         print(i["original"])
#print(termopl_dict)

def get_termopl_for_file(tager_list:list ,termopl_dict:list):
    out = {}
    for i, tager in enumerate(tager_list):
        for termopl in termopl_dict:
            if tager['base'] == termopl['word'][0]:
                #print(f"{tager['base']}, {termopl['word'][0]},  {termopl['word'][1]}")
                if confirm_multiword(tager_list,i,termopl):
                    try:
                        out[termopl['original']]['count'] += 1
                    except KeyError:
                        out[termopl['original']] = termopl
                        out[termopl['original']]['count'] = 1
    return out


def confirm_multiword(tager_list, index ,termopl) -> bool:
    length = termopl['length']
    for i in range(length):
        if termopl['word'][i] != tager_list[index+i]['base']:
            return False
    return True
get_termopl_for_file(tager_dict,termopl_dict)
