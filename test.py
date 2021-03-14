from TagerAPI import TagerAPI, Task
from time import sleep
api = TagerAPI()


text = """Woda jest jedną z najpospolitszych substancji we Wszechświecie.
Cząsteczka wody jest trzecią najbardziej rozpowszechnioną molekułą w ośrodku międzygwiazdowym, po cząsteczkowym wodorze i tlenku węgla. Jest również szeroko rozpowszechniona w Układzie Słonecznym: stanowi istotny element budowy Ceres i księżyców lodowych krążących wokół planet-olbrzymów, jako domieszka występuje w ich atmosferach, a przypuszcza się, że duże jej ilości znajdują się we wnętrzach tych planet. Jako lód występuje także na części planetoid, a zapewne również na obiektach transneptunowych. Woda jest bardzo rozpowszechniona także na powierzchni Ziemi. Występuje głównie w oceanach, które pokrywają 70,8% powierzchni globu, ale także w rzekach, jeziorach i w postaci stałej w lodowcach. Część wody znajduje się w atmosferze (chmury, para wodna). Niektóre związki chemiczne zawierają cząsteczki wody w swojej budowie (hydraty – określa się ją wówczas mianem wody krystalizacyjnej). Zawartość wody włączonej w strukturę minerałów w płaszczu Ziemi może przekraczać łączną zawartość wody w oceanach i innych zbiornikach powierzchniowych nawet dziesięciokrotnie. 
Woda występująca w przyrodzie jest roztworem soli i gazów. Najwięcej soli mineralnych zawiera woda morska i wody mineralne; najmniej woda z opadów atmosferycznych. Wodę o małej zawartości składników mineralnych nazywamy wodą miękką, natomiast zawierającą znaczne ilości soli wapnia i magnezu – wodą twardą. Oprócz tego wody naturalne zawierają rozpuszczone substancje pochodzenia organicznego, np. mocznik, kwasy humusowe itp."""
task = Task(text, 'any2txt|wcrft2({"guesser":false, "morfeusz2":true})')
while not task.is_ready():
    sleep(0.1)
result = task.download_file()
assert result.status_code == 200
