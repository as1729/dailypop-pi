import os
import boto3

def send_to_printer(file_path):
	system_command = 'lp "{file_path}"'
	os.system(system_command)

def fetch_files_from_s3():
	print('fetching files from s3')

send_to_printer('/home/pi/Downloads/A4 (1).pdf')
