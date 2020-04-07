import random as rdm

class New_Password:

    def __init__(self):
        self.paswd_lenght = 0
        self.paswd_complement = []
        self.paswd_result = ""
        self.paswd_build = []
        self.special_chars = ['=', '(', ')', '{', '}', '[', ']', '´', '`', ';', ':', ',', '.', '<', '>', '/', '?', '°',
                              'º',
                              'ª', '^', '~', '|', '\\', '-', '¨', '¬', '+', "'", '"', '!', '§', '£', '¢', '³', '²', '¹',
                              '*']

    def generate (self, num_caracters, ad_comp = False, complemento = ""):
        """"
                classe para criar senha aleatória com o número de caracteres solicitados e podendo adicionar complementos
                recebe:
                num_caracteres = numero de caracteres (String)
                ad_comp = adicionar complemento (Boolean)
                complemento = string com caracteres que podem ser adicionados (String)
                """
        self.paswd_lenght = num_caracters
        self.paswd_result = ''
        self.paswd_build = []
        self.paswd_positions = []
        # constroi lista vazia da senha em construção e posições disponíveis
        for i in range(0, self.paswd_lenght):
            self.paswd_build.append("")
            self.paswd_positions.append(i)

        if ad_comp:
            for char in complemento:
                self.paswd_complement.append(char)

            for j in range(0, self.paswd_lenght):
                # chance de inserir o complemento do usuario
                chance = rdm.randint(0, 2)
                if chance == 1:
                    # adiciona caracter aleatorio do complemento do usuario
                    if len(self.paswd_complement) != 0:
                        char = self.paswd_complement[rdm.randint(0, len(self.paswd_complement) - 1)]
                        # verifica caracter válido e se não foi inserido
                        while (char in self.special_chars):
                            # exclui caracter se for especial
                            if char in self.special_chars:
                                self.paswd_complement.pop(self.paswd_complement.index(char))
                            # insere comlemento se houver ainda
                            if len(self.paswd_complement) != 0:
                                char = self.paswd_complement[rdm.randint(0, len(self.paswd_complement) - 1)]
                                self.paswd_complement.pop(self.paswd_complement.index(char))
                            else:
                                break
                    else:
                        char = chr(rdm.randint(33, 125))
                        tentativas = 0
                        while (char in self.paswd_build) or (char in self.special_chars):
                            char = chr(rdm.randint(33, 125))
                            if char not in self.special_chars and tentativas < 30:
                                break
                            tentativas += 1
                    # verifica se a posição está vazia
                    pos_verif = rdm.randint(0, len(self.paswd_positions) - 1)
                    index = self.paswd_positions[pos_verif]
                    if self.paswd_build[index] == '':
                        self.paswd_positions.pop(pos_verif)
                        self.paswd_build[index] = char

                else:
                    # verifica caracter válido e se não foi inserido ainda
                    char = chr(rdm.randint(33, 125))
                    tentativas = 0
                    while (char in self.paswd_build) or (char in self.special_chars):
                        char = chr(rdm.randint(33, 125))
                        if char not in self.special_chars and tentativas < 30:
                            if char in self.paswd_build:
                                char = chr(rdm.randint(33, 125))
                                break
                        tentativas += 1
                    # verifica se a posição está vazia
                    pos_verif = rdm.randint(0, len(self.paswd_positions) - 1)
                    index = self.paswd_positions[pos_verif]
                    if self.paswd_build[index] == '':
                        self.paswd_positions.pop(pos_verif)
                        self.paswd_build[index] = char

            for char in self.paswd_build:
                self.paswd_result = self.paswd_result + char
            return self.paswd_result
        else:
            try:
                for j in range(self.paswd_lenght):
                    # verifica caracter válido e se não foi inserido ainda
                    char = chr(rdm.randint(33, 125))
                    tentativas = 0
                    while (char in self.paswd_build) or (char in self.special_chars) :
                        char = chr(rdm.randint(33, 125))
                        if char not in self.special_chars and tentativas < 30:
                            break
                        tentativas += 1
                    # verifica se a posição está vazia
                    pos_verif = rdm.randint(0, len(self.paswd_positions) - 1)
                    index = self.paswd_positions[pos_verif]

                    # insere caracter se posição vazia e exclui posição das posições disponíveis
                    if self.paswd_build[index] == '':
                        self.paswd_positions.pop(pos_verif)
                        self.paswd_build[index] = char
                for char in self.paswd_build:
                    self.paswd_result = self.paswd_result + char
            except Exception as ex:
                print(ex.with_traceback())
            return self.paswd_result


