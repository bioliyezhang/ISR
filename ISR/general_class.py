#!/usr/bin/env python
'''
V2015-05-03
'''



import os
import csv
from itertools import ifilter
import sys


"""
COMMON FUNCTIONS
"""
def output_header_file_old(infile,skip,output_handle,sup_list=[],eliminate=0):
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

def output_column_descriptor(infile):
    reader=csv.reader(open(infile,"rU"),delimiter="\t")
    column_descriptor_list = []
    for row in reader:
        test2=row[0][0:2]
        test1=row[0][0:1]
        if test2=="##":
            pass
        elif test1=="#":
            column_descriptor_list=row[:]
        else:
            break
    return column_descriptor_list

def output_header_file(infile,output_handle,sup_list=[],eliminate=0):
        ##Version1.0
        ##write header into files
        reader=csv.reader(open(infile,"rU"),delimiter="\t")
        for row in reader:
                test2=row[0][0:2]
                test1=row[0][0:1]
                if test2=="##":
                        output_row(output_handle,row)
                elif test1=="#":
                        output_row(output_handle,row+sup_list)
                else:
                        break
                
def output_header_VCF_file(infile,output_handle,cmd_record,sup_list=[],eliminate=0):
        ##Version1.0
        ##write header into files
        reader=csv.reader(open(infile,"rU"),delimiter="\t")
        first_line=True
        description_output=False
        for row in reader:
                
                #if first_line!=True and (row[0][0:17]=="##fileformat=VCFv"):
                #       continue
                
                if row[0][0:2]=="##":
                        if first_line and row[0][0:18]!="##fileformat=VCFv4":
                                output_handle.write("##fileformat=VCFv4.0\n")
                                output_row(output_handle,row)
                                if cmd_record!="":
                                        output_handle.write(cmd_record) 
                                
                        elif first_line and row[0][0:18]=="##fileformat=VCFv4":
                                output_row(output_handle,row)
                                if cmd_record!="":
                                        output_handle.write(cmd_record)
                        
                        else:
                                #output_handle.write("##fileformat=VCFv4.0\n")
                                output_row(output_handle,row)   
                                        
                                
                elif row[0][0]=="#" and row[0][1]!="#":
                        if first_line==True:
                                output_handle.write("##fileformat=VCFv4.0\n")
                                if cmd_record!="":
                                        output_handle.write(cmd_record)
                        if eliminate==0:
                                combined_row=row+sup_list
                        else:
                                combined_row=row[:(-1)*eliminate]+sup_list
                        output_row(output_handle,combined_row)
                        description_output=True
                else:
                        if first_line==True:
                                output_handle.write("##fileformat=VCFv4.0\n")
                                if cmd_record!="":
                                        output_handle.write(cmd_record)
                                print "quit early"
                        break
                first_line=False
        if description_output==False:
            description_list=["#CHRO","COOR","ID","REF","ALT","QUAL","FILTER","INFO","FORMAT"]
            description_list=description_list+sup_list
            output_row(output_handle,description_list)
        
def output_header_VCF_file_replace(infile,output_handle,cmd_record,sup_list=[],eliminate=0):
        ##Version1.0
        ##write header into files
        reader=csv.reader(open(infile,"rU"),delimiter="\t")
        first_line=True
        for row in reader:
                
                #if first_line!=True and (row[0][0:17]=="##fileformat=VCFv"):
                #       continue
                
                if row[0][0:2]=="##":
                        if first_line and row[0][0:18]!="##fileformat=VCFv4":
                                output_handle.write("##fileformat=VCFv4.0\n")
                                output_row(output_handle,row,eliminate)
                                if cmd_record!="":
                                        output_handle.write(cmd_record) 
                                
                        elif first_line and row[0][0:18]=="##fileformat=VCFv4":
                                output_row(output_handle,row,eliminate)
                                if cmd_record!="":
                                        output_handle.write(cmd_record)
                        
                        else:
                                #output_handle.write("##fileformat=VCFv4.0\n")
                                output_row(output_handle,row,eliminate) 
                                        
                                
                elif row[0][0]=="#" and row[0][1]!="#":
                        if first_line==True:
                                output_handle.write("##fileformat=VCFv4.0\n")
                                if cmd_record!="":
                                        output_handle.write(cmd_record)
                        #combined_row=row+sup_list
                        #output_row(output_handle,combined_row,eliminate)
                else:
                        if first_line==True:
                                output_handle.write("##fileformat=VCFv4.0\n")
                                if cmd_record!="":
                                        output_handle.write(cmd_record)
                                print "quit early"
                        break
                first_line=False
                
def output_row(handle,row,eliminate=0):
        ##write row into files
        len_row=len(row)-eliminate
        for i in xrange(len_row):
                if i==(len_row-1):
                        handle.write(str(row[i])+'\n')
                else:
                        handle.write(str(row[i])+'\t')
                        
def get_file_name(full_name):
        if full_name.count("/")==0:
                return full_name
        else:
                full_name_list=full_name.split("/")
                return full_name_list[-1]

def get_path(full_name):
        full_name_list=full_name.split("/")
        full_name_len=len(full_name_list)
        path=""
        for index in range(1,full_name_len-1):
                path=path+"/"+full_name_list[index]
        return path
"""
COMMON FUNCTIONS
"""

class GeneralFile_class:
        
        def __init__(self,name):
            self.filename=name
            self.name_only=get_file_name(name)
            self.path_only=get_path(name)
            self.SEP_CHAR='\t'
            self.SKIP_HEADER=0
            self.SAMPLE_ID_LEN=1 #this will determin how many section will be considered to be the unique ID
            self.SAMPLE_ID_POS=0
            self.UNIQUE_ID_COLUMN=0
            self.FILENAME_SPLIT_CHAR='_'
            self.RECORD=""
            self.AUTOSKIP_HEADER=True
            self.OUTPUT_PATH=os.getcwd()
            #self.count_column_number()
        
        def count_column_number(self):
            reader=csv.reader(open(self.filename,'rU'),delimiter=self.SEP_CHAR)
            rows=reader.next()
            self.COLUMN_COUNT=len(rows)
                
        def ID_frequency_dict_gen(self,COLUMN=2,FILEPATH=os.getcwd()):
                if '/' in self.filename:
                        compete_path=self.filename
                else:
                        complete_path=FILEPATH + '/' + self.filename
                reader=csv.reader(open(complete_path,'r'),delimiter=self.SEP_CHAR)
                for i in range(self.SKIP_HEADER):
                        reader.next()
                ID_dict=dict()
                for rows in reader:
                        ID=rows[COLUMN]
                        ID_dict[ID]=0
                reader=csv.reader(open(complete_path,'r'),delimiter=self.SEP_CHAR)
                for i in range(self.SKIP_HEADER):
                        reader.next()
                for rows in reader:
                        ID=rows[COLUMN]
                        ID_dict[ID]+=1
                return ID_dict
                        
                
        def generate_sample_id(self):
                POS=self.SAMPLE_ID_POS
                if '/' not in self.filename:
                        filename_list=(self.name_only).split(self.FILENAME_SPLIT_CHAR)
                else:
                        infile_path_list=self.filename.split('/')
                        infile_name=infile_path_list[-1]
                        filename_list=infile_name.split(self.FILENAME_SPLIT_CHAR)
                
                if self.SAMPLE_ID_LEN==1:
                        sample_id=filename_list[POS]
                else:
                        filename_list_len=len(filename_list)
                        if self.SAMPLE_ID_LEN>filename_list_len:
                                self.SAMPLE_ID_LEN=filename_list_len
                                
                        for i in range(self.SAMPLE_ID_LEN):
                                if i == 0 :
                                        sample_id=filename_list[POS]
                                else:
                                        sample_id+=self.FILENAME_SPLIT_CHAR+filename_list[POS+i]
                return sample_id
        
        def outputfilename_gen(self,name_fragment="std_out",suffix="txt",POS=0):
                ##version2.0
                if '/' not in self.filename:
                        
                        #infile_name_list=(self.filename).split(self.FILENAME_SPLIT_CHAR)
                        #sample_id=infile_name_list[POS]
                        sample_id=self.generate_sample_id()
                        output_filename=sample_id+"_"+name_fragment+'.'+suffix
                        return output_filename
                else:
                        infile_path_list=self.filename.split('/')
                        infile_name=infile_path_list[-1]
                        print "infile_name",infile_name
                        #infile_name_list=(infile_name).split(self.FILENAME_SPLIT_CHAR)
                        #sample_id=infile_name_list[POS]
                        self.name_only=infile_name
                        sample_id=self.generate_sample_id()
                        output_filename=sample_id+"_"+name_fragment+'.'+suffix
                        return output_filename
                        
        
        def sampleID_gen(self):
                
                ##version2.0
                if self.name_only.count("/")>0:
                        tmp_list=self.name_only.split("/")
                        self.name_only=tmp_list[-1]
                tmp_list=(self.name_only).split(self.FILENAME_SPLIT_CHAR)
                sampleID=tmp_list[self.SAMPLE_ID_POS]
                return sampleID
        
        def reader_gen(self,FILEPATH=os.getcwd()):
                
                ## this section solve the potential problem running on the PC, Need to implement more
                if FILEPATH.count('\\')>0:
                        FILEPATH=FILEPATH.replace('\\','/')                      
                
                if '/' in self.filename:
                        complete_path=self.filename
                else:
                        complete_path=FILEPATH + '/' + self.filename
                
                reader=csv.reader(open(complete_path,'rU'),delimiter=self.SEP_CHAR,quoting=csv.QUOTE_NONE)
                
                
                if self.AUTOSKIP_HEADER==True and self.SKIP_HEADER==0:
                        ## this will over-write provided default
                        skip_number=0
                        row=reader.next()
                        while row[0][0]=="#":
                                skip_number+=1
                                row=reader.next()
                        self.SKIP_HEADER=skip_number
                
                #print "current skip header value is", self.SKIP_HEADER
                reader=csv.reader(open(complete_path,'rU'),delimiter=self.SEP_CHAR,quoting=csv.QUOTE_NONE)
                for i in range(self.SKIP_HEADER):
                        reader.next()
                return reader
        
        def unique_ID_list_gen(self,reader,unique_ID_column):
                unique_ID_list=[]
                for row in reader:
                        unique_ID=row[unique_ID_column]
                        unique_ID_list.append(unique_ID)
                return unique_ID_list
        
        def unique_ID_list_gen_v2(self,reader,unique_ID_column):
                ## under development
                unique_ID_list=[]
                for row in reader:
                        unique_ID=row[unique_ID_column]
                        unique_ID_list.append(unique_ID)
                return unique_ID_list
                
        def output_handle_gen(self,header_file=None,FILEPATH=os.getcwd(),sup_list=[],HEAD_LINE=1):
                ##Version2.0
                ##Updated 2012-10-31
                '''
                header_file is the file contains the header information
                FILEPATH is the path for the output file
                sup_list is the additional annotations added to the output file header
                HEAD_LINE is the number of header lines extracted from header file and writen into output file
                '''
                if '/' in self.filename:
                        complete_path=self.filename
                else:
                        complete_path=FILEPATH + '/' + self.filename
                
                self.handle=open(complete_path,'w')
                
                if self.RECORD=="":
                        pass
                else:
                        self.handle.write(self.RECORD)
                
                if header_file==None:
                        pass
                else:
                        output_header_file(header_file,self.handle,sup_list,eliminate=0)
                
                        
class SVDetectFile_class(GeneralFile_class):
        ##This file is SVDetect Subtype
        SVDetect_CHRO1_COLUMN=0
        SVDetect_START1_COLUMN=1
        SVDetect_END1_COLUMN=2
        SVDetect_CHRO2_COLUMN=3
        SVDetect_START2_COLUMN=4
        SVDetect_END2_COLUMN=5
        SVDetect_TYPE_COLUMN=16
        SEP_CHAR='\t'
        SKIP_HEADER=0
        DIST_THRESHOLD=1000
        
        def __init__(self,name):
                GeneralFile_class.__init__(self,name)
                self.SKIP_HEADER=0
                self.CHRO2_COLUMN=3
                self.CHRO1_COLUMN=0
                self.START1_COLUMN=1
                self.END1_COLUMN=2
                self.START2_COLUMN=4
                self.END2_COLUMN=5
                self.ID_COLUMN=-1
                
        
        def region1_output(self):
                return None
        
        def reader_gen(self,FILEPATH=os.getcwd()):
                complete_path=FILEPATH + '/' + self.filename
                #print "complete_path",complete_path
                reader=csv.reader(open(complete_path,'r'),delimiter=self.SEP_CHAR)
                for i in range(self.SKIP_HEADER):
                        reader.next()
                return reader
        
        def filter_chro(self,infile_reader,filter_chro,eliminate_ID):
                data_dict=dict()
                data_list=[]
                previous_point=0
                for rows in infile_reader:
                        chro=rows[self.CHRO2_COLUMN]
                        ID=rows[self.ID_COLUMN]
                        if filter_chro==chro and ID!=eliminate_ID:
                                start1=rows[self.START1_COLUMN]
                                end1=rows[self.END1_COLUMN]
                                middle_point=int((int(start1)+int(end1))/2)
                                if previous_point==middle_point:
                                        middle_point+=0.1
                                previous_point=middle_point     
                                data_dict[middle_point]=rows
                                data_list.append(middle_point)
                #print "data_list,",data_list
                '''
                for data in data_list:
                        if data_list.count(data) > 1:
                                print "Same cooridnate ocurrs, Fix needed"
                                sys.exit()
                '''
                data_list.sort()
                #print "sorted_data", sorted_data
                #print "data_dict", data_dict
                return data_list,data_dict
        
class BEDFile_class(GeneralFile_class):
    SEP_CHAR='\t'
    # this class can be used for BedGraph format as well
    def __init__(self,name):
        GeneralFile_class.__init__(self,name)
        self.SKIP_HEADER=0
        self.CHRO_COLUMN=0
        self.START_COLUMN=1
        self.END_COLUMN=2
        self.ID_COLUMN=3
        self.SCORE_COLUMN=4
        self.STRAND_COLUMN=5


class Indel_GATK_File_class(BEDFile_class):
        
        def __init__(self,name):
                BEDFile_class.__init__(self,name)
                self.TUMOR_STRAND_COLUMN=17
                self.TUMOR_STRAND_COLUMN_SEP=':'
                self.TUMOR_STRAND_COLUMN_INFO=1
                self.INDEL_COLUMN=3
                self.GENE_COLUMN=-1
                self.FREQ_COLUMN=21
                self.SKIP_HEADER=1
                ##Not sure why there is a blank column there in the data
        
                
class VCF_File_class(GeneralFile_class):
        def __init__(self,name):
                GeneralFile_class.__init__(self,name)
                self.QUAL_COLUMN=5
                self.ALT_COLUMN=4
                self.REF_COLUMN=3
                self.ID_COLUMN=2
                self.COOR_COLUMN=1
                self.CHRO_COLUMN=0
                self.FILTER_COLUMN=6
                self.INFO_COLUMN=7
                self.FORMAT_COLUMN=8
                self.SKIP_HEADER=0
                self.SEP_INFO_START_COLUMN=9
                self.ALT_SEP_CHAR=','
                self.REPLACE_DESCRIPTION=0
                self.DESCRIPTION_COLUMN_REMOVAL=0
        
        def check_header(self,FILEPATH=os.getcwd()):
                ##check the description column and first column
                result=0
                if '/' in self.filename:
                        complete_path=self.filename
                else:
                        complete_path=FILEPATH + '/' + self.filename
                reader=csv.reader(open(complete_path,'r'),delimiter=self.SEP_CHAR)
                for row in reader:
                        if row[0][0]!="#":
                                break
                        else:
                                if row[0][1:6].upper()=="CHROM":
                                        result=1                        
                return result
        
        def sample_list_gen(self,FILEPATH=os.getcwd()):
                
                if '/' in self.filename:
                        complete_path=self.filename
                else:
                        complete_path=FILEPATH + '/' + self.filename
                reader=csv.reader(open(complete_path,'r'),delimiter=self.SEP_CHAR)
                for rows in reader:
                        first_item=rows[0]
                        if first_item[0]=='#' and first_item[1]!='#':
                                sample_list=rows[self.SEP_INFO_START_COLUMN:]
                                break
                        else:
                                pass
                return sample_list
                                
        def reader_gen(self,FILEPATH=os.getcwd()):
                if '/' in self.filename:
                        complete_path=self.filename
                else:
                        complete_path=FILEPATH + '/' + self.filename
                
                reader=csv.reader(open(complete_path,'rU'),delimiter=self.SEP_CHAR)
                skip_count=0
                try:
                        rows=reader.next()
                        while rows[0][0]=="#":
                                skip_count+=1
                                rows=reader.next()
                        
                        reader=csv.reader(open(complete_path,'rU'),delimiter=self.SEP_CHAR)
                        for i in range(skip_count):
                                reader.next()
                except:
                        pass
                
                return reader            
        
        def output_sample_info(self,FILEPATH=os.getcwd()):
                if '/' in self.filename:
                        complete_path=self.filename
                else:
                        complete_path=FILEPATH + '/' + self.filename
                
                reader=csv.reader(open(complete_path,'rU'),delimiter=self.SEP_CHAR)
                
                
                for rows in reader:
                        if rows[0][0:2]=="##":
                                pass
                        else:
                                sample_info=rows[9:]
                                break
                return sample_info
        
        def output_handle_gen(self,header_file=None,FILEPATH=os.getcwd(),sup_list=[],HEAD_LINE=1):
                ##Version2.0
                ##Updated 2012-10-31
                '''
                header_file is the file contains the header information
                FILEPATH is the path for the output file
                sup_list is the additional annotations added to the output file header
                HEAD_LINE is the number of header lines extracted from header file and writen into output file
                '''
                if '/' in self.filename:
                        complete_path=self.filename
                else:
                        complete_path=FILEPATH + '/' + self.filename
                
                self.handle=open(complete_path,'w')
                
                
                
                if header_file==None:
                        self.handle.write("##fileformat=VCFv4\n")
                        if self.RECORD=="":
                                pass
                        else:
                                self.handle.write(self.RECORD)
                        pass
                else:
                        #output_header_file(header_file,self.handle,sup_list,eliminate=0)
                        if self.REPLACE_DESCRIPTION==0:
                                ##
                                output_header_VCF_file(header_file,self.handle,self.RECORD,sup_list,eliminate=self.DESCRIPTION_COLUMN_REMOVAL)
                        else:
                                output_header_VCF_file_replace(header_file,self.handle,self.RECORD,sup_list,eliminate=self.DESCRIPTION_COLUMN_REMOVAL)
                        
        def sample_count(self,FILEPATH=os.getcwd()):
                if '/' in self.filename:
                        complete_path=self.filename
                else:
                        complete_path=FILEPATH + '/' + self.filename
                reader=csv.reader(open(complete_path,'rU'),delimiter=self.SEP_CHAR)
                sample_count=0
                for rows in reader:
                        if rows[0][0]=="#":
                                pass
                        else:
                                sample_info=rows[9:]
                                for sample_data in sample_info:
                                        if sample_data.count(":")==2:
                                                sample_count+=1
                                        elif sample_data=="./.":
                                                sample_count+=1
                                        else:
                                                pass
                                break
                return sample_count
                
        def variant_list_gen(self):
                variant_dict=dict()
                infile_reader=self.reader_gen()
                for row in infile_reader:
                        chro=row[self.CHRO_COLUMN]
                        coor=row[self.COOR_COLUMN]
                        ref=row[self.REF_COLUMN]
                        alt=row[self.ALT_COLUMN]
                        unique_ID=chro+"_"+coor+"_"+ref+"_"+alt
                        variant_dict[unique_ID]=[]
                return variant_dict
                                
        def add_to_filter_column(self,vcf_row,additional_filter):
                current_filter=vcf_row[self.FILTER_COLUMN]
                new_filter=current_filter+";" + additional_filter
                new_vcf_row=vcf_row[:]
                new_vcf_row[self.FILTER_COLUMN]=new_filter
                return new_vcf_row
                        
                        
                
class PBS_File_class(GeneralFile_class):
        
        def __init__(self,name,path=os.getcwd()):
                GeneralFile_class.__init__(self,name)
                self.email="zhangliy@bu.edu"
                self.memory="2g"
                self.suffix='pbs'
                self.PROJECT="montilab-p"
                self.MACHINE="scc"
                self.RUNTIME_LIMIT="96:00:00"
                
                #self.
                #GeneralFile_class.output_handle_gen(self,FILEPATH=path)
        
        def output_pbs(self,command_line_list):
                self.output_handle_gen()
                
                if self.MACHINE=="scc":
                        self.handle.write("source ~/.bashrc\n")
                        self.handle.write("#!bin/bash\n")
                        self.handle.write("#$ -l h_rt="+self.RUNTIME_LIMIT+'\n')
                        self.handle.write("\n")
                else:
                        self.handle.write("#!bin/bash\n")
                        self.handle.write("#\n")
                        self.handle.write("\n")
                
                self.handle.write("#Specify which shell to use\n")
                self.handle.write("#$ -S /bin/bash\n")
                self.handle.write("\n")
                
                self.handle.write("#Run on the current working folder\n")
                self.handle.write("#$ -cwd\n")
                self.handle.write("\n")
                
                self.handle.write("#Given this job a name\n")
                if self.filename.count("/")>=1:
                        filename_info_list=self.filename.split("/")
                        filename_info=filename_info_list[-1]
                else:
                        filename_info=self.filename
                self.handle.write("#$ -N S"+filename_info+'\n')
                self.handle.write("\n")
                
                self.handle.write("#Join standard output and error to a single file\n")
                self.handle.write("#$ -j y\n")
                self.handle.write("\n")
                
                self.handle.write("# Name the file where to redict standard output and error\n")
                if self.filename.count("/")>=1:
                        filename_info_list=self.filename.split("/")
                        filename_info=filename_info_list[-1]
                else:
                        filename_info=self.filename             
                self.handle.write("#$ -o "+ filename_info +".qlog\n")
                self.handle.write("\n")
                
                self.handle.write("# Project this job belongs to \n")
                self.handle.write("#$ -P " + self.PROJECT+ " \n")
                self.handle.write("\n")
                
                self.handle.write("# Send an email when the job begins and when it ends running\n")
                self.handle.write("#$ -m be\n")
                self.handle.write("\n")
                
                if (self.email).lower!="no":
                        self.handle.write("# Whom to send the email to\n")
                        self.handle.write("#$ -M "+self.email+ "\n")
                        self.handle.write("\n")
                
                self.handle.write("# memory usage\n")
                self.handle.write("#$ -l mem_free="+self.memory+ "\n")
                self.handle.write("\n")
                
                self.handle.write("# Now let's Keep track of some information just in case anything go wrong\n")
                self.handle.write("echo "+'"'+"========================================" + '"'+'\n')
                self.handle.write("echo "+'"'+"Starting on : $(date)"+'"'+ "\n")
                self.handle.write("echo "+'"'+"Running on node : $(hostname)"+'"'+"\n")
                self.handle.write("echo "+'"'+"Current directory : $(pwd)"+'"'+"\n")
                self.handle.write("echo "+'"'+"Current job ID : $JOB_ID"+'"'+"\n")
                self.handle.write("echo "+'"'+"Current job name : $JOB_NAME"+'"'+"\n")
                self.handle.write("echo "+'"'+"Task index number : $TASK_ID"+'"'+"\n")                     
                self.handle.write("echo "+'"'+"========================================" + '"'+'\n')
                self.handle.write("\n")
                
                for command_line in command_line_list:
                        self.handle.write(command_line)
                        self.handle.write('\n')
                        
                        
                self.handle.write("\n") 
                self.handle.write("echo "+'"'+"========================================" + '"'+'\n')
                self.handle.write("echo "+'"'+"Finished on : $(date)"+'"'+ "\n")
                self.handle.write("echo "+'"'+"========================================" + '"'+'\n')
                self.handle.close()

class PSL_File_class(GeneralFile_class):
        def __init__(self,name):
                GeneralFile_class.__init__(self,name)
                self.MATCH_COLUMN=0
                self.MISMATCH_COLUMN=1
                self.QUERY_INSERTION_COUNT_COLUMN=4
                self.QUERY_INSERTION_LEN_COLUMN=5
                self.REF_INSERTION_COUNT_COLUMN=6
                self.REF_INSERTION_LEN_COLUMN=7
                self.STRAND_COLUMN=8
                self.QUERY_ID_COLUMN=9
                self.QUERY_LEN_COLUMN=10                
                self.QUERY_START_COLUMN=11
                self.QUERY_END_COLUMN=12
                self.REF_ID_COLUMN=13
                self.REF_LEN_COLUMN=14
                self.REF_START_COLUMN=15
                self.REF_END_COLUMN=16
                self.BLOCK_COUNT_COLUMN=17
                self.BLOCK_SIZE_COLUMN=18
                self.QUERY_STARTS_COLUMN=19
                self.REF_STARTS_COLUMN=20
                self.AUTOSKIP_HEADER=False
                self.SKIP_HEADER=5
        
        def output_handle_gen(self,header_file=None,FILEPATH=os.getcwd(),sup_list=[],HEAD_LINE=1):
                ##Version2.0
                ##Updated 2012-10-31
                
                if '/' in self.filename:
                        complete_path=self.filename
                else:
                        complete_path=FILEPATH + '/' + self.filename
                
                self.handle=open(complete_path,'w')
                
                if self.RECORD=="":
                        pass
                else:
                        self.handle.write(self.RECORD)
                
                reader=csv.reader(open(header_file,"rU"),delimiter="\t")
                for index in range(self.SKIP_HEADER):
                        
                        row=reader.next()
                        output_row(self.handle,row)
                        if index==0:
                                self.handle.write('\n')
                

class SAM_File_class(GeneralFile_class):
        def __init__(self,name):
                GeneralFile_class.__init__(self,name)
                self.QNAME_COLUMN=0
                self.FLG_COLUMN=1
                self.CHRO_COLUMN=2
                self.COOR_COLUMN=3
                self.MAPQ_COLUMN=4
                self.CIGAR_COLUMN=5
                self.RNEXT_COLUMN=6
                self.PNEXT_COLUMN=7
                self.TLEN_COLUMN=8
                self.SEQ_COLUMN=9
                self.QUAL_COLUMN=10
                self.READGROUP_COLUMN=12
                self.MULTI_ALIGNMENT_COLUMN=12 ## for the new bwa result version at least
                self.SKIP_HEADER=0
        
        def reader_gen(self,FILEPATH=os.getcwd()):
            if '/' in self.filename:
                complete_path=self.filename
            else:
                complete_path=FILEPATH + '/' + self.filename
                        
            reader=csv.reader(open(complete_path,'rU'),delimiter=self.SEP_CHAR,quoting=csv.QUOTE_NONE)
            if self.AUTOSKIP_HEADER==True:
                ## this will over-write provided default
                skip_number=0
                row=reader.next()
                while row[0][0]=="@":
                        skip_number+=1
                        row=reader.next()
                self.SKIP_HEADER=skip_number
                
            reader=csv.reader(open(complete_path,'rU'),delimiter=self.SEP_CHAR,quoting=csv.QUOTE_NONE)
            for i in range(self.SKIP_HEADER):
                    reader.next()
            return reader

        def ref_dict_gen(self,FILEPATH=os.getcwd()):
            ## this function output the reference chromosome into a dict
            if '/' in self.filename:
                complete_path=self.filename
            else:
                complete_path=FILEPATH + '/' + self.filename
                        
            reader=csv.reader(open(complete_path,'rU'),delimiter=self.SEP_CHAR,quoting=csv.QUOTE_NONE)
            row=reader.next()
            ref_dict= dict()
            while row[0][0]=="@":
                if row[0][1:3]=="SQ":
                    ref_name=row[1][3:]
                    ref_length=int(row[2][3:])
                    ref_dict[ref_name]=ref_length
                row=reader.next()
            return ref_dict    
                
                
class GTF_File_class(GeneralFile_class):
        def __init__(self,name):
                GeneralFile_class.__init__(self,name)
                self.CHRO_COLUMN=0
                self.SOURCE_COLUMN=1
                self.FEATURE_COLUMN=2
                self.START_COLUMN=3
                self.END_COLUMN=4
                self.SCORE_COLUMN=5
                self.STRAND_COLUMN=6
                self.FRAME_COLUMN=7
                self.ATTRIBUTE_COLUMN=8
                self.SKIP_HEADER=0      
                
class MPILEUP_SINGLE_File_class(GeneralFile_class):
        def __init__(self,name):
                GeneralFile_class.__init__(self,name)
                self.CHRO_COLUMN=0
                self.COOR_COLUMN=1
                self.REF_COLUMN=2
                self.COUNT_COLUMN=3
                self.INFO_COLUMN=4
                self.QUALITY_COLUMN=5
                self.SKIP_HEADER=0

class GZ_File_class(GeneralFile_class):
        
        def __init__(self,name):
                GeneralFile_class.__init__(self,name)

        def reader_gen(self,FILEPATH=os.getcwd()):
            import gzip
            if '/' in self.filename:
                complete_path=self.filename
            else:
                complete_path=FILEPATH + '/' + self.filename
            
            reader=csv.reader(gzip.open(complete_path),delimiter=self.SEP_CHAR)
            return reader


class BLASTN6_File_class(GeneralFile_class):
        def __init__(self,name):
                GeneralFile_class.__init__(self,name)
                self.QUERY_ID_COLUMN=0
                self.REF_ID_COLUMN=1
                self.OVERLAP_PERCENTAGE_COLUMN=2
                self.OVERLAP_LENGTH_COLUMN=3
                self.MISMATCH_COLUMN=4
                self.GAP_COLUMN=5
                self.QUERY_START_COLUMN=6
                self.QUERY_END_COLUMN=7
                self.REF_START_COLUMN=8
                self.REF_END_COLUMN=9
                self.EVALUE_COLUMN=10
                self.BITSCORE_COLUMN=11
                self.SKIP_HEADER=0
                