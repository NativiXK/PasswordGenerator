import generator
from googleAPI import SpreadSheets
from tabulate import tabulate
import copy

class Menu:

    def __init__(self):
        print("Abrindo banco de dados")
        self.__database = SpreadSheets()
        print("Lendo senhas armazenadas no banco")
        self.__senhas = self.__database.ler_senhas()
        print("Iniciando gerador de senhas")
        self.__new_pass = generator.New_Password()
        self.__passwd = None
        self.__alert = ''
        self.__comandos = {
            1 : self.__nova_senha,
            2 : self.__salvar_senha,
            3 : self.__visualizar_senhas,
            4 : self.__modificar_senha,
            5 : self.__remove_senha,
            6 : exit
        }

    def run(self):
        """
        Executa menu até o comando sair
        :return:
        """
        print("Carregando menu")
        return self.__mostra_menu()

    def __mostra_menu(self):
        """
        Exibe menu com ou sem a senha criada
        :return:
        """
        # mostra menu se não foi criado senha
        print(
                f"""            
{self.__alert}
1 - Criar nova senha;
2 - Salvar senha;
3 - Visualizar senhas;
4 - Modificar senha;
5 - Remover senha;
6 - Sair.""")
        self.__alert = ''
        try:
            return self.__verifica_comando(int(input("\n>>")))
        except ValueError:
            print("Insira um valor válido")
            return self.__mostra_menu()
        except KeyError:
            print("Insira um valor válido")
            return self.__mostra_menu()

    def __verifica_comando(self, index):
        self.__comandos[index]()
        return self.__mostra_menu()

    def __nova_senha(self):
        """
        Gera nova senha
        :return:
        """
        try:
            caracteres = int(input("\t> Quantos caracteres: "))
            ad_comp = None
            complemento = None
            if input("\t>Adicionar complemento: (s/n)").lower() == 's':
                ad_comp = True
            else:
                ad_comp = False
            if ad_comp:
                complemento = input("\t>Complemento: ")

            # cria nova senha
            self.__passwd = self.__new_pass.generate(caracteres, ad_comp, complemento)
            self.__alert = f"---Nova senha gerada: {self.__passwd}---"
        except:
            self.__alert = "---Erro ao criar a senha, tente novamente---"

    def __visualizar_senhas(self):
        """
        Visualiza as senhas guardadas
        :return:
        """
        try:
            self.__imprime_senhas()
            input("\nPressione qualquer tecla para continuar...")
        except:
            self.__alert = "---Erro ao visualizar senhas, tente novamente---"

    def __modificar_senha(self):
        if self.__senha_criada():
            self.__imprime_senhas()
            index = int(input("Indique o número da senha: "))
            login_index = self.__senhas[index][1]
            local_index = self.__senhas[index][0]
            print(f"Alterar senha de {login_index} em {local_index} por {self.__passwd}? (S/N)", end='')
            if input().lower() == 's':
                # atualiza senha na lista
                self.__senhas[index][2] = self.__passwd
                # solicita atualização do banco de dados
                print("Atualizando banco de dados")
                self.__database.atualiza_senha(self.__senhas)
        else:
            self.__alert = "---Crie uma nova senha primeiro---"

    def __salvar_senha(self):
        if self.__senha_criada():
            local_senha = input("De onde é a senha: ")
            login = input("Qual é o login: ")
            print("Salvando senha no banco de dados")
            self.__database.salvar_senha(local_senha, login, self.__passwd)
            print("Atualizando banco de dados local")
            self.__senhas = self.__database.ler_senhas()
            self.__alert = "Senha salvada com sucesso!"
            self.__passwd = None
        else:
            self.__alert = "--- Crie uma senha primeiro ---"

    def __senha_criada(self):
        return self.__passwd != None

    def __remove_senha(self):
        self.__imprime_senhas()
        index = int(input("Indique o número da senha: "))
        login_index = self.__senhas[index][1]
        print("Remover senha de ", login_index, "? (S/N)", end='')
        if input().lower() == 's':
            # atualiza senha na lista
            self.__senhas.pop(index)
            self.__senhas.append(['', '', ''])
            # solicita atualização do banco de dados
            print("Atualizando banco de dados")
            self.__database.atualiza_senha(self.__senhas)
            self.__senhas = self.__database.ler_senhas()

    def __imprime_senhas(self):
        # for local, login, senha in self.__senhas:
        #     if local == 'local' and senha == 'senha':
        #         print("\t> ", local, '\t\t\t\t\t\t', login, '\t\t\t\t\t\t\t\t', senha, " <")
        #         index += 1
        #         continue
        #     print(index, "\t> ", local, '\t\t\t\t\t\t', login, '\t\t\t\t\t\t\t\t', senha, " <")
        #     index += 1
        lista = copy.deepcopy(self.__senhas[1:])
        for i in range(len(lista)):
            lista[i].insert(0, i+1)
        print(tabulate(lista, headers=self.__senhas[0], tablefmt='orgtbl'))