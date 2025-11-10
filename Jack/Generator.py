"""No comment"""
import sys
import os

import Parser


class Generator:
    """No comment"""

    def __init__(self, file=None):
        if file is not None:
            self.parser = Parser.Parser(file)
            self.arbre = self.parser.jackclass()
            self.vmfile = open(self.arbre['name'] + '.vm', "a")
            self.classname = file[0:-5]
            self.head, self.tail = os.path.split(self.classname)
            self.symbolClassTable = []
            self.symbolRoutineTable = []
            self.fnb = 0
            self.stnb = 0
            self.lnb = 0
            self.anb = 0

    def jackclass(self):
        """
            {'line': line, 'col': col, 'type': 'class', 'name': className,
            'varDec': [variable], 'subroutine':[subroutine]}
        """
        print("// class " + self.arbre['name'])
        print ('// Table symbollique de la classe')

        variables = self.arbre['varDec']
        for v in variables :
            self.variable(v)
        for v in self.symbolClassTable :
            print(v)

        self.subroutineDec(self.arbre['subroutine'])

    def variable(self, var):
        """
        {'line': line, 'col': col, 'name': varName, 'kind': kind, 'type': type}
        """
        if type(var) == list :
            for v in var :
                self.variable(v)
        else :
            match var['kind'] :
                case 'static' :
                    kind = "static " + str(self.stnb)
                    self.stnb += 1
                    self.symbolClassTable.append({'name': var['name'], 'vm': kind})
                case 'field' :
                    kind = "this " + str(self.fnb)
                    self.fnb += 1
                    self.symbolClassTable.append({'name': var['name'], 'vm': kind})
                case 'argument' :
                    kind = "ARG " + str(self.anb)
                    self.anb += 1
                    self.symbolRoutineTable.append({'name': var['name'], 'vm': kind})
                case 'local' :
                    kind = "LCL " + str(self.lnb)
                    self.lnb += 1
                    self.symbolRoutineTable.append({'name': var['name'], 'vm': kind})



    def subroutineDec(self, routine):
        """
        {'line':line, 'col': col,'type': 'constructor'|'function'|'method',
            'return' : 'void| 'int'|'char'|'boolean'|className',
            'name': subroutineName, 'argument': [variable],'local': [variable],
            'instructions' : [instruction]
        """
        print()
        for r in routine :
            print("// Routine : " + r['type'] + " " + r['return'] + " " + r['name'])
            print("//" + str(r))
            self.vmfile.write(f"Function {self.tail}.{r['name']} {len(r['argument'])} \n")
            print("// Table symbollique de la routine")
            args = r['argument']
            for a in args :
                self.variable(a)
            lcls = r['local']
            for l in lcls :
                self.variable(l)
            for v in self.symbolRoutineTable:
                print(v)

            print()


            for i in r['instructions'] :
                print("\nInstructioh : " + str(i))
                self.statement(i)
            print()


    def statement(self, inst):
        """
        statement : letStatements|ifStatement|whileStatement|doStatement|returnStatement
        """
        match inst['type'] :
            case 'let' :
                self.letStatement(inst)
            case 'if' :
                self.ifStatement(inst)
            case 'while' :
                self.whileStatement(inst)
            case 'do' :
                self.doStatement(inst)
            case 'return' :
                self.returnStatement(inst)
            case _ :
                self.error("Type de statement incorrect : " + str(inst))

    def letStatement(self, inst):
        """
        {'line':line, 'col': col,'type': 'let',
        'variable': varName, 'indice': expression, 'valeur': expression
        """
        print(f"// Instruction de type {inst['type']}")
        self.expression(inst['expression'])
        print ("pop " + self.getVM(inst['name']))
        self.vmfile.write("pop " + self.getVM(inst['name'] +"\n"))


    def ifStatement(self, inst):
        """
        {'line':line, 'col': col,
        'type': 'if', 'condition': expression, 'true': [instruction],
        'false': [instruction]}
        """

    def whileStatement(self, inst):
        """
        {'line':line, 'col': col,
        'type': 'while', 'condition': expression,
        'instructions': [instruction]}
        """

    def doStatement(self, inst):
        """
        {'line':line, 'col': col,
        'type': 'do', 'classvar': className ou varName,
        'name': subroutineName, 'argument': [expression]}
        """
        print(f"// Instruction de type {inst['type']}")
        args = inst['valeur']['argument']
        if type(args) is list :
            args = len(args)+1
        else :
            args = 1
        if inst['valeur']['classVar'] == 'vide' :
            print (f"Call {self.tail}.{inst['valeur']['name']} {args}")
        else :
            print (f"Call {inst['valeur']['classVar']}.{inst['valeur']['name']} {args}")


    def returnStatement(self, inst):
        """
        {'line':line, 'col': col, 'type': 'return', 'valeur': expression}
        """
        self.expression(inst['valeur'])
        print ('return')

    def expression(self, exp):
        """
        [term op ...]
            avec op : '+'|'-'|'*'|'/'|'&'|'|'|'<'|'>'|'='
        """
        tempop = 'vide'

        for x in exp :
            if type(x) is dict and tempop == 'vide':
                if x['type'] == 'op' :
                    tempop = self.term(x)
                else :
                    print(self.term(x))
                    self.vmfile.write(self.term(x)+"\n")
            elif type(x) is dict :
                print(self.term(x))
                self.vmfile.write(self.term(x)+"\n")
                print(tempop)
                self.vmfile.write(tempop)
                tempop = 'vide'
            elif type(x) is list :
                self.expression(x)
                if tempop != 'vide' :
                    print(tempop)
                    self.vmfile.write(tempop+"\n")
                    tempop = 'vide'

    def term(self, t):
        """
        {'line':line, 'col': col,
        'type': 'int'| 'string'| 'constant'| 'varName'|'call'| 'expression'|'-'|'~',
         'indice':expression, 'subroutineCall': subroutineCall}
        """
        if t['type'] == 'constant' :
            return "push constant " + t['value']
        elif t['type'] == 'op' :
            match t['value'] :
                case '+' :
                    return 'add'
                case '-' :
                    return 'sub'
                case '*' :
                    return 'Call Math.multiply 2'
                case '/' :
                    return 'Call Math.divide 2'
                case '&' :
                    return 'and'
                case '|' :
                    return 'or'
                case '<' :
                    return 'lt'
                case '>' :
                    return 'gt'

        elif t['type'] == 'identifier' :
            vm = self.getVM(t['value'])
            if vm != 'err404' :
                return "push " + vm
        elif t['type'] == 'keyword' :
            val = t['value']['value']
            match val :
                case 'true' :
                    return ("push constant 0\nneg")
                case 'false' :
                    return "push constant 0"
                case 'this' :
                    return "push pointer 0"
                case 'that' :
                    return "push pointer 1"
        elif t['type'] == 'subroutine' :
            return self.subroutineCall(t)
        else :
            self.error("Mauvaise utilisation de Term (" + str(t) + ")")

    def subroutineCall(self, call):
        """
        {'line':line, 'col': col, 'classvar': className ou varName,
        'name': subroutineName, 'argument': [expression]}
        """

    def error(self, message=''):
        print(f"SyntaxError: {message}")
        exit()

    def getVM(self, value):
        for x in self.symbolClassTable:
            if x['name'] == value:
                return x['vm']
        for x in self.symbolRoutineTable:
            if x['name'] == value:
                return x['vm']
        return 'err404'

    def getVMArray(self, value, array):
        for x in array :
            if x['name'] == value :
                return x['vm']
        return 'err404'

if __name__ == '__main__':
    file = sys.argv[1]
    print('-----debut')
    generator = Generator(file)
    generator.jackclass()
    print('-----fin')
