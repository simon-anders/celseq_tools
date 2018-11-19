import sys, gzip, zlib, base64

fastqR1 = gzip.open( sys.argv[1] )
fastqR2 = gzip.open( sys.argv[2] )

while True:
   r1l1 = fastqR1.readline()
   r1l2 = fastqR1.readline()
   r1l3 = fastqR1.readline()
   r1l4 = fastqR1.readline()

   r2l1 = fastqR2.readline()
   r2l2 = fastqR2.readline()
   r2l3 = fastqR2.readline()
   r2l4 = fastqR2.readline()    

   if r1l4 == "" or r2l4 == "":
      if r1l4 != "" or r2l4 != "":
      	sys.stderr.write( "FASTQ files have unequal number of lines." )
      sys.exit(0)

   read1_id = r1l1[ 1 : r1l1.find( b" " ) ]
   read2_id = r2l1[ 1 : r2l1.find( b" " ) ]

   if read1_id != read2_id:
   	  sys.stderr.write( "Read IDs do not match.\n" )
   	  sys.exit(1)

   if r1l1[0] != ord("@") or r2l1[0] != ord("@") or \
         r1l3[0] != ord("+") or r1l3[0] != ord("+"):
   	  sys.stderr.write( "FASTQ format error.\n" )
   	  sys.exit(1)

   extra = r1l2[1:-1] + b":" + r1l4[1:-1]

   sys.stdout.buffer.write( b"@" + read1_id + 
   	   b"::" + base64.urlsafe_b64encode( zlib.compress( extra ) ) + b"\n" ) 
   sys.stdout.buffer.write( r2l2 )
   sys.stdout.buffer.write( b"+\n" )
   sys.stdout.buffer.write( r2l4 )


# Use with
# STAR --runThreadN 8 --genomeDir ref/starIndex --readFilesIn <(python3 merge_barcodes.py reads/AS-262401-LR-38394_R1.fastq.gz reads/AS-262401-LR-38394_R2.fastq.gz ) --outFileNamePrefix alignments/ --genomeLoad LoadAndKeep