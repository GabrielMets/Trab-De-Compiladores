import pandas as pd

# Autores: Leonardo Balan e Gabriel Santos da Silva

# Analisador Lexico - Compiladores
#Linguagem de Programaçao: GLprog

#Inicio


#------------------------------------- Lexico -------------------------------------------

#Lista para armazenar a tabela de Tokens(Token, Lexema)
tabela_de_tokens = []

#Automato de Reconhecimento
#Estados e transicoes do automato
def transicao(estado, caracter):
    if estado == 'e1': 
        if 'A' <= caracter <= 'Z':
          return 'e2'
        if '0' <= caracter <= '9':
          return 'e11'
        if 'a' <= caracter <= 'z':
          return 'e4'
        if caracter == '!':
          return 'e6'
        if caracter == ' ' or caracter == '\n':
          return 'e9'
        if caracter == '(':
          return 'e16'
        if caracter == ')':
          return 'e17'
        if caracter == '.':
          return 'e18'
        if caracter in '+-*/': # '+' ou '-' ou '*' ou '/'
          return 'e19'
        if caracter in '><':
          return 'e20'
        if caracter == '^':
          return 'e21'
        if caracter == '{':
          return 'e27'
        if caracter == '}':
          return 'e28'
        return 'e10'  # Qualquer outro caracter vai para o estado e10 (erro)
    elif estado == 'e2': 
        if 'A' <= caracter <= 'Z': 
          return 'e2'
        if caracter == '_':
          return 'e2'
        if caracter == ' ' or caracter == '\n':
          return 'e3'
        return 'e25' # Erro, ID invalido
    elif estado == 'e4':
        if '0' <= caracter <= '9':
          return 'e4'
        if 'a' <= caracter <= 'z':
          return 'e4'
        if caracter == ' ' or caracter == '\n':
          return 'e5'
        return 'e26' # Erro, nome_var invalido'
    elif estado == 'e6':
        if caracter == '!':
          return 'e7'
        return 'e10'
    elif estado == 'e7':
        if caracter in ('\n', '\r'):  # Se encontrar quebra de linha, finaliza o comentário
          return 'e8'
        return 'e7'  # Continua consumindo caracteres normalmente
    elif estado == 'e11':
        if '0' <= caracter <= '9':
          return 'e11'
        if caracter == ',':
          return 'e13'
        if caracter == ' ' or caracter == '\n':
          return 'e12'
        return 'e24' #Erro, numero invalido
    elif estado == 'e13':
        if '0' <= caracter <= '9':
          return 'e14' 
        return 'e24' #Erro, numero invalido
    elif estado == 'e14':
        if '0' <= caracter <= '9':
          return 'e14'
        if caracter == ' ' or caracter == '\n':
          return 'e15'
        return 'e24' #Erro, numero invalido
    elif estado == 'e21':
      if caracter != '^':
        return 'e22'
      if caracter == '^':
        return 'e23'
    elif estado == 'e22':
        if caracter != '^':
          return 'e22'
        if caracter == '^':
          return 'e23'

# Estado Inicial
estado_inicial = 'e1'
#Estado de erro
estado_erro = 'e10'
# Estados de Aceitacao (reconhecimento)
estado_final = {
    'e3': 'ID',
    'e5': 'Variavel',
    'e8': 'Comentario',
    'e9': 'Espaco',
    'e10': 'ERRO, caracter_invalido',
    'e12': 'Num_inteiro',
    'e15': 'Num_real',
    'e16': '(',
    'e17': ')',
    'e18': '.',
    'e19': 'op_arit',
    'e20': 'op_relacional',
    'e23': 'Caracter',
    'e24': 'ERRO, numero_invalido',
    'e25': 'ERRO, ID_invalido',
    'e26': 'ERRO, nome_var_invalido',
    'e27': '{',
    'e28': '}'
}

# Modifica a função processar_codigo para evitar salvar comentários e espaços
def processar_codigo(codigo):
    estado = estado_inicial  # estado de inicio de exec
    lexema = ''  # var para armazenar o lexema
    linha = 1  # var para armazenar a linha atual

    with open(codigo, 'r') as codigo:  # Ler o arq
        while True:
            caracter = codigo.read(1)  # Lendo caractere por caractere
            if not caracter:
                if lexema:
                    # Processa o último lexema ao final do arquivo
                    if estado in estado_final:
                        token = estado_final[estado]
                        if token not in {'Comentario', 'Espaco'}:  # Ignora comentário e espaço
                            tabela_de_tokens.append((token, lexema.strip(), linha))
                    else:
                        tabela_de_tokens.append(('ERRO, Caracter Invalido', lexema.strip(), linha))
                break

            # Incrementa a linha se encontrar nova linha
            if caracter == '\n':
                linha += 1

            novo_estado = transicao(estado, caracter)

            if novo_estado:
                if novo_estado == estado_erro:
                    if lexema:
                        # Adiciona o token acumulado até o erro
                        if estado in estado_final:
                            token = estado_final[estado]
                            if token not in {'Comentario', 'Espaco'}:  # Ignora comentário e espaço
                                tabela_de_tokens.append((token, lexema.strip(), linha))
                        else:
                            tabela_de_tokens.append(('ERRO, caracter invalido', lexema.strip(), linha))

                    # Adiciona o caractere atual como erro
                    tabela_de_tokens.append(('ERRO, caracter invalido', caracter, linha))

                    # Reinicia o estado
                    estado = estado_inicial
                    lexema = ''

                elif novo_estado in estado_final:
                    lexema += caracter  # Adiciona o caractere ao lexema
                    token = estado_final[novo_estado]
                    if token not in {'Comentario', 'Espaco'}:  # Ignora comentário e espaço
                        tabela_de_tokens.append((token, lexema.strip(), linha))

                    # Reinicia o estado
                    estado = estado_inicial
                    lexema = ''
                else:
                    estado = novo_estado
                    lexema += caracter  # Adiciona caractere ao lexema

            else:
                # Estado inválido, trata o lexema atual como erro
                if lexema:
                    if estado in estado_final:
                        token = estado_final[estado]
                        tabela_de_tokens.append((token, lexema.strip(), linha))
                    else:
                        tabela_de_tokens.append(('ERRO', lexema.strip(), linha))

                # Adiciona o caractere atual como erro
                tabela_de_tokens.append(('ERRO', caracter, linha))

                # Reinicia o estado
                estado = estado_inicial
                lexema = ''

processar_codigo('codigo.txt')

#print ("Tabela de Tokens (Token, Lexema):\n")
#for token in tabela_de_tokens:
  #print(token)

#Dic para obter_token()
Tipos_id = {
    'VAZIO_DECLS': 'VAZIO_DECLS',
    'VAZIO_INSTRUCOES': 'VAZIO_INSTRUCOES',
    'SENAO_VAZIO': 'SENAO_VAZIO',
    'SE': 'SE',
    'SENAO': 'SENAO',
    'DURANTE': 'DURANTE',
    'PARA': 'PARA',
    'INTEIRO': 'INTEIRO',
    'REAL': 'REAL',
    'CARACTER': 'CARACTER',
    'ZEROUM': 'ZEROUM',
    'AND': 'Op_logico',
    'OR': 'Op_logico',
    'RECEBA': 'RECEBA',
    'RECEBAT': 'RECEBAT',
    'ESCREVA': 'ESCREVA',
    'INICIO': 'INICIO',
    'FIM': 'FIM',
    'INC': 'INC',
    'DIF': 'op_relacional',
    'IGUAL': 'op_relacional',
}

# Func para obter o token correto pros ID
def obter_token(lexema):
    return Tipos_id.get(lexema, 'ID')

# Lista para armazenar os tokens atualizados
tokens_atualizados = []

# Substitui 'ID' pelo token correto com base no lexema
for token, lexema, linha in tabela_de_tokens:
    if token == 'ID':
        novo_token = obter_token(lexema)
        tokens_atualizados.append((novo_token, lexema, linha))
    else:
        tokens_atualizados.append((token, lexema, linha))

print("\n Tabela de Tokens: \n")
for token in tokens_atualizados:
    print(token[0])

print()

# ------------------------------- Sintático ---------------------------------------

def carregar_tabela_SLR(arq):
    #Carrega a planilha
    tabela = pd.read_excel(arq, index_col=0)  # index_col=0 define a primeira coluna como os estados
    return tabela

# arq excel
arq = 'Tabela_SLR4.xlsx'
tabela_SLR = carregar_tabela_SLR(arq)
print("Tabela SLR Carregada.")
print()

#Interpretar E, R, AC e desvios da tabela
def interpretar_entrada_tabela(entrada):
    if isinstance(entrada, str): #Verifica se a entrada é uma string para identificar empilha/reduz/aceita
        
        if entrada.startswith('E'):
            return ('empilha', int(entrada[1:]))
        
        elif entrada.startswith('R'):
            return ('reduz', int(entrada[1:]))
        
        elif entrada == 'AC':
            return ('aceita',)
    
    elif isinstance(entrada, (int, float)):
        #Entrada apenas de um numero representa um desvio
        return ('desvio', int(entrada))
    
    #Se a entrada nao é reconhecida, retorna None para erro de interpretaçao
    return None

#Gramatica
producoes = {
    0: ('<programa`>', ['<programa>']),
    1: ('<programa>', ['INICIO', '<decls_opt>', '<instrucoes_opt>', 'FIM']),
    2: ('<decls_opt>', ['<decls>']),
    3: ('<decls_opt>', ['VAZIO_DECLS']),  # Ɛ
    4: ('<decls>', ['<decl>','<decls>']),
    5: ('<decls>', ['<decl>']),
    6: ('<decl>', ['Variavel', '<tipo>', '.']),
    7: ('<decl>', ['Variavel', '<atrib>']),
    8: ('<tipo>', ['INTEIRO']),
    9: ('<tipo>', ['REAL']),
    10: ('<tipo>', ['CARACTER']),
    11: ('<tipo>', ['ZEROUM']),
    12: ('<instrucoes_opt>', ['<instrucoes>']),
    13: ('<instrucoes_opt>', ['VAZIO_INSTRUCOES']),
    14: ('<instrucoes>', ['<instrucao>', '<instrucoes>']),
    15: ('<instrucoes>', ['<instrucao>']),  # Ɛ
    16: ('<instrucoes>', ['<decls>']),
    17: ('<instrucao>', ['<atrib>']),
    18: ('<instrucao>', ['<atrib_teclado>']),
    19: ('<instrucao>', ['<escrever>']),
    20: ('<instrucao>', ['<condicional_se>']),
    21: ('<instrucao>', ['<loop_durante>']),
    22: ('<instrucao>', ['<loop_para>']),
    23: ('<atrib>', ['RECEBA', '<expr>', '.']),
    24: ('<atrib_teclado>', ['RECEBAT', 'Variavel', '.']),
    25: ('<escrever>', ['ESCREVA', '(', '<expr>', ')', '.']),
    26: ('<condicional_se>', ['SE', '(', '<expr>', ')', '{', '<instrucoes>', '}', '<senao_op>']),
    27: ('<senao_op>', ['SENAO', '{', '<instrucoes>', '}']),
    28: ('<senao_op>', ['SENAO_VAZIO']),  # Ɛ
    29: ('<loop_durante>', ['DURANTE', '(', '<expr>', ')', '{', '<instrucoes>', 'Variavel', '<inc_dec>', '}']),
    30: ('<loop_para>', ['PARA', '(', '<atrib>', '.', '<expr>', '.', 'Variavel', '<inc_dec>', ')', '{', '<instrucoes>', '}']),
    31: ('<condicao>', ['<expr>', '<op_relacional>', '<expr>']),
    32: ('<inc_dec>', ['INC']),
    33: ('<inc_dec>', ['DEC']),
    34: ('<inc_dec>', ['op_arit', 'Num_inteiro']),
    35: ('<expr>', ['<term>', '<op>', '<term>']),
    36: ('<expr>', ['<term>']),
    37: ('<term>', ['Variavel']),
    38: ('<term>', ['Num_inteiro']),
    39: ('<term>', ['Num_real']),
    40: ('<term>', ['Caracter']),
    41: ('<term>', ['ZEROUM']),
    42: ('<op>', ['op_relacional']),
    43: ('<op>', ['op_arit']),
    44: ('<op>', ['op_logico']),
    45: ('<decl>', ['Variavel', '<inc_dec>']),
}


def analisador_sintatico_bottom_up(tokens1, tabela_SLR, producoes):
    pilha = [0]
    cursor = 0

    while cursor < len(tokens1):
        estado_atual = pilha[-1]  
        token_atual = tokens1[cursor][0]  
        #print("Estado atual:", estado_atual)
        #print("Token atual:", token_atual)
        #print("Pilha:", pilha)
        #print()

        if estado_atual == 71 and token_atual == '}': #look ahead
           #print('caso expecial')
           pilha.pop()
           pilha.extend(['Variavel', '<inc_dec>', 95])
           #print(pilha)
           estado_atual = pilha[-1]

        #Variavel <inc_dec>
        if token_atual in tabela_SLR.columns and not pd.isna(tabela_SLR.loc[estado_atual, token_atual]):
            acao = interpretar_entrada_tabela(tabela_SLR.loc[estado_atual, token_atual])
        else:

          
          print(f"Erro: Token '{token_atual}' não encontrado na tabela ou entrada inválida para o estado {estado_atual}.")
          #print(tabela_SLR.loc[estado_atual, token_atual])
          return False

        #print("Ação:", acao)
        #print()

        if acao is None:
            print(f"Erro sintático: token inesperado '{token_atual}' na linha {tokens1[cursor][2]}")
            return False
        
        elif acao[0] == 'aceita':
            print("Aceitação: análise sintática concluída com sucesso.")
            return True
        
        elif acao[0] == 'empilha':
          novo_estado = acao[1]  
            
            
          pilha.append(token_atual)  
          pilha.append(novo_estado)  
          cursor += 1  
          #print(pilha)

        elif acao[0] == 'reduz':
            if acao[1] == 30:
              #print('eita')
              pilha = pilha[:-2]
              #print(pilha)

            num_producao = acao[1]
            nao_terminal, producao = producoes[num_producao]
            tamanho_producao = len(producao) * 2
            pilha = pilha[:-tamanho_producao]
            #print(pilha)
            estado_topo = pilha[-1]

            if nao_terminal in tabela_SLR.columns and not pd.isna(tabela_SLR.loc[estado_topo, nao_terminal]):
                desvio = interpretar_entrada_tabela(tabela_SLR.loc[estado_topo, nao_terminal])
            else:
                print(f"Erro de desvio: não-terminal '{nao_terminal}' inesperado após redução.")
                #print(pilha)
                return False

            if desvio and desvio[0] == 'desvio':
                pilha.append(nao_terminal)
                pilha.append(desvio[1])
            else:
                print(f"Erro: Ação de desvio inválida para o não-terminal '{nao_terminal}'")
                return False
        else:
            print("Erro: Ação desconhecida.")
            return False

        if pilha[-1] == 15 and token_atual == 'FIM': #ULTIMA REDUÇÃO
          estado_atual = pilha[-1]
          acao = interpretar_entrada_tabela(tabela_SLR.loc[estado_atual, token_atual])
          #print(acao)
          num_producao = acao[1]
          nao_terminal, producao = producoes[num_producao]
          tamanho_producao = len(producao) * 2
          pilha = pilha[:-tamanho_producao]
          #print(pilha)
          estado_topo = pilha[-1]

          if nao_terminal in tabela_SLR.columns and not pd.isna(tabela_SLR.loc[estado_topo, nao_terminal]):
              desvio = interpretar_entrada_tabela(tabela_SLR.loc[estado_topo, nao_terminal])
          else:
              print(f"Erro de desvio: não-terminal '{nao_terminal}' inesperado após redução.")
              print(pilha)
              return False

          if desvio and desvio[0] == 'desvio':
              pilha.append(nao_terminal)
              pilha.append(desvio[1])
          else:
              print(f"Erro: Ação de desvio inválida para o não-terminal '{nao_terminal}'")
              return False
          #print()
          print("Aceitação: análise sintática concluída com sucesso. EST 15")
    
# ------------------------------- Semantico  ---------------------------------------

class AnalisadorSemantico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.simbolos = {}  # Tabela de símbolos (nome -> tipo)
        self.erros = []  # Lista de erros semânticos

    def analisar(self):
        i = 0
        while i < len(self.tokens):
            tipo, valor, linha = self.tokens[i]

            # Evita erro de indexação antes de acessar tokens[i + 1]
            if i + 1 < len(self.tokens):  

                # Verifica declaração de variável
                if tipo == "Variavel":
                    proximo_tipo = self.tokens[i + 1][0]

                    if proximo_tipo in {"INTEIRO", "REAL", "CARACTER", "ZEROUM"}:
                        if valor in self.simbolos:
                            self.erros.append(f"Erro na linha {linha}: Variável '{valor}' já declarada.")
                        else:
                            self.simbolos[valor] = proximo_tipo  # Adiciona à tabela de símbolos
                        i += 1  # Pula o tipo da variável





                    # Verifica atribuição de variável
                    elif proximo_tipo == "RECEBA" and i + 2 < len(self.tokens):
                          
                        var_nome = valor
                        #print(var_nome)

                        valor_token = self.tokens[i + 2]
                        #print(valor_token[1])

                        valor_tipo = self.inferir_tipo(valor_token)
                        

                        tipo_da_var_a_ser_atrib = self.obter_tipo_variavel(valor_token[1], self.simbolos) #recebe o tipo da var a ser atribuida ex: j recebe b . (RETURN TIPO DO b)

                        if var_nome not in self.simbolos:
                            self.erros.append(f"Erro na linha {linha}: Variável '{var_nome}' não foi declarada antes do uso.")
                        else:
                            var_tipo = self.simbolos[var_nome]
                            if valor_tipo and var_tipo != valor_tipo :
                                  self.erros.append(f"Erro na linha {linha}: Tipo incompatível para '{var_nome}'. Esperado '{var_tipo}', encontrado '{valor_tipo}'.")  

                        
                        
                        
                        var_tipo = self.simbolos[var_nome] #recebe o tipo da var que recebe a atrib ex: j recebe b . (RETURN TIPO DO j)
                        
                        if tipo_da_var_a_ser_atrib and var_tipo != tipo_da_var_a_ser_atrib:
                           self.erros.append(f"Erro na linha {linha}: Tipo incompatível para '{var_nome}'. Esperado '{var_tipo}', encontrado '{tipo_da_var_a_ser_atrib}'.")

                        i += 2  #pula "RECEBA" e o valor atribuído
                    
                    
              
              

                # Verifica operação entre variáveis    
                elif tipo == "op_arit":
                      op_esquerdo = self.tokens[i - 1]  # Token anterior
                      variavel_esq = op_esquerdo[1]
                      op_direito = self.tokens[i + 1]   # Token seguinte
                      variavel_dir = op_direito[1]
                      
                      

                      
                      tipo_da_var_esq = self.obter_tipo_variavel(variavel_esq, self.simbolos)
                      tipo_da_var_dir = self.obter_tipo_variavel(variavel_dir, self.simbolos)
                      
                     
                      recebe = self.tokens[i - 3]
                      var_recebe = recebe[1]
                      tipo_da_recebe = self.obter_tipo_variavel(var_recebe, self.simbolos)

                      if tipo_da_var_esq and tipo_da_var_dir and tipo_da_var_esq != tipo_da_var_dir:
                        self.erros.append(f"Erro na linha {linha}: Operação inválida entre '{tipo_da_var_esq}' e '{tipo_da_var_dir}'.")

                      if tipo_da_recebe and (tipo_da_recebe != tipo_da_var_esq or tipo_da_recebe != tipo_da_var_dir):
                        self.erros.append(f"Erro na linha {linha}: O valor que recebe '{tipo_da_recebe}' é diferente de '{tipo_da_var_esq}' ou é diferente de '{tipo_da_var_dir}'.")
            

                # Verifica se condição do "SE", "DURANTE", "PARA" é um op_relacional   
                elif tipo in {"SE", "DURANTE", "PARA"}:
                  if not any(tok[0] == "op_relacional" for tok in self.tokens[i:i+5]):  #verifica 5 posições a frente (apos o "SE", "DURANTE", "PARA") se encontra um op_relacional.
                    self.erros.append(f"Erro na linha {linha}: Expressão condicional inválida.") #como não encontrou um op_relacional, então erro.



                # Verifica se a variavel que esta INC ou DEC é um INTEIRO  
                elif tipo == "INC" or tipo == "DEC":
                  var_nome = self.tokens[i - 1][1]  #Pegando variavel anterior ex: x INC . retorna 'x'
    
                  if self.simbolos.get(var_nome) != "INTEIRO":
                    self.erros.append(f"Erro na linha {linha}: INC/DEC só pode ser usado com variáveis inteiras.")











            i += 1  # Avança para o próximo token

        return self.erros

    def obter_tipo_variavel(self, nome_variavel, simbolos):
      if nome_variavel in simbolos:
        return simbolos[nome_variavel]
      else:
        return None


    def inferir_tipo(self, token):
        tipo, valor, _ = token
        #print('tipo', tipo)
        if tipo == "Num_inteiro":
            return "INTEIRO"
        elif tipo == "Num_real":
            return "REAL"
        elif tipo == "Caracter":
            return "CARACTER"
        elif tipo == "Zeroum":
            return "ZEROUM"
        return None











tokens1 = tokens_atualizados #tokens do lexico
analisador_sintatico_bottom_up(tokens1, tabela_SLR, producoes) #sintatico

print()
print(tokens_atualizados)
print()

# Exemplo de análise
analisador = AnalisadorSemantico(tokens_atualizados)
erros = analisador.analisar()

if erros:
    for erro in erros:
        print(erro)
else:
    print("Análise semântica concluída sem erros!")
