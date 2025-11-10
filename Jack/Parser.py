import sys
import Lexer
import todot


class Parser:
    """No comment"""

    def __init__(self, file):
        self.lexer = Lexer.Lexer(file)

    def jackclass(self):
        """
        class: 'class' className '{' classVarDec* subroutineDec* '}'
        """
        col = self.lexer.col
        line = self.lexer.line
        self.process("class")
        name = self.className()
        self.process("{")
        varDec = []
        subroutine = []
        while (self.check('token',{'static','field'})) :
            varDec.append(self.classVarDec())
        while (self.check('token',{'constructor','method','function'})) :
            subroutine.append(self.subroutineDec())

        self.process("}")
        return {'line': line, 'col': col, 'type': 'class', 'name': name, 'varDec': varDec, 'subroutine': subroutine}

    def classVarDec(self):
        """
        classVarDec: ('static'| 'field') type varName (',' varName)* ';'
        """
        col = self.lexer.col
        line = self.lexer.line
        if self.check('token',{'static','field'}) :
            stafield = self.lexer.next()['token']
        else :
            self.error(self.lexer.next())
        type = self.type()
        name = self.varName()
        tab = [{'line': line, 'col': col,'kind': stafield, 'type': type, 'name': name}]
        while self.lexer.look()['token'] == ',':
            self.process(',')
            col = self.lexer.col
            line = self.lexer.line
            name = self.varName()
            tab.append({'line': line, 'col': col,'kind': stafield, 'type': type, 'name': name})
        self.process(';')
        return tab

    def type(self):
        """
        type: 'int'|'char'|'boolean'|className
        """
        if self.check('token',{'int','char','boolean'}) :
            token = self.lexer.next()
            return token['token']
        elif self.check('type','identifier') :
            return self.className()
        else :
            self.error(self.lexer.next())

    def subroutineDec(self):
        """
        subroutineDec: ('constructor'| 'function'|'method') ('void'|type)
        subroutineName '(' parameterList ')' subroutineBody
        """
        col = self.lexer.col
        line = self.lexer.line

        if self.check('token',{'constructor','function','method'}) :
            type = self.lexer.next()['token']
            returntype = 'constructor' # On initialise le type de retour en tant que 'constructeur' sinon BOOM ! Ce sera ré-ecrit si ce n'est pas le cas

        if (self.check('token',{'void','int','char','boolean'}) or self.check('type','identifier')):
            returntype = self.lexer.next()['token']

        name = self.subroutineName()
        parametres = self.parameterList()

        body = self.subroutineBody()
        local = body['local']
        instructions = body['instructions']
        return {'line':line, 'col': col,'type': type, 'return': returntype, 'name': name, 'argument': parametres,'local': local,'instructions' : instructions}

    def parameterList(self):
        """
        parameterList: ((type varName) (',' type varName)*)?
        """
        self.process('(')
        liste = []
        col = self.lexer.col
        line = self.lexer.line

        while not self.check('token', ')'):
            if self.check('type', {'keyword', 'identifier'}):
                type = self.type()
                name = self.varName()
                liste.append({'line': line, 'col': col,'type': type, 'name': name, 'kind': 'argument'})
                if self.check('token',',') :
                    self.process(',')
            else :
                self.error(self.lexer.next())

        self.process(')')
        return liste

    def subroutineBody(self):
        """
        subroutineBody: '{' varDec* statements '}'
        """
        self.process('{')

        local = []
        while self.check('token','var') :
            local.append(self.varDec())

        instructions = self.statements()

        self.process('}')
        return {'local': local, 'instructions': instructions}

    def varDec(self):
        """
        varDec: 'var' type varName (',' varName)* ';'
        """
        col = self.lexer.col
        line = self.lexer.line
        if self.check('token', 'var'):
            var = self.lexer.next()['token']
            type = self.lexer.next()['token']
            name = []
            name.append(self.lexer.next()['token'])
            while (self.check('token', ',')) :
                self.process(',')
                name.append(self.lexer.next()['token'])
            self.process(';')
        else :
            self.error(self.lexer.next())

        return {'line': line,'col': col, 'kind': var, 'type': type, 'name': name}

    def className(self):
        """
        className: identifier
        """
        if not self.check('type', 'identifier') :
            self.error(self.lexer.next())
        return self.lexer.next()['token']

    def subroutineName(self):
        """
        subroutineName: identifier
        """
        if not self.check('type', 'identifier') :
            self.error(self.lexer.next())
        return self.lexer.next()['token']

    def varName(self):
        """
        varName: identifier
        """
        if not self.check('type', 'identifier') :
            self.error(self.lexer.next())
        return self.lexer.next()['token']

    def statements(self):
        """
        statements : statements*
        """

        instructions = []
        while self.check('token',{'let','while','if','do','return'}) :
            instructions.append(self.statement())

        return instructions

    def statement(self):
        """
        statement : letStatements|ifStatement|whileStatement|doStatement|returnStatement
        """

        statementType = self.lexer.look()['token']
        match statementType:
            case 'let':
                return self.letStatement()
            case 'while':
                return self.whileStatement()
            case 'if':
                return self.ifStatement()
            case 'do':
                return self.doStatement()
            case 'return':
                return self.returnStatement()

    def letStatement(self):
        """
        letStatement : 'let' varName ('[' expression ']')? '=' expression ';'
        """
        col = self.lexer.col
        line = self.lexer.line
        type = self.lexer.next()['token']
        indice = "null"

        name = self.varName()
        if self.check("token", "[") :
            self.process("[")
            indice = self.expression()
            self.process(']')
        op = self.op()
        expr = self.expression()
        self.process(';')
        return {'line':line, 'col': col, 'type': type, 'name': name, 'indice': indice,'op': op,'expression': expr }

    def ifStatement(self):
        """
        ifStatement : 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        col = self.lexer.col
        line = self.lexer.line
        type = self.lexer.next()['token']

        self.process('(')
        cond = self.expression()
        self.process(')')
        self.process('{')
        true = []
        false = []
        true.append(self.statements())
        self.process('}')
        if self.check('token', 'else') :
            els = self.lexer.next()['token']
            self.process('{')
            false.append(self.statements())
            self.process('}')

        return {'line': line,'col': col, 'type': type, 'condition': cond, 'true' : true, 'false': false}

    def whileStatement(self):
        """
        whileStatement : 'while' '(' expression ')' '{' statements '}'
        """
        col = self.lexer.col
        line = self.lexer.line
        type = self.lexer.next()['token']

        self.process('(')
        cond = self.expression()
        self.process(')')
        self.process('{')
        statements = []
        statements.append(self.statements())
        self.process('}')

        return {'line': line,'col': col, 'type': type, 'condition': cond, 'instructions' : statements}

    def doStatement(self):
        """
        doStatement : 'do' subroutineCall ';'
        """
        col = self.lexer.col
        line = self.lexer.line
        type = self.lexer.next()['token']

        expr = self.subroutineCall()
        self.process(';')

        return {'line': line,'col': col, 'type': type, 'valeur': expr}

    def returnStatement(self):
        """
        returnStatement : 'return' expression? ';'
        """
        col = self.lexer.col
        line = self.lexer.line
        type = self.lexer.next()['token']
        expr = 'void'
        if not self.check('token',';'):
            expr = self.expression()
        self.process(';')

        return {'line': line,'col': col, 'type': type, 'valeur': expr}

    def expression(self):
        """
        expression : term (op term)*
        """
        col = self.lexer.col
        line = self.lexer.line
        expr = []
        while not self.check('token', {';', ')', ']'}):
            expr.append(self.term())
            if self.check('token', {'+', '-', '*', '/', '&', '|', '<', '>', '='}):
                expr.append(self.op())
            if self.check('token', ','):
                self.process(',')
            if self.check('token', {';', ')', ']'}):
                break

        return expr

    def term(self):
        """
        term : integerConstant|stringConstant|keywordConstant
                |varName|varName '[' expression ']'|subroutineCall
                | '(' expression ')' | unaryOp term
        """
        col = self.lexer.col
        line = self.lexer.line
        type = self.lexer.look()['type']
        t2 = self.lexer.look2()['token']

        if self.check('token', {'this', 'true', 'false', 'null'}) :
            return {'value': self.KeywordConstant(), 'type': 'keyword'}

        elif self.check('type', {'IntegerConstant', 'StringConstant', 'KeywordConstant'}):
            return {'value': self.lexer.next()['token'], 'type': 'constant'}

        elif self.check('type', 'symbol'):
            match self.lexer.look()['token']:
                case '(':
                    self.process('(')
                    exp = self.expression()
                    self.process(')')
                    return exp
                case '~' | '-':
                    return self.unaryOp()

        elif self.check('type', 'identifier'):
            match t2 :
                case '[' :
                    varname = self.varName()
                    self.process('[')
                    indice = self.expression()
                    self.process('[')
                    return {'value': varname, 'indice': indice, 'type': 'identifier'}
                case '.' :
                    return {'value': self.subroutineCall(), 'type': 'subroutine'}
                case _ :
                    return {'value': self.varName(), 'type': 'identifier'}
        else :
            self.error(self.lexer.next())

    def oldterm(self):
        """
        term : integerConstant|stringConstant|keywordConstant
                |varName|varName '[' expression ']'|subroutineCall
                | '(' expression ')' | unaryOp term
        """
        col = self.lexer.col
        line = self.lexer.line
        type = self.lexer.look()['type']
        t2 = self.lexer.look2()['token']

        if self.check('token', {'this', 'true', 'false', 'null'}) :
            return self.KeywordConstant()
        elif self.check('type',{'IntegerConstant', 'StringConstant', 'KeywordConstant'}) :
            return self.lexer.next()['token']
        elif self.check('type', 'symbol') :
            match self.lexer.look()['token']:
                case '(':
                    self.process('(')
                    ret = self.expression()
                    self.process(')')
                    return ret
                case '~' | '-':
                    return self.unaryOp()
        elif self.check('type','identifier') :
            match t2 :
                case '[' :
                    vn = self.varName()
                    self.process('[')
                    indice = self.expression()
                    self.process(']')
                    return vn, {'indice': indice}
                case '.' :
                    return self.subroutineCall()
                case _ :
                    return self.varName()
        else :
            self.error(self.lexer.next())



    def subroutineCall(self):
        """
        subroutineCall : subroutineName '(' expressionList ')'
                | (className|varName) '.' subroutineName '(' expressionList ')'
        Attention : l'analyse syntaxique ne peut pas distingué className et varName.
            Nous utiliserons la balise <classvarName> pour (className|varName)
        """
        col = self.lexer.col
        line = self.lexer.line

        t2 = self.lexer.look2()['token']
        match t2 :
            case '(' :
                name = self.subroutineName()
                self.process('(')
                exprl = self.expressionList()
                self.process(')')
                return {'line': line, 'col': col, 'classVar': 'vide', 'name': name, 'argument': exprl}
            case '.' :
                name = self.subroutineName()
                self.process('.')
                sub = self.subroutineCall()
                return {'line': line, 'col': col, 'classVar': name, 'name': sub['name'], 'argument': sub['argument']}

        return 'Todo'

    def expressionList(self):
        """
        expressionList : (expression (',' expression)*)?
        """
        if not self.check('token', ')'):
            return self.expression()

    def op(self):
        """
        op : '+'|'-'|'*'|'/'|'&'|'|'|'<'|'>'|'='
        """
        col = self.lexer.col
        line = self.lexer.line

        token = self.lexer.look()['token']
        if self.check('token',{'+','-','*','/','&','|','<','>','='}) :
            return {'value': self.lexer.next()['token'], 'type': 'op'}
        else :
            self.error(self.lexer.next())

    def unaryOp(self):
        """
        unaryop : '-'|'~'
        """
        return {'value': self.lexer.next()['token'], 'type': 'unary'}

    def KeywordConstant(self):
        """
        KeyWordConstant : 'true'|'false'|'null'|'this'
        """
        if self.check('token',{'true','false','null','this'}) :
            return {'value': self.lexer.next()['token'], 'type': 'constant'}
        else :
            self.error(self.lexer.next())

    def process(self, str):
        token = self.lexer.next()
        if (token is not None and token['token'] == str):
            return token
        else:
            self.error(token)

    def error(self, token):
        if token is None:
            print("Syntax error: end of file")
        else:
            print(f"SyntaxError (line={token['line']}, col={token['col']}): {token['token']}")
        exit()

    def check(self, attribute, value):         # Le nouveau incr()/decr()
        return self.lexer.hasNext() and self.lexer.look()[f'{attribute}'] in value

if __name__ == "__main__":
    file = sys.argv[1]
    print('-----debut')
    parser = Parser(file)
    arbre = parser.jackclass()
    todot = todot.Todot(file)
    todot.todot(arbre)
    print(arbre)
    print()
    print('variables')
    for x in arbre['varDec'] :
        print(x)
    print()
    print('subroutines')
    for x in arbre['subroutine'] :
        print(x)
    print('-----fin')
