# -*- coding: utf-8 -*-

# utils.py

def generate_filename(year, domain, type_filter=None):

    """
    Génère un nom de fichier dynamique basé sur les filtres fournis.
    
    Paramètres :
    - year (str) : La période pour laquelle les données sont extraites (format : YYYY-YYYY).
    - domain (str) : Le domaine scientifique sélectionné pour le filtrage.
    - type_filter (str, optionnel) : Le type de document utilisé pour le filtrage.

    Retourne :
    - str : Un nom de fichier formaté sous la forme all_data_<domaine>_<periode>_<type>.csv.
    
    Remarque :
    - Les caractères spéciaux dans les domaines et types sont remplacés par leurs équivalents sans accent pour assurer un formatage compatible avec les systèmes de fichiers.
    """
    parts = ["all_data"]  # Commence par un préfixe standard pour tous les fichiers

    if domain:  # Si un domaine est spécifié
        # Remplace les caractères spéciaux pour éviter les conflits dans les noms de fichiers
        safe_domain = domain.replace(" ", "_").replace("é", "e").replace("è", "e").replace("à", "a")
        parts.append(safe_domain)

    if year:  # Si une période est spécifiée
        parts.append(year)

    if type_filter:  # Si un type de document est spécifié
        # Remplace les caractères spéciaux pour garantir la compatibilité
        safe_type = type_filter.replace(" ", "_").replace("é", "e").replace("è", "e").replace("à", "a")
        parts.append(safe_type)

    # Combine toutes les parties pour former le nom final
    return "_".join(parts) + ".csv"

