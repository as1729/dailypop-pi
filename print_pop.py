import os
import boto3

PRINTED_FILES_BUCKET = 'dailypop-printed'
TO_PRINT_FILES_BUCKET = 'dailypop-to-print'
BASE_LOCAL_FILE_PATH = 'home/pi/'

def send_to_printer(file_path):
	system_command = 'lp "%s"'%(file_path)
	os.system(system_command)

def print_files_to_print():
	directory = '/home/pi/' + TO_PRINT_FILES_BUCKET
	for filename in os.listdir(directory):
		send_to_printer(directory + '/' + filename)
		print('Sent the following file to printer: ' + filename)

def fetch_files_from_s3():
	print('fetching files from s3')

def delete_files_in_to_print_directory():
	directory = '/home/pi/' + TO_PRINT_FILES_BUCKET
	for filename in os.listdir(directory):
		os.remove(directory + '/' + filename)
		print('Deleted the following file locally: ' + filename)

def move_files_in_s3_to_printed_bucket():
	s3_bucket = s3_client().Bucket(TO_PRINT_FILES_BUCKET)
	s3 = s3_client()
	for to_print_item in s3_bucket.objects.filter(Prefix='dailypop-1'):
		base, filename = to_print_item.key.split('/')
		if len(filename) == 0:
			continue
		copy_source = { 'Bucket': TO_PRINT_FILES_BUCKET, 'Key': to_print_item.key }
		s3.meta.client.copy(copy_source, PRINTED_FILES_BUCKET, to_print_item.key)
		print('Copied the following file to printed files bucket: ' + to_print_item.key)
		to_print_item.delete()
		print('Deleted the following file from to print bucket: ' + to_print_item.key)
		print('Finished moving of file from to print to printed.')

def s3_client():
	s3 = boto3.resource('s3')
	return s3

def dailypop_to_print_bucket():
	bucket = s3_client().Bucket(TO_PRINT_FILES_BUCKET)
	return bucket

def download_files_to_print():
	s3_bucket = dailypop_to_print_bucket()
	# download file into current directory
	for i in s3_bucket.objects.filter(Prefix='dailypop-1'):
	    base, filename = i.key.split('/')
	    if len(filename) == 0:
            	continue
	    s3_bucket.download_file(i.key, '/home/pi/' + TO_PRINT_FILES_BUCKET + '/' + filename)
	    print('Finished downloading: ' + filename)

def run_cycle():
	download_files_to_print()
	print_files_to_print()
	delete_files_in_to_print_directory()
	move_files_in_s3_to_printed_bucket()

