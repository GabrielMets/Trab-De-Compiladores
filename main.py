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

#func para obter o token correto pros ID
def obter_token(lexema):
    return Tipos_id.get(lexema, 'ID')

#lista para armazenar os tokens atualizados
tokens_atualizados = []

#substitui 'ID' pelo token correto com base no lexema
for token, lexema, linha in tabela_de_tokens:
    if token == 'ID':
        novo_token = obter_token(lexema)
        tokens_atualizados.append((novo_token, lexema, linha))
    else:
        tokens_atualizados.append((token, lexema, linha))

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
    #gerador_codigo = GeradorCodigoETAC()  # Inicializa o gerador de código
    
    while cursor < len(tokens1):
        estado_atual = pilha[-1]  
        token_atual = tokens1[cursor][0] 

        if estado_atual == 71 and token_atual == '}': #look ahead
           pilha.pop()
           pilha.extend(['Variavel', '<inc_dec>', 95])
           estado_atual = pilha[-1]

        if token_atual in tabela_SLR.columns and not pd.isna(tabela_SLR.loc[estado_atual, token_atual]):
            acao = interpretar_entrada_tabela(tabela_SLR.loc[estado_atual, token_atual])
        else:
          print(f"Erro: Token '{token_atual}' não encontrado na tabela ou entrada inválida para o estado {estado_atual}.")
          return False

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

        elif acao[0] == 'reduz':
            if acao[1] == 30: #caso expecial
              pilha = pilha[:-2]

            num_producao = acao[1]
            nao_terminal, producao = producoes[num_producao]
            tamanho_producao = len(producao) * 2
            pilha = pilha[:-tamanho_producao]
            estado_topo = pilha[-1]

            if nao_terminal in tabela_SLR.columns and not pd.isna(tabela_SLR.loc[estado_topo, nao_terminal]):
                desvio = interpretar_entrada_tabela(tabela_SLR.loc[estado_topo, nao_terminal])
            else:
                print(f"Erro de desvio: não-terminal '{nao_terminal}' inesperado após redução.")
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
          num_producao = acao[1]
          nao_terminal, producao = producoes[num_producao]
          tamanho_producao = len(producao) * 2
          pilha = pilha[:-tamanho_producao]
          estado_topo = pilha[-1]

          if nao_terminal in tabela_SLR.columns and not pd.isna(tabela_SLR.loc[estado_topo, nao_terminal]):
              desvio = interpretar_entrada_tabela(tabela_SLR.loc[estado_topo, nao_terminal])
          else:
              print(f"Erro de desvio: não-terminal '{nao_terminal}' inesperado após redução.")

              return False

          if desvio and desvio[0] == 'desvio':
              pilha.append(nao_terminal)
              pilha.append(desvio[1])
          else:
              print(f"Erro: Ação de desvio inválida para o não-terminal '{nao_terminal}'")
              return False

          print("Aceitação: análise sintática concluída com sucesso.")
          return True
    
# ------------------------------- Semantico  ---------------------------------------

class AnalisadorSemantico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.simbolos = {}  # Tabela de símbolos (nome -> tipo)
        self.erros = []  # Lista de erros semânticos
        self.gerador = GeradorCodigoETAC()  #
        
    def analisar(self):
        abrePara = False
        numchaves = 0
        i = 0
        while i < len(self.tokens):
            tipo, valor, linha = self.tokens[i]
            
            if i + 1 < len(self.tokens):  

                #verifica se inicia com INICIO
                if i == 0 and tipo != "INICIO" :
                  self.erros.append(f"Erro na linha {i}: Esperava 'INICIO'")

                #verifica declaração de variável
                if tipo == "Variavel":
                    proximo_tipo = self.tokens[i + 1][0]

                    if proximo_tipo in {"INTEIRO", "REAL", "CARACTER", "ZEROUM"}:
                        if valor in self.simbolos:
                            self.erros.append(f"Erro na linha {linha}: Variável '{valor}' já declarada.")
                        else:
                            self.simbolos[valor] = proximo_tipo  #adiciona à tabela de símbolos   
                        i += 1  #pula o tipo da variável

                    #verifica atribuição de variável
                    elif proximo_tipo == "RECEBA" and i + 2 < len(self.tokens):
                          
                        var_nome = valor

                        valor_token = self.tokens[i + 2]

                        valor_tipo = self.inferir_tipo(valor_token)
                        
                        tipo_da_var_a_ser_atrib = self.obter_tipo_variavel(valor_token[1], self.simbolos) #recebe o tipo da var a ser atribuida ex: j recebe b . (RETURN TIPO DO b)

                        if var_nome not in self.simbolos:
                            self.erros.append(f"Erro na linha {linha}: Variável '{var_nome}' não foi declarada antes do uso.")
    
                        else:
                            var_tipo = self.simbolos[var_nome]
                            
                            if valor_token[0] == 'Variavel':
                              if valor_token[1] not in self.simbolos:
                                 self.erros.append(f"Erro na linha {linha}: Variável '{valor_token[1]}' não foi declarada antes do uso.")

                              elif valor_tipo and var_tipo != valor_tipo :
                                  self.erros.append(f"Erro na linha {linha}: Tipo incompatível para '{var_nome}'. Esperado '{var_tipo}', encontrado '{valor_tipo}'.")  
                        
                              elif tipo_da_var_a_ser_atrib and var_tipo != tipo_da_var_a_ser_atrib:
                                self.erros.append(f"Erro na linha {linha}: Tipo incompatível para '{var_nome}'. Esperado '{var_tipo}', encontrado '{tipo_da_var_a_ser_atrib}'.")
                       
                            if self.tokens[i + 3][0] == '.':
                              self.gerador.gerar_atribuicao(var_nome, valor_token[1]) #geradorC
    
                elif tipo == "op_arit":
                      op_esquerdo = self.tokens[i - 1]  # Token anterior
                      variavel_esq = op_esquerdo[1]
                      op_direito = self.tokens[i + 1]   # Token seguinte
                      variavel_dir = op_direito[1]
                      recebedor = self.tokens[i - 3][1]
                            
                      tipo_da_var_esq = self.obter_tipo_variavel(variavel_esq, self.simbolos)
                      tipo_da_var_dir = self.obter_tipo_variavel(variavel_dir, self.simbolos)
                                 
                      recebe = self.tokens[i - 3]
                      var_recebe = recebe[1]
                      tipo_da_recebe = self.obter_tipo_variavel(var_recebe, self.simbolos)

                      if tipo_da_var_esq and tipo_da_var_dir and tipo_da_var_esq != tipo_da_var_dir:
                        self.erros.append(f"Erro na linha {linha}: Operação inválida entre '{tipo_da_var_esq}' e '{tipo_da_var_dir}'.")
 
                      if tipo_da_recebe and tipo_da_var_esq and tipo_da_var_dir and (tipo_da_recebe != tipo_da_var_esq or tipo_da_recebe != tipo_da_var_dir):
                        self.erros.append(f"Erro na linha {linha}: O valor que recebe '{tipo_da_recebe}' é diferente de '{tipo_da_var_esq}' ou é diferente de '{tipo_da_var_dir}'.")
             
                      temp = self.gerador.gerar_operacao_aritmetica(valor, variavel_esq, variavel_dir) #geradorC
                      self.gerador.gerar_atribuicao(recebedor, temp) #geradorC
   
                elif tipo == "SE":

                  if not any(tok[0] == "op_relacional" for tok in self.tokens[i:i+5]):  #verifica 5 posições a frente (apos o "SE") se encontra um op_relacional.
                    self.erros.append(f"Erro na linha {linha}: Expressão condicional inválida.") #como não encontrou um op_relacional, então erro.

                  tipos = []

                  for tok in self.tokens[i:i+5]:
                    if tok[0] == "Variavel":
                        if tok[1] in self.simbolos:
                           tipos.append(self.simbolos[tok[1]])
                        else:
                           self.erros.append(f"Erro na linha {linha}: Variável '{tok[1]}' não declarada.")

                  if len(tipos) == 2 and tipos[0] != tipos[1]:
                    self.erros.append(f"Erro na linha {linha}: Na condição '{tipo}' os tipos de variáveis são incompatíveis na expressão condicional.")
             
                  for j, tok in enumerate(self.tokens[i:i + 5]):
                    if tok[0] == "op_relacional":
                      op_esquerdo = self.tokens[i + j - 1]
                      op_direito = self.tokens[i + j + 1]
                    
                      temp = self.gerador.gerar_operacao_relacional(tok[1], op_esquerdo[1], op_direito[1]) #geradorC 

                  label_true = self.gerador.novo_label()
                  label_false = self.gerador.novo_label()

                  self.gerador.gerar_condicional(temp, label_true, label_false)
                  self.gerador.gerar_label(label_true)
                
                elif tipo == "}" and (self.tokens[i + 1][0] == 'SENAO' or self.tokens[i + 1][0] == 'SENAO_VAZIO') :
                  self.gerador.gerar_label(label_false)
                  numchaves -= 1
                   
                elif tipo == "ESCREVA":
                   mensagem = self.tokens[i + 2][1]
                   self.gerador.gerar_escreva(mensagem)

                elif tipo == "PARA":

                  if not any(tok[0] == "op_relacional" for tok in self.tokens[i:i+10]):  #verifica 10 posições a frente (apos o "PARA") se encontra um op_relacional.
                    self.erros.append(f"Erro na linha {linha}: Expressão condicional inválida.") #como não encontrou um op_relacional, então erro.

                  tipos = []
                  
                  for tok in self.tokens[i:i+13]:
                    if tok[0] == "Variavel":
                        if tok[1] in self.simbolos:
                           tipos.append(self.simbolos[tok[1]])
                        else:
                           self.erros.append(f"Erro na linha {linha}: Variável '{tok[1]}' não declarada.")

                  if len(tipos) == 2 and tipos[0] != tipos[1]:
                    self.erros.append(f"Erro na linha {linha}: Na condição '{tipo}' os tipos de variáveis são incompatíveis na expressão condicional.")
             
                  for j, tok in enumerate(self.tokens[i:i + 13]):
                    if tok[0] == "op_relacional":
                      op_esquerdo = self.tokens[i + j - 1]
                      op_direito = self.tokens[i + j + 1]
                      tempPARA = self.gerador.gerar_operacao_relacional(tok[1], op_esquerdo[1], op_direito[1]) #geradorC 
                      
                    if tok[0] == "INC":
                       var_inc = self.tokens[i + j - 1][1]
                       
                  label_volta_para = self.gerador.novo_label()
                  label_true = self.gerador.novo_label()
                  label_false = self.gerador.novo_label()

                elif tipo == "{" and self.tokens[i - 2][0] == 'INC':
                      abrePara = True
                      self.gerador.gerar_label(label_volta_para)
                      self.gerador.gerar_condicional(tempPARA, label_true, label_false)
                      self.gerador.gerar_label(label_true)
                      numchaves += 1 
                      
                elif tipo == "}" and abrePara:
                  self.gerador.emitir(f"{var_inc} += 1")
                  self.gerador.emitir(f"goto {label_volta_para}")
                  self.gerador.gerar_label(label_false)
                  abrePara = False
                  numchaves -= 1 

                elif tipo == "DURANTE":
                  label_volta_dura = self.gerador.novo_label()
                  label_true = self.gerador.novo_label()
                  label_false = self.gerador.novo_label()  

                  if not any(tok[0] == "op_relacional" for tok in self.tokens[i:i+5]):  #verifica 5 posições a frente (apos o "DURANTE") se encontra um op_relacional.
                    self.erros.append(f"Erro na linha {linha}: Expressão condicional inválida.") #como não encontrou um op_relacional, então erro.

                  tipos = []
                  
                  for tok in self.tokens[i:i+5]:
                    if tok[0] == "Variavel":
                        if tok[1] in self.simbolos:
                           tipos.append(self.simbolos[tok[1]])
                        else:
                           self.erros.append(f"Erro na linha {linha}: Variável '{tok[1]}' não declarada.")

                  if len(tipos) == 2 and tipos[0] != tipos[1]:
                    self.erros.append(f"Erro na linha {linha}: Na condição '{tipo}' os tipos de variáveis são incompatíveis na expressão condicional.")

                  for j, tok in enumerate(self.tokens[i:i + 13]):
                    if tok[0] == "op_relacional":
                      op_esquerdo = self.tokens[i + j - 1]
                      op_direito = self.tokens[i + j + 1]
                      
                      tempDURA = self.gerador.gerar_operacao_relacional(tok[1], op_esquerdo[1], op_direito[1]) #geradorC
                      self.gerador.gerar_label(label_volta_dura)
                      self.gerador.gerar_condicional(tempDURA, label_true, label_false)
                      self.gerador.gerar_label(label_true)
                
                elif tipo == "}" and self.tokens[i - 1][0] == 'INC' :
                  var_inc = self.tokens[i - 2][1]
                  self.gerador.emitir(f"{var_inc} += 1")
                  self.gerador.emitir(f"goto {label_volta_dura}")
                  self.gerador.gerar_label(label_false)
                  numchaves -= 1   
                    
                #Verifica se a variavel que esta INC ou DEC é um INTEIRO  
                elif tipo == "INC" or tipo == "DEC":
                  var_nome = self.tokens[i - 1][1]  #Pegando variavel anterior ex: x INC . retorna 'x'
    
                  if self.simbolos.get(var_nome) != "INTEIRO":
                    self.erros.append(f"Erro na linha {linha}: INC/DEC só pode ser usado com variáveis inteiras.")

                #Verifica se RECEBAT está para uma variavel.
                elif tipo == "RECEBAT":

                  if self.tokens[i + 1][0] != "Variavel":
                    self.erros.append(f"Erro na linha {linha}: RECEBAT deve receber uma variável, não '{self.tokens[i + 1][1]}'.")

                  if self.tokens[i + 1][1] not in self.simbolos:
                    var_nome = self.tokens[i + 1][1]
                    self.erros.append(f"Erro na linha {linha}: Variável '{var_nome}' não foi declarada antes do uso.")

                  var_nome_receba = self.tokens[i + 1][1]
                  self.gerador.emitir(f"READ {var_nome_receba}")

                elif tipo == "}":
                   numchaves -= 1

                elif tipo == "{":
                  numchaves += 1

            elif i < len(self.tokens): #Verificação se termina em FIM
              if tipo != 'FIM':
                self.erros.append(f"Erro: Esperava 'FIM' ao final do codigo")
              elif tipo == 'FIM':
                self.gerador.emitir(f"END")

            i += 1  #avança para o próximo token
        if numchaves != 0:
          self.erros.append(f"Erro: Numero de chaves imcompativeis, {numchaves}") 
        return self.erros

    def obter_tipo_variavel(self, nome_variavel, simbolos):
      if nome_variavel in simbolos:
        return simbolos[nome_variavel]
      else:
        return None

    def inferir_tipo(self, token):
        tipo, valor, _ = token
        if tipo == "Num_inteiro":
            return "INTEIRO"
        elif tipo == "Num_real":
            return "REAL"
        elif tipo == "Caracter":
            return "CARACTER"
        elif tipo == "Zeroum":
            return "ZEROUM"
        return None

class GeradorCodigoETAC:
    def __init__(self):
        self.codigo = []  #lista para armazenar as instruções ETAC
        self.contador_temp = 0  #contador para gerar variáveis temporárias
        self.contador_label = 0  #contador para gerar rótulos únicos

    def novo_label(self):
        label = f"L{self.contador_label}"
        self.contador_label += 1
        return label

    def nova_temp(self):
        temp = f"t{self.contador_temp}"
        self.contador_temp += 1
        return temp

    def emitir(self, instrucao):
        self.codigo.append(instrucao)

    def gerar_codigo(self):
        return "\n".join(self.codigo)
    
    def gerar_atribuicao(self, destino, origem):
        self.emitir(f"{destino} = {origem}")

    def gerar_operacao_aritmetica(self, operador, op1, op2):
        temp = self.nova_temp()
        self.emitir(f"{temp} = {op1} {operador} {op2}")
        return temp

    def gerar_operacao_relacional(self, operador, op1, op2):
        temp = self.nova_temp()
        self.emitir(f"{temp} = {op1} {operador} {op2}")
        return temp
    
    def gerar_condicional(self, condicao, label_true, label_false):
        self.emitir(f"if {condicao} goto {label_true}")
        self.emitir(f"goto {label_false}")

    def gerar_label(self, label):
        self.emitir(f"{label}:")

    def gerar_goto(self, label):
        self.emitir(f"goto {label}")

    def gerar_escreva(self, mensagem):
      mensagem_formatada = mensagem.replace("^", "").replace("\\q", "\\n")  #substitui \q por \n para nova linha; remove os caracteres especiais (^ e \q) e trata a mensagem
      self.emitir(f'print("{mensagem_formatada}")')

    
tokens1 = tokens_atualizados #tokens do lexico
errosintatico = analisador_sintatico_bottom_up(tokens1, tabela_SLR, producoes) #erros do sintatico
analisador = AnalisadorSemantico(tokens_atualizados) #semantico
errossemanticos = analisador.analisar() #erros do semantico

print()
#print(tokens_atualizados)
print()

if errossemanticos or errosintatico==False : #se possuir erros sematicos ou possuir erros sintaticos: printa os erros semanticos (erros sintaticos são printados dentro do sintatico.)
    for erro in errossemanticos:
        print(erro)
else:
    print("Análise semântica concluída sem erros!")
    print()
    print("Código ETAC gerado:")
    print(analisador.gerador.gerar_codigo())