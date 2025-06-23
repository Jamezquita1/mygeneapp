import requests
from bs4 import BeautifulSoup

def get_strains_for_gene(gene_name):
    base_url = 'https://cgc.umn.edu/strain/search'
    query_params = {
        'st1': gene_name,
        'sf1': 'all',
        'xt1': '',
        'xf1': 'all',
        'st2': '',
        'sf2': 'strain',
        'xt2': '',
        'xf2': 'strain',
        'st3': '',
        'sf3': 'genotype',
        'xt3': '',
        'xf3': 'genotype',
        'st4': '',
        'sf4': 'species',
        'xt4': '',
        'xf4': 'species'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    try:
        response = requests.get(base_url, params=query_params, headers=headers, verify=False)
        response.raise_for_status()
        print(f"Requested URL: {response.url}")  # Debug output
    except Exception as e:
        print(f"Failed to retrieve strain data for {gene_name}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='table table-striped')
    if not table:
        print(f"No table found for gene: {gene_name}")
        return []

    rows = table.find_all('tr')
    strain_data = []

    for row in rows:
        cells = row.find_all('td')
        if cells:
            strain_name = cells[0].text.strip()
            species = cells[1].text.strip()
            genotype = cells[2].text.strip()
            additional_info = cells[2].find('div', style=True)
            additional_info_text = additional_info.text.strip() if additional_info else None

            strain_data.append({
                'gene_name': gene_name,
                'strain_name': strain_name,
                'species': species,
                'genotype': genotype,
                'additional_info': additional_info_text
            })

    return strain_data
