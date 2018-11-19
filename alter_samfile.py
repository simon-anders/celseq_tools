import sys, zlib, base64

CB_indices = slice( 0, 6 )
UMI_indices = slice( 6, 12 )

for line in sys.stdin.buffer:

   # If line starts with '@' (header line), just pass through
   if line[0] == ord(b"@"):
      sys.stdout.buffer.write( line )
      continue

   # Find double colon in read ID
   first_tab = line.find( b"\t" )
   double_colon = line.find( b"::", 0, first_tab )

   # Check that there was exactly one double colon in read ID
   if double_colon == -1:
      sys.stderr.write( "Error: Nodouble colons found in read ID: " + 
         line[:first_tab].decode() + "\n" )
      sys.stderr.write( "Is this really a SAM file generated using celseq_tools?\n" )

   if line.find( b"::", double_colon+2, first_tab ) != -1:
      sys.stderr.write( "Error: Two double colons found in read ID: " + 
         line[:first_tab].decode() + "\n" )
   
   # Decode extra part
   extrapart = zlib.decompress( base64.urlsafe_b64decode( line[double_colon+2:first_tab] ) )
   midpoint = len( extrapart ) // 2   
   if( extrapart[midpoint] != ord(b":") ):
      sys.stderr.write( "Malformatted read ID extra part. Read ID is:" + 
         line[:first_tab].decode() + "\n" )   
   read1seq  = extrapart[:midpoint]
   read1qual = extrapart[midpoint+1:]

   sys.stdout.buffer.write( line[:double_colon] + b"\t" )
   sys.stdout.buffer.write( line[first_tab+1:-1] )
   sys.stdout.buffer.write( b"\tCR:Z:" + read1seq[ CB_indices ] )
   sys.stdout.buffer.write( b"\tUR:Z:" + read1seq[ UMI_indices ] )
   sys.stdout.buffer.write( b"\tCY:Z:" + read1qual[ CB_indices ] )
   sys.stdout.buffer.write( b"\tUY:Z:" + read1qual[ UMI_indices ] )
   sys.stdout.buffer.write( b"\n" )

