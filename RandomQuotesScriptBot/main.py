import subprocess
import os
import shutil

python_interpreter = 'python' # you may need to name this python3, depends on your personal configuration

script_path = 'C:\\Users\\ibrah\\OneDrive\\Desktop\\RandomQuoteTweets+Instagram Posts\\script.py' 
# this will depend on where exactly your script.py file is located, provided to you by me in this folder
# Ex: C:\\Users\\ibrah\\OneDrive\\Desktop\\RandomQuoteTweets+Instagram Posts\\script.py

print("Starting the script...")

subprocess.call([python_interpreter, script_path])

print("Script has been completed. Posts on both X/Twitter and Instagram have been uploaded.")

print("Attempting to remove temp files...")
config_folder = 'config'
temp_file_name = 'temp_image.jpg.REMOVE_ME'

if os.path.exists(config_folder):
    shutil.rmtree(config_folder)
    print("Removed config folder")
            

if os.path.exists(temp_file_name):
    os.remove(temp_file_name)
    print("Removed temp_image.jpg.REMOVE_ME file")

print("Process complete!")


