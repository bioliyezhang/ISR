#!/usr/bin/env python

'''
Version: 2015.3.19
=====================
Updated logs 2015.3.19
1. include the parse parameter files (standard)
'''

import os
import csv
from itertools import ifilter
import sys
import math

from general_class import *
from constant import *
#print "General library Loaded"

## common function documents
def parse_parameters(par_file): 
    dict_param = dict([(l.split("=")[0].strip(), l.split("#")[0].split("=")[1].strip()) for l in par_file.readlines() if "=" in l and l.strip()[0]!="#"])
    return dict_param

def convertInput2Boolean(input_boolean):
    if input_boolean==True or input_boolean==False:
        result=input_boolean
    else:
        result= input_boolean in TRUE_BOOLEAN_LIST
    return result

def checkParameter(param,key,dType,allowed=[],checkFile=False,optional=False):
    #generic function that checks if a parameter was in the parameter file, casts to the right data type and if the parameter is a file/ directory checks if it actually exists

    if optional and key not in param:
        param[key]=''
    else:
        #check if key is present
        if key not in param: print 'Parameter '+key+' is missing in the parameter file.'; sys.exit(0)

        #cast to correct data type
        if dType == bool:
            param[key] = param[key] in ['True','TRUE','true','T','1']
        else:
            param[key]=dType(param[key])

        #check if the value for the key is allowed
        if len(allowed)>0 and param[key] not in allowed:
            print 'Parameter '+key+' can only be one of the following: '+allowed; sys.exit(0)
    
        #if file or directory check if it exists
        if checkFile and not os.path.exists(param[key]):
            print 'The file in '+key+' = ',param[key],' does not exist'; sys.exit(0)

def checkInput(item,dType,allowed=[],checkFile=False,optional=False):
    #generic function that checks if a parameter was in the parameter file, casts to the right data type and if the parameter is a file/ directory checks if it actually exists

    if optional:
        return item
    else:
        #cast to correct data type
        if dType == bool:
            item = item in ['True','TRUE','true','T','1',True]
        else:
            item = dType(item)

        #check if the value for the key is allowed
        if len(allowed)>0 and param[key] not in allowed:
            print 'Input can only be one of the following: '+allowed; sys.exit(0)
    
        #if file or directory check if it exists
        if checkFile and not os.path.exists(item):
            print 'The file  ',item,' does not exist'; sys.exit(0)
        return item

def list2string(input_list,sep_char=";"):
    if len(input_list)>0:
        result=str(input_list[0])
        for item in input_list[1:]:
            result=result+sep_char+str(item)
    else:
        result=""
    return result

def CurrentFolder_to_Infiles(CurrentFolder=os.getcwd(), suffix=""):
    """
    getting all the files with certain suffix
    """
    
    #debug
    #print "function exerted"
    tmp_result, result = [], []
    def checkSuffix(f):
        return f.endswith(suffix) and os.path.isfile(CurrentFolder+'/'+f)

    #CurrentFolder=os.getcwd()
    folder_level=0
    for dirpath, dirname, filename in os.walk(CurrentFolder):
        folder_level+=1
        #the os.walk will go into the all the folders and even daughter folders
        #and therefore make sure you are using it correctly
        #otherwise the correct value will be replaced by others
        #even if there are mutiple ones, the first one is the route number
        if folder_level==1:
            tmp_result = filename
        else:
            pass
            
    
    if suffix != "":
        for filename in tmp_result:
            if checkSuffix(filename)==True:
                result.append(CurrentFolder+"/"+filename)
    else:
        for filename in tmp_result:
            result.append(CurrentFolder+"/"+filename)
            
    return result

def extract_files_with_suffix_from_path_to_full_path(CurrentFolder=os.getcwd(), suffix=""):
    """
    getting all the files with certain suffix
    """
    
    #debug
    #print "function exerted"
    tmp_result, result = [], []
    def checkSuffix(f):
        return f.endswith(suffix) and os.path.isfile(CurrentFolder+'/'+f)

    #CurrentFolder=os.getcwd()
    folder_level=0
    for dirpath, dirname, filename in os.walk(CurrentFolder):
        folder_level+=1
        #the os.walk will go into the all the folders and even daughter folders
        #and therefore make sure you are using it correctly
        #otherwise the correct value will be replaced by others
        #even if there are mutiple ones, the first one is the route number
        if folder_level==1:
            tmp_result = filename
        else:
            pass
            
    
    if suffix != "":
        for filename in tmp_result:
            if checkSuffix(filename)==True:
                result.append(CurrentFolder+'/'+filename)
        
        return result
    else:
        return tmp_result
    
def outfile_name(infile,name_fragment,suffix="txt"):
    ##combined version for output file name
    #suffix=get_suffix(infile)
    #suffix=switchsuffix(suffix)
    #suffix='txt'
    new_suffix=name_fragment+suffix
    return outfile_generator(infile,new_suffix)


def switchsuffix(suffix):
    #generate switching suffix for output file
    if suffix=="tab" or suffix==".tab":
        return "txt"
    else:
        return "tab"
    
def get_suffix(infile):
    #retrieve suffix from a file
    pos=infile.find(".")
    suffix=infile[pos+1:]
    return suffix
        
def outfile_generator(infile,suffix):
    #generate the output file name
    pos=infile.find(".")
    output_header=infile[:pos]
    outfile=output_header+suffix
    return outfile

def skip_header(reader,skip):
    #skip header 
    for i in range(skip):
        reader.next()

def output_header_file(infile,skip,output_handle,sup_list=[],eliminate=0):
    ##Version1.0
    ##write header into files
    reader=csv.reader(open(infile,"rU"),delimiter="\t")
    for i in xrange(skip):
        if len(sup_list)!=0:
            initial_rows=reader.next()
            rows=initial_rows+sup_list
        else:
            rows=reader.next()
    if skip==0:
        pass
    else:
        output_row(output_handle,rows,eliminate)
    
def output_row(handle,row,eliminate=0,sep_char="\t"):
    ##write row into files
    len_row=len(row)-eliminate
    for i in xrange(len_row):
        if i==(len_row-1):
            handle.write(str(row[i])+'\n')
        else:
            handle.write(str(row[i])+sep_char)

def test_header_vcf(row):
    first_item = row[0]
    if first_item[0] != "#":
        return True
    else:
        return False

def convert_chro_format(chro,with_string=True):
    if chro.count("chr")==1:
        if with_string:
            pass
        else:
            chro=chro[3:]
    else:
        if with_string:
            chro="chr"+chro
        else:
            pass
    return chro

def varscan2vcf(rows,filter_result):
    chro=rows[0]
    coor=rows[1]
    ref=rows[2]
    ref_read_count = rows[4]
    alt_read_count = rows[5]
    seq_depth = int(ref_read_count) + int(alt_read_count)
    alt_freq = rows[6]
    alt_strand_count = rows[8]
    ref_base_qual = rows[9]
    alt_base_qual = rows[10]
    p_value = float(rows[11])
    #print "p value is ",p_value
    alt_f_count = rows[16]
    alt_r_count = rows[17]
    alt=rows[18]
    if alt[0]=='+':
        alt=ref+alt[1:]
    elif alt[0]=='-':
        ref_ori=ref
        ref=ref+alt[1:]
        alt=ref_ori
    else:
        pass
    ##info format is AF:Ref_Ave_Qual:Alt_Ave_Qual:AS_count
    info_output = "AF="+ alt_freq + ";" + "Ref_Ave_Qual=" + ref_base_qual \
    +";Alt_Ave_Qual="+ alt_base_qual + ";Alt_Strand_Count=" + alt_strand_count \
    +";Alt_F_Count=" + alt_f_count +";Alt_R_Count=" + alt_r_count
    format_ID ="GT:AD:DP"
    
    alt_freq_number = float(alt_freq[:-1])
    if alt_freq_number > 50 :
        GT="1/1"
    else:
        GT="0/1"
    format_output = GT +":"+ ref_read_count + ','+ alt_read_count + ":" + str(seq_depth)
    
    vcf_row=[]
    vcf_row.append(chro)
    vcf_row.append(coor)
    vcf_row.append(".")
    vcf_row.append(ref)
    vcf_row.append(alt)
    
    if p_value ==0:
        quality_score =100
    else:
        quality_score = int (math.log(p_value,10) * (-10))
        
    vcf_row.append(str(quality_score))
    vcf_row.append(filter_result)
    vcf_row.append(info_output)
    vcf_row.append(format_ID)
    vcf_row.append(format_output)
    return vcf_row

def varscan2vcf_old(rows,filter_result):
    chro=rows[0]
    coor=rows[1]
    ref=rows[2]
    ref_read_count = rows[4]
    alt_read_count = rows[5]
    seq_depth = int(ref_read_count) + int(alt_read_count)
    alt_freq = rows[6]
    alt_strand_count = rows[8]
    ref_base_qual = rows[9]
    alt_base_qual = rows[10]
    p_value = float(rows[11])
    #print "p value is ",p_value
    alt_f_count = rows[16]
    alt_r_count = rows[17]
    alt=rows[18]
    if alt[0]=='+':
        alt=ref+alt[1:]
    elif alt[0]=='-':
        ref_ori=ref
        ref=ref+alt[1:]
        alt=ref_ori
    else:
        pass
    ##info format is AF:Ref_Ave_Qual:Alt_Ave_Qual:AS_count
    info_output = "AF="+ alt_freq + ";" + "Ref_Ave_Qual=" + ref_base_qual \
    +";Alt_Ave_Qual="+ alt_base_qual + ";Alt_Strand_Count=" + alt_strand_count \
    +";Alt_F_Count=" + alt_f_count +";Alt_R_Count=" + alt_r_count
    format_ID ="GT:AD:DP"
    
    alt_freq_number = float(alt_freq[:-1])
    if alt_freq_number > 50 :
        GT="1/1"
    else:
        GT="0/1"
    format_output = GT +":"+ ref_read_count + ','+ alt_read_count + ":" + str(seq_depth)
    
    vcf_row=[]
    vcf_row.append(chro)
    vcf_row.append(coor)
    vcf_row.append(".")
    vcf_row.append(ref)
    vcf_row.append(alt)
    
    if p_value ==0:
        quality_score =100
    else:
        quality_score = int (math.log(p_value,10) * (-10))
        
    vcf_row.append(str(quality_score))
    vcf_row.append(filter_result)
    vcf_row.append(info_output)
    vcf_row.append(format_ID)
    vcf_row.append(format_output)
    return vcf_row

def generate_next_step_folder(prefix,value=1):
        current_folder=os.getcwd()
        current_folder_list=current_folder.split('/')
        path_len=len(current_folder_list)
        current_path=""
        for i in range(path_len-1):
            current_path=current_path+current_folder_list[i]+"/"    
        step_folder=current_folder_list[-1]
        step_folder_list=step_folder.split('-')
        if value==1:
            current_step=int(step_folder_list[0])+1
        else:
            current_step=step_folder_list[0]+".5"
        next_step_folder_name=str(current_step)+'-'+prefix
        next_step_folder=current_path+next_step_folder_name
        #next_step_folder_max = next_step_folder +'/' +"max"
        #next_step_folder_average = next_step_folder +'/' +"average"
        if os.path.exists(next_step_folder)==False:
            #os.mkdir(ori_path,0770)
            os.mkdir(next_step_folder)
        '''
        if os.path.exists(next_step_folder_max)==False:
            #os.mkdir(ori_path,0770)
            os.mkdir(next_step_folder_max)
        if os.path.exists(next_step_folder_average)==False:
            #os.mkdir(ori_path,0770)
            os.mkdir(next_step_folder_average)
        '''
        print "[Step1]output folder created succesfully"
        return next_step_folder
    
def generate_subfolder(prefix):
    current_path=os.getcwd()
    subfolder_path=current_path+"/"+prefix
    if os.path.exists(subfolder_path)==False:
        os.mkdir(subfolder_path)
    
def mk_folder(subfolder_name):
        mk_path="./%s"%(subfolder_name)
        if os.path.exists(mk_path)==False:
                os.mkdir(mk_path,0770)

def mk_folder_fullpath(folder_path):
        
        if os.path.exists(folder_path)==False:
                os.mkdir(folder_path,0770)

def output_header(reader,skip,outfile_handle):
        for i in range(skip):
                rows=reader.next()
                output_row(outfile_handle,rows)

def filter_column_min_max(infile,skip,COLUMN,MIN,MAX,subfolder,abs_value,ID_LENGTH):
    '''
    develped 2011-05-24
    updated 2011-05-28
    Updated 2012-01-16
    add header to output files
    '''
    if MIN==None:
        MIN_name=0
    else:
        MIN_name=MIN
        
    if MAX==None:
        MAX_name=0
    else:
        MAX_name=MAX
    
    #read infile
    infile_handle=open(infile,'r')
    infile_reader=csv.reader(infile_handle,delimiter='\t')

    #filter file
    suffix_output=str(int(MIN_name))+"_"+str(int(MAX_name))+"_WC_filtered.txt"
    #outfile=outfile_generator(infile,suffix_output)
    final_prefix=""
    infile_obj=GeneralFile_class(infile)
    infile_obj.SAMPLE_ID_LEN=ID_LENGTH
    outfile_name=infile_obj.outputfilename_gen(final_prefix,"txt")
    
    outfile="./%s/%s"%(subfolder,outfile_name)
    outfile_handle=open(outfile,'w')

    #folder_stat
    stat_sum_outfile="folder_%2.1f_%2.2f.sum"%(MIN_name,MAX_name)

    stat_sum_outfile="./%s/%s"%(subfolder,stat_sum_outfile)
    stat_sum_handle=open(stat_sum_outfile,'a')

    ##Skip header lines
    ##skip_header(infile_reader,skip)

    ###write header into output files
    output_header(infile_reader,skip,outfile_handle)

    #filter the column according to filter
    filter_total=0
    if abs_value==0:
        for rows in infile_reader:
            value=rows[COLUMN]
            if value=="":
                output_row(outfile_handle,rows)
                filter_total+=1
            else:
                
                try:
                    value=float(value)
                    
                    if MAX==None and MIN!=None:
                        if value>=MIN:
                            filter_total+=1
                            #write to the file if value passes the filtering
                            output_row(outfile_handle,rows)
                    elif MIN==None and MAX!=None:
                        if value<=MAX:
                            filter_total+=1
                            #write to the file if value passes the filtering
                            output_row(outfile_handle,rows)
                            
                    elif MIN!=None and MAX!=None:
                        
                        if value>=MIN and value<=MAX:
                            filter_total+=1
                            #write to the file if value passes the filtering
                            output_row(outfile_handle,rows)
                    else:
                        filter_total+=1
                        #write to the file if value passes the filtering
                        output_row(outfile_handle,rows)
                        
                except:
                    pass
    else:
        for rows in infile_reader:
            value=rows[COLUMN]
            if value=="":
                output_row(outfile_handle,rows)
                filter_total+=1
            else:
                
                try:
                    value=float(value)
                    value=abs(value)
                    if MAX==None and MIN!=None:
                        if value>=MIN:
                            filter_total+=1
                            #write to the file if value passes the filtering
                            output_row(outfile_handle,rows)
                    elif MIN==None and MAX!=None:
                        if value<=MAX:
                            filter_total+=1
                            #write to the file if value passes the filtering
                            output_row(outfile_handle,rows)
                            
                    elif MIN!=None and MAX!=None:
                        
                        if value>=MIN and value<=MAX:
                            filter_total+=1
                            #write to the file if value passes the filtering
                            output_row(outfile_handle,rows)
                    else:
                        filter_total+=1
                        #write to the file if value passes the filtering
                        output_row(outfile_handle,rows)
                        
                except:
                    pass
        

        outfile_handle.close()
        #outfile_stat_handle.write("total_passed_peak_pair\t"+str(filter_total))
        #outfile_stat_handle.close()
        stat_sum_handle.write("infile %s total_passed_peak_pair\t"%(infile)+str(filter_total)+'\n')
        stat_sum_handle.close()

def generate_paired_files_old(infiles_combine,identifier1,identifier2,target=2):
    ##the requirement of this function is that both files have the same sample id location
    ##which is the first position separated by the "_"
    
    ##The target =2 means that as long as files include identifier 2, it will be considered as group 2
    ##the rest will be considered as group 1
    ##The target =1 means that as long as files include identifier 1, it will be considered as group 2
    ##the rest will be considered as group 2


    id_list=[]
    infiles=[]
    paired_dict=dict()
    for infile in infiles_combine:
        infile_name_list=infile.split('_')
        infile_id=infile_name_list[0]
        if infile_id not in id_list:
            paired_dict[infile_id]=["",""]
            id_list.append(infile_id)
        else:
            pass
    
    if target==2:
        identifier=identifier2
    elif target==1:
        identifier=identifier1
    else:
        print "Error:Wrong Identifier input"
        sys.exit()
    
    for infile in infiles_combine:
        infile_name_list=infile.split('_')
        infile_id=infile_name_list[0]
        #print "identifier2, infile and find result: ", identifier2, infile, infile.find(identifier2)
        if infile.find(identifier)>0:
            paired_dict[infile_id][1]=infile
            
        else:
            paired_dict[infile_id][0]=infile
    for id_item in id_list:
        infiles.append((paired_dict[id_item][0],paired_dict[id_item][1]))
        print "Pair1 and Pair 2 is", paired_dict[id_item][0], paired_dict[id_item][1]
    return infiles

def generate_paired_files(infiles_combine,identifier1,identifier2,target=2,unique_ID_length=2,file_name_sep_char="_"):
    ##the requirement of this function is that both files have the same sample id location
    ##which is the first position separated by the "_"
    
    ##The target =2 means that as long as files include identifier 2, it will be considered as group 2
    ##the rest will be considered as group 1
    ##The target =1 means that as long as files include identifier 1, it will be considered as group 2
    ##the rest will be considered as group 2


    id_list=[]
    infiles=[]
    paired_dict=dict()
    for infile in infiles_combine:
        infile_name_list=infile.split(file_name_sep_char)
        
        for index in range(unique_ID_length):
            if index == 0:
                infile_id=infile_name_list[index]
            else:
                infile_id=infile_id+file_name_sep_char+infile_name_list[index]
            
        if infile_id not in id_list:
            paired_dict[infile_id]=["",""]
            id_list.append(infile_id)
        else:
            pass
    
    if target==2:
        identifier=identifier2
    elif target==1:
        identifier=identifier1
    else:
        print "Error:Wrong Identifier input"
        sys.exit()
    
    for infile in infiles_combine:
        infile_name_list=infile.split(file_name_sep_char)
        for index in range(unique_ID_length):
            if index == 0:
                infile_id=infile_name_list[index]
            else:
                infile_id=infile_id+file_name_sep_char+infile_name_list[index]
        #print "identifier2, infile and find result: ", identifier2, infile, infile.find(identifier2)
        if infile.find(identifier)>0:
            paired_dict[infile_id][1]=infile
            
        else:
            paired_dict[infile_id][0]=infile
    for id_item in id_list:
        infiles.append((paired_dict[id_item][0],paired_dict[id_item][1]))
        print "Pair1 and Pair 2 is", paired_dict[id_item][0], paired_dict[id_item][1]
    return infiles

def generate_paired_files_by_ID(infiles_combine,unique_ID_length,vcf_suffix="vcf",bam_suffix="bam",sep_char="_",UNPAIRED_STOP=False):
    ## this script will pair input files based on equal unique_ID_length
    ## Version update, provide flexible pairing for the 2 file case
    
    paired_list=list()
    
    
    if len(infiles_combine)==2:
        ##quick function
        vcf_infile=""
        bam_infile=""
        for infile in infiles_combine:
            
            if infile.endswith(vcf_suffix):
                vcf_infile=infile
            elif infile.endswith(bam_suffix):
                bam_infile=infile
            else:
                print "[ERROR] unsupported file suffix"
                print "Please check your input file"
                sys.exit(0)
        if vcf_infile!="" and bam_infile!="":
            result_list=[vcf_infile,bam_infile]
            paired_list.append(result_list)
            return paired_list
        else:
            
            print "[ERROR] not enough input, input files are missing"
            print "Please check your input file"
            sys.exit(0) 
        
    else:
        data_dict=dict()
        for infile in infiles_combine:
            if infile.count("/")>0:
                infile_temp=infile.split("/")
                infile_info=infile_temp[-1]
            else:
                infile_info=infile
            infile_list=infile_info.split(sep_char)
            for i in range(unique_ID_length):
                if i==0:
                    unique_ID=infile_list[i]
                else:
                    unique_ID=unique_ID+"_"+infile_list[i]
            data_dict[unique_ID]=[]
            
        for infile in infiles_combine:
            if infile.count("/")>0:
                infile_temp=infile.split("/")
                infile_info=infile_temp[-1]
            else:
                infile_info=infile
            infile_list=infile_info.split(sep_char)
            for i in range(unique_ID_length):
                if i==0:
                    unique_ID=infile_list[i]
                else:
                    unique_ID=unique_ID+"_"+infile_list[i]
            data_dict[unique_ID].append(infile)
        
        data_list=data_dict.keys()
        for data_pair in data_list:
            if len(data_dict[data_pair])!=2:
                if UNPAIRED_STOP:
                    print "incorrect data_pair id is", data_pair 
                    print "Incorrect pairing, Please check your input"
                    sys.exit(0)
            else:
                data1,data2=data_dict[data_pair]
                if data1.count(bam_suffix)>=1 and data2.endswith(vcf_suffix):
                    ordered_list=[data2,data1]
                elif data1.endswith(vcf_suffix) and data2.count(bam_suffix)>=1:
                    ordered_list=[data1,data2]
                else:
                    print "incorrect pairing, Please check your input"
                    sys.exit(0)
                paired_list.append(ordered_list)
    ## first item is the vcf file and second is bam file
    return paired_list
            
            
        

def set_database_path():
    ##version1.0
    ##Home Lenovo Destop
    try:
        Lib_PATH="E:\Dropbox\protocol\database\human_genome"
        sys.path.append(Lib_PATH)
    except:
        pass
    
def output_row_sup_list(handle,row,sup_list,sep_char='\t'):
        len_row=len(row)
        if len(sup_list)>0:
            for i in range(len_row):
                handle.write(row[i]+'\t')
        else:
            for i in range(len_row-1):
                handle.write(row[i]+'\t')
            handle.write(row[i+1]+'\n')
        len_list=len(sup_list)
        for i in range(len_list):
            if i==(len_list-1):
                handle.write(str(sup_list[i])+'\n')
            else:
                handle.write(str(sup_list[i])+sep_char)

def Compile_population_to_one(infiles,GENE_COLUMN):
    ##SECTION I: OUTPUT SETUP
    ##output data name
    output_name="compiled_data.txt"
    ##generate the general file object
    outfile_obj=GeneralFile_class(output_name)
    ##Set up file handle and write header
    outfile_obj.output_handle_gen(infiles[0],os.getcwd(),["SAMPLE_ID"])
    outfile_handle=outfile_obj.handle
    
    ##SECTION II:PROCESS OUTPUT
    for infile in infiles:
        ##Report Progress
        print "Start to process infile,",infile
        ##generate the general file object
        infile_obj=GeneralFile_class(infile)
        ##generate the reader for input file
        infile_reader=infile_obj.reader_gen()
        ##generate the sample ID
        sample_ID=infile_obj.sampleID_gen()
        for rows in infile_reader:
            if rows[GENE_COLUMN]!='.':
                output_row_sup_list(outfile_handle,rows,[sample_ID])
        ##Report Progress
        print "Finish processing infile,",infile
    outfile_handle.close()
        
def Compile_genelist_to_one(infiles,GENE_COLUMN):
    
    ##INITILIZE
    sample_number=len(infiles)
    
    ##SECTION I: OUTPUT SETUP FOR GENE LIST 
    ##output data name
    output_name="compiled_genelist.txt"
    ##generate the general file object
    outfile_obj=GeneralFile_class(output_name)
    ##Set up file handle and write header
    outfile_obj.output_handle_gen()
    outfile_handle=outfile_obj.handle
    outfile_handle.write("GENE"+'\t'+"SAMPLE(S)"+'\n')
    
    ##SECTION I: OUTPUT SETUP FOR GENE FREQUENCT AMONG POPULATION STATISTICS 
    ##output data name
    output_stat_name="gene_freq_stat.txt"
    ##generate the general file object
    outfile_stat_obj=GeneralFile_class(output_stat_name)
    ##Set up file handle and write header
    outfile_stat_obj.output_handle_gen()
    outfile_stat_handle=outfile_stat_obj.handle
    outfile_stat_handle.write("Count_Type"+'\t')
    outfile_stat_handle.write("1")
    for i in range(1,sample_number):
        outfile_stat_handle.write('\t'+str(i+1))
    outfile_stat_handle.write("\n")
    
    ##SECTION I: OUTPUT SETUP FOR GENE COUNT PER SAMPLE 
    ##output data name
    count_stat_name="gene_count_stat.txt"
    ##generate the general file object
    outfile_count_obj=GeneralFile_class(count_stat_name)
    ##Set up file handle and write header
    outfile_count_obj.output_handle_gen()
    outfile_count_handle=outfile_count_obj.handle
    outfile_count_handle.write("SAMPLE_ID"+'\t'+"GENE_COUNT"+'\n')
    
    ##SECTION II:PROCESS OUTPUT INITIALIZE THE DICTIONARY
    genelist_dict=dict()
    for infile in infiles:
        
        ##generate the general file object
        infile_obj=GeneralFile_class(infile)
        ##generate the reader for input file
        infile_reader=infile_obj.reader_gen()
        for rows in infile_reader:
            gene=rows[GENE_COLUMN]
            if gene=='.':
                pass
            else:
                genelist_dict[gene]=[]
    
    
    ##SECTION III:PROCESS DATA INTO DICTIONARY 
    for infile in infiles:
        sample_gene_count=0
        ##generate the general file object
        infile_obj=GeneralFile_class(infile)
        ##generate the reader for input file
        infile_reader=infile_obj.reader_gen()
        ##generate the sample ID
        sample_ID=infile_obj.sampleID_gen()
        for rows in infile_reader:
            gene=rows[GENE_COLUMN]
            if gene=='.':
                pass
            else:
                genelist_dict[gene].append(sample_ID)
                sample_gene_count+=1
        outfile_count_handle.write(sample_ID+'\t'+str(sample_gene_count)+'\n')
    outfile_count_handle.close()
            
    ##SECTION III:OUTPUT DATA INTO FILES
    sample_freq_list=[0]*sample_number
    genelist=genelist_dict.keys()
    gene_number=len(genelist)
    for gene in genelist:
        samples=genelist_dict[gene]
        samples_output=""
        samples_number_per_gene=len(samples)
        #print samples_number_per_gene
        sample_freq_list[samples_number_per_gene-1]+=1
        for sample in samples:
            samples_output=samples_output+sample+';'
        outfile_handle.write(gene+'\t'+samples_output+'\n')
    
    ##SECTION IV:OUTPUT GENE FREQUENCY AMONG POPULATION STATISTICS
    outfile_stat_handle.write("Count"+'\t')
    outfile_stat_handle.write(str(sample_freq_list[0]))
    for i in range(1,sample_number):
        outfile_stat_handle.write('\t'+str(sample_freq_list[i]))
    outfile_stat_handle.write("\n")
    ##Output Percentage
    outfile_stat_handle.write("Percentage"+'\t')
    outfile_stat_handle.write(str(round(float(sample_freq_list[0])*100.00/gene_number,2)))
    for i in range(1,sample_number):
        outfile_stat_handle.write('\t'+str(round(float(sample_freq_list[i])*100.00/gene_number,2)))
    outfile_stat_handle.write("\n") 
        
    outfile_handle.close()

def reverse_complementary(base_pairs):
    convert_dict=dict()
    convert_dict["A"]="T"
    convert_dict["T"]="A"
    convert_dict["C"]="G"
    convert_dict["G"]="C"
    convert_dict["I"]="I"
    convert_dict["D"]="D"
    convert_dict["N"]="N"
    new_base_pairs=""
    reverse_complement_sequence=""
    for nt in base_pairs:
        new_base_pairs+=convert_dict[nt]
    seq_length=len(base_pairs)
    for i in range(seq_length-1,-1,-1):
        reverse_complement_sequence+=new_base_pairs[i]
    return reverse_complement_sequence

def freq_y_axis_gen(data_list,x_list):
    ##version 0.1 the value must match exactly
    y_list=[]
    total_count=len(data_list)
    for x in x_list:
        y=data_list.count(x)
        y_percentage=round((100.00 * y / total_count),1)
        y_list.append(y_percentage)
    return y_list
        
def freq_y_axis_gen_v2(data_list,x_list):
    ##version 2, this will output the raw data as well
    y_list=[]
    y_raw_list=[]
    total_count=len(data_list)
    for x in x_list:
        y=data_list.count(x)
        y_raw_list.append(y)
        y_percentage=round((100.00 * y / total_count),1)
        y_list.append(y_percentage)
    return y_list,y_raw_list

def generate_unique_id_from_snv(data_list):
    chro=data_list[0]
    coor=data_list[1]
    ref=data_list[3]
    alt=data_list[4]
    combined_id=chro+"_"+coor+"_"+ref+"_"+alt
    return combined_id
    

def read_fasta_degenerate(fasta_file,detect_Blank_line_mode=True,removeN=True,simple_ID=False,convert_degenerate=True):
    """
    this function read fasta files and be able to convert the 
    degenerated sequences to certain 
    """
    fasta_dict=dict()
    infile_obj=GeneralFile_class(fasta_file)
    infile_obj.SKIP_HEADER=0
    infile_reader=infile_obj.reader_gen()
    Blank_line_mode=False
    if detect_Blank_line_mode==True:
        blank_line_count=0
        for row in infile_reader:
            if len(row)==0:
                blank_line_count+=1
        if blank_line_count>1:
            Blank_line_mode=True
    
    
    infile_obj=GeneralFile_class(fasta_file)
    infile_obj.SKIP_HEADER=0
    infile_reader=infile_obj.reader_gen()
    
    line_count=0
    for row in infile_reader:
        line_count+=1
        if Blank_line_mode:
            if len(row)==0:
                if removeN==True and fasta_seq.count("N")>0:
                    pass
                else:
                    fasta_dict[fasta_ID]=fasta_seq
                
            else:
                if row[0][0]==">":
                    
                    fasta_ID=row[0][1:]
                    if simple_ID==True:
                        tmp_list = fasta_ID.split(" ")
                        fasta_ID = tmp_list[0]

                    fasta_seq=""
                else:
                    current_seq=row[0].upper()
                    final_seq = ""

                    for index in range(len(current_seq)):
                        nt = current_seq[index]
                        if convert_degenerate:

                            replace_nt = nt_degenerate_dict[nt][0]
                            final_seq=final_seq+replace_nt
                        else:
                            final_seq=final_seq+nt
                    
                    fasta_seq=fasta_seq+final_seq

        else:
            try:
                if row[0][0]==">":
                    if line_count!=1 and fasta_seq!="NA":
                        if removeN==True and fasta_seq.count("N")>0:
                            pass
                        else:
                            fasta_dict[fasta_ID]=fasta_seq
                    fasta_ID=row[0][1:]
                    if simple_ID==True:
                        tmp_list = fasta_ID.split(" ")
                        fasta_ID = tmp_list[0]
                    fasta_seq=""
                else:   
                    current_seq=row[0].upper()
                    final_seq = ""

                    for index in range(len(current_seq)):
                        nt = current_seq[index]
                        if convert_degenerate:

                            replace_nt = nt_degenerate_dict[nt][0]
                            final_seq=final_seq+replace_nt
                        else:
                            final_seq=final_seq+nt
                    if len(current_seq)!=0:
                        fasta_seq=fasta_seq+final_seq
                        
            except:
                fasta_seq="NA"
    
    if Blank_line_mode:
        pass
    else:
        fasta_dict[fasta_ID]=fasta_seq
        
    return fasta_dict

def read_fasta(fasta_file,detect_Blank_line_mode=True,removeN=True,simple_ID=False):
    '''
    version:1.0
    this function have additional option to change sequence IDs
    '''
    ## Commonly used function
    ## Now can handle two types of fasta files
    fasta_dict=dict()
    infile_obj=GeneralFile_class(fasta_file)
    infile_obj.SKIP_HEADER=0
    infile_reader=infile_obj.reader_gen()
    Blank_line_mode=False
    if detect_Blank_line_mode==True:
        blank_line_count=0
        for row in infile_reader:
            if len(row)==0:
                blank_line_count+=1
        if blank_line_count>1:
            Blank_line_mode=True
    
    
    infile_obj=GeneralFile_class(fasta_file)
    infile_obj.SKIP_HEADER=0
    infile_reader=infile_obj.reader_gen()
    
    line_count=0
    for row in infile_reader:
        line_count+=1
        if Blank_line_mode:
            if len(row)==0:
                if removeN==True and fasta_seq.count("N")>0:
                    pass
                else:
                    fasta_dict[fasta_ID]=fasta_seq
                
            else:
                if row[0][0]==">":
                    
                    fasta_ID=row[0][1:]
                    if simple_ID==True:
                        tmp_list = fasta_ID.split(" ")
                        fasta_ID = tmp_list[0]

                    fasta_seq=""
                else:
                    current_seq=row[0].upper()
                    fasta_seq=fasta_seq+current_seq
        else:
            try:
                if row[0][0]==">":
                    if line_count!=1 and fasta_seq!="NA":
                        if removeN==True and fasta_seq.count("N")>0:
                            pass
                        else:
                            fasta_dict[fasta_ID]=fasta_seq
                    fasta_ID=row[0][1:]
                    if simple_ID==True:
                        tmp_list = fasta_ID.split(" ")
                        fasta_ID = tmp_list[0]
                    fasta_seq=""
                else:   
                    current_seq=row[0].upper()
                    if len(current_seq)!=0:
                        fasta_seq=fasta_seq+current_seq
            except:
                fasta_seq="NA"
    
    if Blank_line_mode:
        pass
    else:
        fasta_dict[fasta_ID]=fasta_seq
        
    return fasta_dict

def read_fasta_original(fasta_file,detect_Blank_line_mode=True,removeN=True,keep_case=False):
    '''
    version 0.8
    
    '''
    ## Commonly used function
    ## Now can handle two types of fasta files
    fasta_dict=dict()
    infile_obj=GeneralFile_class(fasta_file)
    infile_obj.SKIP_HEADER=0
    infile_reader=infile_obj.reader_gen()
    Blank_line_mode=False
    if detect_Blank_line_mode==True:
        blank_line_count=0
        for row in infile_reader:
            if len(row)==0:
                blank_line_count+=1
        if blank_line_count>1:
            Blank_line_mode=True
    
    print Blank_line_mode 
    infile_obj=GeneralFile_class(fasta_file)
    infile_obj.SKIP_HEADER=0
    infile_reader=infile_obj.reader_gen()
    
    line_count=0
    for row in infile_reader:
        line_count+=1
        if Blank_line_mode:
            if len(row)==0:
                if removeN==True and fasta_seq.count("N")>0:
                    pass
                else:
                    fasta_dict[fasta_ID]=fasta_seq
                
            else:
                if row[0][0]==">":
                    
                    fasta_ID=row[0][1:]
                    fasta_seq=""
                else:
                    if keep_case==False:
                        current_seq=row[0].upper()
                    else:
                        current_seq=row[0]
                    fasta_seq=fasta_seq+current_seq
        else:
            try:
                if row[0][0]==">":
                    if line_count!=1 and fasta_seq!="NA":
                        if removeN==True and fasta_seq.count("N")>0:
                            pass
                        else:
                            fasta_dict[fasta_ID]=fasta_seq
                    fasta_ID=row[0][1:]
                    fasta_seq=""
                else:   
                    if keep_case==False:
                        current_seq=row[0].upper()
                    else:
                        current_seq=row[0]
                    if len(current_seq)!=0:
                        fasta_seq=fasta_seq+current_seq
            except:
                fasta_seq="NA"
    
    if Blank_line_mode:
        pass
    else:
        fasta_dict[fasta_ID]=fasta_seq
        
    return fasta_dict

def row_read(infile,column,skip):
    
    reader=csv.reader(open(infile,"rU"),delimiter="\t")
    skip_header(reader,skip)
    genelist=[]
    for rows in reader:
            ID=rows[column]
            genelist.append(ID)
        ##Future Development: \t replacement by general setup
    return genelist

def row_read_obj(infile_reader,column=0):
    genelist=[]
    for rows in infile_reader:
            ID=rows[column]
            genelist.append(ID)
        ##Future Development: \t replacement by general setup
    return genelist

def sum_column(infile,column):
    """
    this function sum up the value in one file
    """
    reader=csv.reader(open(infile, "rU"), delimiter = '\t')
    total=0
    for row in reader:
        try:
            total+=int(float(row[column]))
        except:
            print "Error"
    print infile,"done"
    return total

def filter_column_ID_v2(infiles,skip,COLUMN,ID_list,equal,sep_chr_infile):
    #Type: general script
    '''
    develped 2011-05-26
    This is a revised version, which is still under development.
    And this meant to deal with not exact matching of column    
    '''
    
    for infile in infiles:
        print "Processing", infile
        
        ##generate outfile name
        name_fragment="_filtered."
        outfile=outfile_name(infile,name_fragment)
        outfile_handle=open(outfile,'w')
            
        ##generate the header for outfile
        output_header_file(infile,skip,outfile_handle)
            
        ##Skip header for the processing
        infile_obj=GeneralFile_class(infile)
        #reader=csv.reader(open(infile,'rU'),delimiter=sep_chr_infile)
        #skip_header(reader,skip)
        reader=infile_obj.reader_gen()
    
    #filter the column according to ID_list
        for rows in reader:
            ID=rows[COLUMN]
            if equal==0:
                output=True
                for test_ID in ID_list:
                    if ID.count(test_ID)!=equal:
                        output=False
            elif equal==1:
                output=False
                for test_ID in ID_list:
                    if ID.count(test_ID)==equal:
                        output=True
            else:
                print "Method undefined"
                sys.exit(0)
            
            if output:
                output_row(outfile_handle,rows)
                
                
            
            ##Version1.0
            '''
            if (ID in ID_list)==equal:
                #write to the file if value passes the filtering
                output_row(outfile_handle,rows)
            '''
            ##Version2.0
            '''
            for filter_id in ID_list:
            if filter_id in ID:
                output_row(outfile_handle,rows)
                break
            '''         
    outfile_handle.close()

def smooth_data(data_list,moving_window):
    # input is a list with data
    # moving window indicates how many bins are smoothed
    # moving window should be odd number
    half_window=moving_window/2
    smoothed_list=[]
    list_len=len(data_list)
    for i in range(list_len):
        if i<half_window:
            tmp_sum=0
            for j in range(i,i+half_window+1):
                tmp_sum+=data_list[j]
            smoothed_value=float(tmp_sum)/moving_window
            smoothed_list.append(smoothed_value)
        elif i>=(list_len-half_window):
            tmp_sum=0
            for j in range(i,list_len-1):
                tmp_sum+=data_list[j]
            smoothed_value=float(tmp_sum)/moving_window
            smoothed_list.append(smoothed_value)
        else:
            tmp_sum=0
            for j in range(i-half_window,i+half_window+1):
                tmp_sum+=data_list[j]
            smoothed_value=float(tmp_sum)/moving_window
            smoothed_list.append(smoothed_value)
    return smoothed_list

def bin_smooth_data(infiles,start_data_column,end_data_column,bin_size,smooth_size,skip):

    len_data=end_data_column-start_data_column+1
    ID_column=0
    bin_len_data=len_data/bin_size
    
    #section I: process one input file each time
    for infile in infiles:

        print "Ordering the input file", infile
        #section II: initiate the output file
        name_fragment="_b"+str(bin_size)+"_s1."
        outfile_s1=outfile_name(infile,name_fragment)
        outfile_s1_handle=open(outfile_s1,'w')

        if smooth_size!=1:
            name_fragment="_b"+str(bin_size)+"_s"+str(smooth_size)+"."
            outfile=outfile_name(infile,name_fragment)
            outfile_handle=open(outfile,'w')

        #section III: process and generate the output
        #the header is included in the output file
        print "binning the data"
        reader=csv.reader(open(infile,'rU'),delimiter='\t')
        #reader=csv.reader(open(infile,'r'),delimiter='\t')
        skip_header(reader,skip)

        bin_data=dict()
        feature_ID_list=[]
        total_line=0
        
        for rows in reader:
            feature_ID=rows[ID_column]
            bin_data[feature_ID]=[]
            feature_ID_list.append(feature_ID)
            bin_count=0
            bin_total=0
            total_line+=1
            for i in range(start_data_column,end_data_column+1):
                bin_total+=float(rows[i])
                bin_count+=1
                if bin_count==bin_size:
                    if total_line==1:
                        bin_data[feature_ID].append(bin_total/bin_size)
                    else:    
                        bin_data[feature_ID].append(bin_total)
                    bin_count=0
                    bin_total=0

        #section III: smooth the data
        print "Generating output"
        
        if smooth_size==1:
            pass
            
        elif smooth_size>1:
            smooth_bin_data=dict()
            for feature_ID in feature_ID_list:
                smooth_list=smooth_data(bin_data[feature_ID],smooth_size)
                smooth_bin_data[feature_ID]=smooth_list
            output_dictionary_to_file(feature_ID_list,smooth_bin_data,bin_len_data,outfile_handle)

        #section IV: output the no smooth data
        output_dictionary_to_file(feature_ID_list,bin_data,bin_len_data,outfile_s1_handle)

def bin_smooth_data_vertical(infiles,start_data_column,end_data_column,bin_size,smooth_size,skip):
    
    for infile in infiles:
        ##Setup input file
        print "Processing infile:", infile
        infile_obj=GeneralFile_class(infile)
        infile_obj.SKIP_HEADER=0
        infile_reader=infile_obj.reader_gen()
        ROW_NUMBER=end_data_column-start_data_column+1
        
        #setup output file
        prefix="b_"+str(bin_size)+"_s_"+str(smooth_size)
        outfile_name=infile_obj.outputfilename_gen(prefix,"txt")
        outfile_obj=GeneralFile_class(outfile_name)
        outfile_obj.output_handle_gen()
        
        ##output the header
        for line in range(skip):
            row=infile_reader.next()
            output_list=row[start_data_column:end_data_column+1]
            output_row(outfile_obj.handle,output_list)
        
        ##initialize the data
        data_dict=dict()
        smoothed_dict=dict()
        for row_number in range(start_data_column,end_data_column+1):
            data_dict[row_number]=[]
            smoothed_dict[row_number]=[]
        
        line=0
        count_info=[0.0]*ROW_NUMBER
        total_count=0
        for row in infile_reader:
            line+=1
            for row_number in range(start_data_column,end_data_column+1):
                count_info[row_number-start_data_column]+=float(row[row_number])
            if (line%bin_size)==0:
                for row_number in range(start_data_column,end_data_column+1):
                    data_dict[row_number].append(count_info[row_number-start_data_column])
                    total_count+=1
                count_info=[0.0]*ROW_NUMBER
        
        if (line%bin_size)!=0:
            for row_number in range(start_data_column,end_data_column+1):
                    data_dict[row_number].append(count_info[row_number-start_data_column])
                    total_count+=1
        
        ##processing the smoothing
        for row_number in range(start_data_column,end_data_column+1):
            raw_list=data_dict[row_number]
            print "raw_list",raw_list
            smoothed_list=smooth_data(raw_list,smooth_size)
            print "smoothed_list", smoothed_list
            smoothed_dict[row_number]=smoothed_list
            
        ##Processing the output
        bin_count=total_count/ROW_NUMBER
        for bin_num in range(bin_count):
            output_list=[]
            for row_number in range(start_data_column,end_data_column+1):
                output_list.append(smoothed_dict[row_number][bin_num])
            output_row(outfile_obj.handle,output_list)
        outfile_obj.handle.close()
            

def record_command_line():
        python_version=str(sys.version_info)
        python_info_list=python_version.split("=")
        python_version_final="##python"
        total=0
        for item in python_info_list[1:4]:
            total+=1
            version_info=item[0]
            if total==1:
                python_version_final=python_version_final+version_info
            else:
                python_version_final=python_version_final+"."+version_info
        command_line_list=sys.argv
        command_line_record=python_version_final
        for command_input in command_line_list:
            command_line_record=command_line_record+" "+command_input
        command_line_record=command_line_record+'\n'
        return command_line_record


def output_dictionary_to_file(feature_ID_list,data_dict,data_len,handle):
    #print data_len
    for feature_ID in feature_ID_list:
        #print feature_ID
        handle.write(str(feature_ID))
        for i in range(data_len):
            #print i
            handle.write('\t'+str(data_dict[feature_ID][i]))
        handle.write('\n')
    handle.close()

