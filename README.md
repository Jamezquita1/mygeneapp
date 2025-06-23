> ⚠️ **Note:** This is the original, independently developed version of this project.
>
> A fork of this project is now maintained by the Grill Lab for their own use and development needs.

# mygeneapp

A Python tool for querying and organizing gene-related data from WormBase. This app retrieves gene descriptions, protein homology (BLASTp), phenotypes, and strain information, then compiles the results into a structured Excel workbook.

## Features

- Query multiple genes from WormBase
- Retrieve gene descriptions, BLASTp results, phenotypes, and strain data
- Organize all results in a well-formatted Excel file with multiple tabs

## Installation

1. Clone the repository:
git clone https://github.com/Jamezquita1/mygeneapp.git
cd mygeneapp

markdown
Copy
Edit

2. Install dependencies:
pip install -r requirements.txt

shell
Copy
Edit

## Usage

Run the app:
python main.py

markdown
Copy
Edit
(Or use the correct entry point script name.)

## Output

Generates an Excel file with:
- Gene Descriptions
- Protein Homology
- Phenotypes
- Strain Info
- Failed Queries (if any)

## Dependencies

- `requests`
- `openpyxl`
- `beautifulsoup4`
- `pandas`

## License

This project is licensed under the [MIT License](LICENSE).

## Author

**Jonathan Amezquita**  
GitHub: [@Jamezquita1](https://github.com/Jamezquita1)

## Acknowledgments

Developed during PhD research at University of Washington/Seattle Children's Research Institute in the Grill Lab.
