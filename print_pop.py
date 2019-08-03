import os
import boto3

PRINTED_FILES_BUCKET = 'dailypop-printed'
TO_PRINT_FILES_BUCKET = 'dailypop-to-print'
BASE_LOCAL_FILE_PATH = 'home/pi/'

def send_to_printer(file_path):
	system_command = 'lp "%s"'%(file_path)
	os.system(system_command)

def fetch_files_from_s3():
	print('fetching files from s3')

def s3_client():
	s3 = boto3.resource('s3')

def dailypop_to_print_bucket():
	s3_client().Bucket(TO_PRINT_FILES_BUCKET)

def download_files_to_print():
	s3_bucket = dailypop_to_print_bucket()
	# download file into current directory
	for s3_object in s3_bucket.objects.all():
	    # Need to split s3_object.key into path and file name, else it will give error file not found.
	    path, filename = os.path.split(s3_object.key)
	    local_path = '%s%s'%(BASE_LOCAL_FILE_PATH, filename)
	    s3_bucket.download_file(s3_object.key, local_path)

# send_to_printer('/home/pi/Downloads/A4 (1).pdf')
download_files_to_print()
