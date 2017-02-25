Infer Splicing Regulator(ISR)

ISR is a Python based tool to infer Key splicing regulator from differential splicing results.
Currently, ISR only support the Skipping Exon analysis.


1. Requirement

   (A) python2.x (>Python2.4)
   
   (B) fisher package: https://pypi.python.org/pypi/fisher/0.1.4
   
   (C) pybedtools package: https://pypi.python.org/pypi/pybedtools
   
   (D) Numpy package: http://www.numpy.org/
   
2. Installation
within the folder:

Python setup.py install

to install it to other directory

Python setup.py install --prefix=="PATH of your choise"

3. Usage

3.1 Input requirement
   ISR support standard MISO (default), MATS and BED format as input.
   
   Note: for MATS output, current version of ISR can only handle SE (Skipped Exon) analysis output.
   
   For BED format, ISR require BED6 format. The Score Column (Column 5), 0 means downregulation, while 1000 means upregulation of skipped    exon.
   
   Here is an example (You can find the raw data from github.com/bioliyezhang/ISR/blob/master/examples/1-human-without-direction/input/). 
   
   chr17	39976093	39976275	chr17:37229619:37229801:hnRNPH.1:PMID19749754	0	+
   
   ...
 
 3.2 Database:
   The compiled databased for human and mouse can be found in the database folder.
 
 3.3 Specific Examples:
   3.3.1 Input as a BED format, Not knowing the Splicing regulator regulation in human
   （See examples/1-human-without-direction folder)
   
    Command line: 
    
    python ISR_PATH/ISR_v1.1.py -i hnRNPH_SupTable4_hnRNPH.1_PMID19749754_reference_hg19.txt \
    -r hg19_Splicing_SF15_ref_20170205_single.bed -t BED
   
   3.3.2 Input as a MISO format, knowing the Splicing regulator regulation in human
    （See examples/2-human-with-direction folder)
    
    Command line:
    
    python ISR_PATH/ISR_v1.1.py -i ALK_RNAi_control_vs_treated.miso_bf.txt \
    -r hg19_Splicing_SF24_ref_20170225_combine.bed -e hg19_feedin_regulation_matrix.txt
    
   3.3.3 Input as a BED format, Not knowing the Splicing regulator regulation in mouse
    (See examples/3-mouse-without-direction folder)
    
    Command line:
    
    python ISR_PATH/ISR_v1.1.py -i ESRP_mm10_ESRP1_PMID27050523_reference.txt \
    -r mm10_Splicing_SF5_ref_20170205_single.bed -t BED
    
    The output should be the same as the one located in the output folder for each example. 
    
