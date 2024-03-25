import subprocess
import os
import requests
import gzip
import shutil


def download(url, file_name):
    # Send a GET request to the URL
    response = requests.get(url)
    save_path = "/users/saedunu/" + file_name


    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Open a file and write the response content (file contents) to it
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print("File ", file_name, " downloaded successfully.")
    else:
        print("Failed to download the ",file_name)
    return file_name


def gunzip_file(gzipped_file, output_file):
    with gzip.open(gzipped_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return output_file




def crop_sequences(input_filename, output_filename):
    # Read the sequences from the input file and calculate their lengths
    sequences = []
    with open(input_filename, 'r') as f:
        for line in f:
            if line.startswith('>'):
                continue  # Skip header lines
            sequences.append(line.strip())

    # Determine the optimal length (median length)
    optimal_length = int(sorted(map(len, sequences))[len(sequences) // 2])

    # Crop sequences to the optimal length
    cropped_sequences = [seq[(len(seq) - optimal_length) // 2:(len(seq) + optimal_length) // 2] for seq in sequences if len(seq) >= optimal_length]

    # Write the cropped sequences to the output file
    with open(output_filename, 'w') as f:
        for seq in cropped_sequences:
            f.write(seq + '\n')
    return optimal_length, output_filename


def read_accessible_bed_file(accessible_bed_filename):
    intervals = []
    with open(accessible_bed_filename, 'r') as access_bed:
        for line in access_bed:
            if not line.startswith('#'):  # Skip comment lines if any
                parts = line.strip().split('\t')
                chromosome = parts[0]
                start_index = int(parts[1])
                end_index = int(parts[2])
                intervals.append((chromosome, start_index, end_index))
    return intervals

def get_unaccessible_portion(accessible_portions):
    unaccess_intervals = []
    last_index = 1
    chrome = None
    for chromosome, start_index, end_index in accessible_portions:
        if chrome is None:
            chrome = chromosome
            last_index = end_index + 1
            break
    print("chromo", chrome)
    print("Last index", last_index)
    for i, (chromosome, start_index, end_index) in enumerate(accessible_portions):
        if i == len(accessible_portions) - 1:
            continue #skipping the last iteration
        if chrome is None:
            chrome = chromosome
            last_index = 1
            #print(chrome, '\n')
            #print(last_index, '\n')
            #print("=====")
            continue
        elif last_index-1 != start_index and last_index != start_index and chrome == chromosome and last_index-1 < start_index:
            #print(last_index, 'elif before inc \n')
            unaccess_intervals.append((chromosome, last_index, start_index-1))
            last_index = end_index + 1
            #print(last_index, 'elif after inc \n')
            chrome = chromosome
            #print(chrome, 'elif \n')
            #print("=====")
            #break
        else:
            #unaccess_intervals.append((chromosome, last_index, start_index-1))
            #print(last_index, 'else before inc \n')
            last_index = end_index + 1
            #print(last_index, 'else after inc \n')
            chrome = chromosome
            #print(chrome, 'else \n')
    return unaccess_intervals


def create_unaccessible_bed_file(output_filename, intervals):
    with open(output_filename, 'w') as output_file:
        for chromosome, start_index, end_index in intervals:
            output_file.write(f"{chromosome}\t{start_index}\t{end_index}\n")
    return output_filename

#import subprocess

def bed_to_txt(bed_file):
    reference_fasta = "/users/saedunu/reference/hg38.fa"
    bed_filename = "/users/saedunu/" + bed_file
    output_txt = input("Enter the file name to extract txt file from bed file-{}: ".format(bed_file))
    output_filename = "/users/saedunu/" + output_txt
    bash_command = "bedtools getfasta -fi {} -bed {} -fo {}".format(reference_fasta, bed_filename, output_filename)

    # Execute the bash command
    process = subprocess.Popen(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if process.returncode != 0:
        print("Error:", error.decode())
    else:
        print(output_txt, "was successfully extracted from", bed_file)
    return output_txt


def crop_unaccess_sequences(input_filename, output_filename, optimal):
    sequences = []
    with open(input_filename, 'r') as f:
        for line in f:
            if line.startswith('>'):
                continue
            sequences.append(line.strip())
    
    optimal_length = optimal
    print("optimal unaccess length:", optimal_length)
    
    cropped_sequences = [seq[(len(seq) - optimal_length) // 2:(len(seq) + optimal_length) // 2] for seq in sequences if len(seq) >= optimal_length]

    with open(output_filename, 'w') as f:
        for seq in cropped_sequences:
            f.write(seq + '\n')
    
    return optimal_length, output_filename


link_list = []
access_bed_list = []
link_list.append("https://www.encodeproject.org/files/ENCFF168GAN/@@download/ENCFF168GAN.bed.gz")
link_list.append("https://www.encodeproject.org/files/ENCFF852UQF/@@download/ENCFF852UQF.bed.gz")
link_list.append("https://www.encodeproject.org/files/ENCFF762IIH/@@download/ENCFF762IIH.bed.gz")
link_list.append("https://www.encodeproject.org/files/ENCFF886LQP/@@download/ENCFF886LQP.bed.gz")
link_list.append("https://www.encodeproject.org/files/ENCFF931FYG/@@download/ENCFF931FYG.bed.gz")
link_list.append("https://www.encodeproject.org/files/ENCFF362RCY/@@download/ENCFF362RCY.bed.gz")
link_list.append("https://www.encodeproject.org/files/ENCFF522GCK/@@download/ENCFF522GCK.bed.gz")
link_list.append("https://www.encodeproject.org/files/ENCFF109WDL/@@download/ENCFF109WDL.bed.gz")
link_list.append("https://www.encodeproject.org/files/ENCFF050GDF/@@download/ENCFF050GDF.bed.gz")
link_list.append("https://www.encodeproject.org/files/ENCFF604ZXG/@@download/ENCFF604ZXG.bed.gz")

for i in range(len(link_list)):
    gz_filename = os.path.basename(link_list[i])
    download(link_list[i], gz_filename)

    unzipped_bed_file = os.path.splitext(gz_filename)[0]
    access_bed_list.append(gunzip_file(gz_filename, unzipped_bed_file))
print(access_bed_list)

bedtool_txt_access_list = []

for i in range(len(access_bed_list)):
    bedtool_txt_access_list.append(bed_to_txt(access_bed_list[i]))
print(bedtool_txt_access_list)

trim_access_seq_list = []
optimal_length_list = []
for i in range(len(bedtool_txt_access_list)):
    access_output_filename = input("Enter filename to store trimmed accessible file- {}: ".format(i+1))
    final_optimal_length, cropped_accessible_file = crop_sequences(bedtool_txt_access_list[i], access_output_filename)
    trim_access_seq_list.append(cropped_accessible_file)
    optimal_length_list.append(final_optimal_length)
    print("Final_optimal_length: ", final_optimal_length)
print(trim_access_seq_list)
print(optimal_length_list)

OPTIMAL_LENGTH = min(optimal_length_list)
print("Final optimal length: ",OPTIMAL_LENGTH)

unaccess_bed_list = []
for i in range(len(access_bed_list)):
    unaccess_bed_filename = input("Enter unaccess bed file name for file {}: ".format(access_bed_list[i]))
    accessible_intervals = read_accessible_bed_file(access_bed_list[i])
    unaccessible_intervals = get_unaccessible_portion(accessible_intervals)
    unaccess_bed_list.append(create_unaccessible_bed_file(unaccess_bed_filename, unaccessible_intervals))

print(unaccess_bed_list)

bedtool_txt_unaccess_list = []

for i in range(len(unaccess_bed_list)):
    bedtool_txt_unaccess_list.append(bed_to_txt(unaccess_bed_list[i]))
print(bedtool_txt_unaccess_list)

trim_unaccess_seq_list = []
unaccess_optimal_length_list = []
for i in range(len(bedtool_txt_unaccess_list)):
	unaccess_output_filename = input("Enter filename to store trimmed unaccessible file- {}: ".format(i+1))
	final_optimal_length, cropped_unaccessible_file = crop_unaccess_sequences(bedtool_txt_unaccess_list[i], unaccess_output_filename, OPTIMAL_LENGTH)
	trim_unaccess_seq_list.append(cropped_unaccessible_file)
	unaccess_optimal_length_list.append(final_optimal_length)

print(trim_unaccess_seq_list)
print(unaccess_optimal_length_list)



'''
# Example usage:
unaccess_input_filename = 'ENCFF168GAN.txt'
unaccess_output_filename = 'cropped_accessible_sequences.txt'
final_optimal_length, cropped_accessible_file = crop_sequences(unaccess_input_filename, unaccess_output_filename)
print('filal_optimal_length: ', final_optimal_length)

existing_bed_filename = 'ENCFF168GAN.bed'
unaccess_bed_filename = 'unaccessible_sequences.bed'

# Read existing BED file
accessible_intervals = read_accessible_bed_file(existing_bed_filename)

# Determine un-accessible intervals
unaccessible_intervals = get_unaccessible_portion(accessible_intervals)

# Write un-accessible intervals to BED file
unaccessible_bedfile = create_unaccessible_bed_file(unaccess_bed_filename, unaccessible_intervals)

bed_to_txt_file = bed_to_txt(unaccess_bed_filename)
trim_unacc = input("Enter trimmed unaccess file name: ")
trim_unacc_file = crop_unaccess_sequences(bed_to_txt_file, trim_unacc, final_optimal_length) 


l = []

url = "https://www.encodeproject.org/files/ENCFF852UQF/@@download/ENCFF852UQF.bed.gz"
gz_filename = os.path.basename(url)
l.append(download(url, gz_filename))

unzipped_bed_file = os.path.splitext(gz_filename)[0]
l.append(gunzip_file(gz_filename, unzipped_bed_file))

print(l)


unzipped_bed_file = os.path.splitext(gz_filename)[0]
unzipped_file = gunzip_file(gzipped_file, unzipped_bed_file)
'''




