import os 
import random

# Includes db & log files & other common extensions:
file_types_1 = ['.txt', '.py', '.html', '.sh' '.css', '.js','.log', '.adb', '.daschema', '.db', '.crypt8',
'.pkg','db', '.dbf', '.dmp', '.doc', '.docx', '.dot', '.dotx', '.dwg', '.dxf', '.eml', '.eps', '.exe', '.fla',
'.flv', '.gif', '.gz', '.hqx', '.htm', '.html', '.indd', '.iso', '.jar', '.jpeg', '.jpg', '.key', '.log', '.m4a'
'.m4v', '.mid', '.mov', '.mp3', '.mp4', '.mpg', '.odf', '.odg', '.odp', '.ods', '.odt', '.ogg', '.pdf', '.png',]
file_types  =['.txt', '.py', '.sh']
# Add the path were you want to create the random files:
path = '/home/'
os.chdir(path)



# Creates random files in the current directory with size between 1 and 100 MB of random data with a extension from the file_types list
def create_random_files_small(num_files):
    for i in range(num_files):
        file_size = random.randint(1200, 1000000)
        file_name = str(random.randint(1,10000)) + str(file_size) + 'Bytes' + random.choice(file_types)
        with open(file_name, 'wb') as f:
            f.write(os.urandom(file_size))

def create_random_files_large(num_files):
    for i in range(num_files):
        file_size = random.randint(1000000, 10000000)
        file_name = str(random.randint(1,10000)) + str(file_size) + 'Bytes' + random.choice(file_types)
        with open(file_name, 'wb') as f:
            f.write(os.urandom(file_size))


# Calls the two functions above and creates files until 100 GB of data is created in the 
# directory 
def create_random_files():
    create_random_files_small(10000)
    create_random_files_large(100)

create_random_files()
print('Done')
