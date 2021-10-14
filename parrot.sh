# !/bin/bash
# from https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)
read phonenum
espeak -ven+f2 -k5 -s150 --stdout  "The number stored in the memo is $phonenum" | aplay