"""No comment"""
import os
import glob
import sys

import Generator


class Translator:
    """Traduit les instructions .vm en asm """

    def __init__(self, files, asm):
        self.asm = open(asm, "w", encoding='utf8')
        self.files = files

    def translate(self):
        """Traduit un ou plusieur fichier"""
        self.asm.write(self._bootstrap())
        # os.listdir("/home/olivier")
        if os.path.isfile(self.files):
            self._translateonefile(self.files)
        else:
            if os.path.isdir(self.files):
                for file in glob.glob(f'{self.files}/*.vm'):
                    self._translateonefile(file)

    def _translateonefile(self, file):
        """Traduit un fichier en assembleur en utilisant le code de generator """
        self.asm.write(f"""\n//code de {file}\n""")
        generator = Generator.Generator(file)
        for command in generator:
            self.asm.write(command)

    def _bootstrap(self):
        """"""
        # init = Generator.Generator()._commandcall({'type': 'Call', 'function': 'Sys.init', 'parameter': '0'})

        return f""" // Bootstrap
        @256          // Boostrap à remettre à 256 à la fin des tests
        D=A
        @SP
        M=D         //Fin du Bootstrap
        
        @10         // BONUStrap
        D=A
        @LCL
        M=D
        
        @20
        D=A
        @ARG
        M=D
        
        @30
        D=A
        @THIS
        M=D
        
        @40
        D=A
        @THAT
        M=D
        """#+ {init} + """ """


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: Translator.py <vm file| dir> <asm file>")
    else:
        vmfiles=sys.argv[1]
        asmfile=sys.argv[2]
        translator = Translator(vmfiles,asmfile)
        translator.translate()
