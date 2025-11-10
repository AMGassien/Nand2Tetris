import sys
from operator import truediv
from os import write

import Lexer


class ParserXML:
    """No comment"""

    def __init__(self, file):
        self.lexer = Lexer.Lexer(file)
        self.xml = open(file[0:-5] + ".xml", "w")
        self.xml.write('<?xml version="1.0" encoding="UTF-8"?>')

    def jackclass(self):
        """
        class: 'class' className '{' classVarDec* subroutineDec* '}'
        """
        self.xml.write(f"""<class>\n""")

        self.process('class')
        self.className()
        self.process('{')

        while self.check('token',{'static','field'}) :                  # Tant qu'on déclare des variables de classe
            self.classVarDec()

        while self.check('token',{'constructor','function','method'}) : # Tant qu'on déclare des constructeurs/methodes
            self.subroutineDec()

        self.process('}')

        self.xml.write(f"""</class>\n""")

    def classVarDec(self):
        """
        classVarDec: ('static'| 'field') type varName (',' varName)* ';'
        """
        self.xml.write(f"""<classVarDec>\n""")

        if self.check('token',{'static','field'}) :
            token = self.lexer.next()
            self.xml.write(f"""<keyword>{token['token']}</keyword>""")
        else :
            self.error(self.lexer.next())
        self.type()
        self.varName()
        while self.lexer.look()['token'] == ',' :
            self.process(',')
            self.varName()
        self.process(';')

        self.xml.write(f"""</classVarDec>\n""")

    def type(self):
        """
        type: 'int'|'char'|'boolean'|className
        """
        self.xml.write(f"""<type>""")

        if self.check('token',{'int','char','boolean'}) :
            token = self.lexer.next()
            self.xml.write(token['token'])
        elif self.check('type','identifier') :
            self.className()
        else :
            self.error(self.lexer.next())

        self.xml.write(f"""</type>""")

    def subroutineDec(self):
        """
        subroutineDec: ('constructor' | 'function'|'method') ('void'|type)
        subroutineName '(' parameterList ')' subroutineBody
        """
        self.xml.write(f"""<subroutineDec>\n""")

        if self.check('token',{'constructor','function','method'}) :
            token = self.lexer.next()['token']
            self.xml.write(f"""<keyword>{token}</keyword>""")

            if token != 'constructor' and self.check('type','keyword') :        # Si ce n'est pas un constructeur
                self.xml.write(f"""<keyword>{self.lexer.next()['token']}</keyword>""")        # Alors type retourné
            else :                              # Si c'est un constructeur
                self.className()                # Alors nom Object construit

            self.subroutineName()
            self.parameterList()

            self.subroutineBody()
        else :
            self.error(self.lexer.next())

        self.xml.write(f"""</subroutineDec>\n""")

    def parameterList(self):
        """
        parameterList: ((type varName) (',' type varName)*)?
        """
        self.process('(')
        self.xml.write(f"""<parameterList>\n""")

        while not self.check('token',')') :          # Tant que le token suivant n'est pas la fin de la parenthèse
            if self.check('type',{'keyword','identifier'}) :  # Si après la ( on a bien le type de la variable à donner
                self.type()                 # Le type de la variable
                self.varName()              # Le nom de la variable
                if self.check('token',',') :   # On regarde s'il y à une , et donc une variable supplémentaire
                    self.process(',')
            else :
                self.error(self.lexer.next())

        self.xml.write(f"""</parameterList>\n""")
        self.process(')')

    def subroutineBody(self):
        """
        subroutineBody: '{' varDec* statements '}'
        """
        self.xml.write(f"""<subroutineBody>\n""")
        self.process('{')

        while self.check('token','var') :       # Tant qu'on déclare des variables
            self.varDec()

        self.statements()

        self.process('}')
        self.xml.write(f"""</subroutineBody>\n""")

    def varDec(self):
        """
        varDec: 'var' type varName (',' varName)* ';'
        """
        self.xml.write(f"""<varDec>\n""")

        if self.check('token','var') :
            token = self.lexer.next()['token']
            self.xml.write(token)
            self.type()
            self.varName()
            while self.check('token',',') :         # Si on déclare plusieurs variables du même type
                self.process(',')
                self.varName()
            self.process(';')
        else :
            self.error(self.lexer.next())

        self.xml.write(f"""</varDec>\n""")

    def className(self):
        """
        className: identifier
        """
        self.xml.write(f"""<className>""")

        if self.check('type','identifier') :
            token = self.lexer.next()
            self.xml.write(token['token'])
        else :
            self.error(self.lexer.next())

        self.xml.write(f"""</className>""")

    def subroutineName(self):
        """
        subroutineName: identifier
        """
        self.xml.write(f"""<subroutineName>""")

        if self.check('type','identifier') :
            token = self.lexer.next()
            self.xml.write(token['token'])
        else :
            self.error(self.lexer.next())

        self.xml.write(f"""</subroutineName>""")

    def varName(self):
        """
        varName: identifier
        """
        self.xml.write(f"""<varName>""")

        if self.check('type','identifier') :
            token = self.lexer.next()
            self.xml.write(token['token'])
            if self.check('token','[') :
                self.process('[')
                self.expression()
                self.process(']')
        else :
            self.error(self.lexer.next())

        self.xml.write(f"""</varName>""")

    def statements(self):
        """
        statements : statements*
        """
        self.xml.write(f"""<statements>\n""")

        while self.check('token',{'let','while','if','do','return'}) :
            self.statement()

        self.xml.write(f"""</statements>\n""")

    def statement(self):
        """
        statement : letStatements|ifStatement|whileStatement|doStatement|returnStatement
        """
        self.xml.write(f"""<statement>\n""")

        statementType = self.lexer.look()['token']
        match statementType :
            case 'let' :
                self.letStatement()
            case 'while' :
                self.whileStatement()
            case 'if' :
                self.ifStatement()
            case 'do' :
                self.doStatement()
            case 'return' :
                self.returnStatement()

        self.xml.write(f"""</statement>\n""")

    def letStatement(self):
        """
        letStatement : 'let' varName ('[' expression ']')? '=' expression ';'
        """
        self.xml.write(f"""<letStatement>\n""")
        self.xml.write(f"""<keyword>{self.lexer.next()['token']}</keyword>""")

        self.varName()
        self.op()
        self.expression()
        self.process(';')

        self.xml.write(f"""</letStatement>\n""")

    def ifStatement(self):
        """
        ifStatement : 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        self.xml.write(f"""<ifStatement>\n""")

        self.xml.write(self.lexer.next()['token'])
        self.process('(')
        self.expression()
        self.process(')')
        self.process('{')
        self.statements()
        self.process('}')

        if self.check('token','else') :
            self.xml.write(self.lexer.next()['token'])
            self.process('{')
            self.statements()
            self.process('}')

        self.xml.write(f"""</ifStatement>\n""")

    def whileStatement(self):
        """
        whileStatement : 'while' '(' expression ')' '{' statements '}'
        """
        self.xml.write(f"""<whileStatement>\n""")

        self.xml.write(self.lexer.next()['token'])
        self.process('(')
        self.expression()
        self.process(')')
        self.process('{')
        self.statements()
        self.process('}')

        self.xml.write(f"""</whileStatement>\n""")

    def doStatement(self):
        """
        doStatement : 'do' subroutineCall ';'
        """
        self.xml.write(f"""<doStatement>\n""")

        self.xml.write(self.lexer.next()['token'])
        self.subroutineCall()
        self.process(';')

        self.xml.write(f"""</doStatement>\n""")

    def returnStatement(self):
        """
        returnStatement : 'return' expression? ';'
        """
        self.xml.write(f"""<returnStatement>\n""")

        self.xml.write(self.lexer.next()['token'])
        if not self.check('token',';'):
            self.expression()
        self.process(';')

        self.xml.write(f"""</returnStatement>\n""")

    def expression(self):
        """
        expression : term (op term)*
        """
        self.xml.write(f"""<expression>\n""")

        while not self.check('token',{';',')',']'}) :
            self.term()
            if self.check('token',{'+','-','*','/','&','|','<','>','='}) :
                self.op()
            if self.check('token',',') :
                self.process(',')
            if self.check('token',{';',')'}) :
                break


        self.xml.write(f"""</expression>\n""")

    def term(self):
        """
        term : integerConstant|stringConstant|keywordConstant
                |varName|varName '[' expression ']'|subroutineCall
                | '(' expression ')' | unaryOp term
        """
        self.xml.write(f"""<term>""")

        type = self.lexer.look()['type']
        t2 = self.lexer.look2()['token']
        if self.check('token', {'this', 'true', 'false','null'}) :
            self.KeywordConstant()
        elif self.check('type',{'IntegerConstant','StringConstant','KeywordConstant'}) :
            self.xml.write(f"""<{type}>{self.lexer.next()['token']}</{type}>""")
        elif self.check('type', 'symbol') :
            match self.lexer.look()['token']:
                case '(' :
                    self.process('(')
                    self.expression()
                    self.process(')')
                case '~'|'-' :
                    self.unaryOp()
        elif self.check('type','identifier') :
            match t2 :
                case '[' :
                    self.varName()
                case '.' :
                    self.subroutineCall()
                case _ :
                    self.varName()
        else :
            self.error(self.lexer.next())

    #    while self.check('token',{'.','(',')'}) :
    #        token = self.lexer.look()['token']
    #        self.process(token)
    #        if token != ')' :
    #            self.xml.write(f"""<{type}>{self.lexer.next()['token']}</{type}>""")

        self.xml.write(f"""</term>""")

    def subroutineCall(self):
        """
        subroutineCall : subroutineName '(' expressionList ')'
                | (className|varName) '.' subroutineName '(' expressionList ')'
        Attention : l'analyse syntaxique ne peut pas distingué className et varName.
            Nous utiliserons la balise <classvarName> pour (className|varName)
        """
        self.xml.write(f"""<subroutineCall>\n""")

        t2 = self.lexer.look2()['token']
        match t2 :
            case '(' :
                self.subroutineName()
                self.process('(')
                self.expressionList()
                self.process(')')
            case '.' :
                self.xml.write(f"""<classvarName>{self.lexer.next()['token']}</classvarName>""")
                self.process('.')
                self.subroutineCall()

        self.xml.write(f"""</subroutineCall>\n""")

    def expressionList(self):
        """
        expressionList : (expression (',' expression)*)?
        """
        self.xml.write(f"""<expressionList>\n""")

        if not self.check('token',')'):
            self.expression()

        self.xml.write(f"""</expressionList>\n""")

    def op(self):
        """
        op : '+'|'-'|'*'|'/'|'&'|'|'|'<'|'>'|'='
        """
        self.xml.write(f"""<op>""")

        token = self.lexer.look()['token']
        if self.check('token',{'+','-','*','/','&','|','<','>','='}) :
            self.process(token)
        else :
            self.error(self.lexer.next())

        self.xml.write(f"""</op>""")

    def unaryOp(self):
        """
        unaryop : '-'|'~'
        """
        self.xml.write(f"""<unaryop>""")

        self.xml.write(self.lexer.next()['token'])

        self.xml.write(f"""</unaryop>""")

    def KeywordConstant(self):
        """
        KeyWordConstant : 'true'|'false'|'null'|'this'
        """
        self.xml.write(f"""<KeyWordConstant>\n""")

        if self.check('token',{'true','false','null','this'}) :
            self.xml.write(self.lexer.next()['token'])
        else :
            self.error(self.lexer.next())

        self.xml.write(f"""</KeyWordConstant>\n""")

    def process(self, str):
        token = self.lexer.next()
        if (token is not None and token['token'] == str):
            self.xml.write(f"""<{token['type']}>{token['token']}</{token['type']}>\n""")
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
    parser = ParserXML(file)
    parser.jackclass()
    print('-----fin')
