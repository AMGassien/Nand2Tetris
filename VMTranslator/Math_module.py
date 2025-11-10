import Util

class Math:

    def __init__(self, util = Util.Util()):
        self.util = util
        self.operator = {'add':'D+M', 'sub':'M-D'}
        pass

    def commandmath(self, command):
        """Selecteur de la methode Math_module à utiliser"""

        type = command['type']
        # type = add|sub|neg
        match type:
            case 'add'|'sub':
                return self.commandaddsub(command)
            case 'neg':
                return self.commandneg(command)

    def commandaddsub(self, command):
        """add/sub - Jio - Dépile val1 et l'ajoute ou le soustrait à val2 (SP-1)"""

        op = self.operator[command['type']]
        return f"""//Code assembleur de {command}\n
            """ + self.util.decr()+ """ //on décrémente SP pour récupérer val1 (elem en haut de la pile)
            A=M
            D=M         //val1 récup et stockée
            M=0         //on dépile val1
        
            @SP
            A=M-1       //on récup l'adresse de val2
            M=""" + op + """       
            """ # Addition/Soustraction faite et on pointe sur l'ancien val1, pas besoin d'incrémenter

    def commandneg(self, command):
        """neg - Nathan & Jio - récupère l'élement en haut de la pile et le remplace par son inverse"""

        return f"""\t//{command['type']}
            """ +  self.util.decr() + """//On décrémente SP pour repointer sur la dernière valeur stockée 
            
            @SP         // Charger l'adresse mémoire SP
            A=M         // On récupère l'adresse stockée en SP
            
            M=-M        // On inverse la valeur stockée en mémoire
            """ + self.util.incr() # On retourne pointer sur SP+1 pour la prochaine insertion

