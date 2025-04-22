       LDI r1 1
       PST r0 r1 1   //dsp state
       PLD r0 r1 2   //fetch input
       INC r1
.count PST r0 r2 0
       INC r2        //r2 + 1
       CMP r1 r2     //branch : compare
       BRH Z .stop   //if r1 = r2 then stop
       JMP .count
.stop  HLT
