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
        print("Estado atual:", estado_atual)
        print("Token atual:", token_atual)
        print("Pilha:", pilha)
        print()

        if estado_atual == 71 and token_atual == '}': #look ahead
           print('caso expecial')
           pilha.pop()
           pilha.extend(['Variavel', '<inc_dec>', 95])
           print(pilha)
           estado_atual = pilha[-1]

        #Variavel <inc_dec>
        if token_atual in tabela_SLR.columns and not pd.isna(tabela_SLR.loc[estado_atual, token_atual]):
            acao = interpretar_entrada_tabela(tabela_SLR.loc[estado_atual, token_atual])
        else:

          
          print(f"Erro: Token '{token_atual}' não encontrado na tabela ou entrada inválida para o estado {estado_atual}.")
          print(tabela_SLR.loc[estado_atual, token_atual])
          return False

        print("Ação:", acao)
        print()

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
            if acao[1] == 30:
              print('eita')
              pilha = pilha[:-2]
              print(pilha)

            num_producao = acao[1]
            nao_terminal, producao = producoes[num_producao]
            tamanho_producao = len(producao) * 2
            pilha = pilha[:-tamanho_producao]
            print(pilha)
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
        else:
            print("Erro: Ação desconhecida.")
            return False

    if pilha[-1] == 15 and token_atual == 'FIM':
       print("Aceitação: análise sintática concluída com sucesso.")
    else:
       print('ERRO ABSURDO')


tokens1 = tokens_atualizados #tokens do lexico
analisador_sintatico_bottom_up(tokens1, tabela_SLR, producoes)
