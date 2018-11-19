sudo mount /dev/vdb1 /aux
sudo swapon /dev/vdc1

subread-buildindex -o subread_ref/mm10 \
   ~/sds/sd17l002/p/LEC/ref/Mus_musculus.GRCm38.dna.primary_assembly.fa 

python3 celseq_tools/merge_barcodes.py \
   ~/sds/sd17l002/p/LEC/reads/AS-262401-LR-38394_R1.fastq.gz \
   ~/sds/sd17l002/p/LEC/reads/AS-262401-LR-38394_R2.fastq.gz \
   > AS-262401-LR-38394_merged.fastq

subread-align -i subread_ref/mm10 -r AS-262401-LR-38394_merged.fastq \
   -o subread_out.bam -t 0 -T 7

samtools view -h subread_out.bam | \
   python3 celseq_tools/alter_samfile.py | \
   samtools view -Sb - | \
   samtools sort -m 7G - LEC_sorted
