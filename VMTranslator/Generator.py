"""No comment"""

import sys

import Parser

import Util
import PushPop
import Math_module
import Logic_module
import Fun_module

class Generator:
    """No comment"""
    labelincr = 0

    def __init__(self, file=None):
        """si ce n'est pas un fichier"""
        if file is not None:
            self.parser = Parser.Parser(file)
            self.labelcount = 0
            self.classname = file[0:-3]     # Enregistre dans self.classname le nom du fichier et supprime les 3 derniers caractères
            self.classname = self.classname.replace("/", ".")   # Remplace les / par des .
            self.classname = self.classname.replace("\\", ".")  # Remplaxe les \ par des .
            self.util = Util.Util(self.classname)
            self.pushPop = PushPop.PushPop(self.util, self.classname)
            self.math_module = Math_module.Math(self.util)
            self.logic_module = Logic_module.Logic(self.util, self.classname)
            self.fun_module = Fun_module.Fun(self.util, self.classname)

    def __iter__(self):
        return self

    def __next__(self):
        if self.parser is not None and self.parser.hasNext():
            return self._next()
        else:
            raise StopIteration

    def _next(self):
        # No comment
        command = self.parser.next()
        if command is None:
            return None
        else:
            type = command['type']
            # type = push|pop|
            #        add|sub|neg|eq|gt|lt|and|or|not
            #        label|goto|if-goto|
            #        Function|Call|return
            match type:
                # Faire une fonction par type de commande
                case 'push'|'pop':                      #-------Fini-------#
                    return self.pushPop.commandpushpop(command)
                case 'add'|'sub'|'neg':                 #-------Fini-------#
                    return self.math_module.commandmath(command)
                case 'eq'|'lt'|'gt'|'and'|'or'|'not':   #-------Fini-------#
                    return self.logic_module.commandlogic(command)
                case 'label'|'goto'|'if-goto':          #-------Fini-------#
                    return self.util.commandjump(command)
                case 'Function'|'return':               #-------Fini-------#
                    return self.fun_module.commandfun(command)
                case 'Call':                            #-------Fini-------#
                    return self._commandcall(command)
                case _:
                    print(f'SyntaxError : {command}')
                    exit()

    def _commandcall(self, command):
        """Call function i - Jio - Appelle la fonction donnée avec i=nArgs de la function
        Sauvegarde la frame de la fonction mère (returnAddress)/LCL/ARG/THIS/THAT et repositionne les pointers"""

        self.labelincr += 1
        para = command['parameter']
        fun = command['function']

        return f"""\t//{command['type']} {command['function']} {command['parameter']}
    
    """ + self.fun_module.saveframe(fun,self.labelincr) + """// La frame est sauvegardée on update les pointers
    
    // Update ARG
    @SP
    A=M
    D=A         // On stocke l'indice de SP
    @5
    D=D-A       // SP = SP-5
    @"""+str(para)+f"""
    D=D-A       // SP = SP-5-nArgs
    @ARG
    M=D         // ARG pointe maintenant sur le 1er argument de ceux donnés au dessus de la frame
    
    // Update LCL
    @SP
    D=M         // On stocke l'indice stocké dans SP
    @LCL
    M=D         // LCL pointe maintenant juste en dessous de la frame avec SP, on peut y stocker nos variables locales
    
    @{fun}                                                                               // Reste l'appel de contion
    0;JMP
    ({self.classname}.{command['function']}.retAddr$"""+str(self.labelincr)+""")
    """

if __name__ == '__main__':
    file = sys.argv[1]
    print('-----debut')
    generator = Generator(file)
    for command in generator:
        print(command)
    print('-----fin')
