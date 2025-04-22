       LDI r3 1
       PST r0 r3 1   //dsp state
       PLD r0 r1 2   //fetch input
       INC r1
.fibon ADD r2 r3 r4  //a + b -> c
       PST r0 r2 0   //display a
       ADD r0 r3 r2  //move r3 -> r2
       ADD r0 r4 r3  //move r4 -> r3
       DEC r1
       BRH Z .stop
       JMP .fibon
.stop  HLT
