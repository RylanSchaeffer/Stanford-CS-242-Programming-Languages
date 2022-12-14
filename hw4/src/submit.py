# Submission script

# DO NOT EDIT THIS FILE

import tarfile, re, os

solution_filename = 'solution.tar.gz'
t = tarfile.open(solution_filename, 'w:gz')
error = False
def try_add(f, default_len = 0):
    global error
    try:
        s = os.stat(f)
        if default_len != 0 and s.st_size == default_len:
            print(f"Warning: did you complete {f}?")
        if f == 'README.txt':
            for l in open("README.txt").readlines():
                if re.match('^id:\\s*\d{8}\\s*$', l):
                    break
            else:
                print(f"Error: your id is not found in {f}")
                error = True
        t.add(f)
    except FileNotFoundError:
        print(f"Error: missing {f}")
        error = True

try_add('interpreter.py')
try_add('problem.objc')
try_add('README.txt')
t.close()

if not error:
    print(f"Wrote '{solution_filename}'. Upload this file to Canvas.")
else:
    print(f'Try again after fixing the above error(s)!')
