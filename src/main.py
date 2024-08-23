from frota import *

def operar_carro(carro : Carro):
    print('1- Ligar motor')
    print('2- Desligar motor')
    print('3- Acelerar')
    op = 0
    while op not in (1, 2, 3):
        op = int(input("Digite as opcoes[1-3]: "))
    if carro == carro1:
        if op == 1:
            carro1.ligar()
        elif op == 2:
            carro1.desligar()
        elif op == 3:
            v = float(input("Informe a velocidade: "))
            t = float(input("Informe o tempo: "))
            carro1.acelerar(v, t)

            print('Infos atuais do carro')
            print(carro1)
    else:
        if op == 1:
            carro2.ligar()
        elif op == 2:
            carro2.desligar()
        elif op == 3:
            v = float(input("Informe a velocidade: "))
            t = float(input("Informe o tempo: "))
            carro2.acelerar(v, t)

            print('Infos atuais do carro')
            print(carro2)

if __name__ == "__main__":
    print('Cadastre um carro')
    nm_modelo = input('Digite o modelo: ')
    nm_marca = input('Digite a marca: ')
    nm_cor = input('Digite a cor: ')

    carro1 = Carro(nm_modelo, nm_marca, nm_cor, 0.0, motor=True)

    print('Cadastre outro carro')
    nm_modelo = input('Digite o modelo: ')
    nm_marca = input('Digite a marca: ')
    nm_cor = input('Digite a cor: ')

    carro2 = Carro(nm_modelo, nm_marca, nm_cor, 0.0, motor=True)

    '''
    Controlando os carros até 600 Km
    '''

    while carro1.odometro < 600 and carro2.odometro < 600:
        try:
            op_carro = 0
            while op_carro not in (1,2):
                op_carro = int(input('Escolha um carro [1,2]: '))

            if op_carro == 1:
                operar_carro(carro1)
                print('Carro 1\n')
            else:
                operar_carro(carro2)
                print('Carro 2\n')
        except Exception as e:
            print("Erro!")
            print(e)

    carro1.desligar()
    carro2.desligar()
    if carro1.odometro > carro2.odometro:
        print(carro1)
    else:
        print(carro2)

