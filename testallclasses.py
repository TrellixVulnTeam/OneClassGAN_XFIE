import options
import ocgantestdisjoint
import numpy as np
import os
import random
random.seed(1000)
opt = options.test_options()
opt.istest = 0

text_file = open(opt.dataset + "_progress.txt", "w")
text_file.close()
#First read all classes one at a time and iterate through all
text_file = open(opt.dataset + "_folderlist.txt", "r")
folders = text_file.readlines()
text_file.close()
folders = [i.split('\n', 1)[0] for i in folders]
follist = range(0,1000,10)
for classname in folders:
    
        epoch = []
        trainerr = []
        valerr =[]
	os.system('python2  cvpriter.py --epochs 1001 --ndf 16 --ngf 64  --istest 0 --expname grapesip64 --img_wd 61  --img_ht 61  --depth 3  --datapath ../ --noisevar 0.2  --lambda1 500 --seed 1000 --append 0 --classes '+ classname)
        res_file = open(opt.expname + "_validtest.txt", "r")
        results = res_file.readlines()
        res_file.close()
        results = [i.split('\n', 1)[0] for i in results]
        for line in results:
            temp = line.split(' ', 1)
	    #print(temp)
            epoch.append(temp[0])
            temp = temp[1].split(' ', 1)
            trainerr.append(temp[0])
            valerr.append(temp[1])

        valep = np.argmin(np.array(valerr))
        trainep = np.argmin(np.array(trainerr))
        #print(valep)
        #print(trainep)
        opt.epochs =follist[ valep]
        roc_aucval = ocgantestdisjoint.main(opt)
        opt.epochs = follist[trainep]
        roc_auctrain = ocgantestdisjoint.main(opt)
    	text_file = open(opt.dataset + "_progress.txt", "a")
        text_file.write("%s %s %s %s\n" % (str(valerr[valep]), str(trainerr[trainep]), str(roc_aucval[1]),str(roc_auctrain[1])))
        text_file.close()
