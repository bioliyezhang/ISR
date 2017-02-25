# -*- coding: cp936 -*-
"""
The main purpose of this script is to Infer the key splicing factor
that regulating the differential splicing events between two conditions.

=============================
Usage: python ISR_obj_v1.1.py
-h help

-i files to processed                           *[No default value]
    it take MISO diff output or BED file

-t type of input file                            [default value: "MISO"]
    Current supported type include: MISO, MATS, BED

-e mRNA/protein level change of Splicing factor [No default value,optional]

-r splicing factor regulation database          *[No default value]
    specific format specified in the README document

-f Bayes factor cutoff                          [default value: 10]
    specific to MISO output 

-F MAX_FDR_score cutoff                         [default value: 0.05]
    specific to MATS output

-g generate expression matrix to fill in        [default: None]

===============================
less important parameters:
-c comparison direction                         [default value: 1]
    if set to 1, the algorithm will expect (Control vs RNAi comparison direction in MISO output)
    diff in MISO/MATS equal to Control - RNAi
    if set to 0, the algorithm will expect (RNAi vs Control comparison direction in MISO output)
    diff in MISO/MATS equal to RNAi - Control

-o fraction of overlap required                 [default value: 0.99]

-d delete intermediate files                    [default value: 1]
    1 means delete intermediate files, 0 means keep intermediate files

-s suffix for the files to be processed         [default value "txt"]

===================
input description:
input files:
1. [splicing regulatory database] -r
2. [diff splicing output] -i
3. [Splicing factor level change] -e 
======================
output files:
1. statistics for all the splicing factor in the database
============================
Python & Module requirement:
Versions 2.x : 2.4 or above 
Module: (1)Pybedtools and (2)Fisher (3)Numpy Python Module is required.

============================
command line example:
## 1. generate the expected regulation direction 
python ISR_v1.0.py -g ref.txt
## 2. generate a prediction witout providing expected regulation on MISO output
python ISR_v1.0.py -r ref.txt -i control_vs_RNAi.miso.bf -t MISO
## 3. generate a prediction with BED as input
python ISR_v1.0.py -r ref.txt -i SF_X.bed -t BED
## 4. generate a prediction with a expected regulation input on MISO output
python ISR_v1.0.py -r ref.txt -i control_vs_RNAi.miso.bf -t MISO -e expected_SF_regulation.txt
"""

##Copyright
##By Liye Zhang
##Contact: bioliyezhang@gmail.com
###Code Framework
'''
1. generate a subset of input files based on bayes factor cutoff
'''
### Specific Functions definiation
def add_SF_regulation(SF,regulation,SF_factor_dict):
    SF_factor_list= SF_factor_dict.keys()
    for SF_factor in SF_factor_list:
        SF_factor_list = SF_factor.split(".")
        final_SF_factor_ID = SF_factor_list[0]
        if SF == final_SF_factor_ID:
            ## Process 
            if regulation in ["up","+"]:
                SF_factor_dict[SF_factor]="+"
            elif regulation in ["dn","-"]:
                SF_factor_dict[SF_factor]="-"
            elif regulation in ["NC"]:
                SF_factor_dict[SF_factor]="NC"
            else:
                pass
    return SF_factor_dict

def chro_formatter(chro):
    ## format the chromosome 
    if chro.startswith("chr"):
        formated_chro=chro
    else:
        formated_chro="chr"+chro
    return formated_chro

def correct_pvalues_for_multiple_testing(pvalues, correction_type = "Benjamini-Hochberg"):                
    """                                                                                                   
    consistent with R - print correct_pvalues_for_multiple_testing([0.0, 0.01, 0.029, 0.03, 0.031, 0.05, 0.069, 0.07, 0.071, 0.09, 0.1]) 
    """
    from numpy import array, empty                                                                        
    pvalues = array(pvalues) 
    n = pvalues.shape[0]                                                                           
    new_pvalues = empty(n)
    if correction_type == "Bonferroni":                                                                   
        new_pvalues = n * pvalues
    elif correction_type == "Bonferroni-Holm":                                                            
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]                                      
        values.sort()
        for rank, vals in enumerate(values):                                                              
            pvalue, i = vals
            new_pvalues[i] = (n-rank) * pvalue                                                            
    elif correction_type == "Benjamini-Hochberg":                                                         
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]                                      
        values.sort()
        values.reverse()                                                                                  
        new_values = []
        for i, vals in enumerate(values):                                                                 
            rank = n - i
            pvalue, index = vals                                                                          
            new_values.append((n/rank) * pvalue)                                                          
        for i in xrange(0, int(n)-1):  
            if new_values[i] < new_values[i+1]:                                                           
                new_values[i+1] = new_values[i]                                                           
        for i, vals in enumerate(values):
            pvalue, index = vals
            new_pvalues[index] = new_values[i]                                                                                                                  
    return new_pvalues


def extract_bed_from_MISO_ID(MISO_ID):
    ## this function to convert MISO ID into BED format
    MISO_ID_list = MISO_ID.split("@")
    skip_exon_info = MISO_ID_list[1]
    skip_exon_info_list = skip_exon_info.split(":")
    chro = chro_formatter(skip_exon_info_list[0])
    start = skip_exon_info_list[1]
    end = skip_exon_info_list[2]
    strand = skip_exon_info_list[3]
    return chro,start,end,strand   

def predict_splicing_factor(infile,reference,SF_level_infile,input_type,cmp_direction):
    import pybedtools ## import pybedtools package
    from fisher import pvalue 
    
    ## Module 1: get splicing factor List from reference File
    splicing_bedtools = pybedtools.BedTool(reference)
    infile_obj=GeneralFile_class(reference)  
    infile_reader=infile_obj.reader_gen()
    splicing_factor_dict = dict() ## how many in each splicing factor
    for row in infile_reader:
        ID= row[3] #ID
        ID_info = ((ID.split(":"))[3]).upper()
        splicing_factor_dict[ID_info]=0 
    splicing_factor_list = splicing_factor_dict.keys() ## all splicing factor tested
    
    ## Module 2: process SF level infile
    SF_regulation_dict=dict()
    for SF in splicing_factor_list:
        SF_regulation_dict[SF]="NA"
    SF_regulation_known=False

    if SF_level_infile!=None:
        SF_regulation_known=True
        infile_obj=GeneralFile_class(SF_level_infile)  ##create file obj(class)
        infile_obj.SKIP_HEADER=0    ##setup up the manual skip header if necessary
        infile_obj.SAMPLE_ID_LEN=unique_id_length  ##unique ID length
        infile_reader=infile_obj.reader_gen()
        for row in infile_reader:
            SF=row[0].upper()
            regulation=row[1]
            SF_regulation_dict=add_SF_regulation(SF,regulation,SF_regulation_dict)

    ## Module 3: Start to Process the MISO output to BED
    ## check input type
    print "Processing infile:", infile
    ##Set up infile object

    if input_type!="BED":
        infile_obj=GeneralFile_class(infile)  ##create file obj(class)
        outfile_name=infile_obj.outputfilename_gen("filtered","bed") ##create output file
        outfile_path=OUTPUT_PATH+"/"+outfile_name
        BED_intermediate_file = outfile_path
        outfile_obj=GeneralFile_class(outfile_path)      ##create output obj                           
        outfile_obj.output_handle_gen()    ##generate output handle       
        #outfile_obj.handle.write("#chro\tStart\tend\tName\tScore\tStrand\n")
        
        if input_type=="MISO":
            infile_obj.SKIP_HEADER=1    ##setup up the manual skip header if necessary
            infile_obj.SAMPLE_ID_LEN=unique_id_length  ##unique ID length
            infile_reader=infile_obj.reader_gen() 
            ## Module:3.1 : create a filtered and BED file
            input_diff_count=0  ## A count for the MISO Diff output
            for row in infile_reader:
                bayes_factor = float(row[8])
                if bayes_factor>=BAYES_MIN:
                    name = row[0] ## MISO ID
                    direction = float(row[7])  ## Strand
                    chro,start,end,strand=extract_bed_from_MISO_ID(name)
                    outfile_obj.handle.write(chro+'\t'+start+'\t'+end+'\t'+name+'\t')
                    if cmp_direction!=0: ## adjust MISO direction 
                        if direction>0:
                            outfile_obj.handle.write("1000\t") ## 1000, upregulation
                        elif direction<0: 
                            outfile_obj.handle.write("0\t")
                        else:
                            outfile_obj.handle.write("500\t")
                            pass
                    else:
                        if direction>0:
                            outfile_obj.handle.write("0\t") ## 1000, upregulation
                        elif direction<0: 
                            outfile_obj.handle.write("1000\t")
                        else:
                            outfile_obj.handle.write("500\t")
                            pass
                    outfile_obj.handle.write(strand+'\n')
                    input_diff_count +=1
            outfile_obj.handle.close()

            ## Module 3.2:: get intersectBED temp file
            infile_diff_bedtools = pybedtools.BedTool(outfile_path)
        
        elif input_type=="MATS":
            infile_obj.SKIP_HEADER=1    ##setup up the manual skip header if necessary
            infile_obj.SAMPLE_ID_LEN=unique_id_length  ##unique ID length
            infile_reader=infile_obj.reader_gen() 
            ## Module:3.1 : create a filtered and BED file

            for row in infile_reader:
                
                fdr = float(row[MATS_FDR_COLUMN])
                if fdr <= FDR_MAX:
                    direction = float(row[MATS_CHANGE_COLUMN])
                    strand = row[MATS_STRAND_COLUMN]  ## Strand
                    chro = row[MATS_CHRO_COLUMN] 
                    start = int(row[MATS_START_COLUMN])+1 ## 1 based coordinate
                    end = row[MATS_END_COLUMN]
                    name = chro+"_"+str(start)+"_"+end+"_"+strand
                    outfile_obj.handle.write(chro+'\t'+str(start)+'\t'+end+'\t'+name+'\t')
                    if cmp_direction!=0: ## adjust MISO direction 
                        if direction>0:
                            outfile_obj.handle.write("1000\t") ## 1000, upregulation
                        elif direction<0: 
                            outfile_obj.handle.write("0\t")
                        else:
                            outfile_obj.handle.write("500\t")
                            pass
                    else:
                        if direction>0:
                            outfile_obj.handle.write("0\t") ## 1000, upregulation
                        elif direction<0: 
                            outfile_obj.handle.write("1000\t")
                        else:
                            outfile_obj.handle.write("500\t")
                            pass
                    outfile_obj.handle.write(strand+'\n')
            outfile_obj.handle.close()
            infile_diff_bedtools = pybedtools.BedTool(outfile_path)



        else:
            print "current format",input_type,"not supported"
            sys.exit(0)

    else:
        infile_diff_bedtools = pybedtools.BedTool(infile)
        infile_obj=GeneralFile_class(infile)  ##create file obj(class)
        infile_obj.SKIP_HEADER=infile_skip    ##setup up the manual skip header if necessary
        infile_obj.SAMPLE_ID_LEN=unique_id_length  ##unique ID length
        infile_reader=infile_obj.reader_gen()  
    
    overlap_bedtools = infile_diff_bedtools.intersect(splicing_bedtools,wo=True,f=MIN_OVERLAP,r=True)
    intersect_outfile_name=infile_obj.outputfilename_gen("filtered","intersect")
    d=overlap_bedtools.saveas(intersect_outfile_name)


    ## Module 3.3: Process intersect File ReadIn to get final stats
    intersect_obj=GeneralFile_class(intersect_outfile_name)  ##create file obj(class)
    intersect_reader=intersect_obj.reader_gen()

    outfile_name=infile_obj.outputfilename_gen("ISR_stat","txt") ##create output file
    outfile_path=OUTPUT_PATH+"/"+outfile_name
    outfile_obj=GeneralFile_class(outfile_path)              ##create output obj                           
    outfile_obj.output_handle_gen()    ##generate output handle
    outfile_obj.handle.write("#splicing_factor\tPvalue\tfdr\tPredicted_direction")
    outfile_obj.handle.write("\tupup\tupdn\tdnup\tdndn\n")

    overlap_dict= dict()
    for splicing_factor in splicing_factor_list:
        overlap_dict[splicing_factor]=[0,0,0,0] 
        ## 1 (up,up) ; 2 (up,dn) ; 3 (dn,up) ; 4 (dn,dn)
        ##      0           1          2        3   
        ## get the fisher exact test
        ## the first item is the data direction, second direction is 
        ## the predicted 

    for row in intersect_reader:
        splicing_factor_ID = row[9]
        splicing_factor = (splicing_factor_ID.split(":")[3]).upper()
        index=0
        data_direction = row[4]
        if data_direction=="1000":
            pass
        elif data_direction=="0":
            index+=2
        else:
            print "undefined"
            pass
        
        ## regulation direction
        regulation_direction=row[10]
        if regulation_direction=="1000":
            pass
        elif regulation_direction=="0":
            index+=1
        else:
            pass

        overlap_dict[splicing_factor][index]+=1

    ## generate the splicing factor related prediction
    ## quantify the fisher exact test
    pvalue_dict=dict()
    index=-1
    pvalue_list=[]
    for splicing_factor in splicing_factor_list:
        index+=1
        
        upup = overlap_dict[splicing_factor][0]
        updn = overlap_dict[splicing_factor][1]
        dnup = overlap_dict[splicing_factor][2]
        dndn = overlap_dict[splicing_factor][3]
        up_evidence = upup+dndn
        dn_evidence = updn+dnup
        p=pvalue(upup,updn,dnup,dndn)
        pvalue_dict[splicing_factor]=index
        if SF_regulation_dict[splicing_factor]=="NA":
            if up_evidence>dn_evidence:
                predicted_direction="predicted:up"
            elif dn_evidence>up_evidence:
                predicted_direction="predicted:dn"
            else:
                predicted_direction="NA"
            p_value=p.two_tail
            pvalue_list.append(p_value)

        elif SF_regulation_dict[splicing_factor]=="-":
            #p_value=max(p.two_tail,p.left_tail)
            p_value=p.left_tail
            predicted_direction="known:dn"
            pvalue_list.append(p_value)
        elif SF_regulation_dict[splicing_factor]=="+":
            #p_value=max(p.two_tail,p.right_tail) #
            p_value=p.right_tail
            predicted_direction="known:up"
            pvalue_list.append(p_value)
        elif SF_regulation_dict[splicing_factor]=="NC":
            #pvalue="NA,not tested"
            index-=1
            pvalue_dict[splicing_factor]=-1
        else:
            print "unexpected"
            pass
            

    fdr_list=correct_pvalues_for_multiple_testing(pvalue_list) 
    for splicing_factor in splicing_factor_list:
        outfile_obj.handle.write(splicing_factor+'\t')
        upup = overlap_dict[splicing_factor][0]
        updn = overlap_dict[splicing_factor][1]
        dnup = overlap_dict[splicing_factor][2]
        dndn = overlap_dict[splicing_factor][3]
        up_evidence = upup+dndn
        dn_evidence = updn+dnup
        index=pvalue_dict[splicing_factor]
        if index==-1:
            fdr="NA,not tested due to No change in SF"
            p_value="NA"
        else:
            fdr=str(fdr_list[index])
            p_value=str(pvalue_list[index])

        if SF_regulation_dict[splicing_factor]=="NA":
            if up_evidence>dn_evidence:
                predicted_direction="predicted:up"
            elif dn_evidence>up_evidence:
                predicted_direction="predicted:dn"
            else:
                predicted_direction="NA"

        elif SF_regulation_dict[splicing_factor]=="-":
            predicted_direction="known:dn"
        elif SF_regulation_dict[splicing_factor]=="+":
            predicted_direction="known:up"
        elif SF_regulation_dict[splicing_factor]=="NC":
            #pvalue="NA,not tested"
            predicted_direction="no prediction Made"
        else:
            print "unexpected"
            pass
        outfile_obj.handle.write(p_value+'\t'+fdr+'\t'+predicted_direction+'\t')
        if predicted_direction[-2:]!="dn":
            outfile_obj.handle.write(str(upup)+'\t'+str(updn)+'\t'+str(dnup)+'\t'+str(dndn)+'\n')
        else:
            outfile_obj.handle.write(str(updn)+'\t'+str(upup)+'\t'+str(dndn)+'\t'+str(dnup)+'\n')
    ##Setup output file
    outfile_obj.handle.close()

    ## Remove intermediate file
    if DELETE_INTERMEDIATE!=0:
        ## remove BED
        if input_type!="BED":
            rm_bed_cmd = "rm "+ BED_intermediate_file
            os.system(rm_bed_cmd)
        ## remove intermediate
        rm_intersect_cmd = "rm "+ intersect_outfile_name
        os.system(rm_intersect_cmd)





if __name__ == "__main__":
    ###Python General Module Import 
    import sys, csv, getopt, re
    import os
    import math
    from itertools import ifilter
    
    ##Liye own common function,class loading
    from constant import *
    from general_functions import *
    from general_class import *  ###
    #from Sequencing_Library import *
    
    OUTPUT_SEP_CHAR='\t'
    
    
            
                 
    #exit if not enough arguments
    if len(sys.argv) < 3:
        print __doc__
        sys.exit(0)
    
    ###set default value
    infile=None
    infile_skip=0
    sep_char='\t'
    sep_gene=','
    unique_id_length=2
    reference=None
    compare_direction=1
    INPUT_PATH=os.getcwd()
    OUTPUT_PATH=os.getcwd()
    DELETE_INTERMEDIATE = 1
    OUTPUT_SUFFIX="txt"
    
    MIN_OVERLAP =0.99
    SF_level_infile =None
    input_type="MISO"
    generate_exp_matrix_ref=None

    ## MISO format related
    BAYES_MIN = 10.00

    ## MATS format Constant
    MATS_STRAND_COLUMN = 3
    MATS_CHRO_COLUMN = 2
    MATS_START_COLUMN = 4
    MATS_END_COLUMN = 5
    MATS_CHANGE_COLUMN = 20
    MATS_FDR_COLUMN = 17
    FDR_MAX = 0.05
    ###get arguments(parameters)
    optlist, cmd_list = getopt.getopt(sys.argv[1:], 'hi:c:r:g:e:d:f:F:D:j:I:t:p:L:o:O:z')
    for opt in optlist:
        if opt[0] == '-h':
            print __doc__; sys.exit(0)
        elif opt[0] == '-i': infile = opt[1]
        elif opt[0] == '-I': INPUT_PATH = opt[1]
        elif opt[0] == '-O': OUTPUT_PATH = opt[1]
        elif opt[0] == '-c': compare_direction = int(opt[1])
        elif opt[0] == '-t': input_type =opt[1]
        elif opt[0] == '-g': generate_exp_matrix_ref = opt[1]
        elif opt[0] == '-D': DELETE_INTERMEDIATE = int(opt[1])
        elif opt[0] == '-f': BAYES_MIN= float(opt[1])
        elif opt[0] == '-F': FDR_MAX = float(opt[1])
        elif opt[0] == '-r': reference = opt[1]
        elif opt[0] == '-e': SF_level_infile = opt[1]  
        elif opt[0] == '-o': MIN_OVERLAP = float(opt[1])
        elif opt[0] == '-L': unique_id_length = int(opt[1])
    
    if generate_exp_matrix_ref==None:
    
        if infile!=None and reference!=None:
            predict_splicing_factor(infile,reference,SF_level_infile,input_type,compare_direction)
    
    else:
        ## generate expression matrix
        infile_obj=GeneralFile_class(generate_exp_matrix_ref)  
        infile_reader=infile_obj.reader_gen()
        outfile_name=infile_obj.outputfilename_gen("feedin_regulation_matrix","txt") ##create output file
        outfile_path=OUTPUT_PATH+"/"+outfile_name
        outfile_obj=GeneralFile_class(outfile_path)              ##create output obj                           
        outfile_obj.output_handle_gen() 
        outfile_obj.handle.write("#SplicingFactor\tRegulation\n")
        factor_list = []
        for row in infile_reader:
            ID= row[3] #ID
            ID_info = (ID.split(":"))[3] 
            ID_info_list= ID_info.split(".")
            ID_info_final = (ID_info_list[0]).upper()
            factor_list.append(ID_info_final)
        unique_set = set(factor_list) 
        unique_list = list(unique_set)
        for factor in unique_list:   
            outfile_obj.handle.write(factor+'\tNA\n')
        outfile_obj.handle.close()

        print "done generated regulation matrix to feedin"

    
