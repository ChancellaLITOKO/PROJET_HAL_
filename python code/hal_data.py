# -*- coding: utf-8 -*-
"""
Auteurs: Anas Nay & Chancella Litoko
"""

import requests
import pandas as pd
from unidecode import unidecode
from mapping import map_doc_type, map_domain, get_domain_code, get_type_code

def clean_name(name):  # Fonction pour nettoyer les noms (suppression des accents, des espaces et mise en minuscules)
    """
    Nettoie un nom en supprimant les caractères non alphanumériques, en le désaccentuant et en le mettant en minuscules.
    Args:
        name (str): Le nom à nettoyer.
    Returns:
        str: Nom nettoyé.
    """
    return ''.join(e for e in unidecode(name) if e.isalnum()).lower()

def get_hal_data(nom, prenom, period=None, domain_filter=None, type_filter=None): # Fonction principale pour extraire les données d'un auteur à partir de l'API HAL
    """
    Récupère les publications et les informations d'un auteur à partir de l'API HAL.
    
    Args:
        nom (str): Nom de l'auteur.
        prenom (str): Prénom de l'auteur.
        period (str, optional): Période de publication au format "AAAA-AAAA".
        domain_filter (list, optional): Liste des domaines scientifiques à filtrer.
        type_filter (list, optional): Liste des types de documents à filtrer.
    
    Returns:
        pandas.DataFrame: Tableau contenant les données extraites des publications.
    """
        
    # Nettoyage des noms pour construire les requetes
    nom_clean = clean_name(nom)
    prenom_clean = clean_name(prenom)

    # Construction de la base de l'URL pour récupérer les identifiants HAL
    id_query_url = f"https://api.archives-ouvertes.fr/search/?q=authFullName_t:{prenom_clean} {nom_clean}&fl=halId_s,authIdHal_s&wt=json"
    id_response = requests.get(id_query_url)

    hal_id_str, hal_id_num = "Non disponible", "Non disponible"
    if id_response.status_code == 200:
        id_data = id_response.json()
        documents = id_data.get("response", {}).get("docs", [])
        
        #Identifier le bon IDHAL en verifiant les correspondances entre le nom/prenom
        for doc in documents:
            if 'authIdHal_s' in doc:
                for id in doc['authIdHal_s']:
                    cleaned_id = clean_name(id)
                    if prenom_clean in cleaned_id and nom_clean[:max(4, len(nom_clean)//2)] in cleaned_id:
                        hal_id_str = id
                        break
            if 'halId_s' in doc:
                hal_id_num = doc['halId_s']

    # Déterminer l'IdHAL de l'auteur final
    idhal_final = hal_id_str if hal_id_str != "Non disponible" else hal_id_num

    # Construction de l'URL pour récupérer les publications
    query_url = f"https://api.archives-ouvertes.fr/search/?q=authFullName_t:{prenom_clean}%20{nom_clean}"

    #Ajout un filtre de periode si specifié 
    if period:
        try:
            start_year, end_year = period.split("-")
            query_url += f"&fq=publicationDateY_i:[{start_year} TO {end_year}]"
        except ValueError:
            print("Le format de la période doit être sous la forme AAAA-AAAA.")
            return pd.DataFrame()
    
    #Ajout filtre de domaine si specifié
    if domain_filter:
        domain_codes = [get_domain_code(d) for d in domain_filter if get_domain_code(d)]
        if domain_codes:
            query_url += f"&fq=domain_s:({' OR '.join(domain_codes)})"
    
    #Ajout un filtre de type de document si specifié
    if type_filter:
        type_codes = [get_type_code(t) for t in type_filter if get_type_code(t)]
        if type_codes:
            query_url += f"&fq=docType_s:({' OR '.join(type_codes)})"
    

    query_url += "&fl=authIdHal_s,docid,title_s,publicationDateY_i,docType_s,domain_s,keyword_s,labStructName_s&wt=json"

    response = requests.get(query_url)

    if response.status_code == 200:
        data = response.json()
        publications = data.get("response", {}).get("docs", [])
        
        #Liste pour stocker les données des publications
        scientist_data = []

        for pub in publications:
            authors = pub.get("authIdHal_s", [])
            authors_sorted = sorted(authors, key=lambda x: clean_name(x.split('-')[-1])) if authors else ["Id non disponible"]

            scientist_data.append(
                {
                    "Nom": nom.capitalize(),
                    "Prenom": prenom.capitalize(),
                    "IdHAL de l'Auteur": idhal_final,
                    "IdHAL des auteurs de la publication": authors_sorted,
                    "Titre": pub.get("title_s", "Titre non disponible"),
                    "Docid": pub.get("docid", "Id non disponible"),
                    "Année de Publication": pub.get("publicationDateY_i", "Année non disponible"),
                    "Type de Document": map_doc_type(pub.get("docType_s", "Type non défini")),
                    "Domaine": map_domain(pub.get("domain_s", "Domaine non défini")),
                    "Mots-clés": pub.get("keyword_s", []),
                    "Laboratoire de Recherche": pub.get("labStructName_s", "Non disponible"),
                }
            )
        # Retourner les donnees sous forme de Dataframe pandas
        return pd.DataFrame(scientist_data)
    else:
        print(f"Erreur lors de la récupération des données pour {nom} {prenom} : {response.status_code}")
        return pd.DataFrame()
