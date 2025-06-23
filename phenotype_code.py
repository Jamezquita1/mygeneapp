import json
import requests
import pandas as pd

def process_evidence_entry(evidence_entry):
    evidence_type = evidence_entry['type']
    evidence_data = evidence_entry['data']

    entry_info_list = []
    if isinstance(evidence_data, list):
        for entry_info in evidence_data:
            label = entry_info.get('label')
            class_ = entry_info.get('class')
            evidence_remarks = process_remark_or_other_evidence(entry_info.get('evidence'))

            if label is None and class_ is None and not evidence_remarks:
                continue  # Skip entries with no relevant information

            entry_info_dict = {
                'Phenotype': entry_info.get('text', {}).get('label'),
                'Evidence Type': evidence_type,
                'Label': label,
                'Class': class_,
                'Remarks': evidence_remarks
            }
            entry_info_list.append(entry_info_dict)
    else:
        entry_info_dict = {
            'Phenotype': evidence_data.get('text', {}).get('label'),
            'Evidence Type': evidence_type,
            'Label': None,
            'Class': None,
            'Remarks': process_remark_or_other_evidence(evidence_data.get('evidence'))
        }
        entry_info_list.append(entry_info_dict)

    return entry_info_list

def process_remark_or_other_evidence(evidence_data):
    remarks = []

    if isinstance(evidence_data, (str, dict)):
        remarks.append(evidence_data)
    elif isinstance(evidence_data, list):
        for item in evidence_data:
            if isinstance(item, (str, dict)):
                remarks.append(item)

    return remarks

def report_phenotype_details(entry):
    phenotype_label = entry.get('phenotype', {}).get('label')
    evidence_entries = entry.get('evidence', {})

    phenotype_info_list = []
    for evidence_type, evidence_data in evidence_entries.items():
        if evidence_type != "Curator":
            evidence_entry = {
                'Phenotype': phenotype_label,
                'Evidence Type': evidence_type,
                'Evidence': process_evidence_entry({'type': evidence_type, 'data': evidence_data})
            }
            phenotype_info_list.append(evidence_entry)

    return phenotype_info_list


def process_phenotypes(gene_id):
    try:
        api_endpoint = f"http://rest.wormbase.org/rest/field/gene/{gene_id}/phenotype"

        # Send API request and get JSON response
        api_response = requests.get(api_endpoint)
        response_body = api_response.text

        # Parse the JSON response body
        api_data = json.loads(response_body)

        phenotype_data = []
        for phenotype_entry in api_data.get('phenotype', {}).get('data', []):
            phenotype_data.extend(report_phenotype_details(phenotype_entry))

        # Filter out entries with empty or None values
        filtered_phenotype_data = [entry for entry in phenotype_data if any(entry.values())]

        # Create a pandas DataFrame
        df = pd.DataFrame(filtered_phenotype_data)

        output_data = []

        for _, row in df.iterrows():
            phenotype = row['Phenotype']
            evidence_type = row['Evidence Type']
            evidence = row['Evidence']

            for entry in evidence:
                new_row = {
                    'Phenotype': phenotype,  # Change this to your desired header
                    'Evidence Type': evidence_type,  # Change this to your desired header
                    'Mutant/Alteration': entry['Phenotype'],  # Change this to your desired header
                    'Evidence_Info': entry.get('Remarks')  # Change this to your desired header
                }
                output_data.append(new_row)

        output_df = pd.DataFrame(output_data)

        # Save the DataFrame to an Excel file
        #output_file = 'phenotype_report.xlsx'
        #output_df.to_excel(output_file, index=False)

        #print(f"Phenotype data has been exported to {output_file}")

        return output_data

    except json.JSONDecodeError as e:
        print("Error parsing JSON response:", str(e))
    except Exception as e:
        print("An error occurred:", str(e))