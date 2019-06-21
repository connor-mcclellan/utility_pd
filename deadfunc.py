# B. Connor McClellan, 2019

import argparse
from glob import glob
import os
import numpy as np


parser = argparse.ArgumentParser(description="Insert debug code into all "
                                             "python scripts in a directory to"
                                             " record when each function is "
                                             "being used.")

parser.add_argument('directory', type=str, help='parent directory to search')
parser.add_argument('-c', '--clean', action='store_true', help='previously '
                                                               'inserted debug'
                                                               ' code will be '
                                                               'removed')

args = parser.parse_args()
clean = args.clean
parent_dir = os.path.abspath(args.directory+'/')
files = glob(parent_dir+'/**/*.py')+glob(parent_dir+'/*.py')

if not clean:
    # Remove any existing log files
    try:
        os.remove(parent_dir+'/funcs_unused.txt')
        os.remove(parent_dir+'/funcs_used.txt')
    except:
        pass

counter = 0
clean_counter = 0

for pyfile in files:
    with open(pyfile, 'r+') as f:
        lines = np.array(f.readlines(), dtype=object)

        whitespace = []
        func_names = []

        # Find all of the function definitions, note their indentation level
        # and name
        for i, item in enumerate(lines):
            if item.lstrip().startswith('def'):
                whitespace.append(item.split('def ')[0])
                func_names.append(item.split('def ')[1].split('(')[0])

        # Loop over the functions and insert the debug code
        for j in range(len(func_names)):

            # Set up reporting format
            n_space = 40 - len(func_names[j])
            report = "{}{}:    {}\\n".format(func_names[j], n_space*' ', 
                                             pyfile)

            # Write all functions to a file, so used functions can be removed
            if not clean:
                with open(parent_dir+'/funcs_unused.txt', 'a+') as allfuncs:
                    allfuncs.write(report[:-2]+'\n')

            # 'writer' is code inserted into each function in all the python
            # files that writes a report to a log file when the function is 
            # called
            writer = [
                whitespace[j]+'    ###########################\n',
                whitespace[j]+'    # INSERTED BY DEADFUNC.PY #    # Do not edit!\n',
                whitespace[j]+'    ###########################\n',
                whitespace[j]+'\n',
                whitespace[j]+'    report = "{}"\n'.format(report),
                whitespace[j]+'    try:\n',
                whitespace[j]+'        with open("{}", "r+") as used:\n'.format(parent_dir+'/funcs_used.txt'),
                whitespace[j]+'            lines = used.readlines()\n',
                whitespace[j]+'            if not report in lines:\n',
                whitespace[j]+'                used.write(report)\n',
                whitespace[j]+'    except:\n',
                whitespace[j]+'        with open("{}", "w") as used:\n'.format(parent_dir+'/funcs_used.txt'),
                whitespace[j]+'            used.write(report)\n',
                whitespace[j]+'    with open("{}", "r+") as unused:\n'.format(parent_dir+'/funcs_unused.txt'),
                whitespace[j]+'        lines = unused.readlines()\n',
                whitespace[j]+'        unused.seek(0)\n',
                whitespace[j]+'        for line in lines:\n',
                whitespace[j]+'            if report != line:\n',
                whitespace[j]+'                unused.write(line)\n',
                whitespace[j]+'        unused.truncate()\n',
                whitespace[j]+'\n',
                whitespace[j]+'    ###########################\n',
            ]

            # the lines of code are actively changing as 'writer' is inserted, 
            # so we need to reindex every time
            liveind = []
            for i, item in enumerate(lines):
                if item.lstrip().startswith('def'):
                    liveind.append(i)

            # access the right line number for the jth function after any 
            # changes
            k = liveind[j]

            if clean:
                # Check that the user hasn't edited any code
                if ('# INSERTED BY DEADFUNC.PY #' in lines[k+2] and
                    '###########################' in lines[k+len(writer)]):
                    lines = np.delete(lines, slice(k+1, k+len(writer)+1))
                    clean_counter += 1
                else:
                    print('WARNING: Incorrect or missing pattern found in "{}"'
                          ' in {}. No changes made.'.format(func_names[j], 
                                                            pyfile))
            else:
                # CHeck if deadfunc has already been run on this function
                if 'INSERTED BY DEADFUNC.PY' in lines[k+2]:
                    print('WARNING: Function "{}" in {} has existing deadfunc '
                          'code. Skipping.'.format(func_names[j], pyfile))
                else:
                    # Insert the 'writer' debug code
                    lines = np.insert(lines, k+1, writer)
                    counter += 1

        # Rewrite the python script in place to include the changes
        f.seek(0)
        for line in lines:
            f.write(line)
        f.truncate()

print('\n#####################')
print('# DEADFUNC COMPLETE #')
print('#####################')
print('')
print('Functions edited: {}'.format(counter))
print('Functions cleaned: {}'.format(clean_counter))  

if clean:
    print('\nClean complete. If no warnings were given, your code should be '
          'returned to normal.')
else:
    print('\nYou may now run your scripts. Then, check the logfiles '
          '"funcs_used.txt" and "funcs_unused.txt" in {} to see which '
          'functions exist in your code but are not used. Afterwards, "python '
          'deadfunc.py --clean {}" to remove the inserted debugging code.'
          .format(parent_dir, args.directory))
