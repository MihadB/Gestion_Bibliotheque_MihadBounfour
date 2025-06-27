class LivreIndisponibleError(Exception):
    def __init__(self,message = " Livre indisponible !"):
        super(). __init__(message)




class QuotaEmpruntDepasseError(Exception) :
    def __init__(self,message = " Quota maximum d'emprunts atteint "):
        super(). __init__(message)


class MembreInexistantError(Exception) :
    def __init__(self,message = "Membre Inexistant !"):
        super(). __init__(message)


class LivreInexistantError(Exception) :
    def __init__(self,message = "Livre inexistant !"):
        super(). __init__(message)



