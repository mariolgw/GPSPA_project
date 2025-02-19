
def process_data(input_file):
    """
    Processes the stop times data by removing specified columns and modifying the trip_id.

    Args:
        input_file (str): The path to the input stop times data file.

    Returns:
        str: The path to the output file with the processed data.
    """

    import pandas as pd
    import os
    
    #Load the necessary data files
    routes = pd.read_csv('data/routes.txt')
    stop_times = pd.read_csv('data/stop_times.txt')
    stops = pd.read_csv('data/stops.txt')

    input_file = 'data/stop_times.txt'
    output_file = 'ETL/data/stop_times_modified.txt'

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Columns to remove
    columns_to_remove = ['departure_time', 'pickup_type', 'drop_off_type', 'stop_sequence', 'shape_dist_traveled']

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Read the header line
        header = infile.readline().strip().split(',')
    
        # Determine the indices of the columns to remove
        indices_to_remove = [header.index(col) for col in columns_to_remove]
    
        # Write the modified header to the output file
        modified_header = [col for i, col in enumerate(header) if i not in indices_to_remove]
        outfile.write(','.join(modified_header) + '\n')
    
        # Process each line in the input file
        for line in infile:
            fields = line.strip().split(',')

            # Modify the trip_id to keep only the string between the underscores
            trip_id = fields[0].split('_')[1] if len(fields[0].split('_')) > 1 else fields[0]
            fields[0] = trip_id

            if fields[0] == 'WKDY':
                fields[0] = '1'
            elif fields[0] == 'SASUHO':
                fields[0] = '0'

            modified_fields = [field for i, field in enumerate(fields) if i not in indices_to_remove]
            outfile.write(','.join(modified_fields) + '\n')

    return output_file

# Call the process_data function with the path to the input file
 # Adjust the path as needed