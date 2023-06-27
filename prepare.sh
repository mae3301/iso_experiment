#!/usr/bin/bash

# download the iso manually

# download the tinycore iso with wget
wget http://tinycorelinux.net/4.x/x86/archive/4.7.2/Core-4.7.2.iso

# some summaries with isoutil
isoinfo -i 3301.iso -R -l

# extract vmlinuz 
isoinfo -i 3301.iso -x /BOOT/VMLINUZ\.\;1 > 3301_VMLINUZ 
isoinfo -i Core-4.7.2.iso -x /BOOT/VMLINUZ\.\;1 > TINYCORE_VMLINUZ 


# run md5sum on vmlinuz
md5sum 3301_VMLINUX > md5sum_linux_kernels.txt
md5sum TINYCORE_VMLINUX > md5sum_tinycore_kernels.txt


# extract the core of the OS from the ISO
isoinfo -i 3301.iso -x /BOOT/3301.IMG\;1  > 3301.gz
isoinfo -i Core-4.7.2.iso -x /BOOT/CORE.GZ\;1 > core.gz

# unzip both files
gunzip core.gz
gunzip 3301.gz

#un-archive both operation systems into the directories tinycore (for tinycore) and cicada (for cicada)
mkdir tinycore
cd tinycore
cpio -iv < ../core

cd ..
mkdir cicada
cd cicada
cpio -iv < ../3301
cd ..

# you will need to be the owner of all the files in both repositories 
# to run the python script
sudo chown -R -L $USER cicada
sudo chown -R -L $USER tinycore

# after running the python script you can examine the differences that it turns up
diff tinycore/etc/passwd cicada/etc/passwd
diff tinycore/etc/init.d/tc-config cicada/etc/init.d/tc-config
