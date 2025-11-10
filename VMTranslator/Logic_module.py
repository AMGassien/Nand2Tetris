import Util
import Math_module

class Logic:
    labelincr = 0

    def __init__(self, util = Util.Util(), classname = "class"):
        self.util = util
        self.classname = classname
        self.math_module = Math_module.Math(self.util)
        self.logic = {'eq':'JEQ', 'gt':'JGT', 'lt':'JLT', 'and':'&', 'or':'|'}
        pass

    def commandlogic(self, command):
        """Selecteur de la methode Logic_module à utiliser"""

        type = command['type']
        # type = eq|lt|gt | and|or | not
        match type:
            case 'eq'|'gt'|'lt':
                return self.commandeqglt(command)
            case 'and'|'or':
                return self.commandandor(command)
            case 'not':
                return self.commandnot(command)

    # -----------------------------------------------------------------------------LOGIC-----------------------------------------------------------------------------

    def commandeqglt(self, command):
        """eq/gt/lt - Jio - On dépile val1 et val2=val2-v1 (Si val2=0 alors eq True, si positif alors gt True, si negatif alors lt True)"""

        cond = self.logic[command['type']] # On utilise notre dictionnaire pour stocker JEQ / JGT / JLT
        self.labelincr += 1
        return f"""//code assembleur de {command}\n
        """ + self.math_module.commandaddsub({'type':'sub'}) + """ // On appelle sub pour dépiler les deux valeurs et récupérer le résultat
        """ + self.util.decr() + f""" // On retourne pointer sur le haut de la pile, si SP=0 alors true, sinon false
        @SP
        A=M
        D=M         // On stocke la valeur rendue par sub
        
        @{self.classname}.{cond}_TRUE$"""+str(self.labelincr)+"""
        D;"""+cond+f"""       // Si sub à renvoyée 0 on jump
                
        D=0         // On enregistre False (0) dans D
        @{self.classname}.{cond}_END$"""+str(self.labelincr)+"""
        0;JMP       // On sors 
        
        """ +self.util.commandlabel({'type': 'label', 'label': f'{cond}_TRUE$'+str(self.labelincr)})+ """                                
        D=-1        // On enregistre True (-1) dans D
        
        """ + self.util.commandlabel({'type': 'label', 'label': f'{cond}_END$'+str(self.labelincr)})+""" 
        @SP
        A=M
        M=D
        """ + self.util.incr() # Notre 'boolean' est enregistré en haut de la pile, on incrémente

    def commandandor(self, command):
        """and/or - Nathan & Jio - On dépile val1 et val2=val2&val1 / val2|val1"""

        # on commence par décrémenter SP pour pointer sur le haut de la pile
        return self.util.decr() + f"""//code assembleur de {command}\n
        // les valeurs à comparer sont à l'adresse SP et SP-1
        @SP
        A=M
        D=M         // Charge la valeur (val1) à l'indice pointé par SP dans D
        
        """ + self.util.decr() + """  // On décrémente SP pour aller chercher val2
        
        @SP
        A=M
        D=D""" + self.logic[command['type']] + """M       // Effectue l'opération AND entre D(val1) et val2
        
        A=A+1
        M=0         // On dépile val1 (juste pour mieux voir dans la pile
        
        @SP
        A=M
        M=D
        """ + self.util.incr() # Notre 'boolean' est enregistré dans val2, on incrémente pour pointer sur val1 elle est donc dépilée

    def commandnot(self, command):
        """not - Jio - On remplace val1 par !val1 : True val1=-1 , False val1=0 """

        # on commence par décrémenter SP pour pointer sur le haut de la pile
        return self.util.decr() + f"""//code assembleur de {command}\n
        @SP
        A=M
        M=!M            // *(SP)=!*(SP)
        """ + self.util.incr()  # Notre 'boolean' est enregistré en haut de la pile, on incrémente