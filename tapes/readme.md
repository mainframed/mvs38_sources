## MVS Source Tapes

These tapes were obtained from Jay Moseley and extracted to these folders with the following commands:

* First gunzip the files: `gunzip *.aws.gz`
* Then using `extract.py` extracted the files:

```bash
for i in *.aws; do 
	s=${i##*/}; 
	echo ${s%.aws};
	rm -rf ${s%.aws};
	mkdir ${s%.aws};
	./extract.py --force --json --unnum --modify --jsonfile ${s%.aws} --outputdir ${s%.aws} $i;
done
```
