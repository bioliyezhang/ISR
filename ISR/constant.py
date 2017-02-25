#!/usr/bin/env python
'''
V2015-05-03
'''


###general Constant
digit_list=["0","1","2","3","4","5","6","7","8","9"]
DIGIT_LIST=["0","1","2","3","4","5","6","7","8","9"]
pure_nt_list = ["A","T","C","G"]
pure_nt_withN_list = ["A","T","C","G","N"]
nt_list=["A","T","C","G","D"]
nt_full_list=["A","T","C","G","a","t","c","g"]
nt_withN_full_list=["A","T","C","G","a","t","c","g","n","N"]
chr_len_human_hg19_dict = {
    "chr1" :249250621, 
    "chr2" :243199373, 
    "chr3" :198022430, 
    "chr4" :191154276, 
    "chr5" :180915260, 
    "chr6" :171115067, 
    "chr7" :159138663, 
    "chr8" :146364022, 
    "chr9" :141213431, 
    "chr10" :135534747, 
    "chr11" :135006516, 
    "chr12" :133851895, 
    "chr13" :115169878, 
    "chr14" :107349540, 
    "chr15" :102531392, 
    "chr16" :90354753, 
    "chr17" :81195210, 
    "chr18" :78077248, 
    "chr19" :59128983, 
    "chr20" :63025520, 
    "chr21" :48129895, 
    "chr22" :51304566, 
    "chrX" :155270560, 
    "chrY" :59373566
}

chr_left_arm_hg19 = {

    "chr1" :125000000,
    "chr10" :40200000,
    "chr11" :53700000,
    "chr12" :35800000,
    "chr13" :17900000,
    "chr14" :17600000,
    "chr15" :19000000,
    "chr16" :36600000,
    "chr17" :24000000,
    "chr18" :17200000,
    "chr19" :26500000,
    "chr2" :93300000,
    "chr20" :27500000,
    "chr21" :13200000,
    "chr22" :14700000,
    "chr3" :91000000,
    "chr4" :50400000,
    "chr5" :48400000,
    "chr6" :61000000,
    "chr7" :59900000,
    "chr8" :45600000,
    "chr9" :49000000,
    "chrX" :60600000,
    "chrY" :12500000

    }
human_chro_list=["chr1","chr2","chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11","chr12",\
         "chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr20","chr21","chr22","chrX","chrY"]

full_human_chro_list=["chr1","chr2","chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11","chr12",\
         "chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr20","chr21","chr22","chrX","chrY","chrM"]
##database file name
SINGLE_DIGIT_NUMBER_LIST=['0','1','2','3','4','5','6','7','8','9']


substitution_list=["AC","AT","AG","TC","TA","TG","CA","CT","CG","GA","GC","GT"]
substitution_combined_list=["AG","AT","AC","CA","CG","CT"]

nt_degenerate_dict={
    "A":["A"],
    "T":["T"],
    "C":["C"],
    "G":["G"],
    "R":["G","A"],
    "Y":["T","C"],
    "K":["G","T"],
    "M":["A","C"],
    "S":["G","C"],
    "W":["A","T"],
    "B":["G","T","C"],
    "D":["G","A","T"],
    "H":["A","C","T"],
    "V":["G","C","A"],
    "N":["N"]
    }

##Constant of SVDetect File
###SVDetect Constant v1.0
###Updated on 2012-09-23
SVDetect_ID_COLUMN=-1
SVDetect_CHRO1_COLUMN=0
SVDetect_START1_COLUMN=1
SVDetect_END1_COLUMN=2
SVDetect_CHRO2_COLUMN=3
SVDetect_START2_COLUMN=4
SVDetect_END2_COLUMN=5
SVDetect_RCOUNT_COLUMN=6
SVDetect_TYPE_COLUMN=16
SVDetect_SKIP=0
SVDetect_SEP_CHAR='\t'
DIST_THRESHOLD=1000

BLANK_VCF_LINE="chr1"+'\t'+"1"+'\t'+"."+'\t'+"A"+'\t'+"T"+'\t'+"50"+'\t'+"PASS"+'\t'+"AC=1"+'\t'+"GT:AD:DP"+'\t'+'./.'
ANNOT_VCF_LINE="#CHRO"+'\t'+"COOR"+'\t'+"ID"+'\t'+"REF"+'\t'+"ALT"+'\t'+"QUAL"+'\t'+"FILTER"+'\t'+"INFO"+'\t'+"TYPE"+'\t'
SVDetect_TYPE_LIST=["DELETION","INSERTION","INV_FRAGMT","INVERSION"
                    ,"INS_FRAGMT","INV_INS_FRAGMT","LARGE_DUPLI",
                    "DUPLICATION","SMALL_DUPLI","INV_DUPLI","TRANSLOC",
                    "INV_TRANSLOC","COAMPLICON","INV_COAMPLICON","UNDEFINED",
                    "SINGLETON"]

def combined_ID_SVDetect(rows):
    ID=rows[-1]
    chro1=rows[SVDetect_CHRO1_COLUMN]
    start1=rows[SVDetect_START1_COLUMN]
    end1=rows[SVDetect_END1_COLUMN]
    chro2=rows[SVDetect_CHRO2_COLUMN]
    start2=rows[SVDetect_START2_COLUMN]
    end2=rows[SVDetect_END2_COLUMN]
    combined_ID=ID+'_'+chro1+'_'+start1+'_'+end1+'_'+chro2+'_'+start2+'_'+end2
    return combined_ID

def combined_SVDetect(rows):
    chro1=rows[SVDetect_CHRO1_COLUMN]
    start1=rows[SVDetect_START1_COLUMN]
    end1=rows[SVDetect_END1_COLUMN]
    chro2=rows[SVDetect_CHRO2_COLUMN]
    start2=rows[SVDetect_START2_COLUMN]
    end2=rows[SVDetect_END2_COLUMN]
    combined_ID=chro1+'_'+start1+'_'+end1+'_'+chro2+'_'+start2+'_'+end2
    return combined_ID

###Cuffinks Diff output COLUMN
CUFFLINKS_DIFF_ISOFORM_ISOFORMID_COLUMN=0
CUFFLINKS_DIFF_ISOFORM_GENEID_COLUMN=1
CUFFLINKS_DIFF_ISOFORM_GENENAME_COLUMN=2
CUFFLINKS_DIFF_ISOFORM_LOCUS_COLUMN=3
CUFFLINKS_DIFF_ISOFORM_SAMPLE1_COLUMN=4
CUFFLINKS_DIFF_ISOFORM_SAMPLE2_COLUMN=5
CUFFLINKS_DIFF_ISOFORM_STATUS_COLUMN=6
CUFFLINKS_DIFF_ISOFORM_VALUE1_COLUMN=7
CUFFLINKS_DIFF_ISOFORM_VALUE2_COLUMN=8
CUFFLINKS_DIFF_ISOFORM_FOLDCHANGE_COLUMN=9
CUFFLINKS_DIFF_ISOFORM_QVALUE_COLUMN=12
CUFFLINKS_DIFF_ISOFORM_SIGNIFICANCE_COLUMN=13


##
TRUE_BOOLEAN_LIST = ['True',"TRUE","true","T","1"]

##CUfflink expression quantification column
CUFFLINKS_ID_COLUMN=0
CUFFLINKS_EXP_MEDIAN_COLUMN=9
CUFFLINKS_EXP_TSSID_COLUMN=5

### MISO COMPARE OUTPUT
### TYPE: SPECIFIC
### MISO VERSION: 0.4.6
MISO_CMP_EVENT_NAME_COLUMN=0
MISO_CMP_S1_MEAN_COLUMN=1
MISO_CMP_S1_CI_LOW_COLUMN=2
MISO_CMP_S1_CI_HIGH_COLUMN=3
MISO_CMP_S2_MEAN_COLUMN=4
MISO_CMP_S2_CI_LOW_COLUMN=5
MISO_CMP_S2_CI_HIGH_COLUMN=6        
MISO_CMP_DIFF_COLUMN=7
MISO_CMP_BAYES_FACTOR_COLUMN=8
MISO_CMP_ISOFORM_COLUMN=9
MISO_CMP_S1_COUNTS_COLUMN=10
MISO_CMP_S1_ASSIGNED_COLUMN=11
MISO_CMP_S2_COUNTS_COLUMN=12
MISO_CMP_S2_ASSIGNED_COLUMN=13
MISO_CMP_CHR_COLUMN=14
MISO_CMP_STRAND_COLUMN=15
MISO_CMP_START_COLUMN=16
MISO_CMP_END_COLUMN=17

HUMAN_GENE_NUMBER=23963
## this number comes from Hugo statistics
## the number of protein coding gene and non-coding gene

## GISTIC SEG FORMAT
GISTIC_SEG_SAMPLE_COLUMN=0
GISTIC_SEG_CHRO_COLUMN=1
GISTIC_SEG_START_COLUMN=2
GISTIC_SEG_END_COLUMN=3
GISTIC_SEG_FRAGMENT_COUNT_COLUMN=4
GISTIC_SEG_FOLD_CHANGE_COLUMN=5

## GISTIC MARKERS FORMAT
GISTIC_MARKER_ID_COLUMN=0
GISTIC_MARKER_CHRO_COLUMN=1
GISTIC_MARKER_COOR_COLUMN=2

### MISO Cell Intersect OUTPUT
### TYPE: SPECIFIC
### MISO VERSION: 0.4.6
MISO_CHRO_COLUMN=4
MISO_START_COLUMN=5
MISO_END_COLUMN=6
CELL_CHRO_COLUMN=0
CELL_START_COLUMN=1
CELL_END_COLUMN=2
CELL_INFO_COLUMN=3

### MISO SUMMARY FILE OUTPUT
### TYPE: SPECIFIC
MISO_SUMMARY_EXON_COLUMN=0
MISO_SUMMARY_MEAN_COLUMN=1
MISO_SUMMARY_ciLOW_COLUMN=2
MISO_SUMMARY_ciHIGH_COLUMN=3

#CIGAR
CIGAR_LIST =["H","M","S","X","=","I","D","N"]

##GATK parameter
JAVA_4G_CMD="java -Xmx4g "
JAVA_SCRATCH="-Djava.io.tmpdir=/scratch "
RG_CMD="-jar /protected/individuals/zhangliy/tools/picard1.71/picard1.71/AddOrReplaceReadGroups.jar "
RG_PAR="VALIDATION_STRINGENCY=LENIENT SO=coordinate "

##DEXSeq differential analysis output ConStant
DEXSeq_unique_ID_COLUMN=0
DEXSeq_gene_COLUMN=1
DEXSeq_Dispersion_COLUMN=3
DEXSeq_pvalue_COLUMN=4
DEXSeq_padjust_COLUMN=5
DEXSeq_meanBase_COLUMN=6
DEXSeq_log2fold_treated_vs_control_COLUMN=7

##Varscan pileup2snp FILE
VARSCAN_PILEUP2SNP_ALT_COUNT_COLUMN=5
VARSCAN_PILEUP2SNP_ALT_FREQ_COLUMN=6
VARSCAN_PILEUP2SNP_ALT_STRAND_COUNT_COLUMN=8
VARSCAN_PILEUP2SNP_REF_QUALITY_COUNT_COLUMN=9
VARSCAN_PILEUP2SNP_ALT_QUALITY_COUNT_COLUMN=10
VARSCAN_PILEUP2SNP_ALT_STRAND1_COUNT_COLUMN=16
VARSCAN_PILEUP2SNP_ALT_STRAND2_COUNT_COLUMN=17
VarScan_PATH = "/restricted/projectnb/montilab-p/personal/liye/shared/tools/Varscan/VarScan.v2.3.6.jar"

## GENE
EGFR_hg19_REGION = "chr7:55086714-55270769"

##Common path
LINGA_hg19_REF_PATH="/restricted/projectnb/montilab-p/personal/liye/shared/database/hg19_old/hg19.fa"

##VCF common constant
VCF_CHRO_COLUMN=0
VCF_COOR_COLUMN=1
VCF_ALT_COLUMN=4
VCF_REF_COLUMN=3
VCF_INFO_COLUMN=7
VCF_FILTER_COLUMN=6
VCF_INFO_SEP=';'
VCF_SAMPLE_COLUMN=9

##
YES_LIST=["Y","y","Yes","yes","YES"]
NO_LIST=["N","n","No","NO","no"]

##
SAM_FLG_COLUMN=1
SAM_READGROUP_COLUMN=12
SAM_CHR1_COLUMN=2
SAM_CHR2_COLUMN=6
SAM_COOR_COLUMN=3
SAM_CIGAR_COLUMN=5
SAM_SEQ_COLUMN=9
SAM_LEN_COLUMN=8
SAM_QUALITY_COLUMN=10

##BED Format
BED_CHRO_COLUMN=0
BED_START_COLUMN=1
BED_END_COLUMN=2
BED_ID_COLUMN=3
BED_HEIGHT_COLUMN=4

##BLAT alignment output file constant
PSL_MATCH_COLUMN=0
PSL_MISMATCH_COLUMN=1
PSL_CHRO_COLUMN=13
PSL_START_COLUMN=15
PSL_END_COLUMN=16
PSL_ID_COLUMN=9
PSL_HEADER_COUNT=5

##intersectBed output constant
INTERSECT_ID1_COLUMN=3 ##correct one
INTERSECT_ID2_COLUMN=5 ##need fix, normally the gene id

##ANNOVAR OUTPUT (exome/genome)
ANNOVAR_FUNC_COLUMN=0
ANNOVAR_TYPE_COLUMN=2
ANNOVAR_CHRO_COLUMN=21
ANNOVAR_COOR_COLUMN=22
ANNOVAR_REF_COLUMN=24
ANNOVAR_ALT_COLUMN=25
ANNOVAR_SKIP_HEADER=1
ANNOVAR_SAMPLE_COLUMN=35

##ensemble database
ENSEMBLE_CHRO_COLUMN=0
ENSEMBLE_TYPE_COLUMN=1
ENSEMBLE_STRUCTURE_COLUMN=2
ENSEMBLE_START_COLUMN=3
ENSEMBLE_END_COLUMN=4
ENSEMBLE_INFO_COLUMN=8

## GENERAL
ID_COLUMN=0

## Copy number alteration related file column
VARSCAN_ADJUST_HEADER=1
VARSCAN_ADJUST_CHRO_COLUMN=0
VARSCAN_ADJUST_ADJUST_LOG_COLUMN=6
VARSCAN_ADJUST_RAW_LOG_COLUMN=9

CBS_LOG_RATIO_COLUMN=4

VARSCAN_CHRO_COLUMN=0
VARSCAN_COOR_COLUMN=1
VARSCAN_REF_COLUMN=2
VARSCAN_ALT_COLUMN=3
VARSCAN_ALTCOUNT_COLUMN=5
VARSCAN_ALTPERCENT_COLUMN=6

## HTSeq output file
HTSeq_ID_COLUMN = 0
HTSeq_COUNT_COLUMN = 1

## FeatureCounts output file
FeatureCounts_SKIP_HEADER = 2
FeatureCounts_ID_COLUMN = 0
FeatureCounts_COUNT_COLUMN = 6 

##GENE_BORDER_reference
GENE_BORDER_REFERENCE_LIST=["mini","linga","scc","pc","asus","pro"]
## This still needs improvement
GENE_BORDER_REFERENCE_DICT={
    "mini":"/Users/liyezhang/Dropbox/protocol/3-database/human_genome/hg19_geneborder_annovar.txt",
    "linga":"/protected/individuals/zhangliy/database/hg19_geneborder_annovar.txt"
}

## constant for genome.dict type files
GENOME_DICT_HEADER=1
GENOME_DICT_CHROM_COLUMN=1
GENOME_DICT_SIZE_COLUMN=2

## default Next Generation Sequencing Error Rate
SEQ_ERROR_RATE=0.001
PACBIO_SEQ_ERROR_RATE=0.20
