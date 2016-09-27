import ply.lex as lex
from ply.lex import TOKEN
import sys
# List of token names.   This is always required
tokens = (
   'ID',
   'FLOAT_LITERAL',
   'WHITESPACE',
   'COMMENT',
   'EQUAL',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
)

# Regular expression rules for simple tokens
t_ID      = r'[A-Za-z_][A-Za-z_0-9]*'
t_EQUAL   = r'\='
t_PLUS    = r'\@'
t_MINUS   = r'\$'
t_TIMES   = r'\#'
t_DIVIDE  = r'\&'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_WHITESPACE = r'\s+'
FLOATLITERAL =  r'[-]*[\d+][\.\d+]*[e\d+]*[E\-\d+]*'
t_COMMENT = r'//.* | /\*[^\*/]*\*/'


# A regular expression rule with some action code
@TOKEN(FLOATLITERAL)
def t_FLOAT_LITERAL(t):
    #convert to string
    t.value = str(t.value)
    return t


# Error handling rule
def t_error(t):
    global error
    error = True
    global errorLine
    errorLine.append(t.lineno)
    #print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def tokeniseFile():
    filename = sys.argv[1]
    inputFile = open(filename, 'r')
    # Give the lexer some input
    lexer.input(inputFile.read())
    inputFile.close()
    if isLex == True:
        files = filename.split('.')
        outputFile = open(files[0] + '.tkn', 'w')
        # Tokenize
        while True:
            tok = lexer.token()
            if not tok:
                break      # No more input
            if tok.type in ['EQUAL','PLUS','MINUS','TIMES','DIVIDE','LPAREN','RPAREN']:
                print(tok.value,file = outputFile)
                print(tok.value)
            elif tok.type in ['WHITESPACE']:
                print(tok.type,file = outputFile)
                print(tok.type)
            elif tok.type in ['COMMENT']:
                print(tok.type,file = outputFile)
                print(tok.type)
            else:
                print(tok.type + "," + tok.value,file = outputFile)
                print(tok.type + "," + tok.value)

        outputFile.close()

    # else:
    #     while True:
    #         tok = lexer.token()
    #         if not tok:
    #             break


error = False
errorLine =[]
# Build the lexer
lexer = lex.lex()
isLex = False
def main():
    tokeniseFile()

if __name__== "__main__":
    isLex = True
    main()






