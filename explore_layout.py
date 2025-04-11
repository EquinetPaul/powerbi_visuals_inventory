import os
import zipfile
import shutil
import json
import csv

repertoire_a_traiter = "." 
liste_fichiers_zip = []
repertoire_temporaire = "."

for nom_fichier in os.listdir(repertoire_a_traiter):
    if nom_fichier.endswith(".zip"):
        chemin_fichier = os.path.join(repertoire_a_traiter, nom_fichier)
        liste_fichiers_zip.append(chemin_fichier)

# print(f"Fichiers .zip trouvés: {liste_fichiers_zip}")

# os.makedirs(repertoire_temporaire, exist_ok=True)

# for chemin_zip in liste_fichiers_zip:
#     nom_fichier_zip = os.path.basename(chemin_zip)
#     nom_repertoire_dezippe = os.path.splitext(nom_fichier_zip)[0]
#     chemin_dezippe = os.path.join(repertoire_temporaire, nom_repertoire_dezippe)

#     try:
#         with zipfile.ZipFile(chemin_zip, 'r') as zip_ref:
#             zip_ref.extractall(chemin_dezippe)
#             chemin_layout = os.path.join(chemin_dezippe, "Report", "Layout")
#             # if os.path.exists(chemin_layout):
#             #     print(f"'{nom_fichier_zip}' contient 'Report/Layout'.")
#             # else:
#             #     print(f"'{nom_fichier_zip}' ne contient pas 'Report/Layout'.")
#     except zipfile.BadZipFile:
#         print(f"Erreur: '{nom_fichier_zip}' n'est pas un fichier ZIP valide.")
#     except Exception as e:
#         print(f"Une erreur s'est produite lors du traitement de '{nom_fichier_zip}': {e}")


def format_fields_or_datasource(list):
    string_result = ""
    for i, element in enumerate(list):
        string_result += str(i + 1) + ". " + str(element)
        if i != len(list) - 1:
            string_result += "\n"

    return string_result


dataToSave = []

for fichier in liste_fichiers_zip:
    folderName = fichier.replace(".zip", "").replace(".\\", "")
    chemin_fichier_layout = os.path.join(folderName, "Report", "Layout")

    # print(chemin_fichier_layout)

    with open(chemin_fichier_layout, "r", encoding="utf-16-le") as file:
        content = file.read()

    chemin_fichier_layout_utf8 = chemin_fichier_layout + "UTF8"

    with open(chemin_fichier_layout_utf8, "w", encoding="utf-8") as file:
        file.write(content)
        file.close()

    with open(chemin_fichier_layout_utf8, "r", encoding="utf-8") as file:
        raw_data = file.read()

    json_data = json.loads(raw_data)

    sections = json_data["sections"]
    # print(f"\t{len(sections)} pages found")

    reportName = folderName
    for section in sections:
        containers = section["visualContainers"]
        page_name = section["displayName"]
        # print(f"\t\t {page_name} - {len(containers)} visuals found")

        for container in containers:
            config = container["config"]
            config_json = json.loads(config)
            try:
                visualType = config_json["singleVisual"]["visualType"]
                projections = config_json["singleVisual"]["projections"]
                titleText = config_json

                Fields = list(projections.keys())
                Data_Source = [
                    item["queryRef"]
                    for key in projections.keys()
                    for item in projections[key]
                ]

                # print(visualType)
                formated_fields = format_fields_or_datasource(Fields)
                formated_data_source = format_fields_or_datasource(Data_Source)
                
                
                dataToSave.append({
                  "Report Name" : reportName,
                  "Page" : page_name,
                  "Visual Type" : visualType,
                  "Fields": formated_fields,
                  "Data Sources" : formated_data_source,
                  "rawConfig" : config
                })
                # dataToSave["Report Name"].append(reportName)
                # dataToSave["Page"].append(page_name)
                # dataToSave["Visual Type"].append(page_name)
                # dataToSave["Fields"].append(page_name)
                # dataToSave["Data Source"].append(page_name)
                # dataToSave["rawConfig"].append(page_name)

            except Exception as e:
                # print(e)
                pass


# with open("output.csv", "w", newline="") as csvfile:
#     fieldnames = [
#         "Report Name",
#         "Page",
#         "Visual Type",
#         "Fields",
#         "Data Source",
#         "rawConfig",
#     ]
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")




with open("output.csv", "w", newline="") as csvfile:
    fieldnames = [
        "Report Name",
        "Page",
        "Visual Type",
        "Fields",
        "Data Sources",
        "rawConfig",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

    writer.writeheader()
    
    for element in dataToSave:
      writer.writerow(
          {
              "Report Name": element["Report Name"],
              "Page": element["Page"],
              "Visual Type": element["Visual Type"],
              "Fields": element["Fields"],
              "Data Sources": element["Data Sources"],
              "rawConfig": element["rawConfig"],
          }
      )

#     for section in sections[:1]:
#         containers = section["visualContainers"]
#         page_name = section["displayName"]

#         for container in containers:
#             config = container["config"]
#             config_json = json.loads(config)
#             try:
#                 visualType = config_json["singleVisual"]["visualType"]
#                 projections = config_json["singleVisual"]["projections"]
#                 Fields = list(projections.keys())
#                 Data_Source = [
#                     item["queryRef"]
#                     for key in projections.keys()
#                     for item in projections[key]
#                 ]
#                 formated_fields = format_fields_or_datasource(Fields)
#                 formated_data_source = format_fields_or_datasource(Data_Source)
#                 writer.writerow(
#                     {
#                         "Report Name": reportName,
#                         "Page": page_name,
#                         "Visual Type": visualType,
#                         "Fields": formated_fields,
#                         "Data Source": formated_data_source,
#                         "rawConfig": config,
#                     }
#                 )

#             except Exception as e:
#                 pass

print("Fichier CSV créé avec succès.")
