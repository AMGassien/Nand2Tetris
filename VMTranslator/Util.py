class Util :

    def __init__(self, classname ='class'):
        self.classname = classname
        pass

    def incr(self): # à appeler avec self.util.incr()
        return f"""
        @SP
        M=M+1       // On incrémente SP
        
        """

    def decr(self): # à appeler avec self.util.decr()
        return f"""
        @SP
        M=M-1       // On décrémente SP
        
        """

    # -----------------------------------------------------------------------------JUMPS-----------------------------------------------------------------------------

    def commandjump(self, command):
        """Selecteur de la methode Util, sous-catégorie "Jumps" à utiliser"""
        type = command['type']
        # type = label|goto|if-goto
        match type:
            case 'label':
                return self.commandlabel(command)
            case 'goto':
                return self.commandgoto(command)
            case 'if-goto':
                return self.commandif_goto(command)

    def commandlabel(self, command):
        """label nom - Jio - Créé un (nom) """ # à appeler avec self.util.commandlabel({'type': 'label', 'label': 'nom'})

        label = command['label']
        return f"""\t//{command['type']} {label}
         ({self.classname}.{label})
        """

    def commandflabel(self, command):
        """Jio - Créé un (nom) """  # Copie de la création de label utilisé pour les Functions

        label = command['label']
        return f"""\t//{command['type']} {label}
            ({label})
           """

    def commandgoto(self, command):
        """goto label - Jio - Jump au label donné sans réfléchir """

        label = command['label']
        return f"""\t//{command['type']} {label}
         @{self.classname}.{label}        // On pointe sur notre étiquete
         0;JMP           // On jump
         """

    def commandif_goto(self, command):
        """if_goto label - Jio - Jump au label donné si SP=-1 et le dépile ! doit être appelé juste après un eq/lt/gt/... ! """
        label = command['label']
        return self.decr() + f"""\t//{command['type']} {label}
         A=M
         D=M+1
         M=0             // Inutile mais pour la visibilité des tests on dépile la valeur
         @{self.classname}.{label}
         D;JEQ
         """  # On pointe sur val1, pas besoin d'incrémenter elle est donc dépilée
