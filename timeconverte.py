import re

def fix_invalid_times(times_list):
    """
    Correct times that surpass the 24-hour format by converting them to valid times.

    :param times_list: List of time strings in 'HH:MM:SS' format.
    :return: List of corrected time strings.
    """
    corrected_times = []

    for time_str in times_list:
        match = re.match(r"(\d{2}):(\d{2}):(\d{2})", time_str)
        if match:
            hours, minutes, seconds = map(int, match.groups())

            # Adjust if hours exceed 23
            if hours >= 24:
                hours = hours % 24

            # Format back to a time string with leading zeros
            corrected_time = f"{hours:02}:{minutes:02}:{seconds:02}"
            corrected_times.append(corrected_time)
        else:
            # If the time format is incorrect, keep it unchanged
            corrected_times.append(time_str)

    return corrected_times

# Example usage: Reading from the provided file
input_file_path = 'data\grouped_result_fixed.txt'
output_file_path = 'database\corrected_times_output.txt'

corrected_lines = []

with open(input_file_path, 'r') as file:
    for line in file:
        times = re.findall(r"\d{2}:\d{2}:\d{2}", line)
        corrected_times = fix_invalid_times(times)

        # Replace old times with corrected times in the line
        corrected_line = line
        for old_time, new_time in zip(times, corrected_times):
            corrected_line = corrected_line.replace(old_time, new_time, 1)

        corrected_lines.append(corrected_line)

# Write the corrected times to a new file
with open(output_file_path, 'w') as output_file:
    output_file.writelines(corrected_lines)

print("Time correction completed. Check corrected_times_output.txt.")