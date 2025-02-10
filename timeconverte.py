import csv

def correct_time(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))

    if seconds >= 60:
        minutes += seconds // 60
        seconds = seconds % 60

    if minutes >= 60:
        hours += minutes // 60
        minutes = minutes % 60

    if hours >= 24:
        hours = hours % 24

    return f"{hours:02}:{minutes:02}:{seconds:02}"

input_file = 'ETL/data/stop_times_modified.txt'
output_file = 'database\corrected_times_output.txt'

with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Write the header
    header = next(reader)
    writer.writerow(header)

    for row in reader:
        row[1] = correct_time(row[1])
        writer.writerow(row)

print(f"Corrected times have been written to {output_file}")