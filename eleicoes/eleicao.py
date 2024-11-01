import pickle
import csv
from typing import List
from common import *
from Interface_Eleicao import Transparencia
import tkinter as tk
from tkinter import ttk, messagebox

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

    def get_eleitores(self):
        return [eleitor.get_titulo() for eleitor in self.__eleitores]
    
    def verificar_candidato(self, numero):
        return any(candidato.get_numero() == numero for candidato in self.__candidatos)

    def registrar_voto(self, eleitor : Eleitor, n_cand : int):
        self.__eleitores_presentes.append(eleitor)
        if n_cand == "NULO" or n_cand == "BRANCO":
            self.__votos[n_cand] += 1
        else:
            if n_cand in self.__votos:
                self.__votos[n_cand] += 1
            else:
                self.__votos[n_cand] = 1

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

class InterfaceUrna:
    def __init__(self, urna: Urna):
        self.urna = urna

        self.root = tk.Tk()
        self.root.title("Urna Eleitoral")

        lbl_eleitor = tk.Label(self.root, text="Eleitores")
        lbl_eleitor.pack(padx=10, pady=5)

        self.eleitores_combobox = ttk.Combobox(self.root)
        self.eleitores_combobox.pack(padx=10, pady=10)
        
        self.dados_eleitor_label = tk.Label(self.root, text="Zona:\nSeção:")
        self.dados_eleitor_label.pack(padx=10, pady=5)

        lbl_candidato = tk.Label(self.root, text="Número do Candidato (00 para Nulo)")
        lbl_candidato.pack(padx=10, pady=5)
        
        self.candidato_entry = tk.Entry(self.root)
        self.candidato_entry.pack(padx=10, pady=10)

        votar_button = tk.Button(self.root, text="Votar", command=self.registrar_voto)
        votar_button.pack(padx=10, pady=10)

        self.carregar_eleitores()

        # Seleção da Combobox
        self.eleitores_combobox.bind("<<ComboboxSelected>>", self.exibir_dados_eleitor)

        self.root.mainloop()

    def carregar_eleitores(self):
        eleitores_titulos = self.urna.get_eleitores()
        self.eleitores_combobox['values'] = eleitores_titulos

    def exibir_dados_eleitor(self, event):
        # Exibe a zona e a seção do eleitor selecionado na Label
        titulo_selecionado = self.eleitores_combobox.get()
        
        eleitor = next((eleitor for eleitor in self.urna._Urna__eleitores if eleitor.get_titulo() == int(titulo_selecionado)), None)
        
        if eleitor:
            self.dados_eleitor_label.config(text=f"Zona: {eleitor.zona}\nSeção: {eleitor.secao}")
        else:
            self.dados_eleitor_label.config(text="Eleitor não encontrado")

    def registrar_voto(self):
        # Registra o voto do eleitor selecionado e limpa a interface
        titulo_selecionado = self.eleitores_combobox.get()
        numero_candidato = self.candidato_entry.get().strip()
        
        if not titulo_selecionado:
            messagebox.showerror("Erro", "Por favor, selecione um eleitor.")
            return
        
        # Encontrar o eleitor pelo título
        eleitor = next((eleitor for eleitor in self.urna._Urna__eleitores if eleitor.get_titulo() == int(titulo_selecionado)), None)
        
        if numero_candidato == "00":
            n_cand = "NULO"
        else:
            try:
                n_cand = int(numero_candidato)
                if not self.urna.verificar_candidato(n_cand):
                    n_cand = "BRANCO"
            except ValueError:
                messagebox.showerror("Erro", "O número do candidato deve ser um número válido ou '00' para nulo.")
                return

        self.urna.registrar_voto(eleitor, n_cand)

        self.eleitores_combobox.set('')
        self.dados_eleitor_label.config(text="Zona:\nSeção:")
        self.candidato_entry.delete(0, tk.END)

        messagebox.showinfo("Voto Registrado", "Voto registrado com sucesso!")


if __name__ == "__main__":
    c1 = Candidato("joao do coco", "1231231-3", "1231231-3", 99)
    c2 = Candidato("Maria", "2231231-3", "2231231-3", 66)

    e1 = Eleitor("jose", "234234-6", "234734-6", 156, 54, 272)
    e2 = Eleitor("mariana", "232234-6", "233734-6", 274, 54, 272)
    e3 = Eleitor("eleitor3", "532234-6", "533734-6", 2342, 54, 272)

    urna = Urna(e3, 54, 272, [c1,c2], [e1,e2,e3])
    urna.registrar_voto(e1, 99)
    app = InterfaceUrna(urna)
    urna.to_csv()
    urna.to_txt()
    print(urna)