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
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

precedence = (
    ('nonassoc', 'LESSTHAN', 'GREATERTHAN'),  # Nonassociative operators
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'LESSTHAN', 'GREATERTHAN'),
    ('right', 'ATTR', 'TIMESEQUAL', 'PLUSEQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'EXP'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = { }

def p_STATMENT(p):
  '''STATMENT :  EXPR1
                | BLOCK
                | CMD
                | FORS
                | DEFINES 
                | LID'''

def p_EXPR1_EXPR_OPER_EXPR(p):
  '''EXPR1 : EXPR OPER EXPR'''
  if p[2] == '+':
    p[0] = p[1] + p[3]
  elif p[2] == '-':
    p[0] = p[1] - p[3]
  elif p[2] == '*':
    p[0] = p[1] * p[3]
  elif p[2] == '/':
    p[0] = p[1] / p[3]
  elif p[2] == '^':
    p[0] = p[1] ** p[3]
  elif p[2] == '=':
    p[0] = p[1] = p[3]


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

def p_EXPR_PLUSEQUAL_EXPR(p):
  '''EXPR : EXPR PLUSEQUAL EXPR'''
  p[0] = p[1] + p[3]

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
  temp = names.get(p[2] , None)
  if temp != None:
    evaluate(temp)
  elif:
    names[p[2]] = ('define', p[4], p[6])

def p_FORS(p):
  # for(a=0;a<10;a+=1){a+=2;}
  '''FORS : FOR LPAREN EXPR SEMICOLON EXPR SEMICOLON EXPR RPAREN BLOCK'''
  p[0] = ('for', p[3], p[5], p[7], p[9])
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









