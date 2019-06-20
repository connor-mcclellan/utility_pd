import subprocess
import argparse
from glob import glob
import os
from itertools import compress
import numpy as np

parser = argparse.ArgumentParser(description="Insert debug code into all python scripts in a directory to record when each function is being used.")
parser.add_argument('directory', type=str, help='parent directory to search')
parser.add_argument('-c', '--clean', action='store_true')

args = parser.parse_args()
clean = args.clean
parent_dir = os.path.abspath(args.directory)
files = glob(parent_dir+'/**/*.py')+glob(parent_dir+'/*.py')

if not clean:
    try:
        os.remove(parent_dir+'/funcs_unused.txt')
        os.remove(parent_dir+'/funcs_used.txt')
    except FileNotFoundError:
        pass

counter = 0
clean_counter = 0

for pyfile in files:
    with open(pyfile, 'r+') as f:
        lines = np.array(f.readlines(), dtype=object)

        whitespace = []
        func_names = []
        for i, item in enumerate(lines):
            if item.lstrip().startswith('def'):
                whitespace.append(item.split('def ')[0])
                func_names.append(item.split('def ')[1].split('(')[0])

        for j in range(len(func_names)):

            # Set up reporting format
            n_space = 40 - len(func_names[j])
            report = "{}{}:    {}\\n".format(func_names[j], n_space*' ', pyfile)

            # Write all functions to a file, so used functions can be removed
            if not clean:
                with open(parent_dir+'/funcs_unused.txt', 'a+') as allfuncs:
                    allfuncs.write(report[:-2]+'\n')

            # 'writer' inserts code into each python script that will write a
            # report to a log file when the script is run
            writer = [
                whitespace[j]+'    ###########################\n',
                whitespace[j]+'    # INSERTED BY DEADFUNC.PY #    # Do not edit!\n',
                whitespace[j]+'    ###########################\n',
                whitespace[j]+'\n',
                whitespace[j]+'    import os\n',
                whitespace[j]+'    with open("{}", "a+") as log:\n'.format(parent_dir+'/funcs_used.txt'),
                whitespace[j]+'        log.write("{}")\n'.format(report),
                whitespace[j]+'    with open("{}") as oldlog, open("{}", "w") as newlog:\n'.format(parent_dir+'/funcs_unused.txt', parent_dir+'/tmp.txt'),
                whitespace[j]+'        lines = oldlog.readlines()\n',
                whitespace[j]+'        for line in lines:\n',
                whitespace[j]+'            if not "{}" in line:\n'.format(func_names[j]),
                whitespace[j]+'                newlog.write(line)\n',
                whitespace[j]+'    os.remove("{}")\n'.format(parent_dir+'/funcs_unused.txt'),
                whitespace[j]+'    os.rename("{}", "{}")\n'.format(parent_dir+'/tmp.txt', parent_dir+'/funcs_unused.txt'),
                whitespace[j]+'\n',
                whitespace[j]+'    ###########################\n',
            ]

            # the 'lines' are changing, so we need to reindex every time
            liveind = []
            for i, item in enumerate(lines):
                if item.lstrip().startswith('def'):
                    liveind.append(i)

            # access the right line number for this function after any changes
            k = liveind[j]

            if clean:
                if ('# INSERTED BY DEADFUNC.PY #' in lines[k+2] and
                    '###########################' in lines[k+len(writer)]):
                    lines = np.delete(lines, slice(k+1, k+len(writer)+1))
                    clean_counter += 1
                else:
                    print('WARNING: Incorrect or missing pattern found in "{}" in {}. No changes made.'.format(func_names[j], pyfile))
            else:
                # Insert the new lines into the code
                if 'INSERTED BY DEADFUNC.PY' in lines[k+2]:
                    print('WARNING: Function "{}" in {} has existing deadfunc code. Skipping.'.format(func_names[j], pyfile))
                else:
                    lines = np.insert(lines, k+1, writer)
                    counter += 1
        # Rewrite the python script to include the changes
        f.seek(0)
        for line in lines:
            f.write(line)
        f.truncate()

print(
    '\n ####################################\n',
    '# DEADFUNC CODE INJECTION COMPLETE #\n',
    '####################################\n',
    '\n',
    'Functions injected: {}\n'.format(counter),    
    'Functions cleaned: {}'.format(clean_counter)
)    

if clean:
    print('\nClean complete. Your code should be returned to normal.')
else:
    print('\nYou may now run your scripts. Then, check the logfiles "funcs_used.txt" and "funcs_unused.txt" in {} to see which functions exist in your code but are not used. Afterwards, "python deadfunc.py --clean" to remove the inserted debugging code.'.format(parent_dir))
