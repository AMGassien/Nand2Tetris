import Util

class PushPop:

    def __init__(self, util = Util.Util(), classname = 'class'):
        self.classname = classname
        self.util = util
        self.segment = {'local':'LCL', 'argument':'ARG', 'this':'THIS', 'that':'THAT'}
        pass

    def commandpushpop(self, command):
        """Selectionne s'il faut appeler une methode push ou pop"""
        type = command['type']
        # type = push|pop
        match type:
            case 'push':
                return self.commandpushselect(command)
            case 'pop':
                return self.commandpopselect(command)

    # -----------------------------------------------------------------------------PUSH-----------------------------------------------------------------------------

    def commandpushselect(self, command):
        """push - Jio - S'occupe de scanner l'argument donné avec le push et appelle le bon"""

        segment = command['segment']
        # segment = constant | local|argument|this|that | pointer | static | temp
        match segment:
            # On appelle la sous fonction voulue
            case 'constant':
                return self.commandpushconstant(command)
            case 'local'|'argument'|'this'|'that':
                return self.commandpushother(command)
            case 'static':
                return self.commandpushstatic(command)
            case 'pointer':
                return self.commandpushpointer(command)
            case 'temp':
                return self.commandpushtemp(command)
            case _:
                return f'SyntaxError : {command}'
                exit()



    def commandpushconstant(self, command):
        """push constant i - Jio - insère i(@parameter) dans la pile et incrémente"""

        parameter = command['parameter']
        # segment = constant
        return f"""\t//{command['type']} {command['segment']} {parameter}
        @{parameter}    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        """ + self.util.incr()  # La valeur est push, on incrémente SP

    def commandpushother(self, command):
        """push segment i - Jio - insère i(@parameter) de la pile [segment] dans la pile et incrémente"""

        parameter = command['parameter']
        # segment = local|argument|this|that
        return f"""\t//{command['type']} {command['segment']} {parameter}
                @{parameter}
                D=A             // On stocke i(parameter)(indice de la variable segment à push)       

                @"""+ self.segment[command['segment']] +"""      // On pointe sur le segment voulu
                A=D+M           // On pointe sur la variable du segment cherchée (indice = i + indice de base)
                D=M

                @SP
                A=M
                M=D
                """ + self.util.incr()  # La variable segment i est pop, on incrémente SP

    def commandpushstatic(self,command):
        """push static i - Jio & Gassien - envoi la valeur dans class.i dans le haut de la pile"""

        parameter = command['parameter']
        # segment = static
        return f"""\t//{command['type']} {command['segment']} {parameter}
            @{self.classname}.{parameter}
            D=A
            @SP
            A=M
            M=D
            """+self.util.incr()

    def commandpushpointer(self,command):
        """push pointer i - Jio & Gassien - envoi la valeur de (THIS ou THAT) en haut de la pile"""

        parameter = command['parameter']
        pointer = {"0":"THIS","1":"THAT"}
        # segment = pointer
        return f"""\t//{command['type']} {command['segment']} {parameter}
            @{pointer[parameter]}
            D=M
            @SP
            A=M
            M=D
            """+self.util.incr()    # L'indicde de THIS ou THAT est push en haut de la pile, on incrémente

    def commandpushtemp(self,command):
        """push temp i - Jio & Gassien - envoi la valeur du haut de la pile dans le segment temp (5+i)"""

        parameter = command['parameter']
        # segment = local|argument|constant|this|that|pointer
        if int(parameter) > 7 and int(parameter)< 0:
            return "Le paramètre d'un push temp doit être entre 0 et 7 !"

        return f"""\t//{command['type']} {command['segment']} {parameter}
            @{parameter}
            D=A             // On stocke i(parameter)(indice de la variable segment à push)       

            @5 
            A=D+A           
            D=M
            
            @SP
            A=M
            M=D
            """ + self.util.incr()  # La variable 5+i est push, on incrémente SP

    #-----------------------------------------------------------------------------POP-----------------------------------------------------------------------------

    def commandpopselect(self, command):
        """pop segment i - Jio - choisis la bonne methode à appeler"""

        segment = command['segment']
        # segment = constant | local|argument|this|that | pointer|static|temp
        match segment:
            # On appelle la sous fonction voulue
            case 'local' | 'argument' | 'this' | 'that':
                return self.commandpop(command)
            case 'static':
                return self.commandpopstatic(command)
            case 'pointer':
                return self.commandpoppointer(command)
            case 'temp':
                return self.commandpoptemp(command)
            case _:
                return f'SyntaxError : {command}'
                exit()



    def commandpop(self, command):
        """pop segment i - Jio & Gassien - dépile la valeur du haut de la pile globale dans la pile [segment] à l'emplacement i(parameter)"""

        parameter = command['parameter']
        # segment = local|argument|this|that
        # on commence par décrémenter SP pour pointer sur le haut de la pile
        return self.util.decr() + f"""\t//{command['type']} {command['segment']} {parameter}
                @{parameter}
                D=A
                @""" + self.segment[command['segment']] + """
                A=D+M       // A pointe sur *segment[parameter]
                D=A
                
                @R13
                M=D         // On stocke l'adresse ou stocker temporairement
                
                @SP
                A=M
                D=M         // On récupère val1 (valeur du haut de la pile)
                
                @R13
                A=M
                M=D         // On envoie val1 dans *segment[parameter]
                """ # + self.util.incr() La variable segment i est pop, on incrémente PAS SP pour eviter outofmemory

    def commandpopstatic(self,command):
        """pop static i - Jio & Gassien - dépile la valeur du haut de la pile dans la variable class.i"""

        parameter = command['parameter']
        # segment = static
        # on commence par décrémenter SP pour pointer sur le haut de la pile
        return self.util.decr() + f"""\t//{command['type']} {command['segment']} {parameter}
            @SP
            A=M
            D=M
            
            @{self.classname}.{parameter}
            M=D
            """

    def commandpoppointer(self, command):
        """pop pointer - Jio & Gassien - depile la valeur du haut de la pile et la place dans (THIS ou THAT)"""

        parameter = command['parameter']
        # segment = pointer
        pointer = {"0": "THIS", "1": "THAT"}
        # on commence par décrémenter SP pour pointer sur le haut de la pile
        return self.util.decr() + f"""\t//{command['type']} {command['segment']} {parameter}
            @SP
            A=M
            D=M
            
            @{pointer[parameter]}
            M=D
            """

    def commandpoptemp(self,command):
        """pop temp i - Jio & Gassien - dépile la valeur du haut de la pile dans le segment temp (5+i)"""

        parameter = command['parameter']
        # segment = temp
        if int(parameter)>7 and int(parameter)<0:
            return "Le paramètre d'un pop temp doit être entre 0 et 7 !"
        # on commence par décrémenter SP pour pointer sur le haut de la pile
        return self.util.decr() + f"""\t//{command['type']} {command['segment']} {parameter}
            @SP
            A=M
            D=M             // On récupère la valeur du haut de la pile
            
            @{parameter}
            A=A+1
            A=A+1
            A=A+1
            A=A+1
            A=A+1           // On pointe sur i+5
            M=D
            """  # La valeur en haut de la pile est dépilée et envoyée en 5+i