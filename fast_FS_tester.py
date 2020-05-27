from time import process_time
import os
import argparse

def test_speed(path, testfile_size_bytes):
    # First we will establish the prerequisites for testing. File name, size etc.
    testfile_size_MB = testfile_size_bytes/1024/1024
    filename = 'pytestfile.bin'

    # Here we generate random bytes to test write and read speeds with, as well as later test content.
    # ran_number is how many different byte strings will be generated.
    ran_number = 4
    random_bytestrs = [os.urandom(4096) for i in range(0, ran_number)]
    iterations = int(testfile_size_bytes/(4096*ran_number))

    # since file size can be not divisible by 4096, the leftovers will be assigned to last_bytestr
    last_bytestr = os.urandom(testfile_size_bytes%(ran_number*4096))
    
    with open(os.path.join(path, filename),'wb') as fil:
        write_start = process_time()
        # write all data to the file. each bytestr in sequence, every iteration.
        for i in range(iterations):
            for s in random_bytestrs:
                fil.write(s)
        # write the leftovers.
        fil.write(last_bytestr)
        write_done = process_time()

    write_time_elapsed = (write_done - write_start)
    # megabytes write time
    MBYps_write = testfile_size_MB / write_time_elapsed
    # megabits write time
    Mbips_write = MBYps_write * 8

    # read performance testing. Has to be separate from content checking to avoid overhead of comparisons.
    with open(os.path.join(path, filename),'rb') as fil:
        read_start = process_time()
        while True:
            piece = fil.read(1024)
            if not piece:
                break
        read_done = process_time()

    read_time_elapsed = (read_done  - read_start)
    MBYps_read = testfile_size_MB / read_time_elapsed
    Mbips_read = MBYps_read * 8

    passed = 0
    failed = 0
    # file content integrity check. each chunk should correspond to the same chunk written previously.
    with open(os.path.join(path, filename),'rb') as fil:
        for i in range(iterations):
            for j in random_bytestrs:
                if j == fil.read(4096):
                    passed+=1
                else:
                    failed+=1
        if len(last_bytestr) > 0:
            if fil.read() == last_bytestr:
                passed+=1
            else:
                failed+=1

    # Finally delete the written junk file, and for good measure time that performance too.
    delete_start = process_time()
    os.remove(os.path.join(path, filename))
    delete_done = process_time()
    delete_time_elapsed = (delete_done - read_start)

    return [passed, failed, MBYps_write, Mbips_write, write_time_elapsed, MBYps_read, Mbips_read, read_time_elapsed,delete_time_elapsed]

def get_bool(prompt):
    stval = input(prompt)
    if stval.lower() in ['y','yes','true']:
        return True
    return False

parser = argparse.ArgumentParser()
parser.add_argument('test_path', help='File path to filesystem or directory to test')
parser.add_argument('output_name',
                    help='Name for the output file. If file ends in .tsv or .tab, a tab separated file \
                     will be created. Otherwise a .csv will be created, and .csv will be appended to \
                     file name if necessary.')
parser.add_argument('-s', '--test_size', help='Size of the test file to generate in MB.',
                    default=500, type=int)
parser.add_argument('-b', '--bytes', action='store_true',
                    help='Use the specified test_size (-s) as number of bytes instead of megabytes.')
parser.add_argument('-i', '--iterations', help='Number of write-read-delete iterations to do.',
                    default=10, type=int)
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
parser.add_argument("-o", "--overwrite_existing", action="store_true",
                    help="Ignore possibly existing output file. If not used, user will be asked if file exists.")
args = parser.parse_args()

sep=','
if args.output_name[-4:].lower() in ['.tab', '.tsv']:
    sep='\t'
elif args.output_name[-4:].lower() != '.csv':
    args.output_name = args.output_name + '.csv'

if os.path.isfile(args.output_name) and not args.overwrite_existing:
    if not get_bool(f'File {args.output_name} exists. Overwrite (y/N)?'):
        exit(0)

test_size = args.test_size
if not args.bytes:
    test_size = test_size * 1024 * 1024

data = []
columns = ['iteration', 'path tested', 'file size', 'file content checks passed', 'file concent checks failed', 'MBps write speed', 'Mbps write speed', 'file write time (seconds)', 'MBps read speed', 'Mbps read speed', 'file read time (seconds)', 'delete time']
for i in range(0, args.iterations):
    results = test_speed(args.test_path, test_size)
    data.append([i, args.test_path, test_size])
    data[-1].extend(results)
    if args.verbose:
        print(f'Iteration {i+1} complete.')

if args.verbose:
    print(f'Writing output file: {args.output_name}')
with open(args.output_name, 'w') as fil:
    fil.write(sep.join(columns)+'\n')
    for line in data:
        fil.write(sep.join([str(x) for x in line])+'\n')
