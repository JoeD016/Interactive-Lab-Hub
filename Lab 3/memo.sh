# !/bin/bash
# from https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)
espeak -ven+f2 -k5 -s150 --stdout  "The number stored in the memo is seven three three eight eight eight nine nine nine nine" | aplay