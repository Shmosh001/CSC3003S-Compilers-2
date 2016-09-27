from llvmlite import ir
from ctypes import CFUNCTYPE, c_float
import llvmlite.binding as llvm
import sys
import parser_ula_2 as parser2

def buildTree():
    global tree
    #run parser - parser results
    tree = parser2.parseFile(False)

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



def code_gen(tree): # traverse tree recursively to generate code
    global last_var
    global builder
    global var_dict
    if tree[0] == "Program":
        for t in tree[1:]:
            code_gen(t)
    elif tree[0] == "=":
        last_var = tree[1][0]
        var_dict[last_var] = builder.alloca(ir.FloatType())
        builder.store(code_gen(tree[2]), var_dict[last_var])
    elif tree[0] == "@":
        return(builder.fadd(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] == "$":
        return(builder.fsub(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] == "#":
        return(builder.fmul(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] == "&":
        return(builder.fdiv(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0].isnumeric() or is_float(tree[0]):
        return(ir.Constant(ir.FloatType(), float(tree[0])))
    else:
        return builder.load(var_dict[tree[0]])

def ir_program(canWrite):
    global tree
    global last_var
    global builder
    global var_dict

    tree = ["Program", ["=", ["a"], ["@", ["1"], ["2"]]]] # compact ast
    buildTree() #rebuilds tree from ULA file specified by arguement
    last_var = "" # keeps track of the last var assigned
    var_dict = {}  # var names associated with memory location

    flttyp = ir.FloatType() # create float type
    fnctyp = ir.FunctionType(flttyp, ()) # create function type to return a float
    module = ir.Module(name="ula") # create module named "ula"
    func = ir.Function(module, fnctyp, name="main") # create "main" function
    block = func.append_basic_block(name="entry") # create block "entry" label
    builder = ir.IRBuilder(block) # create irbuilder to generate code
    code_gen(tree) # call code_gen() to traverse tree & generate code
    builder.ret(builder.load(var_dict[last_var])) # specify return value
    if(canWrite):
        filename = sys.argv[1]
        files = filename.split('.')
        outputFile = open(files[0] + '.ir', 'w')
        print(module)
        print(module, file=outputFile)
    else:
        return module


def main():
    ir_program(True)

if __name__== "__main__":
    main()














