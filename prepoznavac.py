import random

key_a        = 0x9900aabbccddeeff1122334455667788
delta_key_pp = 0x00008000000000000000000000000000
key_b = key_a ^ delta_key_pp

print("Kljuc a: ")
print(hex(key_a))
print("Kljuc b: ")
print(hex(key_b))

#diferencijalne razlike za otvoreni tekst P_a, P_b (to su P i P' iz rada)
delta      = 0x0000000000100000
delta_star = 0x0000000000100000
print("Diferencijal koji biramo:")
print(hex(delta))

#diferencijalne razlike za sifrate C_a, C_b (to su C i C' iz rada)
nabla      = 0x0000000000100000
nabla_star = 0x0000000000100000

print("\n")

#konstanta koja ce da broji uspesnost
Z = 0 
for i in range(1, 10000):
    #print("Provera eksperimenta " + str(i) + ". put")
    #print("***************************************")
    P_a = random.getrandbits(64)  #kreira 64 bita pa predstavi kao int -> P_a je int
    P_b = P_a ^ delta   

    #print("Otvoreni tekstovi Pa, Pb koji ispunjavaju diferencijal: ")
    #print(hex(P_a))
    #print(hex(P_b))

    #print("Pozivam KASUMI za njih i dobijam sifrate: ")
    Kasumi_P_a = Kasumi()
    Kasumi_P_a.set_key(key_a)
    C_a = Kasumi_P_a.enc(P_a)
    
    Kasumi_P_b = Kasumi()
    Kasumi_P_b.set_key(key_b)
    C_b = Kasumi_P_b.enc(P_b)
    
    #print(hex(C_a))
    #print(hex(C_b))
    
    #print("\n")
    
    C_c = C_a ^ nabla
    C_d = C_b ^ nabla
    #print("Sifrati C_c i C_d koji ispunjavaju drugi diferencijal: ")
    #print(hex(C_c))
    #print(hex(C_d))
    
    #print("Pozivam KASUMI desifrovanje za njih i dobijam otvorene tekstove: ")
    Kasumi_C_c = Kasumi()
    Kasumi_C_c.set_key(key_a)
    P_c = Kasumi_C_c.dec(C_c)
    
    Kasumi_C_d = Kasumi()
    Kasumi_C_d.set_key(key_b)
    P_d = Kasumi_P_b.dec(C_d)
    
    #print(hex(P_c))
    #print(hex(P_d))
    
    #print("Novi otvoreni tekstovi imaju razliku: ")
    temp = P_c ^ P_d
    #print(hex(temp))
    #print("\n")
    
    if delta == temp:
        #print("Jednako kao polazni diferencijal!")
        Z = Z + 1
    #else: 
        #print("Nije jednako kao polazni diferencijal!")
        
    #print("\n")

    
print(Z)