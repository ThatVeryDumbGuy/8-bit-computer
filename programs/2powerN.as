       LDI r2 1
       PST r0 r2 1   //dsp state
       PLD r0 r1 2   //fetch input
       INC r1        //input + 1
.pow   PLD r0 r3 0   //load dsp into reg3
       ADD r3 r2 r2  //reg3 + reg4 -> reg4
       PST r0 r2 0   //dsp reg4
       DEC r1        //loop
       BRH Z .stop
       JMP .pow
.stop  HLT
