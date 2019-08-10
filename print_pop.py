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
	return s3

def dailypop_to_print_bucket():
	bucket = s3_client().Bucket(TO_PRINT_FILES_BUCKET)
	return bucket

def download_files_to_print():
	s3_bucket = dailypop_to_print_bucket()
	# download file into current directory
	print(s3_bucket)
	print(s3_bucket.objects)
	for i in s3_bucket.objects.all():
	    print(i)
	for i in s3_bucket.objects.filter(Prefix='dailypop-1'):
	    base, filename = i.key.split('/')
	    print(i)
	    # print(base)
	    if len(filename) == 0:
            	continue
	    s3_bucket.download_file(i.key, '/home/pi/' + TO_PRINT_FILES_BUCKET + '/' + filename)


# send_to_printer('/home/pi/Downloads/A4 (1).pdf')
download_files_to_print()
