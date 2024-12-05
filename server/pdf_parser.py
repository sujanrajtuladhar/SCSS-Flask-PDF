import logging
import pandas as pd
import tabula

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_pdf(file_path, csv_path, error_path):
    """
    Parses a PDF file to extract tables and save them as a CSV file.

    This function uses the tabula library to read all tables from the specified
    PDF file. It combines the tables into a single DataFrame, standardizing the
    columns to match the structure of the first table. The combined DataFrame
    is then saved to the specified CSV file path. If no tables are found in the
    PDF, an error message is written to the specified error file path.

    Args:
        file_path (str): The path to the PDF file to be parsed.
        csv_path (str): The path where the resulting CSV file will be saved.
        error_path (str): The path where an error message will be written if no tables are found.

    Returns:
        None
    """
    logger.info(f"Starting PDF parsing for {file_path}")
            
    # Extract tables from PDF using tabula
    # Read all tables from the PDF
    tables = tabula.read_pdf(file_path, pages='all', multiple_tables=True, lattice=True)

    # Check if no tables or all tables are empty
    if not tables or all(table.empty for table in tables):
        logger.warning("No tables found in the PDF.")
        with open(error_path, 'w') as error_file:
            error_file.write("No tables found in the PDF.")
        return
        
    if tables:
        logger.info('table exists')
        logger.info(f"Found {len(tables)} table(s) in the PDF.")
        combined_df = pd.DataFrame()  # Initialize an empty DataFrame for combining tables

        for i, table in enumerate(tables):
            if table.empty:
                continue  # Skip empty tables

            # Standardize the columns to match the first table's structure
            if combined_df.empty:
                combined_df = table  # Use the first table's structure as a reference
            else:
                table.columns = combined_df.columns[:len(table.columns)]
                combined_df = pd.concat([combined_df, table], ignore_index=True)

        # Save the combined DataFrame to a single CSV file
        combined_df.to_csv(csv_path, index=False)
        
        logger.info(f"PDF parsing completed. Output saved to {csv_path}")
    else:
        logger.info('table doesnt exists')
        logger.warning(f"No tables found in the PDF {file_path}")
        with open(error_path, 'w') as f:
            f.write(f"No tables found in the PDF {file_path}\n")
