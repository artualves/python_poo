import pickle
from typing import List
from common import *
import csv
from Interface_Eleicao import Transparencia

class Urna(Transparencia):
    mesario : Pessoa
    __secao : int
    __zona : int
    __eleitores_presentes : List[Eleitor] = []
    __votos = {} #dicionario chave = numero do candidato, valor é a quantidade de votos

    def __init__(self, mesario : Pessoa, secao : int, zona : int,
                 candidatos : List[Candidato], eleitores : List[Eleitor]):
        self.mesario = mesario
        self.__secao = secao
        self.__zona = zona
        self.__nome_arquivo = f'{self.__zona}_{self.__secao}.pkl'
        self.__candidatos = candidatos
        self.__eleitores = []
        for eleitor in eleitores:
            if eleitor.zona == zona and eleitor.secao == secao:
                self.__eleitores.append(eleitor)

        for candidato in self.__candidatos:
            self.__votos[candidato.get_numero()] = 0
        self.__votos['BRANCO'] = 0
        self.__votos['NULO'] = 0

        with open(self.__nome_arquivo, 'wb') as arquivo:
            pickle.dump(self.__votos, arquivo)

    def get_eleitor(self, titulo : int):
        for eleitor in self.__eleitores:
            if eleitor.get_titulo() == titulo:
                return eleitor
        return False

    def registrar_voto(self, eleitor : Eleitor, n_cand : int):
        self.__eleitores_presentes.append(eleitor)
        if n_cand in self.__votos:
            self.__votos[n_cand] += 1
        else:
            self.__votos['NULO'] += 1

        with open(self.__nome_arquivo, 'wb') as arquivo:
            pickle.dump(self.__votos, arquivo)

    def __str__(self):
        info =  f'Urna da seção {self.__secao}, zona {self.__zona}\n'
        info += f'Mesario {self.mesario}\n'
        return info

    def to_csv(self):
        with open(f'{self.__zona}_{self.__secao}.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Secao', 'Zona', 'Titulo dos E. Presentes'])

            for eleitorp in self.__eleitores_presentes:
                writer.writerow([self.__secao, self.__zona, eleitorp.get_titulo()])

    def to_txt(self):
        with open(f'{self.__zona}_{self.__secao}.txt', mode='w') as file:
            for eleitorp in self.__eleitores_presentes:
                file.write(eleitorp.__str__())

if __name__ == "__main__":
    c1 = Candidato("joao do coco", "1231231-3", "1231231-3", 99)
    c2 = Candidato("Maria", "2231231-3", "2231231-3", 66)

    e1 = Eleitor("jose", "234234-6", "234734-6", 1, 54, 272)
    e2 = Eleitor("mariana", "232234-6", "233734-6", 2, 54, 272)
    e3 = Eleitor("eleitor3", "532234-6", "533734-6", 3, 54, 272)

    urna = Urna(e3, 54, 272, [c1,c2], [e1,e2,e3])
    urna.registrar_voto(e1, 99)
    urna.to_csv()
    urna.to_txt()
    print(urna)