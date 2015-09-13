from converter import *

#1: Dexter
#2: Eric


V1 = VarRule(Var("p"), "move", "robot")

#1) Fp
"""

c11 = Converter("Eventually the robot moves.", [V1], multi_translations = True)
a11 = c11.get_statement()
print_ltl(a11)
#sometimes? INCORRECT (SP can't parse correctly, must add comma after "Eventually")
#UNGRAMMATICAL

c12 = Converter("The robot will move at some time in the future.", [V1], multi_translations = True)
a12 = c12.get_statement()
print_ltl(a12)
#CORRECT #FIXED


#2) Gp

c21 = Converter("The robot is always moving", [V1], multi_translations = True)
a21 = c21.get_statement()
print_ltl(a21)
#CORRECT



c22 = Converter("The robot will always move", [V1], multi_translations = True)
a22 = c22.get_statement()
print_ltl(a22)
#CORRECT

#3) Xp

c31 = Converter("At the next time the robot will move.", [V1], multi_translations = True)
a31 = c31.get_statement()
print_ltl(a31)
#CORRECT #FIXED


c32 = Converter("The robot will be moving at the next time step.", [V1], multi_translations = True)
a32 = c32.get_statement()
print_ltl(a32)
#CORRECT
"""

V2 = VarRule(Var("p"), "push", noun = "button")
V3 = VarRule(Var("q"), "open", noun = "door")
V3_neg = VarRule(NegVar("q"), "close", noun = "door")

"""
#4) q U p

c41 = Converter("The door is open until the button is pushed.", [V2, V3], multi_translations = True)
a41 = c41.get_statement()
print_ltl(a41)
#CORRECT

#c42 is same as c41

#5) p or q

c51 = Converter("The button is pushed or the door is open.", [V2, V3], multi_translations = True)
a51 = c51.get_statement()
print_ltl(a51)
#CORRECT

c52 = Converter("The door is open or the button is pushed.", [V2, V3], multi_translations = True)
a52 = c52.get_statement()
print_ltl(a52)
#CORRECT




#6) G(p -> Xq)
c61 = Converter("Always button is pushed implies at the next time the door will be open.", [V2, V3], multi_translations = True)
a61 = c61.get_statement()
print_ltl(a61)
#INCORRECT
#UNGRAMMATICAL


c62 = Converter("If the button is pushed, then the door will be open at the next time step.", [V2, V3], multi_translations = True)
a62 = c62.get_statement()
print_ltl(a62)
#CORRECT

c63 = Converter("It's always the case that if the button is pushed, the door will open in the next step.", [V2, V3], multi_translations = True)
a63 = c63.get_statement()
print_ltl(a63)
#CORRECT
#also yields GG(p->Xq), which is a bit wierd.

#7) G!q
c71 = Converter("The door is never open.", [V2, V3], multi_translations = True)
a71 = c71.get_statement()
print_ltl(a71)
#CORRECT

c72 = Converter("The door is always closed.", [V2, V3, V3_neg], multi_translations = True)
a72 = c72.get_statement()
print_ltl(a72)
#CORRECT #FIXED


#8) GFq
c81 = Converter("The door is open infinitely often.", [V2, V3], multi_translations = True)
a81 = c81.get_statement()
print_ltl(a81)
#INCORRECT #SP #UNGRAMMATICAL?
#'The door is infinitely often open' works

c82 = Converter("The door will be open infinitely often.", [V2, V3], multi_translations = True)
a82 = c82.get_statement()
print_ltl(a82)
#INCORRECT #same reason


V4 = VarRule(Var("p"), "sound", noun="alarm")
V5 = VarRule(Var("q"), "flash", noun="light")


#9) !G(p & q)
c91 = Converter("Eventually either the alarm doesn't sound or the light doesn't flash.", [V4, V5], multi_translations = True)
a91 = c91.get_statement()
print_ltl(a91)
#INCORRECT #SP #can't handle contractions

c92 = Converter("It is not true that for all future time, the alarm will sound and the light will flash.", [V4, V5], multi_translations = True)
a92 = c92.get_statement()
print_ltl(a92)
#INCORRECT
#Need multiple parses of stanford parser

c93 = Converter("It is not always the case that the alarm sounds and the light flashes.", [V4, V5], multi_translations)
a93 = c93.get_statement()
print_ltl(a93)
#INCORRECT

#10) G(p -> Fq)
c10_1 = Converter("The alarm sounding always implies that eventually the light flashes.", [V4, V5], multi_translations = True)
a10_1 = c10_1.get_statement()
print_ltl(a10_1)
#INCORRECT


c10_2 = Converter("If the alarm sounds, then eventually the light will flash.", [V4, V5], multi_translations = True)
a10_2 = c10_2.get_statement()
print_ltl(a10_2)
#CORRECT #FIXED


#11) p W q

#12) G(p -> X(q U !p))
c12_1 = Converter("The alarm sounding always implies that starting at the next time, the light will flash until the alarm doesn't sound.", [V4, V5], multi_translations = True)
a12_1 = c12_1.get_statement()
print_ltl(a12_1)
#INCORRECT #DUH


c12_2 = Converter("If the alarm sounds, then starting from the next time step, the light will flash until the alarm ceases.", [V4, V5], multi_translations = True)
a12_2 = c12_2.get_statement()
print_ltl(a12_2)
#INCORRECT


#13) Fp -> Gq
c13_1 = Converter("If the alarm will eventually sound, then the light always flashes.", [V4, V5], multi_translations = True)
a13_1 = c13_1.get_statement()
print_ltl(a13_1)
#CORRECT #FIXED
#has double F

c13_2 = Converter("If the alarm will eventually sound, then the light must always be flashing in the future.", [V4, V5], multi_translations = True)
a13_2 = c13_2.get_statement()
print_ltl(a13_2)
#CORRECT


#14) p -> Xq
c14_1 = Converter("If the alarm sounds then the light flashes at the next time.", [V4, V5], multi_translations = True)
a14_1 = c14_1.get_statement()
print_ltl(a14_1)
#CORRECT #FIXED


c14_2 = Converter("If the alarm sounds now, then the light will be flashing at the next time step.", [V4, V5], multi_translations = True)
a14_2 = c14_2.get_statement()
print_ltl(a14_2)
#CORRECT, but also yields G(p -> Xq), should add negative constraints


#15) G(p <-> q)
#Eric: The alarm sounds and light flashes always occur at the same time.

#16) p & X!p & XXGp
c16_1 = Converter("The alarm sounds, then it does not sound, then it always sounds.", [V4, V5], multi_translations = True)
a16_1 = c16_1.get_statement()
print_ltl(a16_1)
#INCORRECT #SP (sort of) # 3rd 'sound' is parataxis to 1st 'sound' (should be 2nd)

#Eric: The alarm will not sound at the next time step, but is sounding now and will sound for all other future times

#17) FGp
c17_1 = Converter("Eventually the alarm will always sound.", [V4, V5], multi_translations = True)
a17_1 = c17_1.get_statement()
print_ltl(a17_1)
#CORRECT

#Eric: The alarm will eventually sound and not trn off


#18) (p U q) U p

c18_1 = Converter("The alarm sounds until the light flashes, and the light then flashes until the alarm sounds", [V4, V5], multi_translations = True)
a18_1 = c18_1.get_statement()
print_ltl(a18_1)
#INCORRECT

Eric: Either the alarm sounds now, or if it doesn't sound now, then the light must be flashing now.


"""

#Structure LTL controllers
r5 = VarRule(Var("go_r5"), "go", prep = "to", pobj = "position")
actCP = VarRule(Var("actCP"), "activate", dobj = "carryperson")
senseM = VarRule(Var("senseM"), "sense", dobj = "Medic")
doCP = VarRule(Var("CP"), "do", dobj = "carryperson")

#s1 = Converter("Go to r5 unless you are activating cp.", [r5, actCP], multi_translations = True)
s1 = Converter("Go to position unless you are activating carryperson.", [r5, actCP], multi_translations = True)

s2 = Converter("If you are activating carryperson, go to position.", [r5, actCP], multi_translations = True)

s3 = Converter("If you are not sensing Medic and you activated carryperson, then do carryperson.", [actCP, senseM, doCP], multi_translations = True)


"""
#Other Tests

cO1 = Converter("The door isn't open", [V3])
aO1 = cO1.get_statement()
print_ltl(aO1)
#Should be !p, but is p. Apparently, stanford parser can't handle contractions


cO2 = Converter("For all time, the alarm will sound.", [V4])
aO2 = cO2.get_statement()
print_ltl(aO2)


cO3 = Converter("It is always false that the alarm will sound.", [V4])
aO3 = cO3.get_statement()
print_ltl(aO3)
"""
