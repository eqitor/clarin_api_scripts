from TagerAPI import TagerAPI, Task
from time import sleep
from processing import CorpusProcessing




# api = TagerAPI()


text = """Woda jest jedną z najpospolitszych substancji we Wszechświecie.
Cząsteczka wody jest trzecią najbardziej rozpowszechnioną molekułą w ośrodku międzygwiazdowym, po cząsteczkowym wodorze i tlenku węgla. Jest również szeroko rozpowszechniona w Układzie Słonecznym: stanowi istotny element budowy Ceres i księżyców lodowych krążących wokół planet-olbrzymów, jako domieszka występuje w ich atmosferach, a przypuszcza się, że duże jej ilości znajdują się we wnętrzach tych planet. Jako lód występuje także na części planetoid, a zapewne również na obiektach transneptunowych. Woda jest bardzo rozpowszechniona także na powierzchni Ziemi. Występuje głównie w oceanach, które pokrywają 70,8% powierzchni globu, ale także w rzekach, jeziorach i w postaci stałej w lodowcach. Część wody znajduje się w atmosferze (chmury, para wodna). Niektóre związki chemiczne zawierają cząsteczki wody w swojej budowie (hydraty – określa się ją wówczas mianem wody krystalizacyjnej). Zawartość wody włączonej w strukturę minerałów w płaszczu Ziemi może przekraczać łączną zawartość wody w oceanach i innych zbiornikach powierzchniowych nawet dziesięciokrotnie. 
Woda występująca w przyrodzie jest roztworem soli i gazów. Najwięcej soli mineralnych zawiera woda morska i wody mineralne; najmniej woda z opadów atmosferycznych. Wodę o małej zawartości składników mineralnych nazywamy wodą miękką, natomiast zawierającą znaczne ilości soli wapnia i magnezu – wodą twardą. Oprócz tego wody naturalne zawierają rozpuszczone substancje pochodzenia organicznego, np. mocznik, kwasy humusowe itp."""
text2 = """Dodatni wynik na obecność przeciwciał przeciw SARS-CoV-2 w klasie IgG jest tylko potwierdzeniem kontaktu, a niekoniecznie przebycia choroby – stwierdził lekarz Bartosz Fiałek w rozmowie z portalem Medonet.

W jego ocenie testy na pewno będą chętnie kupowane, ale ich walor jest przede wszystkim dydaktyczny. Mogą też zadziałać uspokajająco w razie uzyskania dodatniego wyniku w klasie IgG.

Wynik testu nie pozwoli zdobyć statusu ozdrowieńca, nie pozwoli też lecieć bez kwarantanny do innych krajów."""
#option = 'any2txt|wcrft2({"guesser":false, "morfeusz2":true})'
#option = 'any2txt|wcrft2|liner2({"model":"n82"})'

options = ['any2txt|wcrft2|liner2({"model":"n82"})', 'any2txt|wcrft2({"guesser":false, "morfeusz2":true})']
documents = [text, text2]
process = CorpusProcessing(documents,options)
print(process.process_corpus())



# task = Task(text, option)
# while not task.is_ready():
#     print(task.get_progress())
#     sleep(0.5)
# result = task.download_file()
# assert result.status_code == 200
# print(result.text)