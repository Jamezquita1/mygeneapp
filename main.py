from gene_functions import get_gene_id, get_protein_id, get_gene_description, get_gene_position, get_gene_othernames, get_blastp, is_wormbase_gene_id, get_gene_name_from_id
from excel_utils import create_excel_file, write_gene_data_to_excel, write_protein_data_to_excel, \
    write_phenotype_data_to_excel, write_strain_data_to_excel, write_failed_queries_to_excel
from cgc_match import get_strains_for_gene


if __name__ == "__main__":
    gene_inputs = input("Enter C. elegans gene names or IDs separated by commas: ").split(',')
    gene_data = []
    protein_data = []
    strain_data = []
    failed_queries = []

    for gene_input in gene_inputs:
        gene_input = gene_input.strip()

        try:
            if is_wormbase_gene_id(gene_input):
                gene_id = gene_input
                gene_name = get_gene_name_from_id(gene_id)
            else:
                gene_name = gene_input
                gene_id = get_gene_id(gene_name)

            if gene_id is None or gene_name is None:
                raise ValueError("Gene ID or name could not be resolved")

            gene_description = get_gene_description(gene_id)
            gene_position = get_gene_position(gene_id)
            gene_othernames = get_gene_othernames(gene_id)
            protein_info_list = get_protein_id(gene_id)

            gene_info = {
                'gene_id': gene_id,
                'gene_name': gene_name,
                'gene_description': gene_description,
                'gene_position': gene_position,
                'gene_othernames': gene_othernames,
                'protein_info': protein_info_list
            }
            gene_data.append(gene_info)

            for protein_info in protein_info_list:
                protein_id = protein_info["protein_id"]
                blastp_results = get_blastp([protein_id])
                if blastp_results:
                    protein_info["blastp_results"] = blastp_results
                    protein_data.append(protein_info)

            strains = get_strains_for_gene(gene_name)
            if strains:
                strain_data.extend(strains)

        except Exception as e:
            print(f"❌ Failed to process '{gene_input}': {e}")
            failed_queries.append((gene_input, str(e)))  

    # ✅ Save all data to Excel
    excel_filename = "gene_protein_data.xlsx"
    create_excel_file(excel_filename)
    write_gene_data_to_excel(excel_filename, gene_data)
    write_protein_data_to_excel(excel_filename, protein_data)
    write_phenotype_data_to_excel(excel_filename, gene_data)
    write_strain_data_to_excel(excel_filename, strain_data)

    # ✅ Write failed queries if any
    if failed_queries:
        write_failed_queries_to_excel(excel_filename, failed_queries)
        print(f"\n⚠️ {len(failed_queries)} query failures were logged to the Excel file.")