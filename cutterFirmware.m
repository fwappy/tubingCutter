cutter program



1  HM 1
  5  H 
  7  P = 0
  11  MA 300000
  18  H 
  20  P = 0
  24  VM = 19000
  29  MA 250000
  36  H 
  38  VM = 100000
  45  MA 0
  49  E 

  51  S 





feeder program


PG 100
  100  LB SU 
  100      VA K5
  104      VA K6
  108      VA K7
  112      VA CT
  116  
  116  LB GA 
  116      P = 0
  120      pr "   "
  127      pr "Total cuts using current blade is: " , R1
  168      
  168  LB G1 
  168      PR "Please enter tube length in cm"
  202      IV K5
  207  LB K0 
  207      BR K0, IF = 1
  217  LB KB 
  217      PR "Measuring Length ......"
  244      pr "     "
  253      K6 = K5 / 2
  263      K7 = K5 * - 22913
  275      P = 0
  279  LB KK 
  279      PR "How Many Cuts?"
  297      IV CT
  302      
  302  LB K1 
  302      BR K1, IF = 1
  312  LB K2 
  312      pr " Okay, " , CT
  327      pr "   "
  334      
  334  LB L1 
  334      PR "Cutting Tube ......"
  357      H 1000
  362      BR L2, CT > 0
  374  LB L2 
  374      
  374  
  374      BR L5, CT = 0
  386      H 1000
  391      PR CT
  396      MA K7
  401      H 
  403      S1 = 16, 1, 0
  413      H 1000
  418      S1 = 16, 0, 0
  428      R1 = R1 + 1
  434      H 25000
  439      P = 0
  443      CT = CT - 1
  453      BR L2, CT > 0
  465  LB L5 
  465      PR "Complete!"
  478      pr "     "
  487      pr "Total cuts using current blade is: " , R1
  528  
  528      S
  530      S
  532      BR G1
  537  
  537      E 
  539  PG


