import sys
import ply.yacc as yacc
import lex_ula
from lex_ula import tokens

error = False
errorLine = []

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Get the token map from the lexer.  This is required.
def p_statement_id(p):
    'statement : ID EQUAL expression'
    p[0] = ('AssignStatement', ('ID', p[1]), p[3])

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = ('AddExpression', p[1], p[3])

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = ('SubExpression', p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = ('MulExpression', p[1], p[3])

def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = ('DivExpression', p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_factor_float(p):
    'factor : FLOAT_LITERAL'
    p[0] = ('FloatExpression', ('FLOAT_LITERAL', p[1]))

def p_factor_id(p):
    'factor : ID'
    p[0] = ('IdentifierExpression',('ID',p[1]))

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

#makes 'perfect code'. No COMMENTS or WHITESPACES
def buildStatements():
    #Tokenize
    previous = ''
    iteration = 1
    linePos = 1
    while True:
        tok = lex_ula.lexer.token()
        if not tok and linePos > 1:
            statement = ''
            previous = stringList[-2]
            for string in stringList:   #build one string for statement from each token value
                statement = statement + string
            del stringList[:]
            statementList.append(statement)
            break      # No more input
        elif not tok and linePos == 1:
            statement = ''
            for string in stringList:   #build one string for statement from each token value
                statement = statement + string
            del stringList[:]
            statementList.append(statement)
            break      # No more input

        elif tok.type in ['WHITESPACE', 'COMMENT']: #ignores whitespace and comment
            continue

        else:
            stringList.append(tok.value)

        if tok.value == '=':
            statement = ''

            #if its not the first iteration
            if iteration == 2:
                previous = stringList[-2]
                del stringList[-2]
                del stringList[-1]
                for string in stringList:   #build one string for statement from each token value
                    statement = statement + string
                del stringList[:]
                statementList.append(statement)
                stringList.append(previous)
                stringList.append(tok.value)

            iteration = 2
        linePos = linePos + 1

#creates tree
def createTree(parserResult, tabCounter):
    if type(parserResult[0]) == str and len(parserResult) > 2:
        print('\t'*tabCounter + str(parserResult[0]),file = outputFile)
        for x in range (1, len(parserResult)):
            createTree(parserResult[x], tabCounter+1)
    else:
        if parserResult[0] == 'ID':
            print('\t' * tabCounter + str(parserResult[0]) + ',' + str(parserResult[1]),file = outputFile)
        elif type(parserResult[0]) == int:
            print(parserResult[0],file = outputFile)
        elif type(parserResult[0]) == str:
            print('\t'*tabCounter + str(parserResult[0]),file = outputFile)
            for x in range (1, len(parserResult)):
                if type(x) == int:
                    print('\t' * (tabCounter+1) + str(parserResult[1][0]) + ',' + str(parserResult[1][1]),file = outputFile)
                else:
                    createTree(parserResult[x], tabCounter+1)
        else:
           createTree(parserResult[1], tabCounter+1)





def parseFile(canWrite):
    global stringList
    global statementList
    global outputFile
    global error
    global errorLine
    global resultsList
    resultsList = []    #stores results from parser
    stringList = []     #stores strings of each item from lexer
    statementList = []  #stores statements that are sent to parser
    lex_ula.tokeniseFile()
    buildStatements() #creates 'perfect' code for parser
    # Build the parser
    parser = yacc.yacc()
    filename = sys.argv[1]
    files = filename.split('.')
    if canWrite == True:
        outputFile = open(files[0] + '.ast', 'w')

    for s in statementList:
       result = parser.parse(s, lex_ula.lexer)
       linePosition = 0
       print(result)
       if result != None:
            resultsList.append(result)
            linePosition = linePosition + 1
       else:
           error = True
           errorLine.append(linePosition + 1)

    if canWrite == True:
        print('Start', file=outputFile)
        print('\t' + 'Program', file=outputFile)
        tabCounter = 2
        for r in resultsList:
            createTree(r, 2)
        outputFile.close()





def main():
    parseFile(True)

if __name__== "__main__":
    main()




