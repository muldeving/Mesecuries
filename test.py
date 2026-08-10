import csv

def convertir_avec_compte_rendu(fichier_entree='in.csv', fichier_sortie='out.csv'):
    """
    Convertit un fichier CSV (cp1252) de factures/avoirs en écritures comptables
    et affiche un compte rendu détaillé du traitement.
    """
    en_tete_sortie = [
        'Journal', 'Date', 'Compte', 'Nom', 'Code', 'Dénomination',
        'Débit', 'Crédit', 'Lettrage', 'Code TVA'
    ]
    lignes_sortie = [en_tete_sortie]

    # --- NOUVEAU : Initialisation pour le compte rendu ---
    nombre_factures = 0
    total_ht_factures, total_tva_factures, total_ttc_factures = 0.0, 0.0, 0.0
    nombre_avoirs = 0
    total_ht_avoirs, total_tva_avoirs, total_ttc_avoirs = 0.0, 0.0, 0.0

    try:
        with open(fichier_entree, mode='r', newline='', encoding='cp1252') as f_entree:
            lecteur_csv = csv.DictReader(f_entree, delimiter=';')

            for ligne in lecteur_csv:
                ligne = {cle.strip(): valeur.strip() for cle, valeur in ligne.items()}
                type_document = ligne['Type']

                # Récupération des données
                date, numero_facture, objet = ligne['Date'], ligne['Numéro'], ligne['Objet']
                total_ht_str = ligne['Total  HT']
                total_tva_str = ligne['Total  TVA']
                total_ttc_str = ligne['Total  TTC'] # Récupération du TTC

                try:
                    total_ht = float(total_ht_str.replace(',', '.'))
                    total_tva = float(total_tva_str.replace(',', '.'))
                    total_ttc = float(total_ttc_str.replace(',', '.'))
                except ValueError:
                    print(f"Avertissement : Ligne ignorée en raison d'une erreur de format de nombre : {ligne}")
                    continue

                # --- NOUVEAU : Mise à jour des cumuls pour le rapport ---
                if type_document == 'Facture':
                    nombre_factures += 1
                    total_ht_factures += total_ht
                    total_tva_factures += total_tva
                    total_ttc_factures += total_ttc
                elif type_document == 'Avoir':
                    nombre_avoirs += 1
                    total_ht_avoirs += total_ht
                    total_tva_avoirs += total_tva
                    total_ttc_avoirs += total_ttc
                
                # ... (Logique de conversion existante) ...
                code_tva, compte_tva = '', ''
                if total_ht > 0:
                    taux_tva = (total_tva / total_ht) * 100
                    if 5.0 < taux_tva < 6.0: code_tva, compte_tva = 'v', '445715'
                    elif 9.5 < taux_tva < 10.5: code_tva, compte_tva = 'p', '445712'

                debit_ht, credit_ht, debit_tva, credit_tva = '', '', '', ''
                if type_document == 'Avoir':
                    debit_ht, debit_tva = total_ht_str, total_tva_str
                else:
                    credit_ht, credit_tva = total_ht_str, total_tva_str

                lignes_sortie.append(['2', date, '7061', 'test', numero_facture, objet, debit_ht, credit_ht, '', code_tva])
                lignes_sortie.append(['2', date, compte_tva, 'test', numero_facture, objet, debit_tva, credit_tva, '', code_tva])

        # Écriture du fichier de sortie
        with open(fichier_sortie, mode='w', newline='', encoding='cp1252') as f_sortie:
            ecrivain_csv = csv.writer(f_sortie, delimiter=';')
            ecrivain_csv.writerows(lignes_sortie)

        print(f"✅ La conversion est terminée. Le fichier '{fichier_sortie}' a été généré.")

        # --- NOUVEAU : Affichage du compte rendu final ---
        net_ht = total_ht_factures - total_ht_avoirs
        net_tva = total_tva_factures - total_tva_avoirs
        net_ttc = total_ttc_factures - total_ttc_avoirs
        
        print("\n" + "="*45)
        print("      📝 COMPTE RENDU DU TRAITEMENT")
        print("="*45)
        print(f"Factures traitées : {nombre_factures}")
        # Le formatage :>12.2f aligne les nombres et les affiche avec 2 décimales
        print(f"  - Cumul HT   : {total_ht_factures:>12.2f} €")
        print(f"  - Cumul TVA  : {total_tva_factures:>12.2f} €")
        print(f"  - Cumul TTC  : {total_ttc_factures:>12.2f} €")

        if nombre_avoirs > 0:
            print("-"*45)
            print(f"Avoirs traités    : {nombre_avoirs}")
            print(f"  - Cumul HT   : {total_ht_avoirs:>12.2f} €")
            print(f"  - Cumul TVA  : {total_tva_avoirs:>12.2f} €")
            print(f"  - Cumul TTC  : {total_ttc_avoirs:>12.2f} €")
        
        print("="*45)
        print("SOLDE NET (Factures - Avoirs)")
        print(f"  - Solde HT     : {net_ht:>12.2f} €")
        print(f"  - Solde TVA    : {net_tva:>12.2f} €")
        print(f"  - Solde TTC    : {net_ttc:>12.2f} €")
        print("="*45)

    except FileNotFoundError:
        print(f"Erreur : Le fichier d'entrée '{fichier_entree}' n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")

# --- Lancement du script ---
if __name__ == "__main__":
    convertir_avec_compte_rendu(fichier_entree='in.csv', fichier_sortie='out.csv')
