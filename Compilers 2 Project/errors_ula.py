import sys
import lex_ula as lex
import parse_ula as parser

def errorCheck(canWrite):

    filename = sys.argv[1]
    files = filename.split('.')
    if(canWrite == True):
        outputFile = open(files[0] + '.err', 'w')
    lex.tokeniseFile()
    parser.parseFile(False)
    if(lex.error == True):
        if(canWrite == True):
            print('lexical error on line ' + str(lex.errorLine[0]), file=outputFile)
    elif(parser.error == True):
        if(canWrite == True):
            print('parse error on line ' + str(parser.errorLine[0]), file=outputFile)
    else:
        semanticError = False
        errorLine = 0
        leftVariable = False
        rightVariable = False
        variables = []

        for r in parser.resultsList:
            errorLine = errorLine + 1
            if(r[0] == 'AssignStatement'):
                #print(r[1][1])
                if(r[1][1] in variables):
                    semanticError = True
                    break
                else:
                    variables.append(r[1][1])

            for i in range(1, len(r)):
                if('AddExpression' in r[i] or 'SubExpression' in r[i] or 'MulExpression' in r[i] or 'DivExpression' in r[i]):
                    for expression in r[i]:
                        if(expression[0] == 'IdentifierExpression'):
                            if(expression[1][1] not in variables):
                                semanticError = True
                                break
                        if(semanticError == True):
                            break
                if (semanticError == True):
                    break
            if(semanticError == True):
                break
        if(semanticError == True):
            if(canWrite == True):
                print('semantic error on line ' + str(errorLine), file=outputFile)

    if(canWrite == True):
        outputFile.close()





def main():
    errorCheck(True)

if __name__== "__main__":
    main()
