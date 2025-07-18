import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def extract_data_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    data = []
    
    # Trouver toutes les rangées principales
    main_rows = soup.select('table.tw-min-w-full tbody tr:not(.tw-border-none)')
    
    for main_row in main_rows:
        # Extraire les données de la rangée principale
        school = main_row.select_one('td:nth-child(1) .tw-font-medium')
        school = school.get_text(strip=True) if school else 'N/A'

        program = main_row.select_one('td:nth-child(2) .tw-text-gray-900 span:first-child')
        program = program.get_text(strip=True) if program else 'N/A'

        added_on = main_row.select_one('td:nth-child(3)')
        added_on = added_on.get_text(strip=True) if added_on else 'N/A'

        decision = main_row.select_one('td:nth-child(4) .tw-text-sm')
        decision = decision.get_text(strip=True) if decision else 'N/A'

        # Trouver la rangée de détails suivante
        details_row = main_row.find_next_sibling('tr', class_='tw-border-none')
        details_text = details_row.get_text(strip=True) if details_row else ''

        # Extraire les valeurs de GPA et GRE (sans inclure la colonne details)
        gpa_gre_details = extract_gpa_gre(details_text)
        
        # Structurer les données sans la colonne details
        entry = {
            'school': school,
            'program': program,
            'added_on': added_on,
            'decision': decision,
            **gpa_gre_details
        }

        data.append(entry)

    return data

def extract_gpa_gre(details):
    patterns = {
        'GPA': r'GPA (\d+\.\d+)',
        'GRE': r'GRE (\d+)',
        'GRE_V': r'GRE V (\d+)',
        'GRE_Q': r'GRE Q (\d+)',
        'GRE_AW': r'GRE AW (\d+\.\d+)',
        'TOEFL': r'TOEFL (\d+)',
        'IELTS': r'IELTS (\d+\.\d+)'
    }
    
    extracted = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, details)
        extracted[key] = match.group(1) if match else None
    
    return extracted

def main():
    base_url = 'https://www.thegradcafe.com/survey/?q=&sort=newest&institution=&program=&degree=&season=&decision=&decision_start=&decision_end=&added_start=&added_end=&page='
    pages = 6000
    all_data = []

    for i in range(1, pages + 1):
        url = f'{base_url}{i}'
        print(f"Extracting data from page {i}...")
        page_data = extract_data_from_page(url)
        all_data.extend(page_data)

        if len(all_data) >= 1000000:
            break

    # Créer le DataFrame
    df = pd.DataFrame(all_data)

    # Sauvegarder sans la colonne details (elle n'est déjà plus incluse)
    df.to_csv('grad_cafe_data.csv', index=False)
    print("Data extraction complete. Data saved to grad_cafe_data.csv")

if __name__ == '__main__':
    main()