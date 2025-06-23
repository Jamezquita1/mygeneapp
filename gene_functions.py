# gene_tools/gene_functions.py
import requests
import json
import pandas as pd

base_url = "https://wormbase.org/"
api_base_url = "http://rest.wormbase.org"

def get_gene_id(gene_name):
    search_url = f"{base_url}search/gene/{gene_name}"
    response = requests.get(search_url)
    print(f"{gene_name} Gene URL Requested:", response.url)  # Debug output

    if response.status_code == 200:
        # Extract gene identifier from the URL
        gene_id = response.url.rsplit("/", 1)[-1]
        return gene_id
    else:
        print("Gene not found.")
        return None

def is_wormbase_gene_id(s):
    return s.startswith("WBGene")

def get_gene_name_from_id(gene_id):
    api_base_url = "http://rest.wormbase.org"
    url = f"{api_base_url}/rest/widget/gene/{gene_id}/overview"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        label = data.get("fields", {}).get("name", {}).get("data", {}).get("label")
        return label
    except Exception as e:
        print(f"Failed to get gene name: {e}")
        return None

def get_protein_id(gene_id):
    api_endpoint = f"{api_base_url}/rest/widget/gene/{gene_id}/sequences"
    api_response = requests.get(api_endpoint)
    response_body = api_response.text

    # Parse the JSON response body
    api_data = json.loads(response_body)

    protein_iso_data = []

    if "fields" in api_data and "gene_models" in api_data["fields"]:
        isoforms = api_data["fields"]["gene_models"]["data"]["table"]

        sorted_isoforms = sorted(isoforms, key=lambda x: x["protein"]["label"])

        for i, isoform in enumerate(sorted_isoforms, start=1):
            gene_id = isoform["gene"]["id"]
            gene_label = isoform["gene"]["label"]
            protein_id = isoform["protein"]["id"]
            protein_label = isoform["protein"]["label"]
            protein_length = isoform["length_protein"]

            protein_iso_info = {
                "gene_id": gene_id,
                "gene_label": gene_label,
                "protein_id": protein_id,
                "protein_label": protein_label,
                "protein_length": protein_length
            }
            protein_iso_data.append(protein_iso_info)

    return protein_iso_data


def get_gene_description(gene_id):
    api_endpoint = f"{api_base_url}/rest/widget/gene/{gene_id}/overview"
    api_response = requests.get(api_endpoint)
    response_body = api_response.text

    # Parse the JSON response body
    api_data = json.loads(response_body)

    # Extract concise description from API response
    if "concise_description" in api_data["fields"]:
        gene_description = api_data["fields"]["concise_description"]["data"]["text"]
        return gene_description
    else:
        return "Gene description not found."

def get_gene_position(gene_id):
    api_endpoint = f"{api_base_url}/rest/field/gene/{gene_id}/genetic_position"
    api_response = requests.get(api_endpoint)
    response_body = api_response.text

    # Parse the JSON response body
    api_data = json.loads(response_body)

    if "genetic_position" in api_data:
        genetic_position = api_data["genetic_position"]["data"][0]
        chromosome = genetic_position["chromosome"]
        position = genetic_position["position"]
        formatted_position = genetic_position["formatted"]
        return f"Chromosome: {chromosome}, Position: {position}, Formatted: {formatted_position}"
    else:
        return "Gene position not found."

def get_gene_othernames(gene_id):
    api_endpoint = f"{api_base_url}/rest/widget/gene/{gene_id}/overview"
    api_response = requests.get(api_endpoint)
    response_body = api_response.text

    # Parse the JSON response body
    api_data = json.loads(response_body)

    if "fields" in api_data and "other_names" in api_data["fields"]:
        other_names = api_data["fields"]["other_names"]["data"]
        return f"{', '.join(other_names)}"
    else:
        return "No other gene names found."


def get_blastp(protein_ids):
    all_sapiens_hits = []

    for protein_id in protein_ids:
        api_endpoint = f"{api_base_url}/rest/field/protein/{protein_id}/blastp_details"
        api_response = requests.get(api_endpoint)
        print(api_endpoint)

        if api_response.status_code == 200:
            # Parse the JSON response body
            api_data = api_response.json()

            # Extract hits from the blastp details
            hits_data = api_data.get("blastp_details", {}).get("data", [])

            if hits_data:
                sapiens_hits = []
                for hit in hits_data:
                    hit_info = hit.get("hit", {})
                    taxonomy_info = hit.get("taxonomy", {})

                    if isinstance(hit_info, dict) and \
                            isinstance(taxonomy_info, dict) and \
                            taxonomy_info.get("genus") == "H" and \
                            taxonomy_info.get("species") == "sapiens":
                        sapiens_hit = {
                            "description": hit_info.get("description"),
                            "id": hit_info.get("id"),
                            "percentage": hit.get("percentage"),
                            "evalue": hit.get("evalue"),
                            "source_range": hit.get("source_range"),
                            "target_range": hit.get("target_range")
                        }
                        sapiens_hits.append(sapiens_hit)

                all_sapiens_hits.extend(sapiens_hits)

    return all_sapiens_hits