# ------------------------------------------------------------
# sintatico.py
# Nomes: Hariel G., Lucas Teixeira, Bruno Kieling
# Descricao: Trabalho da disciplina de compiladores de 2016/2
# ------------------------------------------------------------

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lex import tokens
import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename) s:%(lineno) d:%(message)s"
)
log = logging.getLogger()

precedence = (
    ('nonassoc', 'LESSTHAN', 'GREATERTHAN'),  # Nonassociative operators
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),            # Unary minus operator
)

# dictionary of names
names = { }

def p_EXPR_NUMBER(p):
  '''EXPR : NUMBER'''
  p[0] = p[1]

def p_EXPR_ID_ATTR_EXPR(t):
  '''EXPR : ID ATTR NUMBER
            | ID ATTR BOOL'''
  names[t[1]] = t[3]
  t[0] = t[3]

def p_EXPR_ID(p):
  '''EXPR : ID'''
  try:
    p[0] = names[p[1]]
  except LookupError:
    print("Undefined name '%s'" % p[1])
    p[0] = 0

def p_EXPR_LPAREN_EXPR_RPAREN(p):
  '''EXPR : LPAREN EXPR RPAREN'''
  p[0] = p[2]

def p_EXPR_ATTR_EXPR(p):
  '''EXPR : EXPR ATTR EXPR'''
  p[0] = p[3]

def p_EXPR_PLUS_EXPR(p):
  '''EXPR : EXPR PLUS EXPR'''
  p[0] = p[1] + p[3]

def p_EXPR_MINUS_EXPR(p):
  '''EXPR : EXPR MINUS EXPR'''
  p[0] = p[1] - p[3]

def p_EXPR_DIVIDE_EXPR(p):
  '''EXPR : EXPR DIVIDE EXPR'''
  p[0] = p[1] / p[3]

def p_EXPR_TIMES_EXPR(p):
  '''EXPR : EXPR TIMES EXPR'''
  p[0] = p[1] * p[3]

def p_EXPR_PLUSEQUAL_EXPR(p):
  '''EXPR : EXPR PLUSEQUAL EXPR'''
  p[0] = p[1] + p[3]

def p_EXPR_EXP_EXPR(p):
  '''EXPR : EXPR EXP EXPR'''
  p[0] = int(p[1]) ** int(p[3])

def p_EXPR_MINUSEQUAL_EXPR(p):
  '''EXPR : EXPR MINUSEQUAL EXPR'''
  p[0] = p[1] - p[3]

def p_EXPR_TIMESEQUAL_EXPR(p):
  '''EXPR : EXPR TIMESEQUAL EXPR'''
  p[0] = p[1] * p[3]

def p_LID(p):
  '''LID : ID'''
  p[0] = p[1]

def p_BLOCK(p):
  '''BLOCK : LCURLYBRACKETS CMD RCURLYBRACKETS'''
  #TODO
  pass

def p_OPER(p):
  '''OPER : PLUS
          | MINUS
          | DIVIDE
          | TIMES
          | LESSTHAN
          | GREATERTHAN
          | ATTR'''
  p[0] = p[1]

def p_CMD(p):
  '''CMD : EXPR SEMICOLON
         | EXPR SEMICOLON CMD
         | empty'''
  pass

def p_DEFINES(p):
  '''DEFINES : DEFINE ID LPAREN LID RPAREN BLOCK'''
  pass

def p_FORS(p):
  # for(a=0;a<10;a+=1){a+=2;}
  # '''FORS : FOR LPAREN EXPR SEMICOLON EXPR SEMICOLON EXPR RPAREN BLOCK'''
  '''FORS : FOR'''
  p[0] = ('for', p[3], p[5], p[7], p[10])
  print(p[3])
  print(p[5])
  print(p[7])
  evaluate(p[0])

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!", p)

# Empty rule for the sake of needing
def p_empty(p):
    'empty :'
    pass

def evaluate(lst):
  if(lst[0] == 'for'):
    for i in range(lst[1],lst[2], lst[3]):
      print lst[4]


# Build the parser
parser = yacc.yacc(tabmodule='parsingTable', debug=True, debuglog=log, errorlog=log)

while True:
   try:
       s = raw_input('calc > ')
   except EOFError:
       break
   if not s: continue
   if(s == '#help'):
    print('#############')
    print('#  Manual   #')
    print('#############')
    print('''Examples
             1+1 Input
             2   Result
             1 / 3 Input
            .33333333333333333333 Result
             4 * (6 + 7) Input
             52 Result''')
    continue
   if('#save' in s):
    arquivo = open(s.split()[1], 'w+')
    for chave,valor in names.items():
      arquivo.write(chave+' : '+str(valor)+'\n')
    arquivo.close()
    continue
   if('#load' in s):
    fileName = s.split()[1]
    arquivo = open(fileName, 'r')
    dados = arquivo.read()
    result = parser.parse(dados, debug=log)
    print(result)
    continue
   if('#show_all' in s):
    for coisa in names:
      print(coisa)
    continue
   if('#show' in s):
    ident = s.split()[1]
    print(names[ident])
    continue
   result = parser.parse(s, debug=log)
   print(result)









