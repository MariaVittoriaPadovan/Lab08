from database.impianto_DAO import ImpiantoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        # TODO
        risultato = []

        for impianto in self._impianti:
            consumi = impianto.get_consumi()
            consumi_mese=[]

            for consumo in consumi:
                if consumo.data.month==mese:
                    consumi_mese.append(consumo.kwh)

            if consumi_mese:
                media = sum(consumi_mese) / len(consumi_mese)
            else:
                media = 0

            risultato.append((impianto.nome, round(media,2)))

        return risultato

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # TODO

        # condizione terminale
        if giorno == 8:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = sequenza_parziale.copy()
            return

        for imp_id in consumi_settimana.keys():

            costo = costo_corrente

            # costo spostamento (solo dal giorno 2 in poi)
            if ultimo_impianto is not None and imp_id != ultimo_impianto:
                costo += 5

            # costo variabile = kwh di quel giorno
            costo += consumi_settimana[imp_id][giorno - 1]

            # costruzione nuova sequenza
            sequenza_parziale.append(imp_id)

            self.__ricorsione(sequenza_parziale, giorno + 1, imp_id, costo, consumi_settimana)

            sequenza_parziale.pop()  # backtracking

    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        # TODO

        consumi = {}

        for impianto in self._impianti:
            lista_consumi = impianto.get_consumi()
            consumi_settimana=[]

            for consumo in lista_consumi:
                if consumo.data.month==mese and 1 <= consumo.data.day <= 7:
                    consumi_settimana.append(consumo.kwh)

            consumi[impianto.id] = consumi_settimana #assegno la lista al dizionario

        return consumi

