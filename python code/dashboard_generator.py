# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 16:38:57 2024


"""

# dashboard_generator.py

def create_dashboard():
    """
    Génère un tableau de bord interactif (dashboard) en HTML pour visualiser les graphiques générés.
    
    Le tableau de bord inclut des graphiques interactifs intégrés sous forme d'iframe, qui permettent de visualiser
    les données analysées. Chaque graphique correspond à une analyse spécifique des données extraites de la base HAL.
    
    Returns:
        str: Chemin d'accès au fichier HTML généré pour le tableau de bord.
    """



    #Contenu HTML du tableau de bord
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Dashboard de Publications</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            iframe { width: 100%; height: 500px; border: none; margin-bottom: 20px; }
            h1 { text-align: center; color: #333; }
        </style>
    </head>
    <body>
        <h1>Dashboard de Visualisation des Publications</h1>
        <iframe src="pubs_by_year.html"></iframe>
        <iframe src="type_distribution.html"></iframe>
        <iframe src="keywords_distribution.html"></iframe>
        <iframe src="domain_distribution.html"></iframe>
        <iframe src="top_authors.html"></iframe>
        <iframe src="structures_stacked.html"></iframe>
        <iframe src="publication_trends.html"></iframe>
    </body>
    </html>
    """
    dashboard_path = "html/dashboard.html"
    with open(dashboard_path, "w", encoding="utf-8") as file:
        file.write(html_content)
    return dashboard_path
