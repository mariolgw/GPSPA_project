import csv

#Essential file that converts incorrect times that pass the 24 hour mark to the correct time, for example 25:00:00 will be converted to 01:00:00 

def correct_time(time_str):
    """
    Corrects a time string that may have hours >= 24, minutes >= 60, or seconds >= 60.

    Args:
        time_str (str): The time string in the format "HH:MM:SS".

    Returns:
        str: The corrected time string in the format "HH:MM:SS".
    """
    # Split the time string into hours, minutes, and seconds
    hours, minutes, seconds = map(int, time_str.split(':'))
    # Correct the seconds if they are >= 60
    if seconds >= 60:
        minutes += seconds // 60
        seconds = seconds % 60
    # Correct the minutes if they are >= 60
    if minutes >= 60:
        hours += minutes // 60
        minutes = minutes % 60
    # Correct the hours if they are >= 24
    if hours >= 24:
        hours = hours % 24
    # Return the corrected time string in the format "HH:MM:SS"
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def process_times(input_file, output_file):
    with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the header
        header = next(reader)
        writer.writerow(header)

<<<<<<< HEAD
        for row in reader:
            row[1] = correct_time(row[1])
            writer.writerow(row)

    print(f"Corrected times have been written to {output_file}")
=======
    # Write the header
    header = next(reader)
    writer.writerow(header)
    # Process each row in the input file
    for row in reader:
        row[1] = correct_time(row[1])
        writer.writerow(row)
>>>>>>> a1a89848e273f632beeef20e211c2ecb6a2ef2ee

if __name__ == "__main__":
    input_file = 'ETL/data/stop_times_modified.txt'
    output_file = 'ETL/data/stop_times_output.txt'
    process_times(input_file, output_file)