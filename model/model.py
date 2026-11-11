from database.distributore_DAO import DistributoreDAO
from database.prezzo_DAO import PrezzoDAO
from model.distributore_DTO import Distributore

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        # TODO
        lista_tuple = []
        for distributore in self._distributori:
            #estraggo lista_prezzi per il mese scelto

            lista_prezzi = PrezzoDAO.get_prezzi(distributore.id)
            counter = 0
            somma = 0
            #per ogni record prezzo della benzina giornata per quel distrib.
            for oggetto_prezzo in lista_prezzi:
                if oggetto_prezzo.data.month == mese:
                    counter += 1
                    somma += oggetto_prezzo.prezzo_litro

            media = somma / counter
            lista_tuple.append((distributore.nome, media))

        return lista_tuple



    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        # TODO

        if giorno == 8:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = sequenza_parziale

        else:
            for distributore in self._distributori:
                prezzo = prezzi_settimana[distributore.id][giorno - 1]
                nuovo_costo = costo_corrente + prezzo * 100

                if ultimo_distributore is not None and distributore.id != ultimo_distributore:
                    nuovo_costo += 5

                nuova_sequenza = sequenza_parziale + [distributore.id]
                giorno += 1
                self.__ricorsione(nuova_sequenza, giorno , distributore.id, nuovo_costo, prezzi_settimana)





    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        # TODO
        distributori = DistributoreDAO.get_distributori()
        dict_prezzi_distributore = {}
        for distributore in distributori:

            lista_prezzi = distributore.get_prezzi()

            for oggetto_prezzo in lista_prezzi:
                if oggetto_prezzo.data.month == mese and 1 <= oggetto_prezzo.data.day <= 7:
                            if distributore.id not in dict_prezzi_distributore.keys():
                                dict_prezzi_distributore[distributore.id] = []
                            dict_prezzi_distributore[distributore.id].append(oggetto_prezzo.prezzo_litro)


        return dict_prezzi_distributore