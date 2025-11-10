 // Bootstrap
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
        
//code de test/Maths.vm
	//goto skipMaths
         @test.Maths.skipMaths        // On pointe sur notre étiquete
         0;JMP           // On jump
         	//Function mult 2
        	//label mult
            (mult)
           

        // Initialisation des 2 variables locales
	//push constant 0
        @0    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        	//push constant 0
        @0    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        	//push constant 0
        @0    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @SP
        M=M-1       // On décrémente SP
        
        	//pop local 0
                @0
                D=A
                @LCL
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
                	//push constant 1
        @1    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @SP
        M=M-1       // On décrémente SP
        
        	//pop local 1
                @1
                D=A
                @LCL
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
                	//label FMULTLOOP
         (test.Maths.FMULTLOOP)
        	//push argument 0
                @0
                D=A             // On stocke i(parameter)(indice de la variable segment à push)       

                @ARG      // On pointe sur le segment voulu
                A=D+M           // On pointe sur la variable du segment cherchée (indice = i + indice de base)
                D=M

                @SP
                A=M
                M=D
                
        @SP
        M=M+1       // On incrémente SP
        
        	//push local 0
                @0
                D=A             // On stocke i(parameter)(indice de la variable segment à push)       

                @LCL      // On pointe sur le segment voulu
                A=D+M           // On pointe sur la variable du segment cherchée (indice = i + indice de base)
                D=M

                @SP
                A=M
                M=D
                
        @SP
        M=M+1       // On incrémente SP
        
        //Code assembleur de {'line': 11, 'col': 5, 'type': 'add'}

            
        @SP
        M=M-1       // On décrémente SP
        
         //on décrémente SP pour récupérer val1 (elem en haut de la pile)
            A=M
            D=M         //val1 récup et stockée
            M=0         //on dépile val1
        
            @SP
            A=M-1       //on récup l'adresse de val2
            M=D+M       
            
        @SP
        M=M-1       // On décrémente SP
        
        	//pop local 0
                @0
                D=A
                @LCL
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
                	//push argument 1
                @1
                D=A             // On stocke i(parameter)(indice de la variable segment à push)       

                @ARG      // On pointe sur le segment voulu
                A=D+M           // On pointe sur la variable du segment cherchée (indice = i + indice de base)
                D=M

                @SP
                A=M
                M=D
                
        @SP
        M=M+1       // On incrémente SP
        
        	//push local 1
                @1
                D=A             // On stocke i(parameter)(indice de la variable segment à push)       

                @LCL      // On pointe sur le segment voulu
                A=D+M           // On pointe sur la variable du segment cherchée (indice = i + indice de base)
                D=M

                @SP
                A=M
                M=D
                
        @SP
        M=M+1       // On incrémente SP
        
        //code assembleur de {'line': 16, 'col': 5, 'type': 'eq'}

        //Code assembleur de {'type': 'sub'}

            
        @SP
        M=M-1       // On décrémente SP
        
         //on décrémente SP pour récupérer val1 (elem en haut de la pile)
            A=M
            D=M         //val1 récup et stockée
            M=0         //on dépile val1
        
            @SP
            A=M-1       //on récup l'adresse de val2
            M=M-D       
             // On appelle sub pour dépiler les deux valeurs et récupérer le résultat
        
        @SP
        M=M-1       // On décrémente SP
        
         // On retourne pointer sur le haut de la pile, si SP=0 alors true, sinon false
        @SP
        A=M
        D=M         // On stocke la valeur rendue par sub
        
        @test.Maths.JEQ_TRUE$1
        D;JEQ       // Si sub à renvoyée 0 on jump
                
        D=0         // On enregistre False (0) dans D
        @test.Maths.JEQ_END$1
        0;JMP       // On sors 
        
        	//label JEQ_TRUE$1
         (test.Maths.JEQ_TRUE$1)
                                        
        D=-1        // On enregistre True (-1) dans D
        
        	//label JEQ_END$1
         (test.Maths.JEQ_END$1)
         
        @SP
        A=M
        M=D
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @SP
        M=M-1       // On décrémente SP
        
        	//if-goto FMULTEND
         A=M
         D=M+1
         M=0             // Inutile mais pour la visibilité des tests on dépile la valeur
         @test.Maths.FMULTEND
         D;JEQ
         	//push local 1
                @1
                D=A             // On stocke i(parameter)(indice de la variable segment à push)       

                @LCL      // On pointe sur le segment voulu
                A=D+M           // On pointe sur la variable du segment cherchée (indice = i + indice de base)
                D=M

                @SP
                A=M
                M=D
                
        @SP
        M=M+1       // On incrémente SP
        
        	//push constant 1
        @1    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        //Code assembleur de {'line': 21, 'col': 5, 'type': 'add'}

            
        @SP
        M=M-1       // On décrémente SP
        
         //on décrémente SP pour récupérer val1 (elem en haut de la pile)
            A=M
            D=M         //val1 récup et stockée
            M=0         //on dépile val1
        
            @SP
            A=M-1       //on récup l'adresse de val2
            M=D+M       
            
        @SP
        M=M-1       // On décrémente SP
        
        	//pop local 1
                @1
                D=A
                @LCL
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
                	//goto FMULTLOOP
         @test.Maths.FMULTLOOP        // On pointe sur notre étiquete
         0;JMP           // On jump
         	//label FMULTEND
         (test.Maths.FMULTEND)
        	//push local 0
                @0
                D=A             // On stocke i(parameter)(indice de la variable segment à push)       

                @LCL      // On pointe sur le segment voulu
                A=D+M           // On pointe sur la variable du segment cherchée (indice = i + indice de base)
                D=M

                @SP
                A=M
                M=D
                
        @SP
        M=M+1       // On incrémente SP
        
        	//{command['type']}
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
        
        
        @SP
        M=M-1       // On décrémente SP
        
        	//pop argument 0
                @0
                D=A
                @ARG
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
        	//label skipMaths
         (test.Maths.skipMaths)
        	//label continue
         (test.Maths.continue)
        
//code de test/Main.vm
	//Function main 0
        	//label main
            (main)
           

        // Initialisation des 0 variables locales
	//push constant 1
        @1    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        	//push constant 2
        @2    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        	//push constant 3
        @3    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        	//Call mult 2
    
    // On sauvegarde la frame de la fonction précédente
        @test.Main.mult.retAddr$1         // On push la return adress
        D=A
        @SP
        A=M
        M=D
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @LCL
        D=M         // On stocke le pointer LCL dans D
        @SP
        A=M
        M=D         // On le place dans la pile 
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @ARG
        D=M         // On stocke le pointer ARG dans D
        @SP
        A=M
        M=D         // On le place dans la pile 
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @THIS
        D=M         // On stocke le pointer THIS dans D
        @SP
        A=M
        M=D         // On le place dans la pile 
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @THAT
        D=M         // On stocke le pointer THAT dans D
        @SP
        A=M
        M=D         // On le place dans la pile 
        
        @SP
        M=M+1       // On incrémente SP
        
        // La frame est sauvegardée on update les pointers
    
    // Update ARG
    @SP
    A=M
    D=A         // On stocke l'indice de SP
    @5
    D=D-A       // SP = SP-5
    @2
    D=D-A       // SP = SP-5-nArgs
    @ARG
    M=D         // ARG pointe maintenant sur le 1er argument de ceux donnés au dessus de la frame
    
    // Update LCL
    @SP
    D=M         // On stocke l'indice stocké dans SP
    @LCL
    M=D         // LCL pointe maintenant juste en dessous de la frame avec SP, on peut y stocker nos variables locales
    
    @mult                                                                               // Reste l'appel de contion
    0;JMP
    (test.Main.mult.retAddr$1)
    	//push constant 2
        @2    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        	//push constant 9
        @9    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        	//Call mult 2
    
    // On sauvegarde la frame de la fonction précédente
        @test.Main.mult.retAddr$2         // On push la return adress
        D=A
        @SP
        A=M
        M=D
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @LCL
        D=M         // On stocke le pointer LCL dans D
        @SP
        A=M
        M=D         // On le place dans la pile 
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @ARG
        D=M         // On stocke le pointer ARG dans D
        @SP
        A=M
        M=D         // On le place dans la pile 
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @THIS
        D=M         // On stocke le pointer THIS dans D
        @SP
        A=M
        M=D         // On le place dans la pile 
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @THAT
        D=M         // On stocke le pointer THAT dans D
        @SP
        A=M
        M=D         // On le place dans la pile 
        
        @SP
        M=M+1       // On incrémente SP
        
        // La frame est sauvegardée on update les pointers
    
    // Update ARG
    @SP
    A=M
    D=A         // On stocke l'indice de SP
    @5
    D=D-A       // SP = SP-5
    @2
    D=D-A       // SP = SP-5-nArgs
    @ARG
    M=D         // ARG pointe maintenant sur le 1er argument de ceux donnés au dessus de la frame
    
    // Update LCL
    @SP
    D=M         // On stocke l'indice stocké dans SP
    @LCL
    M=D         // LCL pointe maintenant juste en dessous de la frame avec SP, on peut y stocker nos variables locales
    
    @mult                                                                               // Reste l'appel de contion
    0;JMP
    (test.Main.mult.retAddr$2)
    //code assembleur de {'line': 9, 'col': 5, 'type': 'lt'}

        //Code assembleur de {'type': 'sub'}

            
        @SP
        M=M-1       // On décrémente SP
        
         //on décrémente SP pour récupérer val1 (elem en haut de la pile)
            A=M
            D=M         //val1 récup et stockée
            M=0         //on dépile val1
        
            @SP
            A=M-1       //on récup l'adresse de val2
            M=M-D       
             // On appelle sub pour dépiler les deux valeurs et récupérer le résultat
        
        @SP
        M=M-1       // On décrémente SP
        
         // On retourne pointer sur le haut de la pile, si SP=0 alors true, sinon false
        @SP
        A=M
        D=M         // On stocke la valeur rendue par sub
        
        @test.Main.JLT_TRUE$1
        D;JLT       // Si sub à renvoyée 0 on jump
                
        D=0         // On enregistre False (0) dans D
        @test.Main.JLT_END$1
        0;JMP       // On sors 
        
        	//label JLT_TRUE$1
         (test.Main.JLT_TRUE$1)
                                        
        D=-1        // On enregistre True (-1) dans D
        
        	//label JLT_END$1
         (test.Main.JLT_END$1)
         
        @SP
        A=M
        M=D
        
        @SP
        M=M+1       // On incrémente SP
        
        	//push constant 710
        @710    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        	//push constant 666
        @666    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        	//neg
            
        @SP
        M=M-1       // On décrémente SP
        
        //On décrémente SP pour repointer sur la dernière valeur stockée 
            
            @SP         // Charger l'adresse mémoire SP
            A=M         // On récupère l'adresse stockée en SP
            
            M=-M        // On inverse la valeur stockée en mémoire
            
        @SP
        M=M+1       // On incrémente SP
        
        //code assembleur de {'line': 13, 'col': 5, 'type': 'gt'}

        //Code assembleur de {'type': 'sub'}

            
        @SP
        M=M-1       // On décrémente SP
        
         //on décrémente SP pour récupérer val1 (elem en haut de la pile)
            A=M
            D=M         //val1 récup et stockée
            M=0         //on dépile val1
        
            @SP
            A=M-1       //on récup l'adresse de val2
            M=M-D       
             // On appelle sub pour dépiler les deux valeurs et récupérer le résultat
        
        @SP
        M=M-1       // On décrémente SP
        
         // On retourne pointer sur le haut de la pile, si SP=0 alors true, sinon false
        @SP
        A=M
        D=M         // On stocke la valeur rendue par sub
        
        @test.Main.JGT_TRUE$2
        D;JGT       // Si sub à renvoyée 0 on jump
                
        D=0         // On enregistre False (0) dans D
        @test.Main.JGT_END$2
        0;JMP       // On sors 
        
        	//label JGT_TRUE$2
         (test.Main.JGT_TRUE$2)
                                        
        D=-1        // On enregistre True (-1) dans D
        
        	//label JGT_END$2
         (test.Main.JGT_END$2)
         
        @SP
        A=M
        M=D
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @SP
        M=M-1       // On décrémente SP
        
        //code assembleur de {'line': 14, 'col': 5, 'type': 'and'}

        // les valeurs à comparer sont à l'adresse SP et SP-1
        @SP
        A=M
        D=M         // Charge la valeur (val1) à l'indice pointé par SP dans D
        
        
        @SP
        M=M-1       // On décrémente SP
        
          // On décrémente SP pour aller chercher val2
        
        @SP
        A=M
        D=D&M       // Effectue l'opération AND entre D(val1) et val2
        
        A=A+1
        M=0         // On dépile val1 (juste pour mieux voir dans la pile
        
        @SP
        A=M
        M=D
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @SP
        M=M-1       // On décrémente SP
        
        	//if-goto vrai
         A=M
         D=M+1
         M=0             // Inutile mais pour la visibilité des tests on dépile la valeur
         @test.Main.vrai
         D;JEQ
         	//label zombie
         (test.Main.zombie)
        	//push constant 3
        @3    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        	//push constant 15
        @15    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        	//push constant 15
        @15    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        //code assembleur de {'line': 21, 'col': 5, 'type': 'eq'}

        //Code assembleur de {'type': 'sub'}

            
        @SP
        M=M-1       // On décrémente SP
        
         //on décrémente SP pour récupérer val1 (elem en haut de la pile)
            A=M
            D=M         //val1 récup et stockée
            M=0         //on dépile val1
        
            @SP
            A=M-1       //on récup l'adresse de val2
            M=M-D       
             // On appelle sub pour dépiler les deux valeurs et récupérer le résultat
        
        @SP
        M=M-1       // On décrémente SP
        
         // On retourne pointer sur le haut de la pile, si SP=0 alors true, sinon false
        @SP
        A=M
        D=M         // On stocke la valeur rendue par sub
        
        @test.Main.JEQ_TRUE$3
        D;JEQ       // Si sub à renvoyée 0 on jump
                
        D=0         // On enregistre False (0) dans D
        @test.Main.JEQ_END$3
        0;JMP       // On sors 
        
        	//label JEQ_TRUE$3
         (test.Main.JEQ_TRUE$3)
                                        
        D=-1        // On enregistre True (-1) dans D
        
        	//label JEQ_END$3
         (test.Main.JEQ_END$3)
         
        @SP
        A=M
        M=D
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @SP
        M=M-1       // On décrémente SP
        
        	//if-goto presque
         A=M
         D=M+1
         M=0             // Inutile mais pour la visibilité des tests on dépile la valeur
         @test.Main.presque
         D;JEQ
         	//goto continue
         @test.Main.continue        // On pointe sur notre étiquete
         0;JMP           // On jump
         	//label vrai
         (test.Main.vrai)
        	//push constant 2
        @2    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        	//push constant 710
        @710    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        	//push constant 91
        @91    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        //Code assembleur de {'line': 30, 'col': 5, 'type': 'sub'}

            
        @SP
        M=M-1       // On décrémente SP
        
         //on décrémente SP pour récupérer val1 (elem en haut de la pile)
            A=M
            D=M         //val1 récup et stockée
            M=0         //on dépile val1
        
            @SP
            A=M-1       //on récup l'adresse de val2
            M=M-D       
            	//push constant 0
        @0    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @SP
        M=M-1       // On décrémente SP
        
        //code assembleur de {'line': 32, 'col': 5, 'type': 'not'}

        @SP
        A=M
        M=!M            // *(SP)=!*(SP)
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @SP
        M=M-1       // On décrémente SP
        
        //code assembleur de {'line': 33, 'col': 5, 'type': 'or'}

        // les valeurs à comparer sont à l'adresse SP et SP-1
        @SP
        A=M
        D=M         // Charge la valeur (val1) à l'indice pointé par SP dans D
        
        
        @SP
        M=M-1       // On décrémente SP
        
          // On décrémente SP pour aller chercher val2
        
        @SP
        A=M
        D=D|M       // Effectue l'opération AND entre D(val1) et val2
        
        A=A+1
        M=0         // On dépile val1 (juste pour mieux voir dans la pile
        
        @SP
        A=M
        M=D
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @SP
        M=M-1       // On décrémente SP
        
        	//if-goto zombie
         A=M
         D=M+1
         M=0             // Inutile mais pour la visibilité des tests on dépile la valeur
         @test.Main.zombie
         D;JEQ
         	//label presque
         (test.Main.presque)
        
        @SP
        M=M-1       // On décrémente SP
        
        	//pop temp 0
            @SP
            A=M
            D=M             // On récupère la valeur du haut de la pile
            
            @0
            A=A+1
            A=A+1
            A=A+1
            A=A+1
            A=A+1           // On pointe sur i+5
            M=D
            
        @SP
        M=M-1       // On décrémente SP
        
        	//pop temp 1
            @SP
            A=M
            D=M             // On récupère la valeur du haut de la pile
            
            @1
            A=A+1
            A=A+1
            A=A+1
            A=A+1
            A=A+1           // On pointe sur i+5
            M=D
            
        @SP
        M=M-1       // On décrémente SP
        
        	//pop temp 2
            @SP
            A=M
            D=M             // On récupère la valeur du haut de la pile
            
            @2
            A=A+1
            A=A+1
            A=A+1
            A=A+1
            A=A+1           // On pointe sur i+5
            M=D
            	//push constant 300
        @300    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @SP
        M=M-1       // On décrémente SP
        
        	//pop pointer 0
            @SP
            A=M
            D=M
            
            @THIS
            M=D
            	//push constant 400
        @400    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @SP
        M=M-1       // On décrémente SP
        
        	//pop pointer 1
            @SP
            A=M
            D=M
            
            @THAT
            M=D
            	//push constant 710
        @710    // @i (la constante) pour envoyer sa valeur dans A
        D=A             // On la stocke

        @SP             
        A=M             // On pars chercher l'indice pointé par SP où la stocker
        M=D             // On envoie la constante dans l'emplacement
        
        @SP
        M=M+1       // On incrémente SP
        
        
        @SP
        M=M-1       // On décrémente SP
        
        	//pop static 0
            @SP
            A=M
            D=M
            
            @test.Main.0
            M=D
            	//label fin
         (test.Main.fin)
        	//goto fin
         @test.Main.fin        // On pointe sur notre étiquete
         0;JMP           // On jump
         