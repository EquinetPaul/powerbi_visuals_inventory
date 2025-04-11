import os

def changer_extension(repertoire):
  """
  Change l'extension de tous les fichiers .pbix en .zip dans le répertoire spécifié.

  Args:
    repertoire (str): Le chemin du répertoire à traiter.
  """
  for nom_fichier in os.listdir(repertoire):
    if nom_fichier.endswith(".pbix"):
      ancien_chemin = os.path.join(repertoire, nom_fichier)
      nouveau_nom_fichier = nom_fichier[:-5] + ".zip" 
      print(nouveau_nom_fichier)
      nouveau_chemin = os.path.join(repertoire, nouveau_nom_fichier)
      try:
        os.rename(ancien_chemin, nouveau_chemin)
        print(f"Renommé: {nom_fichier} en {nouveau_nom_fichier}")
      except OSError as e:
        print(f"Erreur lors du renommage de {nom_fichier}: {e}")

if __name__ == "__main__":
  repertoire_a_modifier = "."  
  changer_extension(repertoire_a_modifier)
  print("Opération de changement d'extension terminée.")