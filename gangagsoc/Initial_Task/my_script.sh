#!/bin/bash
pdftotext $@.pdf -| sed -e 's/ /\n/g' |grep -ci 'the' > job_output.txt
#echo 'Args: ' $@.txt > my_output.txt
