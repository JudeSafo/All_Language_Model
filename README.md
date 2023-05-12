[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/569/badge)](https://bestpractices.coreinfrastructure.org/projects/569)<br>

# Ecocrumb - ESG Reporting

The Ecocrumb (End-to-End) script is a utility script that automates the processing of PDF files to generate topics and parsed sections data. It utilizes other supporting scripts such as `pdf_to_text.sh`, `run_topic_modeling.sh`, and `parse_by_topic.sh`.

## Prerequisites

- Linux or macOS operating system
- Bash shell (version 4.x or later)
- `pdf_to_text.sh` script
- `run_topic_modeling.sh` script
- `parse_by_topic.sh` script
- Python 3.x (with required dependencies)
- jq (a lightweight command-line JSON processor)

## Usage

```bash
./ecocrumb.sh -i <target_directory_or_file> [-o output_directory] [-f] [-n number] [-b]
```

- `-i <target_directory_or_file>`: Specifies the target directory or file to process. For batch mode, provide the path to a directory containing PDF files. For individual mode, provide the path to a single PDF file.
- `-o output_directory`: (Optional) Specifies the output directory where the generated files will be saved. If not provided, the output will be stored in the same directory as the target.
- `-f`: (Optional) Forces the script to overwrite existing output files.
- `-n number`: (Optional) Specifies the number of topics for topic modeling. The default value is 15.
- `-b`: (Optional) Enables batch mode, allowing the script to process multiple files in the target directory.

## Examples

### Individual Mode

To process a single PDF file:

```bash
./ecocrumb.sh -i path/to/myfile.pdf
```

This will convert the PDF file to plaintext, generate topics and parsed sections, and save the output in the same directory as the input file.

### Batch Mode

To process all PDF files in a directory:
```bash
./ecocrumb.sh -i path/to/my_directory -o path/to/output_directory -f -b -n 20
```


This will convert all PDF files in the specified directory to plaintext, generate topics and parsed sections for each file, and save the output in the specified output directory. The `-f` flag forces overwriting of existing output files. The `-n` flag sets the number of topics to 20.

