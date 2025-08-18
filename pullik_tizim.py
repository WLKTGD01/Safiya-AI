a = []


def frac():
    b = input('Siz: ')
    if b:
        a.append(b)
        print(b)


limit = 5
tolov_qilingan = False

while True:
    if len(a) < limit:
        frac()
    else:
        if not tolov_qilingan:
            print('❗ Iltimos, pul to\'lang. Limitingiz tugadi.')
            print('Simple - 4000 UZS (8 ta yozish)')
            print('Medium - 10000 UZS (20 ta yozish)')
            print('Pro - 40000 UZS (110 ta yozish)')
            r = input('Pulni kiriting: ')

            if r == '4000':
                limit = 8
                tolov_qilingan = True
            elif r == '10000':
                limit = 20
                tolov_qilingan = True
            elif r == '40000':
                limit = 110
                tolov_qilingan = True
            else:
                print('❌ Ayni to‘g‘ri summani kiriting.')
                break
        else:
            print('❌ Limit tugadi. Yana pul to‘lang.')
            break
