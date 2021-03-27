//IDCAMS  JOB (1),IDCAMS,CLASS=A,MSGCLASS=X                             00010000
//IDCAMS01 EXEC PGM=IDCAMS,REGION=4096K                                 00020000
//SYSPRINT DD  SYSOUT=*                                                 00030000
//MVSSRC   DD  UNIT=3380,DISP=OLD,VOL=SER=MVSSRC                        00040000
//SYSIN    DD  *                                                        00050000
                                                                        00060000
   /* THERE IS A USER CATALOG IN EXISTENCE ON MVSSRC THAT       */      00070000
   /* CONTAINS CATALOG ENTRIES FOR THE DATASETS ON THAT VOLUME. */      00080000
   /* IT IS CONNECTED TO THE MASTER CATALOG AND AN ALIAS TO THE */      00090000
   /* HIGH ORDER INDEX IS DEFINED TO ALLOW ACCESS TO THE        */      00100000
   /* DATASETS CATALOGUED IN THAT USER CATALOG.                 */      00110000
                                                                        00120000
   IMPORT CONNECT OBJECTS ( -                                           00130000
          UCMVSSRC  -                                                   00140000
          DEVICETYPE (3380) -                                           00150000
          VOLUMES (MVSSRC) )                                            00160000
                                                                        00170000
   DEFINE ALIAS ( -                                                     00180000
         NAME (MVSSRC) -                                                00190000
         RELATE (UCMVSSRC  )                                            00200000
                                                                        00210000
//                                                                      00220000
