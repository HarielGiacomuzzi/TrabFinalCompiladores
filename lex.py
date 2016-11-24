# ------------------------------------------------------------
# lex.py
# Nomes: Hariel G., Lucas Teixeira, Bruno Kieling
# Descricao: Trabalho da disciplina de compiladores de 2016/2
# ------------------------------------------------------------
import ply.lex as lex
import sys

# lista de palavras reservadas
reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   # 'for' : 'FOR',
   'define' : 'DEFINE'
}

# lista de nomes de tokens
tokens = [
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'ATTR',
   'LESSTHAN',
   'GREATERTHAN',
   'UMINUS',
   'LCURLYBRACKETS',
   'RCURLYBRACKETS',
   'SEMICOLON',
   'ID',
   'COMMA',
   'PLUSEQUAL',
   'MINUSEQUAL',
   'TIMESEQUAL',
   'BOOL',
   'EXP',
   'FOR'
]+list(reserved.values())

# expressoes regulares para expressoes simples
t_LPAREN  = r'\('
t_FOR  = r'for'
t_RPAREN  = r'\)'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_EXP     = r'\^'
t_DIVIDE  = r'/'
t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'
t_UMINUS = r'-'
t_LCURLYBRACKETS = r'{'
t_RCURLYBRACKETS = r'}'
t_SEMICOLON = r';'
t_ATTR = r'='
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_COMMA = r','
t_PLUSEQUAL = r'\+='
t_MINUSEQUAL = r'-='
t_TIMESEQUAL = r'\*='


# uma string para guardar caracteres descartados como espacos e tabs...
t_ignore  = ' \t'

#############################
# regras mais complexas...
#############################
# regra para identificar numeros inteiros
def t_NUMBER(t):
	r'\d+'
	t.value = float(t.value)    
	return t

#regra para identificar bolean
def t_BOOL(t):
   r'true|false'
   if(t.value == 'true'):
      t.value = True
   else:
      t.value = False
   return t

#  regra para mostrar erros...
def t_error(t):
	print("Illegal character '%s' on position: %s" % (t.value[0], t.lineno))
	t.lexer.skip(1)

# para manter o track do numedor de linhas
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# Constroi o objeto
lexer = lex.lex()

def main():
	# leitura do arquivo
	try: 
		nomeDoArquivo = sys.argv[1]
	except IndexError:
		print('Utilizacao: python lex.py <nome do arquivo>')
		return 0
	arquivo = open(nomeDoArquivo, 'r')
	dados = arquivo.read()

	# parte de interpretador lexico
	lexer.input(dados)
	for tok in lexer:
		print(tok)


if __name__ == '__main__':
	main()




