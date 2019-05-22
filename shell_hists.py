from subprocess import call

for i in range(6):
    call(['python', 'make_image.py', '-f', './filters/progressive_'+str(i)+'.filter', '-d', './output/lowZ/manual/example.134.rtout.image'])
    call(['python', 'flux_hist.py', '/home/cmcclellan1010/pdwork/output/lowZ/manual/pdimageout_progressive_'+str(i)+'.dat'])
   
