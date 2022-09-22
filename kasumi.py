#Vraca duzinu ulaza, tj. koliko ima bitova dato x
def _bitlen(x):
    assert x >= 0
    return len(bin(x)) - 2

#Pomera x za odgovarajuci broj bitova s ulevo
def _shift(x, s):
    assert _bitlen(x) <= 16
    return ((x << s) & 0xFFFF) | (x >> (16 - s))


def _mod(x):
    return ((x - 1) % 7) + 1


#Unapred poznate tabele
S7 = (
     54, 50, 62, 56, 22, 34, 94, 96, 38,  6, 63, 93, 2,  18,123, 33,
     55,113, 39,114, 21, 67, 65, 12, 47, 73, 46, 27, 25,111,124, 81,
     53,  9,121, 79, 52, 60, 58, 48,101,127, 40,120,104, 70, 71, 43,
     20,122, 72, 61, 23,109, 13,100, 77,  1, 16,  7, 82, 10,105, 98,
    117,116, 76, 11, 89,106,  0,125,118, 99, 86, 69, 30, 57,126, 87,
    112, 51, 17,  5, 95, 14, 90, 84, 91,  8, 35,103, 32, 97, 28, 66,
    102, 31, 26, 45, 75,  4, 85, 92, 37, 74, 80, 49, 68, 29,115, 44,
     64,107,108, 24,110, 83, 36, 78, 42, 19, 15, 41, 88,119, 59,  3,
)

S9 = (    
    167,239,161,379,391,334,  9,338, 38,226, 48,358,452,385, 90,397,
    183,253,147,331,415,340, 51,362,306,500,262, 82,216,159,356,177,
    175,241,489, 37,206, 17,  0,333, 44,254,378, 58,143,220, 81,400,
     95,  3,315,245, 54,235,218,405,472,264,172,494,371,290,399, 76,
    165,197,395,121,257,480,423,212,240, 28,462,176,406,507,288,223,
    501,407,249,265, 89,186,221,428,164, 74,440,196,458,421,350,163,
    232,158,134,354, 13,250,491,142,191, 69,193,425,152,227,366,135,
    344,300,276,242,437,320,113,278, 11,243, 87,317, 36, 93,496, 27,
    487,446,482, 41, 68,156,457,131,326,403,339, 20, 39,115,442,124,
    475,384,508, 53,112,170,479,151,126,169, 73,268,279,321,168,364,
    363,292, 46,499,393,327,324, 24,456,267,157,460,488,426,309,229,
    439,506,208,271,349,401,434,236, 16,209,359, 52, 56,120,199,277,
    465,416,252,287,246,  6, 83,305,420,345,153,502, 65, 61,244,282,
    173,222,418, 67,386,368,261,101,476,291,195,430, 49, 79,166,330,
    280,383,373,128,382,408,155,495,367,388,274,107,459,417, 62,454,
    132,225,203,316,234, 14,301, 91,503,286,424,211,347,307,140,374,
     35,103,125,427, 19,214,453,146,498,314,444,230,256,329,198,285,
     50,116, 78,410, 10,205,510,171,231, 45,139,467, 29, 86,505, 32,
     72, 26,342,150,313,490,431,238,411,325,149,473, 40,119,174,355,
    185,233,389, 71,448,273,372, 55,110,178,322, 12,469,392,369,190,
      1,109,375,137,181, 88, 75,308,260,484, 98,272,370,275,412,111,
    336,318,  4,504,492,259,304, 77,337,435, 21,357,303,332,483, 18,
     47, 85, 25,497,474,289,100,269,296,478,270,106, 31,104,433, 84,
    414,486,394, 96, 99,154,511,148,413,361,409,255,162,215,302,201,
    266,351,343,144,441,365,108,298,251, 34,182,509,138,210,335,133,
    311,352,328,141,396,346,123,319,450,281,429,228,443,481, 92,404,
    485,422,248,297, 23,213,130,466, 22,217,283, 70,294,360,419,127,
    312,377,  7,468,194,  2,117,295,463,258,224,447,247,187, 80,398,
    284,353,105,390,299,471,470,184, 57,200,348, 63,204,188, 33,451,
     97, 30,310,219, 94,160,129,493, 64,179,263,102,189,207,114,402,
    438,477,387,122,192, 42,381,  5,145,118,180,449,293,323,136,380,
     43, 66, 60,455,341,445,202,432,  8,237, 15,376,436,464, 59,461,
)


class Kasumi:
    #Odgovarajući potključevi koji će se koristiti u različitim 
    #funkcijama u algoritmu
    def __init__(self):
        self.key_KL1 = [None] * 8
        self.key_KL2 = [None] * 8
        self.key_KO1 = [None] * 8
        self.key_KO2 = [None] * 8
        self.key_KO3 = [None] * 8
        self.key_KI1 = [None] * 8
        self.key_KI2 = [None] * 8
        self.key_KI3 = [None] * 8

    #Ova funkcija koristi tabele S7 i S9
    def FI(self, input, key):    
        #Sesnaestobitni ulaz se deli na dva dela od sedam i devet bita
        left  = input >> 7
        right = input & 0b1111111

        key_1 = key >> 9
        key_2 = key & 0b111111111

        tmp_l = right
        tmp_r = S9[left] ^ right

        left  = tmp_r ^ key_2
        right = S7[tmp_l] ^ (tmp_r & 0b1111111) ^ key_1

        tmp_l = right
        tmp_r = S9[left] ^ right

        left  = S7[tmp_l] ^ (tmp_r & 0b1111111)
        right = tmp_r
          
        #Spajanje podeljenog ulaza
        return (left << 9) | right


    def FO(self, input, round):
        #Delimo ulaz na dva 16-bitna dela
        left  = input >> 16
        right = input & 0xFFFF

        #Tri puta se transformise
        first_left  = right 
        first_right = self.FI(left ^ self.key_KO1[round], self.key_KI1[round]) ^ right

        second_left   = first_right 
        second_right  = self.FI(first_left ^ self.key_KO2[round], self.key_KI2[round]) ^ first_right

        third_left  = second_right
        third_right = self.FI(second_left ^ self.key_KO3[round], self.key_KI3[round]) ^ second_right

        return (third_left << 16) | third_right


    def FL(self, input, round):
        #Ulaz se opet deli na levi i desni deo
        left  = input >> 16
        right = input & 0xFFFF

        first_right = right ^ _shift(left   & self.key_KL1[round], 1)
        first_left  = left  ^ _shift(first_right | self.key_KL2[round], 1)

        return (first_left << 16) | first_right


    def kasumi(self, input, round):
        #Odgovarajuci redosled poziva funkcija u zavisnosti od 
        #toga da li je runda parna ili neparna
        if round % 2 == 1:
            tmp  = self.FL(input, round)
            output = self.FO(tmp, round)
        else:
            tmp  = self.FO(input, round)
            output = self.FL(tmp, round)

        return output

    #Odgovarajući potključevi se kreiraju od promenljive poslate
    #kroz funkciju
    def KeySchedule(self, k):
        assert _bitlen(k) <= 128
        
        C = [0x0123,0x4567,0x89AB,0xCDEF, 0xFEDC,0xBA98,0x7654,0x3210]
        key       = [None] * 8
        key_prime = [None] * 8

        for i in range(0, 8):
            key[i] = (k >> (16 * (7 - i))) & 0xFFFF
            #transformacija sa konstantama unaped datim
            key_prime[i] = key[i] ^ C[i] 

        for i in range(0, 8):
            self.key_KL1[i] = _shift(key[_mod(i + 0)], 1)
            self.key_KL2[i] =  key_prime[_mod(i + 2)]
            self.key_KO1[i] = _shift(key[_mod(i + 1)], 5)
            self.key_KO2[i] = _shift(key[_mod(i + 5)], 8)
            self.key_KO3[i] = _shift(key[_mod(i + 6)], 13)
            self.key_KI1[i] =  key_prime[_mod(i + 4)]
            self.key_KI2[i] =  key_prime[_mod(i + 3)]
            self.key_KI3[i] =  key_prime[_mod(i + 7)]

    #Funkcija sifrovanja
    def encription(self, plaintext):
        assert _bitlen(plaintext) <= 64
        
        #Delimo ulaz-otvoreni tekst na dva dela
        left  = plaintext >> 32
        right = plaintext & 0xFFFFFFFF
        
        #8 rundi koje se pozivaju u odnosu na parnost runde
        for i in range(0, 8):
            left, right = (right ^ self.kasumi(left, i), left )
            
        return (left << 32) | right 

    #Funkcija desifrovanja
    def decription(self, ciphertext):
        assert _bitlen(ciphertext) <= 64
        
        #Delimo ulaz-otvoreni tekst na dva dela
        left  = ciphertext >> 32
        right = ciphertext & 0xFFFFFFFF
        
        #8 rundi koje se pozivaju u odnosu na parnost runde
        for i in range(7, -1, -1):
            left, right = (right, self.kasumi(right, i) ^ left)
            
        return (left << 32) | right
    

if __name__ == '__main__':
    key     = 0x9900aabbccddeeff1122334455667788    
    text    = 0xfe12120987654321

    print ('Text is:   ', hex(text))
    print ('\n')
    
    my_kasumi = Kasumi()
    my_kasumi.KeySchedule(key)

    encrypted = my_kasumi.encription(text)
    print ('Encrypted: ', hex(encrypted))

    
    decrypted = my_kasumi.decription(encrypted)
    print ('Decrypted: ', hex(decrypted))
