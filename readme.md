# Source Comparison Between Jay, TK4- and STBEN

## Obtaining Files

The following was done to obtain the sources files. For both tk4 and
Jay Moseley the source DASD were attached to TK4- current (08).

### tk4-

* Downloaded http://wotho.ethz.ch/tk4-/tk4-source.zip
* Copied the DASD files to the `dasd` folder in tk4
* Added the source dasd to `local_conf/01`:

```
#
# Source DASD
#
0348 3350 dasd/src000.348
0349 3350 dasd/src001.349
034a 3350 dasd/src002.34a
034b 3350 dasd/srccat.34b
```

* Enabled console mode in tk4: `cd unattended/;./set_console_mode`
* Enabled the FTP server after tk4 was loaded: `/s ftpd,srvport=21021`
* Using `lftp` obtained a list of all source datasets: `lftp -u herc01,cul8tr -e "ls;bye" ftp://localhost:21021 |grep MVSSRC |awk '{ print  $9 } > MVSSRC.tk4.datasets.txt`
* Used the following script to download all files:

```bash
#!/bin/bash

for i in `cat MVSSRC.tk4.datasets.txt`; do
       echo "Getting $i"
       lftp -u herc01,cul8tr -e "mirror -v --ascii $i ./$i; bye" localhost:21021
done
```

### Jay Moseley

:warning: You can't use the same TK4 as you did above with the below instructions, it must be a fresh tk4

* Downloaded http://www.jaymoseley.com/hercules/downloads/archives/mvssrc.tgz from http://www.jaymoseley.com/hercules/installMVS/mvssource.htm
* Copied the file `mvssrc.3380` to the `dasd` folder in tk4
* Replaced the contents of `local_conf/01` with `0181 3380 dasd/mvssrc.3380`
* Enabled console mode in tk4: `cd unattended/;./set_console_mode`
* Uploaded the folowing JCL to `HERC01.TEST.CNTL(IMPORT)` and submitted it.

```jcl
//IDCAMS  JOB (1),IDCAMS,CLASS=A,MSGCLASS=H,NOTIFY=HERC01         
//IDCAMS01 EXEC PGM=IDCAMS,REGION=4096K                           
//SYSPRINT DD  SYSOUT=*                                           
//MVSSRC   DD  UNIT=3380,DISP=OLD,VOL=SER=MVSSRC                  
//SYSIN    DD  *                                                  
   /* THERE IS A USER CATALOG IN EXISTENCE ON MVSSRC THAT       */
   /* CONTAINS CATALOG ENTRIES FOR THE DATASETS ON THAT VOLUME. */
   /* IT IS CONNECTED TO THE MASTER CATALOG AND AN ALIAS TO THE */
   /* HIGH ORDER INDEX IS DEFINED TO ALLOW ACCESS TO THE        */
   /* DATASETS CATALOGUED IN THAT USER CATALOG.                 */
   IMPORT CONNECT OBJECTS ( -                                     
          UCMVSSRC  -                                             
          DEVICETYPE (3380) -                                     
          VOLUMES (MVSSRC) )                                      
   DEFINE ALIAS ( -                                               
         NAME (MVSSRC) -                                          
         RELATE (UCMVSSRC  )                                      
//                                                                
```
* Enabled the FTP server after tk4 was loaded: `/s ftpd,srvport=21021`
* Using `lftp` obtained a list of all source datasets: `lftp -u herc01,cul8tr -e "ls;bye" ftp://localhost:21021 |grep MVSSRC |awk '{ print  $9 } > MVSSRC.jay.datasets.txt`
* Used the following script to download all files:

```bash
#!/bin/bash

for i in `cat MVSSRC.tk4.datasets.txt`; do
       echo "Getting $i"
       lftp -u herc01,cul8tr -e "mirror -v --ascii $i ./$i; bye" localhost:21021
done
```

### STBEN

The site http://www.stben.net/files/MVS_3.8/asm/ was mirrored with: `wget --mirror -np https://www.stben.net/files/MVS_3.8/`

The STBEN source files have `/r/n` whereas the FTP download TK4-/Jay source files do not. To remedy this the following was run: `find ./ -type f -exec dos2unix -f {} \;`

## Analysis

The tool fslint was installed http://www.pixelbeat.org/fslint/ and run against all three folders. This removed duplicate files and the following was noted:

1) TK4- and Jay Moseley Sources are the same except for `IBCDMPRS` in `MVSSRC.SYM2-1` (Jay Moseley) and `MVSSRC.SYM201.F10` (tk4-).The difference is on line 1731, the letter 'H' is capitalized in Jay sources, but lowercase on TK4- sources.
1) Though the file is the same (based on sha256sum) the filenames are different between jay and tk4-: `./tk4-/MVSSRC.SYM701.F08/MSSCVXIT` vs `./jay/MVSSRC.SYM1-1/IEECVXIT`
1) Multiple files were marked as different from the Jay Moseley source and STBEN sources. The following script was written to compare the files:

```
IFS=$'\n'
for i in $(find ./stben -type f); do 
	b=$(basename $i)
	echo "FILENAME: $b"
	if [[ $(find -name "$b"|wc -l) -ge 2 ]]; then 
		find -name "$b" -print0 | xargs -0 -o vbindiff
		rm -i $i
	fi
done
```

1) Multiple files were noted as having slight (one character) differences between how the penny symbol was translated from EBCDIC to ASCII. These files were removed. Other files were more complex and were left in the stben folder. Oh Note is the folder `HASPSRC` which does not seem to appear in either the Jay Moseley source nor the TK4- source. 


## Additional Resources:

1) Sha256sum of each folder: In the folder `sha256` are three text files which contains the path, name and sha256 sum of each file
1) In the folder is a python script `compare.py` which compares the hashes between Jay and TK4 which outputs:

```
Comparing Jay to TK4 Sources
File Diff
	JAY: ./jay/MVSSRC.SYM2-1/IBCDMPRS 24125e5684df6f4536f8acfcf3371c9edd91bb22704ed1f35781f5c42bdf41c6
	TK4: ./tk4-/MVSSRC.SYM201.F10/IBCDMPRS de6282e1c7cb96bef654b4d61f2550a0cd908878089557f6bc5c4818a83e36f3
File Name Mismatch:
	JAY: IEECVXIT ./jay/MVSSRC.SYM1-1/IEECVXIT
	TK4: MSSCVXIT ./tk4-/MVSSRC.SYM701.F08/MSSCVXIT
Comparing TK4 to JAY Sources
File Name Mismatch:
	TK4: MSSCVXIT ./tk4-/MVSSRC.SYM701.F08/MSSCVXIT
	JAY: IEECVXIT ./jay/MVSSRC.SYM1-1/IEECVXIT
File Diff
	TK4: ./tk4-/MVSSRC.SYM201.F10/IBCDMPRS de6282e1c7cb96bef654b4d61f2550a0cd908878089557f6bc5c4818a83e36f3
	JAY: ./jay/MVSSRC.SYM2-1/IBCDMPRS 24125e5684df6f4536f8acfcf3371c9edd91bb22704ed1f35781f5c42bdf41c6
```



