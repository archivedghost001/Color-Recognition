import cv2
import numpy as np
import pandas as pd
import argparse


ap = argparse.ArgumentParser()

# run with "pyton.exe .\main.py --image .\images\flowers.jpg"
ap.add_argument("-i", "--image", required=True,
                help="Image Path")
args = vars(ap.parse_args())
img_path = args["image"]

# membaca gambar dengan library opencv
img = cv2.imread(img_path)

# mendeklarasikan variabel secara global (digunakan nanti)
clicked = False
r = g = b = xpos = ypos = 0

# Membaca file csv dengan lib panda dan memberi nama pada setiap kolom
index = ["color", "color_name", "hex", "R", "G", "B"]

# Berfungsi untuk menghitung jarak minimum dari semua warna dan mendapatkan warna paling cocok
csv = pd.read_csv("colors.csv", names=index, header=None)

# Mendefinisikan fungsi getColorName dengan tiga parameter R, G, dan B


def getColorName(R, G, B):
    # inisialisasi variabel minimum dengan nilai yang sangat besar
    minimum = 10000
    # Menghitung iterasi (perulangan) pada setiap barus di file csv
    for i in range(len(csv)):
        # Menghitung jarak antara warna yang dicari dengan warna pada baris i di file csv menggunakan rumus Manhattan distance
        d = (
            abs(R - int(csv.loc[i, "R"]))
            + abs(G - int(csv.loc[i, "G"]))
            + abs(B - int(csv.loc[i, "B"]))
        )
        # Jika jarak yang dihitung lebih kecil dari minimum saat ini, maka update nilai minimum dan nama warna
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    # Mengembalikan nama warna yang paling cocok
    return cname

# Fungsi untuk mendapatkan koordinat x, y dari double click mouse


def draw_function(event, x, y, flags, param):
    # Periksa apakah tombol kiri mouse diklik dua kali
    if event == cv2.EVENT_LBUTTONDBLCLK:
        # Deklarasikan variabel global untuk menyimpan nilai warna dan posisi pixel yang diklik
        global b, g, r, xpos, ypos, clicked
        # Setel flag clicked menjadi True
        clicked = True
        # Simpan koordinat x dan y dari pixel yang di klik
        xpos = x
        ypos = y
        # Dapatkan nilai warna dari pixel yang di klik
        b, g, r = img[y, x]
        # Konversi nilai warna menjadi bilangan bulat
        b = int(b)
        g = int(g)
        r = int(r)


# Membuat window dengan nama "image"
cv2.namedWindow("image")
# Menetapkan fungsi 'draw_function' sebagai callback untuk peristiwa mouse pada jendela 'image'
cv2.setMouseCallback("image", draw_function)
while 1:
    cv2.imshow("image", img)
    if clicked:
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        text = getColorName(r, g, b) + " R=" + str(r) + \
            " G=" + str(g) + " B=" + str(b)
        cv2.putText(img, text, (50, 50), 2, 0.8,
                    (255, 255, 255), 2, cv2.LINE_AA)
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        clicked = False
    # Break the loop jika pengguna menekan tombol "esc"
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
