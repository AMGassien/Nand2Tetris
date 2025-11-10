import Util
import PushPop

class Fun:
    labelincr = 0

    def __init__(self, util = Util.Util(), classname = 'class'):
        self.util = util
        self.classname = classname
        self.pushPop = PushPop.PushPop()
        pass

    def commandfun(self, command):
        """ """
        type = command['type']
        # type= Function|return
        match type:
            case 'Function':
                return self.commandfunction(command)
            case 'return':
                return self.commandreturn(command)

    def saveframe(self, functionName, labelincr):
        """S'occupe de sauvegarder la frame du la fonction actuelle (returnAdress / LCL / ARG / THIS / THAT)
        avant qu'on appelle la suivante"""

        return f"""// On sauvegarde la frame de la fonction précédente
        @{self.classname}.{functionName}.retAddr$""" + str(labelincr) +"""         // On push la return adress
        D=A
        @SP
        A=M
        M=D
        """ + self.util.incr() + """
        @LCL
        D=M         // On stocke le pointer LCL dans D
        @SP
        A=M
        M=D         // On le place dans la pile 
        """  + self.util.incr() + """
        @ARG
        D=M         // On stocke le pointer ARG dans D
        @SP
        A=M
        M=D         // On le place dans la pile 
        """  + self.util.incr() + """
        @THIS
        D=M         // On stocke le pointer THIS dans D
        @SP
        A=M
        M=D         // On le place dans la pile 
        """  + self.util.incr() + """
        @THAT
        D=M         // On stocke le pointer THAT dans D
        @SP
        A=M
        M=D         // On le place dans la pile 
        """ + self.util.incr()

    def commandfunction(self, command):
        """Function name i - Jio - Initialise i cases pour les variables locale et lance la fonction
        A APPELER A CHAQUE FOIS QUE VOUS DEFINISSEZ UNE FONCTION DANS VOS .VM"""

        para = command['parameter']
        fun = command['function']
        initstr = f"// Initialisation des {para} variables locales\n"

        # va appeler i fois "push constant 0" pour allouer l'espace nécéssaire aux variables locales de la fonction
        for i in range(0, int(para)):
            initstr += self.pushPop.commandpushconstant({'type': 'push', 'segment': 'constant', 'parameter': '0'})

        return f"""\t//{command['type']} {command['function']} {command['parameter']}
        """ + self.util.commandflabel({'type': 'label', f'label': fun}) + """\n
        """ + initstr

    def commandreturn(self, command):
        """return - Jio - Push la valeur renvoyée par la fonction en haut de la pile pour remplacer l'argument 0
        et dépiler tout le reste puis restaure la frame de la fonction précédente """
# self.PushPop.commandpop({'type': 'pop', 'segment': 'argument', 'parameter': '0'})+
        return """\t//{command['type']}
        @LCL
        D=M             // On récupère l'adresse poitnée par LCL (première val locale/savedFrame+1)
        
        @endFrame
        M=D             // On stocke cette adresse dans un variable temp endFrame
        
        @5
        D=A
        @endFrame
        D=M-D           // On pars chercher l'indice 5 cases au dessus de endFrame
        @retAddr        // On le stocke dans une autre variable temp
        M=D
        
        """ + self.pushPop.commandpop({'type': 'pop', 'segment': 'argument', 'parameter': '0'}) + """ 
        // La valeur de la fonction est retournée, on réplace les pointers de la frame précédente
        
        @ARG
        D=M+1
        @SP
        M=D        
        
        @endFrame
        A=M
        A=A-1           // On pointe sur *(endFrame-1)
        D=M
        @THAT
        M=D             // THAT restored
        
        @2
        D=A
        @endFrame
        A=M
        A=A-D           // On pointe sur *(endFrame-2)
        D=M
        @THIS
        M=D
        
        
        
        @3
        D=A
        @endFrame
        A=M
        A=A-D           // On pointe sur *(endFrame-3)
        D=M
        @ARG            // ARG restored
        M=D
        
        @4
        D=A
        @endFrame
        A=M
        A=A-D           // On pointe sur *(endFrame-4)
        D=M
        @LCL           // LCL restored
        M=D
        
        @retAddr
        A=M
        A=M
        0;JMP
        """