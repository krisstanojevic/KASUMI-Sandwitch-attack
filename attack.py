def append_hex(a, b):
    sizeof_b = 0

    # get size of b in bits
    while((b >> sizeof_b) > 0):
        sizeof_b += 1

    # align answer to nearest 4 bits (hex digit)
    sizeof_b += sizeof_b % 4

    return (a << sizeof_b) | b


key_a        = 0x9900aabbccddeeff1122334455667788
delta_key_ab = 0x00008000000000000000000000000000
delta_key_ac = 0x00000000000000000000000080000000
key_b = key_a ^ delta_key_ab
key_c = key_a ^ delta_key_ac
key_d = key_c ^ delta_key_ab

delta = 0x0000000000100000
nabla = 0x0000000000100000

C_a = [None] * 2**24   #2**24
P_a = [None] * 2**24   #2**24
P_b = [None] * 2**24   #2**24
C_b = [None] * 2**24   #2**24
C_c = [None] * 2**24   #2**24
P_c = [None] * 2**24   #2**24
P_d = [None] * 2**24   #2**24
C_d = [None] * 2**24   #2**24

A = 0x2950412b
Kasumi_P_a = Kasumi()
Kasumi_P_a.set_key(key_a)
Kasumi_P_b = Kasumi()
Kasumi_P_b.set_key(key_b)
Kasumi_P_c = Kasumi()
Kasumi_P_c.set_key(key_c)
Kasumi_P_d = Kasumi()
Kasumi_P_d.set_key(key_d)

dict = {}

for i in range(0, 2**5):  #2**24
    print("****************")
    X_a = random.getrandbits(32)
    C_a[i] = hex(append_hex(X_a, A)) #f'0x{A:x}{X_a:x}'
    print(C_a[i])
    
    P_a[i] = hex(Kasumi_P_a.dec(int(C_a[i], base = 16)))
    print(P_a[i])
    
    P_b[i] = int(P_a[i], base = 16) ^ delta
    C_b[i] = Kasumi_P_b.enc(P_b[i])
    print(hex(P_b[i]))
    print(hex(C_b[i]))
    
    #stavljam u hes tabelu
    dict[hex(C_b[i] & 0xFFFFFFFF)] = (C_a[i], hex(C_b[i])) 
    
    
for i in range(0, 2**5):  #2**24
    print("-------------------")
    Y_c = random.getrandbits(32)
    C_c[i] = hex(append_hex(Y_c, A ^ nabla))
    print(C_c[i])
    
    P_c[i] = hex(Kasumi_P_c.dec(int(C_c[i], base = 16)))
    print(P_c[i])
    
    P_d[i] = int(P_c[i], base = 16) ^ delta
    C_d[i] = Kasumi_P_d.enc(P_d[i])
    print(hex(P_d[i]))
    print(hex(C_d[i]))

          
    if hex((C_d[i] & 0xFFFFFFFF) ^ nabla) in dict:
        print(  dict[hex((C_d[i] & 0xFFFFFFFF) ^ nabla)]  )

print("i ondaaaa")
print(dict)
print('kraj')        