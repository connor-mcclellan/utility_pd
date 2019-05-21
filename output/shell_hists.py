from subprocess import call

call(['python', 'flux_hist.py', './noconv/images/pd_raw_660nm.dat'])
call(['python', 'flux_hist.py', './autoconv/images/pd_raw_autoconv.dat'])
call(['python', 'flux_hist.py', './manualconv/images/pd_raw_manualconv.dat'])
