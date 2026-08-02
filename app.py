import streamlit as st
import re
import difflib

# ---------------------------------------------------------
# 1. ตั้งค่าหน้าตาของแอปพลิเคชัน
# ---------------------------------------------------------
st.set_page_config(page_title="MLBB Draft Coach", page_icon="🎮", layout="centered")

st.title("🎮 ยูริ💗นังอ้วน MLBB Draft Hero🕹️")
st.caption("ระบบช่วยดราฟตัวละครแก้ทาง Mobile Legends: Bang Bang")

# ---------------------------------------------------------
# 2. ฐานข้อมูลฮีโร่และสรุปความสามารถ
# ---------------------------------------------------------
raw_data = """
Beatrix เบียร์ทริก ตัวดราฟแก้ทาง
Khufra คูฟรา 5.4 บทบาท: Tank | เลน: Roam Counters: Beatrix
Marcel มาเซลล์ 4.4 บทบาท: Support | เลน: Roam Counters: Beatrix
Granger เกรนเจอร์ 3.8 บทบาท: Marksman | เลน: Gold Lane Counters: Beatrix
Joy จอย 3.7 บทบาท: Assassin | เลน: Jungle Counters: Beatrix
Wanwan หวานหว่าน 2.9 บทบาท: Marksman | เลน: Gold Lane Counters: Beatrix
Obsidia ฮอปซิเดีย 2.1 บทบาท: Marksman | เลน: Gold Lane Counters: Beatrix
Moskov มอสโคฟ 1.0 บทบาท: Marksman | เลน: Gold Lane Counters: Beatrix
Irithel ไอริเทล 0.6 บทบาท: Marksman | เลน: Gold Lane Counters: Beatrix

Brody โบร์ดี้ ตัวดราฟแก้ทาง
Barats บารัต 5.6 บทบาท: Tank, Fighter | เลน: Jungle Counters: Brody
Sun ซัน 4.6 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Brody
Khufra คูฟรา 3.7 บทบาท: Tank | เลน: Roam Counters: Brody
Gloo กลู 2.3 บทบาท: Tank | เลน: Roam, Exp Lane Counters: Brody
Atlas แอตลาส 2.1 บทบาท: Tank | เลน: Roam Counters: Brody
Diggie ดิกกี้ 1.7 บทบาท: Support | เลน: Roam Counters: Brody
Minsitthar มินชิตา 0.9 บทบาท: Fighter | เลน: Exp Lane, Roam Counters: Brody
Masha มาช่า 0.7 บทบาท: Fighter, Tank | เลน: Exp Lane Counters: Brody

Bruno บรูโน่ ตัวดราฟแก้ทาง
Lolita โลลิตา 7.0 บทบาท: Support, Tank | เลน: Roam Counters: Bruno
Lesley เลสลี่ย์ 5.4 บทบาท: Marksman, Assassin | เลน: Gold Lane Counters: Bruno
Estes เอสเตส 4.4 บทบาท: Support | เลน: Roam Counters: Bruno
Karina คารีน่า 3.7 บทบาท: Assassin | เลน: Jungle Counters: Bruno
Aamon อาม่อน 3.6 บทบาท: Assassin | เลน: Jungle Counters: Bruno
Layla ไลล่า 2.3 บทบาท: Marksman | เลน: Gold Lane Counters: Bruno
Khufra คูฟรา 0.3 บทบาท: Tank | เลน: Roam Counters: Bruno
Gloo กลู 0.2 บทบาท: Tank | เลน: Roam, Exp Lane Counters: Bruno

Claude คลอดด์ ตัวดราฟแก้ทาง
Lesley เลสลี่ย์ 6.9 บทบาท: Marksman, Assassin | เลน: Gold Lane Counters: Claude
Aamon อาม่อน 6.0 บทบาท: Assassin | เลน: Jungle Counters: Claude
Edith อิดิธ 5.0 บทบาท: Tank, Marksman | เลน: Exp Lane, Roam Counters: Claude
Natalia นาตาเลีย 3.9 บทบาท: Assassin | เลน: Jungle, Roam Counters: Claude
Baxia ปาเซีย 2.6 บทบาท: Tank | เลน: Jungle, Roam Counters: Claude
Bruno บรูโน่ 2.5 บทบาท: Marksman | เลน: Gold Lane Counters: Claude
Cyclops ไซคลอปส์ 0.7 บทบาท: Mage | เลน: Mid Lane Counters: Claude
Kaja คาจา 0.6 บทบาท: Support, Fighter | เลน: Roam Counters: Claude

Clint คลินท์ ตัวดราฟแก้ทาง
Fanny แฟนนี่ 4.7 บทบาท: Assassin | เลน: Jungle Counters: Clint
Mathilda มาธิลดา 3.0 บทบาท: Support, Assassin | เลน: Roam Counters: Clint
Gloo กลู 2.9 บทบาท: Tank | เลน: Roam, Exp Lane Counters: Clint
Alice อลิซ 2.5 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Clint
Layla ไลล่า 1.6 บทบาท: Marksman | เลน: Gold Lane Counters: Clint
Khufra คูฟรา 1.5 บทบาท: Tank | เลน: Roam Counters: Clint
Obsidia ออปซิเดีย 0.6 บทบาท: Marksman | เลน: Gold Lane Counters: Clint
Moskov มอสโคฟ 0.2 บทบาท: Marksman | เลน: Gold Lane Counters: Clint

Granger เกรนเจอร์ ตัวดราฟแก้ทาง
Fanny แฟนนี่ 6.8 บทบาท: Assassin | เลน: Jungle Counters: Granger
Hilda ฮิลด้า 5.1 บทบาท: Fighter, Tank | เลน: Roam, Exp Lane Counters: Granger
Mathilda มาธิลดา 4.2 บทบาท: Support, Assassin | เลน: Roam Counters: Granger
Obsidia ฮอปซิเดีย 3.4 บทบาท: Marksman | เลน: Gold Lane Counters: Granger
Esmeralda เอสเมอรัลด้า 3.3 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Granger

Hanabi ฮานาบิ ตัวดราฟแก้ทาง
Lolita โลลิตา 5.3 บทบาท: Support, Tank | เลน: Roam Counters: Hanabi
Beatrix เบียร์ทริก 5.2 บทบาท: Marksman | เลน: Gold Lane Counters: Hanabi
Karina คารีน่า 4.8 บทบาท: Assassin | เลน: Jungle Counters: Hanabi
Joy จอย 4.7 บทบาท: Assassin | เลน: Jungle Counters: Hanabi
Nolan โนแลน 2.4 บทบาท: Assassin | เลน: Jungle Counters: Hanabi
Ixia อิกเซีย 2.3 บทบาท: Marksman | เลน: Gold Lane Counters: Hanabi

Harith ฮาริธ ตัวดราฟแก้ทาง
Phoveus โฟเวียส 8.2 บทบาท: Fighter | เลน: Exp Lane Counters: Harith
Edith อิดิธ 6.7 บทบาท: Tank, Marksman | เลน: Exp Lane, Roam Counters: Harith
Minsitthar มินชิตา 5.6 บทบาท: Fighter | เลน: Exp Lane, Roam Counters: Harith
Alucard อลูการ์ด 4.0 บทบาท: Fighter, Assassin | เลน: Jungle Counters: Harith
Aamon อาม่อน 2.6 บทบาท: Assassin | เลน: Jungle Counters: Harith
Popol and Kupa โปโปลและคูปา 1.8 บทบาท: Marksman | เลน: Jungle, Gold Lane Counters: Harith

Irithel ไอริเทล ตัวดราฟแก้ทาง
Brody โบร์ดี้ 4.6 บทบาท: Marksman | เลน: Gold Lane Counters: Irithel
Eudora ยูโดร่า 4.5 บทบาท: Mage | เลน: Mid Lane Counters: Irithel
Harith ฮาริธ 4.1 บทบาท: Mage | เลน: Gold Lane, Jungle Counters: Irithel
Uranus ยูเรนัส 2.1 บทบาท: Tank | เลน: Exp Lane Counters: Irithel
Karina คารีน่า 2.1 บทบาท: Assassin | เลน: Jungle Counters: Irithel
Hilda ฮิลด้า 2.1 บทบาท: Fighter, Tank | เลน: Roam, Exp Lane Counters: Irithel

Ixia อิกเซีย ตัวดราฟแก้ทาง
Wanwan หวานหว่าน 7.4 บทบาท: Marksman | เลน: Gold Lane Counters: Ixia
Kadita คาดิต้า 5.7 บทบาท: Mage, Assassin | เลน: Mid Lane Counters: Ixia
Hanzo ฮันโซ 5.3 บทบาท: Assassin | เลน: Jungle Counters: Ixia
Atlas แอตลาส 4.3 บทบาท: Tank | เลน: Roam Counters: Ixia
Johnson จอห์นสัน 2.5 บทบาท: Tank, Support | เลน: Roam Counters: Ixia
Claude คลอดด์ 2.3 บทบาท: Marksman | เลน: Gold Lane Counters: Ixia

Karrie คารีย์ ตัวดราฟแก้ทาง
Sun ซัน 7.0 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Karrie
Rafaela ราฟาเอลา 5.7 บทบาท: Support | เลน: Roam Counters: Karrie
Diggie ดิกกี้ 3.7 บทบาท: Support | เลน: Roam Counters: Karrie
Marcel มาเซลล์ 2.6 บทบาท: Support | เลน: Roam Counters: Karrie
Lolita โลลิตา 2.5 บทบาท: Support, Tank | เลน: Roam Counters: Karrie
Minsitthar มินชิตา 2.2 บทบาท: Fighter | เลน: Exp Lane, Roam Counters: Karrie

Kimmy คิมมี่ ตัวดราฟแก้ทาง
Karina คารีน่า 7.7 บทบาท: Assassin | เลน: Jungle Counters: Kimmy
Lolita โลลิตา 7.3 บทบาท: Support, Tank | เลน: Roam Counters: Kimmy
Natalia นาตาเลีย 5.0 บทบาท: Assassin | เลน: Jungle, Roam Counters: Kimmy
Belerick เบเลริค 4.5 บทบาท: Tank | เลน: Roam Counters: Kimmy

Layla ไลล่า ตัวดราฟแก้ทาง
Sun ซัน 7.2 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Layla
Atlas แอตลาส 5.8 บทบาท: Tank | เลน: Roam Counters: Layla
Johnson จอห์นสัน 5.8 บทบาท: Tank, Support | เลน: Roam Counters: Layla
Chip ชิป 2.8 บทบาท: Support, Tank | เลน: Roam Counters: Layla
Hylos ไฮลอส 2.1 บทบาท: Tank | เลน: Roam Counters: Layla
Tigreal ไทเกรียว 1.6 บทบาท: Tank | เลน: Roam Counters: Layla

Lesley เลสลี่ย์ ตัวดราฟแก้ทาง
Sun ซัน 7.6 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Lesley
Estes เอสเตส 6.2 บทบาท: Support | เลน: Roam Counters: Lesley
Gloo กลู 5.7 บทบาท: Tank | เลน: Roam, Exp Lane Counters: Lesley
Tigreal ไทเกรียว 4.1 บทบาท: Tank | เลน: Roam Counters: Lesley
Popol and Kupa โปโปลและคูปา 3.5 บทบาท: Marksman | เลน: Jungle, Gold Lane Counters: Lesley
Melissa เมลิสสา 0.6 บทบาท: Marksman | เลน: Gold Lane Counters: Lesley
Minotaur มิโนทอร์ 0.2 บทบาท: Tank, Support | เลน: Roam Counters: Lesley
Angela แองเจล่า 0.2 บทบาท: Support | เลน: Roam Counters: Lesley

Melissa เมลิสสา ตัวดราฟแก้ทาง
Ixia อิกเซีย 4.5 บทบาท: Marksman | เลน: Gold Lane Counters: Melissa
Harley ฮาร์ลีย์ 4.4 บทบาท: Assassin, Mage | เลน: Mid Lane, Jungle Counters: Melissa
Vale เวล 4.1 บทบาท: Mage | เลน: Mid Lane Counters: Melissa
Layla ไลล่า 2.4 บทบาท: Marksman | เลน: Gold Lane Counters: Melissa
Yi Sun-shin ยีซุนชิน 2.3 บทบาท: Assassin, Marksman | เลน: Jungle Counters: Melissa
Belerick เบเลริค 1.9 บทบาท: Tank | เลน: Roam Counters: Melissa
Baxia ปาเซีย 1.0 บทบาท: Tank | เลน: Jungle, Roam Counters: Melissa
Granger เกรนเจอร์ 0.4 บทบาท: Marksman | เลน: Gold Lane Counters: Melissa

Miya มิยะ ตัวดราฟแก้ทาง
Gatotkaca ฆโฎตกัจ 3.7 บทบาท: Tank, Fighter | เลน: Roam, Exp Lane Counters: Miya
Beatrix เบียร์ทริก 3.6 บทบาท: Marksman | เลน: Gold Lane Counters: Miya
Lolita โลลิตา 3.3 บทบาท: Support, Tank | เลน: Roam Counters: Miya
Belerick เบเลริค 2.4 บทบาท: Tank | เลน: Roam Counters: Miya
Uranus ยูเรนัส 2.2 บทบาท: Tank | เลน: Exp Lane Counters: Miya
Terizla เทริซลา 2.1 บทบาท: Fighter, Tank | เลน: Exp Lane Counters: Miya
Thamuz ธามัส 1.1 บทบาท: Fighter | เลน: Exp Lane Counters: Miya
Barats บารัต 0.7 บทบาท: Tank, Fighter | เลน: Jungle Counters: Miya

Moskov มอสโคฟ ตัวดราฟแก้ทาง
Hanabi ฮานาบิ 4.9 บทบาท: Marksman | เลน: Gold Lane Counters: Moskov
Karina คารีน่า 4.5 บทบาท: Assassin | เลน: Jungle Counters: Moskov
Cyclops ไซคลอปส์ 4.4 บทบาท: Mage | เลน: Mid Lane Counters: Moskov
Masha มาช่า 2.1 บทบาท: Fighter, Tank | เลน: Exp Lane Counters: Moskov
Estes เอสเตส 1.9 บทบาท: Support | เลน: Roam Counters: Moskov
Alpha อัลฟ่า 1.5 บทบาท: Fighter | เลน: Jungle, Exp Lane Counters: Moskov
Eudora ยูโดร่า 0.9 บทบาท: Mage | เลน: Mid Lane Counters: Moskov

Natan นาธาน ตัวดราฟแก้ทาง
Karina คารีน่า 4.3 บทบาท: Assassin | เลน: Jungle Counters: Natan
Lolita โลลิตา 4.3 บทบาท: Support, Tank | เลน: Roam Counters: Natan
Benedetta เบเนเด็ตต้า 2.6 บทบาท: Assassin, Fighter | เลน: Exp Lane Counters: Natan
Baxia ปาเซีย 2.3 บทบาท: Tank | เลน: Jungle, Roam Counters: Natan
Granger เกรนเจอร์ 2.3 บทบาท: Marksman | เลน: Gold Lane Counters: Natan
Arlott อาร์ลอร์ต 1.9 บทบาท: Fighter, Assassin | เลน: Exp Lane Counters: Natan
Nolan โนแลน 1.8 บทบาท: Assassin | เลน: Jungle Counters: Natan
Brody โโบร์ดี้ 1.1 บทบาท: Marksman | เลน: Gold Lane Counters: Natan

Obsidia ฮอปซิเดีย ตัวดราฟแก้ทาง
Baxia ปาเซีย 6.4 บทบาท: Tank | เลน: Jungle, Roam Counters: Obsidia
Estes เอสเตส 5.1 บทบาท: Support | เลน: Roam Counters: Obsidia
Belerick เบเลริค 5.0 บทบาท: Tank | เลน: Roam Counters: Obsidia
Karina คารีน่า 4.4 บทบาท: Assassin | เลน: Jungle Counters: Obsidia
Faramis ฟารามิส 2.7 บทบาท: Support, Mage | เลน: Mid Lane, Roam Counters: Obsidia
Cyclops ไซคลอปส์ 1.1 บทบาท: Mage | เลน: Mid Lane Counters: Obsidia

Popol and Kupa โปโปลและคูปา ตัวดราฟแก้ทาง
Atlas แอตลาส 8.0 บทบาท: Tank | เลน: Roam Counters: Popol and Kupa
Hanabi ฮานาบิ 6.9 บทบาท: Marksman | เลน: Gold Lane Counters: Popol and Kupa
Carmilla คาร์มิลลา 6.7 บทบาท: Support, Tank | เลน: Roam Counters: Popol and Kupa
Alice อลิซ 6.3 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Popol and Kupa
Lapu-Lapu ลาปู-ลาปู 3.6 บทบาท: Fighter | เลน: Exp Lane Counters: Popol and Kupa
Sun ซัน 2.6 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Popol and Kupa

Aldous อัลดัส ตัวดราฟแก้ทาง
Esmeralda เอสเมอรัลด้า 4.9 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Aldous
Karina คารีน่า 4.8 บทบาท: Assassin | เลน: Jungle Counters: Aldous
Dyrroth เดียร์รอธ 3.7 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Aldous
Silvanna ซิลวาน่า 2.9 บทบาท: Fighter | เลน: Exp Lane Counters: Aldous
Paquito ปาคิโต 2.8 บทบาท: Fighter, Assassin | เลน: Exp Lane Counters: Aldous
Cyclops ไซคลอปส์ 2.0 บทบาท: Mage | เลน: Mid Lane Counters: Aldous

Alice อลิซ ตัวดราฟแก้ทาง
Angela แองเจล่า 8.5 บทบาท: Support | เลน: Roam Counters: Alice
Karrie คารีย์ 7.5 บทบาท: Marksman | เลน: Gold Lane Counters: Alice
Estes เอสเตส 7.4 บทบาท: Support | เลน: Roam Counters: Alice
Floryn ฟลอริน 7.2 บทบาท: Support | เลน: Roam Counters: Alice
Cici ซีซี่ 5.6 บทบาท: Fighter | เลน: Exp Lane Counters: Alice

Alpha อัลฟ่า ตัวดราฟแก้ทาง
Diggie ดิกกี้ 6.8 บทบาท: Support | เลน: Roam Counters: Alpha
Benedetta เบเนเด็ตต้า 6.2 บทบาท: Assassin, Fighter | เลน: Exp Lane Counters: Alpha
Wanwan หวานหว่าน 5.5 บทบาท: Marksman | เลน: Gold Lane Counters: Alpha
X.Borg เอ็กซ์บอร์ก 4.7 บทบาท: Fighter | เลน: Exp Lane Counters: Alpha
Kimmy คิมมี่ 2.7 บทบาท: Marksman, Mage | เลน: Mid Lane, Gold Lane Counters: Alpha
Hanzo ฮันโซ 1.0 บทบาท: Assassin | เลน: Jungle Counters: Alpha

Argus อาร์กัส ตัวดราฟแก้ทาง
Uranus ยูเรนัส 6.4 บทบาท: Tank | เลน: Exp Lane Counters: Argus
Terizla เทริซลา 6.1 บทบาท: Fighter, Tank | เลน: Exp Lane Counters: Argus
Barats บารัต 5.8 บทบาท: Tank, Fighter | เลน: Jungle Counters: Argus
Fredrinn เฟรดรินน์ 4.1 บทบาท: Fighter, Tank | เลน: Jungle Counters: Argus
Esmeralda เอสเมอรัลด้า 2.9 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Argus
Lapu-Lapu ลาปู-ลาปู 2.6 บทบาท: Fighter | เลน: Exp Lane Counters: Argus

Arlott อาร์ลอร์ต ตัวดราฟแก้ทาง
Jawhead จอห์นเฮด 3.6 บทบาท: Fighter | เลน: Roam, Exp Lane Counters: Arlott
Hanabi ฮานาบิ 3.4 บทบาท: Marksman | เลน: Gold Lane Counters: Arlott
Zhask แซส์ค 3.3 บทบาท: Mage | เลน: Mid Lane Counters: Arlott
Sun ซัน 3.2 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Arlott
Argus อาร์กัส 2.8 บทบาท: Fighter | เลน: Exp Lane Counters: Arlott

Badang บาดัง ตัวดราฟแก้ทาง
Esmeralda เอสเมอรัลด้า 4.5 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Badang
Karina คารีน่า 4.1 บทบาท: Assassin | เลน: Jungle Counters: Badang
Alice อลิซ 3.4 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Badang
Aulus ออลุส 2.5 บทบาท: Fighter | เลน: Jungle Counters: Badang
Diggie ดิกกี้ 2.3 บทบาท: Support | เลน: Roam Counters: Badang

Balmond บาลมอนด์ ตัวดราฟแก้ทาง
Cici ซีซี่ 9.4 บทบาท: Fighter | เลน: Exp Lane Counters: Balmond
X.Borg เอ็กซ์บอร์ก 7.0 บทบาท: Fighter | เลน: Exp Lane Counters: Balmond
Angela แองเจล่า 6.5 บทบาท: Support | เลน: Roam Counters: Balmond
Diggie ดิกกี้ 6.2 บทบาท: Support | เลน: Roam Counters: Balmond
Kimmy คิมมี่ 3.4 บทบาท: Marksman, Mage | เลน: Mid Lane, Gold Lane Counters: Balmond
Valir วาเรีย 3.1 บทบาท: Mage | เลน: Mid Lane Counters: Balmond
Estes เอสเตส 2.5 บทบาท: Support | เลน: Roam Counters: Balmond

Bane เบน ตัวดราฟแก้ทาง
Lolita โลลิตา 8.8 บทบาท: Support, Tank | เลน: Roam Counters: Bane
Nolan โนแลน 4.8 บทบาท: Assassin | เลน: Jungle Counters: Bane
Atlas แอตลาส 3.6 บทบาท: Tank | เลน: Roam Counters: Bane
Hanzo ฮันโซ 3.1 บทบาท: Assassin | เลน: Jungle Counters: Bane

Benedetta เบเนเด็ตต้า ตัวดราฟแก้ทาง
Obsidia ฮอปซิเดีย 5.7 บทบาท: Marksman | เลน: Gold Lane Counters: Benedetta
Phoveus โฟเวียส 5.3 บทบาท: Fighter | เลน: Exp Lane Counters: Benedetta
Zilong จูล่ง 4.1 บทบาท: Fighter, Assassin | เลน: Exp Lane Counters: Benedetta
Argus อาร์กัส 2.4 บทบาท: Fighter | เลน: Exp Lane Counters: Benedetta
Selena เซเลน่า 2.3 บทบาท: Assassin, Mage | เลน: Mid Lane, Roam Counters: Benedetta

Chou ชู ตัวดราฟแก้ทาง
Cyclops ไซคลอปส์ 4.6 บทบาท: Mage | เลน: Mid Lane Counters: Chou
Phoveus โฟเวียส 4.5 บทบาท: Fighter | เลน: Exp Lane Counters: Chou
Esmeralda เอสเมอรัลด้า 3.9 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Chou
Sun ซัน 1.9 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Chou
Lukas ลูคัส 1.5 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Chou
Popol and Kupa โปโปลและคูปา 1.2 บทบาท: Marksman | เลน: Jungle, Gold Lane Counters: Chou

Cici ซีซี่ ตัวดราฟแก้ทาง
Sun ซัน 8.9 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Cici
Aamon อาม่อน 7.9 บทบาท: Assassin | เลน: Jungle Counters: Cici
Estes เอสเตส 7.4 บทบาท: Support | เลน: Roam Counters: Cici
X.Borg เอ็กซ์บอร์ก 7.0 บทบาท: Fighter | เลน: Exp Lane Counters: Cici
Zilong จูล่ง 5.4 บทบาท: Fighter, Assassin | เลน: Exp Lane Counters: Cici

Dyrroth เดียร์รอธ ตัวดราฟแก้ทาง
Masha มาช่า 5.8 บทบาท: Fighter, Tank | เลน: Exp Lane Counters: Dyrroth
Argus อาร์กัส 4.3 บทบาท: Fighter | เลน: Exp Lane Counters: Dyrroth
Thamuz ธามัส 4.0 บทบาท: Fighter | เลน: Exp Lane Counters: Dyrroth
Khufra คูฟรา 2.9 บทบาท: Tank | เลน: Roam Counters: Dyrroth

Edith อิดิธ ตัวดราฟแก้ทาง
Lolita โลลิตา 9.3 บทบาท: Support, Tank | เลน: Roam Counters: Edith
Layla ไลล่า 5.7 บทบาท: Marksman | เลน: Gold Lane Counters: Edith
Sun ซัน 5.1 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Edith
Beatrix เบียร์ทริก 4.9 บทบาท: Marksman | เลน: Gold Lane Counters: Edith

Esmeralda เอสเมอรัลด้า ตัวดราฟแก้ทาง
Estes เอสเตส 6.0 บทบาท: Support | เลน: Roam Counters: Esmeralda
Dyrroth เดียร์รอธ 5.6 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Esmeralda
Natan นาธาน 5.5 บทบาท: Marksman | เลน: Gold Lane Counters: Esmeralda
Gloo กลู 5.5 บทบาท: Tank | เลน: Roam, Exp Lane Counters: Esmeralda
Fredrinn เฟรดรินน์ 2.9 บทบาท: Fighter, Tank | เลน: Jungle Counters: Esmeralda

Freya เฟรย่า ตัวดราฟแก้ทาง
Phoveus โฟเวียส 9.3 บทบาท: Fighter | เลน: Exp Lane Counters: Freya
Minsitthar มินชิตา 7.5 บทบาท: Fighter | เลน: Exp Lane, Roam Counters: Freya
Edith อิดิธ 4.7 บทบาท: Tank, Marksman | เลน: Exp Lane, Roam Counters: Freya
Esmeralda เอสเมอรัลด้า 3.7 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Freya
Franco ฟรังค์โก้ 3.1 บทบาท: Tank | เลน: Roam Counters: Freya

Gatotkaca ฆโฎตกัจ ตัวดราฟแก้ทาง
X.Borg เอ็กซ์บอร์ก 5.9 บทบาท: Fighter | เลน: Exp Lane Counters: Gatotkaca
Lesley เลสลี่ย์ 5.7 บทบาท: Marksman, Assassin | เลน: Gold Lane Counters: Gatotkaca
Alpha อัลฟ่า 4.4 บทบาท: Fighter | เลน: Jungle, Exp Lane Counters: Gatotkaca
Natalia นาตาเลีย 3.0 บทบาท: Assassin | เลน: Jungle, Roam Counters: Gatotkaca

Gloo กลู ตัวดราฟแก้ทาง
Faramis ฟารามิส 9.2 บทบาท: Support, Mage | เลน: Mid Lane, Roam Counters: Gloo
Moskov มอสโคฟ 9.0 บทบาท: Marksman | เลน: Gold Lane Counters: Gloo
Natan นาธาน 7.2 บทบาท: Marksman | เลน: Gold Lane Counters: Gloo
Ling หลิง 5.7 บทบาท: Assassin | เลน: Jungle Counters: Gloo

Guinevere กวินเนียร์ ตัวดราฟแก้ทาง
Masha มาช่า 5.9 บทบาท: Fighter, Tank | เลน: Exp Lane Counters: Guinevere
Wanwan หวานหว่าน 5.4 บทบาท: Marksman | เลน: Gold Lane Counters: Guinevere
Diggie ดิกกี้ 4.8 บทบาท: Support | เลน: Roam Counters: Guinevere
Khufra คูฟรา 4.3 บทบาท: Tank | เลน: Roam Counters: Guinevere

Hilda ฮิลด้า ตัวดราฟแก้ทาง
Aamon อาม่อน 5.1 บทบาท: Assassin | เลน: Jungle Counters: Hilda
Alpha อัลฟ่า 5.0 บทบาท: Fighter | เลน: Jungle, Exp Lane Counters: Hilda
Esmeralda เอสเมอรัลด้า 4.3 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Hilda
Kimmy คิมมี่ 3.9 บทบาท: Marksman, Mage | เลน: Mid Lane, Gold Lane Counters: Hilda

Jawhead จอห์นเฮด ตัวดราฟแก้ทาง
Sun ซัน 7.4 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Jawhead
Gloo กลู 5.3 บทบาท: Tank | เลน: Roam, Exp Lane Counters: Jawhead
Lolita โลลิตา 5.1 บทบาท: Support, Tank | เลน: Roam Counters: Jawhead
Esmeralda เอสเมอรัลด้า 5.1 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Jawhead
Chip ชิป 3.2 บทบาท: Support, Tank | เลน: Roam Counters: Jawhead

Julian จูเลียน ตัวดราฟแก้ทาง
Guinevere กวินเนียร์ 4.5 บทบาท: Fighter | เลน: Exp Lane Counters: Julian
Baxia ปาเซีย 3.4 บทบาท: Tank | เลน: Jungle, Roam Counters: Julian
Thamuz ธามัส 2.8 บทบาท: Fighter | เลน: Exp Lane Counters: Julian
Minsitthar มินชิตา 2.6 บทบาท: Fighter | เลน: Exp Lane, Roam Counters: Julian

Khaleed คาลีด ตัวดราฟแก้ทาง
Phoveus โฟเวียส 5.9 บทบาท: Fighter | เลน: Exp Lane Counters: Khaleed
Lesley เลสลี่ย์ 3.9 บทบาท: Marksman, Assassin | เลน: Gold Lane Counters: Khaleed
Balmond บาลมอนด์ 2.2 บทบาท: Fighter | เลน: Jungle, Exp Lane Counters: Khaleed

Lapu-Lapu ลาปู-ลาปู ตัวดราฟแก้ทาง
Esmeralda เอสเมอรัลด้า 5.4 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Lapu-Lapu
Kaja คาจา 3.4 บทบาท: Support, Fighter | เลน: Roam Counters: Lapu-Lapu
Fanny แฟนนี่ 3.1 บทบาท: Assassin | เลน: Jungle Counters: Lapu-Lapu
Paquito ปาคิโต 1.7 บทบาท: Fighter, Assassin | เลน: Exp Lane Counters: Lapu-Lapu

Lukas ลูคัส ตัวดราฟแก้ทาง
Baxia ปาเซีย 6.6 บทบาท: Tank | เลน: Jungle, Roam Counters: Lukas
Balmond บาลมอนด์ 6.5 บทบาท: Fighter | เลน: Jungle, Exp Lane Counters: Lukas
Minsitthar มินชิตา 5.8 บทบาท: Fighter | เลน: Exp Lane, Roam Counters: Lukas
Phoveus โฟเวียส 4.5 บทบาท: Fighter | เลน: Exp Lane Counters: Lukas

Martis มาทิซ ตัวดราฟแก้ทาง
X.Borg เอ็กซ์บอร์ก 8.2 บทบาท: Fighter | เลน: Exp Lane Counters: Martis
Minsitthar มินชิตา 5.7 บทบาท: Fighter | เลน: Exp Lane, Roam Counters: Martis
Marcel มาเซลล์ 5.0 บทบาท: Support | เลน: Roam Counters: Martis
Yve อีฟ 2.7 บทบาท: Mage | เลน: Mid Lane Counters: Martis

Masha มาช่า ตัวดราฟแก้ทาง
Argus อาร์กัส 9.7 บทบาท: Fighter | เลน: Exp Lane Counters: Masha
Sun ซัน 9.5 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Masha
Estes เอสเตส 6.6 บทบาท: Support | เลน: Roam Counters: Masha
Uranus ยูเรนัส 5.7 บทบาท: Tank | เลน: Exp Lane Counters: Masha

Minsitthar มินชิตา ตัวดราฟแก้ทาง
Natalia นาตาเลีย 7.5 บทบาท: Assassin | เลน: Jungle, Roam Counters: Minsitthar
Yin หยิน 6.1 บทบาท: Fighter, Assassin | เลน: Jungle, Exp Lane Counters: Minsitthar
Aulus ออลุส 5.5 บทบาท: Fighter | เลน: Jungle Counters: Minsitthar

Paquito ปาคิโต ตัวดราฟแก้ทาง
Esmeralda เอสเมอรัลด้า 6.7 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Paquito
Chip ชิป 4.3 บทบาท: Support, Tank | เลน: Roam Counters: Paquito
Khufra คูฟรา 3.5 บทบาท: Tank | เลน: Roam Counters: Paquito
Melissa เมลิสสา 3.3 บทบาท: Marksman | เลน: Gold Lane Counters: Paquito
Eudora ยูโดร่า 2.6 บทบาท: Mage | เลน: Mid Lane Counters: Paquito

Phoveus โฟเวียส ตัวดราฟแก้ทาง
X.Borg เอ็กซ์บอร์ก 8.1 บทบาท: Fighter | เลน: Exp Lane Counters: Phoveus
Minsitthar มินชิตา 6.9 บทบาท: Fighter | เลน: Exp Lane, Roam Counters: Phoveus
Alpha อัลฟ่า 6.7 บทบาท: Fighter | เลน: Jungle, Exp Lane Counters: Phoveus
Bane เบน 4.9 บทบาท: Fighter, Mage | เลน: Jungle, Exp Lane Counters: Phoveus
Baxia ปาเซีย 4.4 บทบาท: Tank | เลน: Jungle, Roam Counters: Phoveus

Ruby รูบี้ ตัวดราฟแก้ทาง
X.Borg เอ็กซ์บอร์ก 6.5 บทบาท: Fighter | เลน: Exp Lane Counters: Ruby
Phoveus โฟเวียส 5.7 บทบาท: Fighter | เลน: Exp Lane Counters: Ruby
Balmond บาลมอนด์ 3.0 บทบาท: Fighter | เลน: Jungle, Exp Lane Counters: Ruby
Diggie ดิกกี้ 2.9 บทบาท: Support | เลน: Roam Counters: Ruby

Silvanna ซิลวาน่า ตัวดราฟแก้ทาง
Barats บารัต 6.0 บทบาท: Tank, Fighter | เลน: Jungle Counters: Silvanna
Edith อิดิธ 5.4 บทบาท: Tank, Marksman | เลน: Exp Lane, Roam Counters: Silvanna
Benedetta เบเนเด็ตต้า 5.1 บทบาท: Assassin, Fighter | เลน: Exp Lane Counters: Silvanna
Karina คารีน่า 4.9 บทบาท: Assassin | เลน: Jungle Counters: Silvanna
Khufra คูฟรา 3.8 บทบาท: Tank | เลน: Roam Counters: Silvanna

Sora โซรา ตัวดราฟแก้ทาง
Phoveus โฟเวียส 4.5 บทบาท: Fighter | เลน: Exp Lane Counters: Sora
Melissa เมลิสสา 3.6 บทบาท: Marksman | เลน: Gold Lane Counters: Sora
Khufra คูฟรา 3.6 บทบาท: Tank | เลน: Roam Counters: Sora
Alice อลิซ 3.0 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Sora
Valentina วาเลนติน่า 1.5 บทบาท: Mage | เลน: Mid Lane Counters: Sora

Sun ซัน ตัวดราฟแก้ทาง
Natan นาธาน 9.0 บทบาท: Marksman | เลน: Gold Lane Counters: Sun
Aldous อัลดัส 8.9 บทบาท: Fighter | เลน: Exp Lane Counters: Sun
Alucard อลูการ์ด 7.3 บทบาท: Fighter, Assassin | เลน: Jungle Counters: Sun
Faramis ฟารามิส 5.4 บทบาท: Support, Mage | เลน: Mid Lane, Roam Counters: Sun

Terizla เทริซลา ตัวดราฟแก้ทาง
X.Borg เอ็กซ์บอร์ก 9.1 บทบาท: Fighter | เลน: Exp Lane Counters: Terizla
Valir วาเรีย 4.2 บทบาท: Mage | เลน: Mid Lane Counters: Terizla
Gord กอร์ด 4.2 บทบาท: Mage | เลน: Mid Lane Counters: Terizla
Karrie คารีย์ 2.6 บทบาท: Marksman | เลน: Gold Lane Counters: Terizla

Thamuz ธามัส ตัวดราฟแก้ทาง
Cici ซีซี่ 6.6 บทบาท: Fighter | เลน: Exp Lane Counters: Thamuz
Valir วาเรีย 5.2 บทบาท: Mage | เลน: Mid Lane Counters: Thamuz
Wanwan หวานหว่าน 4.4 บทบาท: Marksman | เลน: Gold Lane Counters: Thamuz
Karrie คารีย์ 4.0 บทบาท: Marksman | เลน: Gold Lane Counters: Thamuz
Rafaela ราฟาเอลา 2.5 บทบาท: Support | เลน: Roam Counters: Thamuz

Uranus ยูเรนัส ตัวดราฟแก้ทาง
Dyrroth เดียร์รอธ 6.9 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Uranus
Cici ซีซี่ 6.6 บทบาท: Fighter | เลน: Exp Lane Counters: Thamuz
Estes เอสเตส 5.5 บทบาท: Support | เลน: Roam Counters: Uranus
Karrie คารีย์ 5.3 บทบาท: Marksman | เลน: Gold Lane Counters: Thamuz, Uranus
Valir วาเรีย 5.2 บทบาท: Mage | เลน: Mid Lane Counters: Thamuz

X.Borg เอ็กซ์บอร์ก ตัวดราฟแก้ทาง
Zilong จูล่ง 7.3 บทบาท: Fighter, Assassin | เลน: Exp Lane Counters: X.Borg
Sun ซัน 7.1 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: X.Borg
Helcurt เฮลเคอร์ท 6.9 บทบาท: Assassin | เลน: Jungle, Roam Counters: X.Borg
Paquito ปาคิโต 5.9 บทบาท: Fighter, Assassin | เลน: Exp Lane Counters: X.Borg
Valentina วาเลนติน่า 4.2 บทบาท: Mage | เลน: Mid Lane Counters: X.Borg

Yin หยิน ตัวดราฟแก้ทาง
Wanwan หวานหว่าน 9.0 บทบาท: Marksman | เลน: Gold Lane Counters: Yin
Esmeralda เอสเมอรัลด้า 6.2 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Yin
Kaja คาจา 4.9 บทบาท: Support, Fighter | เลน: Roam Counters: Yin

Yu Zhong อวี่จง ตัวดราฟแก้ทาง
Masha มาช่า 6.9 บทบาท: Fighter, Tank | เลน: Exp Lane Counters: Yu Zhong
Claude คลอดด์ 2.7 บทบาท: Marksman | เลน: Gold Lane Counters: Yu Zhong
Edith อิดิธ 2.3 บทบาท: Tank, Marksman | เลน: Exp Lane, Roam Counters: Yu Zhong

Zilong จูล่ง ตัวดราฟแก้ทาง
Popol and Kupa โปโปลและคูปา 7.0 บทบาท: Marksman | เลน: Jungle, Gold Lane Counters: Zilong
Johnson จอห์นสัน 4.6 บทบาท: Tank, Support | เลน: Roam Counters: Zilong
Diggie ดิกกี้ 3.7 บทบาท: Support | เลน: Roam Counters: Zilong
Chip ชิป 3.4 บทบาท: Support, Tank | เลน: Roam Counters: Zilong
Natan นาธาน 3.3 บทบาท: Marksman | เลน: Gold Lane Counters: Zilong

Aurora ออโรร่า ตัวดราฟแก้ทาง
Benedetta เบเนเด็ตต้า 3.5 บทบาท: Assassin, Fighter | เลน: Exp Lane Counters: Aurora
Diggie ดิกกี้ 3.3 บทบาท: Support | เลน: Roam Counters: Aurora
Beatrix เบียร์ทริก 2.6 บทบาท: Marksman | เลน: Gold Lane Counters: Aurora

Cecilion เซซิเลียน ตัวดราฟแก้ทาง
Hanzo ฮันโซ 3.8 บทบาท: Assassin | เลน: Jungle Counters: Cecilion
Natalia นาตาเลีย 3.1 บทบาท: Assassin | เลน: Jungle, Roam Counters: Cecilion
Hayabusa ฮายาบุซะ 3.0 บทบาท: Assassin | เลน: Jungle Counters: Cecilion
Helcurt เฮลเคอร์ท 2.7 บทบาท: Assassin | เลน: Jungle, Roam Counters: Cecilion

Chang'e ฉางเอ๋อ ตัวดราฟแก้ทาง
Lolita โลลิตา 8.4 บทบาท: Support, Tank | เลน: Roam Counters: Chang'e
Gloo กลู 5.1 บทบาท: Tank | เลน: Roam, Exp Lane Counters: Chang'e
Esmeralda เอสเมอรัลด้า 3.6 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Chang'e
Claude คลอดด์ 2.4 บทบาท: Marksman | เลน: Gold Lane Counters: Chang'e
Irithel ไอริเทล 1.9 บทบาท: Marksman | เลน: Gold Lane Counters: Chang'e

Cyclops ไซคลอปส์ ตัวดราฟแก้ทาง
Lolita โลลิตา 18.5 บทบาท: Support, Tank | เลน: Roam Counters: Cyclops
Estes เอสเตส 9.1 บทบาท: Support | เลน: Roam Counters: Cyclops
Ixia อิกเซีย 5.7 บทบาท: Marksman | เลน: Gold Lane Counters: Cyclops
Minotaur มิโนทอร์ 5.4 บทบาท: Tank, Support | เลน: Roam Counters: Cyclops
Baxia ปาเซีย 3.5 บทบาท: Tank | เลน: Jungle, Roam Counters: Cyclops
Atlas แอตลาส 2.3 บทบาท: Tank | เลน: Roam Counters: Cyclops

Eudora ยูโดร่า ตัวดราฟแก้ทาง
Atlas แอตลาส 6.2 บทบาท: Tank | เลน: Roam Counters: Eudora
Barats บารัต 5.7 บทบาท: Tank, Fighter | เลน: Jungle Counters: Eudora
Masha มาช่า 4.8 บทบาท: Fighter, Tank | เลน: Exp Lane Counters: Eudora
Johnson จอห์นสัน 4.2 บทบาท: Tank, Support | เลน: Roam Counters: Eudora
Zhask แซส์ค 3.4 บทบาท: Mage | เลน: Mid Lane Counters: Eudora

Faramis ฟารามิส ตัวดราฟแก้ทาง
Estes เอสเตส 8.1 บทบาท: Support | เลน: Roam Counters: Faramis
Angela แองเจล่า 6.2 บทบาท: Support | เลน: Roam Counters: Faramis
Floryn ฟลอริน 4.5 บทบาท: Support | เลน: Roam Counters: Faramis
Luo Yi ลั่วยี 3.3 บทบาท: Mage | เลน: Mid Lane Counters: Faramis
Edith อิดิธ 3.2 บทบาท: Tank, Marksman | เลน: Exp Lane, Roam Counters: Faramis
Alice อลิซ 3.2 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Faramis

Gord กอร์ด ตัวดราฟแก้ทาง
Natalia นาตาเลีย 6.8 บทบาท: Assassin | เลน: Jungle, Roam Counters: Gord
Helcurt เฮลเคอร์ท 5.1 บทบาท: Assassin | เลน: Jungle, Roam Counters: Gord
Ling หลิง 4.5 บทบาท: Assassin | เลน: Jungle Counters: Gord
Yin หยิน 3.3 บทบาท: Fighter, Assassin | เลน: Jungle, Exp Lane Counters: Gord

Gusion กูชิออน ตัวดราฟแก้ทาง
Lolita โลลิตา 5.1 บทบาท: Support, Tank | เลน: Roam Counters: Gusion
Khufra คูฟรา 3.7 บทบาท: Tank | เลน: Roam Counters: Gusion
Roger โรเจอร์ 2.4 บทบาท: Fighter, Marksman | เลน: Jungle Counters: Gusion
Leomord ลีโอมอร์ด 1.7 บทบาท: Fighter | เลน: Jungle Counters: Gusion

Harley ฮาร์ลีย์ ตัวดราฟแก้ทาง
Lolita โลลิตา 7.7 บทบาท: Support, Tank | เลน: Roam Counters: Harley
Sun ซัน 6.4 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Harley
Popol and Kupa โปโปลและคูปา 5.1 บทบาท: Marksman | เลน: Jungle, Gold Lane Counters: Harley
Gloo กลู 3.8 บทบาท: Tank | เลน: Roam, Exp Lane Counters: Harley

Kadita คาดิต้า ตัวดราฟแก้ทาง
Marcel มาเซลล์ 5.2 บทบาท: Support | เลน: Roam Counters: Kadita
Alice อลิซ 3.6 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Kadita
Valentina วาเลนติน่า 3.4 บทบาท: Mage | เลน: Mid Lane Counters: Kadita
Kaja คาจา 3.1 บทบาท: Support, Fighter | เลน: Roam Counters: Kadita

Kagura คาคุระ ตัวดราฟแก้ทาง
Phoveus โฟเวียส 4.1 บทบาท: Fighter | เลน: Exp Lane Counters: Kagura
Esmeralda เอสเมอรัลด้า 3.2 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Kagura
Hilda ฮิลด้า 2.6 บทบาท: Fighter, Tank | เลน: Roam, Exp Lane Counters: Kagura
Kaja คาจา 2.2 บทบาท: Support, Fighter | เลน: Roam Counters: Kagura

Lunox ลูน็อกซ์ ตัวดราฟแก้ทาง
Fredrinn เฟรดรินน์ 4.8 บทบาท: Fighter, Tank | เลน: Jungle Counters: Lunox
Ruby รูบี้ 4.3 บทบาท: Fighter | เลน: Exp Lane Counters: Lunox
Estes เอสเตส 3.7 บทบาท: Support | เลน: Roam Counters: Lunox
Saber เซเบอร์ 2.3 บทบาท: Assassin | เลน: Jungle, Roam Counters: Lunox
Barats บารัต 2.0 บทบาท: Tank, Fighter | เลน: Jungle Counters: Lunox

Luo Yi ลั่วยี ตัวดราฟแก้ทาง
Hanzo ฮันโซ 3.4 บทบาท: Assassin | เลน: Jungle Counters: Luo Yi
Novaria โนวาเรีย 2.9 บทบาท: Mage | เลน: Mid Lane Counters: Luo Yi
Lolita โลลิตา 2.8 บทบาท: Support, Tank | เลน: Roam Counters: Luo Yi
Marcel มาเซลล์ 2.7 บทบาท: Support | เลน: Roam Counters: Luo Yi

Lylia ลิเลีย ตัวดราฟแก้ทาง
Mathilda มาธิลดา 3.3 บทบาท: Support, Assassin | เลน: Roam Counters: Lylia
Joy จอย 3.0 บทบาท: Assassin | เลน: Jungle Counters: Lylia
Rafaela ราฟาเอลา 2.6 บทบาท: Support | เลน: Roam Counters: Lylia

Nana นาน่า ตัวดราฟแก้ทาง
Gloo กลู 4.9 บทบาท: Tank | เลน: Roam, Exp Lane Counters: Nana
Hylos ไฮลอส 3.3 บทบาท: Tank | เลน: Roam Counters: Nana
Akai อะไค 2.9 บทบาท: Tank | เลน: Roam Counters: Nana
Sun ซัน 1.7 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Nana

Novaria โนวาเรีย ตัวดราฟแก้ทาง
Hilda ฮิลด้า 5.8 บทบาท: Fighter, Tank | เลน: Roam, Exp Lane Counters: Novaria
Natalia นาตาเลีย 5.2 บทบาท: Assassin | เลน: Jungle, Roam Counters: Novaria
Zilong จูล่ง 4.3 บทบาท: Fighter, Assassin | เลน: Exp Lane Counters: Novaria
Aldous อัลดัส 3.1 บทบาท: Fighter | เลน: Exp Lane Counters: Novaria
Gloo กลู 2.4 บทบาท: Tank | เลน: Roam, Exp Lane Counters: Novaria
Ling หลิง 2.2 บทบาท: Assassin | เลน: Jungle Counters: Novaria

Odette โอเด็ดด์ ตัวดราฟแก้ทาง
Vale เวล 5.3 บทบาท: Mage | เลน: Mid Lane Counters: Odette
Fredrinn เฟรดรินน์ 4.9 บทบาท: Fighter, Tank | เลน: Jungle Counters: Odette
Nana นาน่า 3.5 บทบาท: Mage | เลน: Mid Lane Counters: Odette
Aurora ออโรร่า 3.3 บทบาท: Mage | เลน: Mid Lane Counters: Odette

Pharsa ฟาร์ซ่า ตัวดราฟแก้ทาง
Natalia นาตาเลีย 4.4 บทบาท: Assassin | เลน: Jungle, Roam Counters: Pharsa
Masha มาช่า 2.8 บทบาท: Fighter, Tank | เลน: Exp Lane Counters: Pharsa
Hirara ฮิราระ 1.4 บทบาท: Assassin | เลน: Jungle Counters: Pharsa
Aldous อัลดัส 1.3 บทบาท: Fighter | เลน: Exp Lane Counters: Pharsa

Selena เซเลน่า ตัวดราฟแก้ทาง
Popol and Kupa โปโปลและคูปา 5.2 บทบาท: Marksman | เลน: Jungle, Gold Lane Counters: Selena
Gloo กลู 4.8 บทบาท: Tank | เลน: Roam, Exp Lane Counters: Selena
Chip ชิป 4.3 บทบาท: Support, Tank | เลน: Roam Counters: Selena
Johnson จอห์นสัน 3.4 บทบาท: Tank, Support | เลน: Roam Counters: Selena
Sun ซัน 1.9 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Selena
Lolita โลลิตา 1.5 บทบาท: Support, Tank | เลน: Roam Counters: Selena

Vale เวล ตัวดราฟแก้ทาง
Gloo กลู 3.8 บทบาท: Tank | เลน: Roam, Exp Lane Counters: Vale
Alice อลิซ 3.5 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Vale
Khaleed คาลีด 3.4 บทบาท: Fighter | เลน: Roam, Exp Lane Counters: Vale
Hylos ไฮลอส 2.8 บทบาท: Tank | เลน: Roam Counters: Vale

Valentina วาเลนติน่า ตัวดราฟแก้ทาง
Phoveus โฟเวียส 4.9 บทบาท: Fighter | เลน: Exp Lane Counters: Valentina
Minsitthar มินชิตา 4.8 บทบาท: Fighter | เลน: Exp Lane, Roam Counters: Valentina
Barats บารัต 3.9 บทบาท: Tank, Fighter | เลน: Jungle Counters: Valentina
Marcel มาเซลล์ 3.0 บทบาท: Support | เลน: Roam Counters: Valentina
Julian จูเลียน 2.6 บทบาท: Assassin, Fighter | เลน: Jungle, Exp Lane Counters: Valentina
Johnson จอห์นสัน 1.7 บทบาท: Tank, Support | เลน: Roam Counters: Valentina

Valir วาเรีย ตัวดราฟแก้ทาง
Rafaela ราฟาเอลา 7.0 บทบาท: Support | เลน: Roam Counters: Valir
Helcurt เฮลเคอร์ท 5.3 บทบาท: Assassin | เลน: Jungle, Roam Counters: Valir
Lolita โลลิตา 4.9 บทบาท: Support, Tank | เลน: Roam Counters: Valir
Ling หลิง 4.9 บทบาท: Assassin | เลน: Jungle Counters: Valir
Nolan โนแลน 2.7 บทบาท: Assassin | เลน: Jungle Counters: Valir

Vexana เว็กซ์ซานา ตัวดราฟแก้ทาง
Alice อลิซ 5.2 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Vexana
Natalia นาตาเลีย 4.2 บทบาท: Assassin | เลน: Jungle, Roam Counters: Vexana
X.Borg เอ็กซ์บอร์ก 3.5 บทบาท: Fighter | เลน: Exp Lane Counters: Vexana
Marcel มาเซลล์ 3.4 บทบาท: Support | เลน: Roam Counters: Vexana
Kimmy คิมมี่ 1.9 บทบาท: Marksman, Mage | เลน: Mid Lane, Gold Lane Counters: Vexana

Xavier ซาเวียร์ ตัวดราฟแก้ทาง
Natalia นาตาเลีย 7.9 บทบาท: Assassin | เลน: Jungle, Roam Counters: Xavier
Lolita โลลิตา 5.6 บทบาท: Support, Tank | เลน: Roam Counters: Xavier
Helcurt เฮลเคอร์ท 4.6 บทบาท: Assassin | เลน: Jungle, Roam Counters: Xavier
Angela แองเจล่า 4.6 บทบาท: Support | เลน: Roam Counters: Xavier
Aamon อาม่อน 3.0 บทบาท: Assassin | เลน: Jungle Counters: Xavier

Yve อีฟ ตัวดราฟแก้ทาง
Fanny แฟนนี่ 6.3 บทบาท: Assassin | เลน: Jungle Counters: Yve
Joy จอย 4.2 บทบาท: Assassin | เลน: Jungle Counters: Yve
Helcurt เฮลเคอร์ท 4.1 บทบาท: Assassin | เลน: Jungle, Roam Counters: Yve
Freya เฟรย่า 3.2 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Yve
Hayabusa ฮายาบุซะ 2.4 บทบาท: Assassin | เลน: Jungle Counters: Yve
Selena เซเลน่า 2.3 บทบาท: Assassin, Mage | เลน: Mid Lane, Roam Counters: Yve

Zetian บูเซ็กเทียน ตัวดราฟแก้ทาง
Gloo กลู 4.4 บทบาท: Tank | เลน: Roam, Exp Lane Counters: Zetian
Valentina วาเลนติน่า 3.9 บทบาท: Mage | เลน: Mid Lane Counters: Zetian
Harith ฮาริธ 3.1 บทบาท: Mage | เลน: Gold Lane, Jungle Counters: Zetian
Baxia ปาเซีย 2.9 บทบาท: Tank | เลน: Jungle, Roam Counters: Zetian

Zhask แซส์ค ตัวดราฟแก้ทาง
Natan นาธาน 6.4 บทบาท: Marksman | เลน: Gold Lane Counters: Zhask
Alice อลิซ 5.4 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Zhask
Estes เอสเตส 4.2 บทบาท: Support | เลน: Roam Counters: Zhask
Belerick เบเลริค 3.3 บทบาท: Tank | เลน: Roam Counters: Zhask
Vexana เว็กซ์ซานา 2.7 บทบาท: Mage | เลน: Mid Lane Counters: Zhask

Zhuxin จูซิน ตัวดราฟแก้ทาง
Hayabusa ฮายาบุซะ 4.3 บทบาท: Assassin | เลน: Jungle Counters: Zhuxin
Valir วาเรีย 3.5 บทบาท: Mage | เลน: Mid Lane Counters: Zhuxin
Diggie ดิกกี้ 2.3 บทบาท: Support | เลน: Roam Counters: Zhuxin
Melissa เมลิสสา 2.2 บทบาท: Marksman | เลน: Gold Lane Counters: Zhuxin
Rafaela ราฟาเอลา 2.1 บทบาท: Support | เลน: Roam Counters: Zhuxin

Akai อะไค ตัวดราฟแก้ทาง
Alice อลิซ 5.9 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Akai
Marcel มาเซลล์ 5.5 บทบาท: Support | เลน: Roam Counters: Akai
Esmeralda เอสเมอรัลด้า 5.3 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Akai
Cici ซีซี่ 4.3 บทบาท: Fighter | เลน: Exp Lane Counters: Akai
Yve อีฟ 3.2 บทบาท: Mage | เลน: Mid Lane Counters: Akai
Hanabi ฮานาบิ 1.9 บทบาท: Marksman | เลน: Gold Lane Counters: Akai

Angela แองเจล่า ตัวดราฟแก้ทาง
Lolita โลลิตา 6.9 บทบาท: Support, Tank | เลน: Roam Counters: Angela
Franco ฟรังค์โก้ 5.5 บทบาท: Tank | เลน: Roam Counters: Angela
Zilong จูล่ง 5.0 บทบาท: Fighter, Assassin | เลน: Exp Lane Counters: Angela
Nolan โนแลน 2.5 บทบาท: Assassin | เลน: Jungle Counters: Angela
Silvanna ซิลวาน่า 2.3 บทบาท: Fighter | เลน: Exp Lane Counters: Angela

Atlas แอตลาส ตัวดราฟแก้ทาง
Marcel มาเซลล์ 11.5 บทบาท: Support | เลน: Roam Counters: Atlas
Wanwan หวานหว่าน 7.5 บทบาท: Marksman | เลน: Gold Lane Counters: Atlas
Alice อลิซ 6.3 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Atlas
Ling หลิง 4.9 บทบาท: Assassin | เลน: Jungle Counters: Atlas
Lancelot แลนสลอต 2.9 บทบาท: Assassin | เลน: Jungle Counters: Atlas
Valentina วาเลนติน่า 1.4 บทบาท: Mage | เลน: Mid Lane Counters: Atlas

Baxia ปาเซีย ตัวดราฟแก้ทาง
X.Borg เอ็กซ์บอร์ก 9.1 บทบาท: Fighter | เลน: Exp Lane Counters: Baxia
Nolan โนแลน 5.3 บทบาท: Assassin | เลน: Jungle Counters: Baxia
Fanny แฟนนี่ 5.3 บทบาท: Assassin | เลน: Jungle Counters: Baxia
Beatrix เบียร์ทริก 4.9 บทบาท: Marksman | เลน: Gold Lane Counters: Baxia
Granger เกรนเจอร์ 3.7 บทบาท: Marksman | เลน: Gold Lane Counters: Baxia
Joy จอย 2.5 บทบาท: Assassin | เลน: Jungle Counters: Baxia

Belerick เบเลริค ตัวดราฟแก้ทาง
Lesley เลสลี่ย์ 5.2 บทบาท: Marksman, Assassin | เลน: Gold Lane Counters: Belerick
X.Borg เอ็กซ์บอร์ก 5.1 บทบาท: Fighter | เลน: Exp Lane Counters: Belerick
Aldous อัลดัส 3.9 บทบาท: Fighter | เลน: Exp Lane Counters: Belerick
Cici ซีซี่ 3.6 บทบาท: Fighter | เลน: Exp Lane Counters: Belerick
Xavier ซาเวียร์ 2.7 บทบาท: Mage | เลน: Mid Lane Counters: Belerick

Carmilla คาร์มิลลา ตัวดราฟแก้ทาง
Valentina วาเลนติน่า 6.4 บทบาท: Mage | เลน: Mid Lane Counters: Carmilla
X.Borg เอ็กซ์บอร์ก 6.1 บทบาท: Fighter | เลน: Exp Lane Counters: Carmilla
Benedetta เบเนเด็ตต้า 3.7 บทบาท: Assassin, Fighter | เลน: Exp Lane Counters: Carmilla
Wanwan หวานหว่าน 2.4 บทบาท: Marksman | เลน: Gold Lane Counters: Carmilla
Lesley เลสลี่ย์ 2.3 บทบาท: Marksman, Assassin | เลน: Gold Lane Counters: Carmilla
Diggie ดิกกี้ 2.1 บทบาท: Support | เลน: Roam Counters: Carmilla

Chip ชิป ตัวดราฟแก้ทาง
Carmilla คาร์มิลลา 7.4 บทบาท: Support, Tank | เลน: Roam Counters: Chip
Marcel มาเซลล์ 7.1 บทบาท: Support | เลน: Roam Counters: Chip
Alice อลิซ 6.6 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Chip
Hanabi ฮานาบิ 4.7 บทบาท: Marksman | เลน: Gold Lane Counters: Chip
Zhask แซส์ค 3.1 บทบาท: Mage | เลน: Mid Lane Counters: Chip

Diggie ดิกกี้ ตัวดราฟแก้ทาง
Sun ซัน 7.1 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Diggie
Hanzo ฮันโซ 7.1 บทบาท: Assassin | เลน: Jungle Counters: Diggie
Esmeralda เอสเมอรัลด้า 6.9 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Diggie
Chang'e ฉางเอ๋อ 5.4 บทบาท: Mage | เลน: Mid Lane Counters: Diggie
Estes เอสเตส 4.1 บทบาท: Support | เลน: Roam Counters: Diggie
Beatrix เบียร์ทริก 3.5 บทบาท: Marksman | เลน: Gold Lane Counters: Diggie

Estes เอสเตส ตัวดราฟแก้ทาง
Ixia อิกเซีย 9.7 บทบาท: Marksman | เลน: Gold Lane Counters: Estes
Nolan โนแลน 9.5 บทบาท: Assassin | เลน: Jungle Counters: Estes
Beatrix เบียร์ทริก 9.3 บทบาท: Marksman | เลน: Gold Lane Counters: Estes
Sora โซรา 7.4 บทบาท: Fighter, Assassin | เลน: Exp Lane Counters: Estes
Carmilla คาร์มิลลา 3.3 บทบาท: Support, Tank | เลน: Roam Counters: Estes
Luo Yi ลั่วยี 3.0 บทบาท: Mage | เลน: Mid Lane Counters: Estes

Floryn ฟลอริน ตัวดราฟแก้ทาง
Lolita โลลิตา 9.0 บทบาท: Support, Tank | เลน: Roam Counters: Floryn
Ixia อิกเซีย 5.7 บทบาท: Marksman | เลน: Gold Lane Counters: Floryn
Yin หยิน 5.3 บทบาท: Fighter, Assassin | เลน: Jungle, Exp Lane Counters: Floryn
Baxia ปาเซีย 3.4 บทบาท: Tank | เลน: Jungle, Roam Counters: Floryn
Nolan โนแลน 3.1 บทบาท: Assassin | เลน: Jungle Counters: Floryn
Franco ฟรังค์โก้ 2.4 บทบาท: Tank | เลน: Roam Counters: Floryn
Silvanna ซิลวาน่า 2.4 บทบาท: Fighter | เลน: Exp Lane Counters: Floryn
Beatrix เบียร์ทริก 0.2 บทบาท: Marksman | เลน: Gold Lane Counters: Floryn

Franco ฟรังค์โก้ ตัวดราฟแก้ทาง
Hanzo ฮันโซ 5.3 บทบาท: Assassin | เลน: Jungle Counters: Franco
Sun ซัน 4.9 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Franco
Tigreal ไทเกรียว 4.9 บทบาท: Tank | เลน: Roam Counters: Franco
Johnson จอห์นสัน 4.6 บทบาท: Tank, Support | เลน: Roam Counters: Franco
Zhask แซส์ค 2.7 บทบาท: Mage | เลน: Mid Lane Counters: Franco

Grock กร็อก ตัวดราฟแก้ทาง
Alice อลิซ 6.5 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Grock
Valentina วาเลนติน่า 4.6 บทบาท: Mage | เลน: Mid Lane Counters: Grock
Esmeralda เอสเมอรัลด้า 4.5 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Grock
Yve อีฟ 3.5 บทบาท: Mage | เลน: Mid Lane Counters: Grock
Marcel มาเซลล์ 2.4 บทบาท: Support | เลน: Roam Counters: Grock

Helcurt เฮลเคอร์ท ตัวดราฟแก้ทาง
Argus อาร์กัส 6.7 บทบาท: Fighter | เลน: Exp Lane Counters: Helcurt
Karina คารีน่า 6.2 บทบาท: Assassin | เลน: Jungle Counters: Helcurt
Aldous อัลดัส 5.6 บทบาท: Fighter | เลน: Exp Lane Counters: Helcurt
Obsidia ฮอปซิเดีย 5.4 บทบาท: Marksman | เลน: Gold Lane Counters: Helcurt
Chip ชิป 3.7 บทบาท: Support, Tank | เลน: Roam Counters: Helcurt

Hylos ไฮลอส ตัวดราฟแก้ทาง
X.Borg เอ็กซ์บอร์ก 7.1 บทบาท: Fighter | เลน: Exp Lane Counters: Hylos
Valir วาเรีย 4.8 บทบาท: Mage | เลน: Mid Lane Counters: Hylos
Cici ซีซี่ 4.7 บทบาท: Fighter | เลน: Exp Lane Counters: Hylos
Kimmy คิมมี่ 3.0 บทบาท: Marksman, Mage | เลน: Mid Lane, Gold Lane Counters: Hylos
Alice อลิซ 2.4 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Hylos

Johnson จอห์นสัน ตัวดราฟแก้ทาง
Gloo กลู 7.0 บทบาท: Tank | เลน: Roam, Exp Lane Counters: Johnson
Alice อลิซ 6.0 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Johnson
Alpha อัลฟ่า 4.8 บทบาท: Fighter | เลน: Jungle, Exp Lane Counters: Johnson
Balmond บาลมอนด์ 4.5 บทบาท: Fighter | เลน: Jungle, Exp Lane Counters: Johnson
Kadita คาดิต้า 3.6 บทบาท: Mage, Assassin | เลน: Mid Lane Counters: Johnson

Kaja คาจา ตัวดราฟแก้ทาง
Lesley เลสลี่ย์ 4.2 บทบาท: Marksman, Assassin | เลน: Gold Lane Counters: Kaja
Cyclops ไซคลอปส์ 4.0 บทบาท: Mage | เลน: Mid Lane Counters: Kaja
Odette โอเด็ดด์ 2.0 บทบาท: Mage | เลน: Mid Lane Counters: Kaja
Eudora ยูโดร่า 2.0 บทบาท: Mage | เลน: Mid Lane Counters: Kaja

Kalea คาเลอา ตัวดราฟแก้ทาง
Hanzo ฮันโซ 4.3 บทบาท: Assassin | เลน: Jungle Counters: Kalea, Kaja
Lesley เลสลี่ย์ 4.2 บทบาท: Marksman, Assassin | เลน: Gold Lane Counters: Kaja
Cyclops ไซคลอปส์ 4.0 บทบาท: Mage | เลน: Mid Lane Counters: Kaja
Hanabi ฮานาบิ 3.6 บทบาท: Marksman | เลน: Gold Lane Counters: Kalea

Khufra คูฟรา ตัวดราฟแก้ทาง
Alice อลิซ 6.5 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Khufra
Marcel มาเซลล์ 5.8 บทบาท: Support | เลน: Roam Counters: Khufra
Zhuxin จูซิน 4.5 บทบาท: Mage | เลน: Mid Lane Counters: Khufra
Arlott อาร์ลอร์ต 2.9 บทบาท: Fighter, Assassin | เลน: Exp Lane Counters: Khufra
Estes เอสเตส 2.8 บทบาท: Support | เลน: Roam Counters: Khufra
Minotaur มิโนทอร์ 2.3 บทบาท: Tank, Support | เลน: Roam Counters: Khufra

Lolita โลลิตา ตัวดราฟแก้ทาง
Aurora ออโรร่า 11.5 บทบาท: Mage | เลน: Mid Lane Counters: Lolita
Yve อีฟ 10.9 บทบาท: Mage | เลน: Mid Lane Counters: Lolita
Esmeralda เอสเมอรัลด้า 10.6 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Lolita
Kadita คาดิต้า 7.6 บทบาท: Mage, Assassin | เลน: Mid Lane Counters: Lolita
Zhuxin จูซิน 5.2 บทบาท: Mage | เลน: Mid Lane Counters: Lolita
Melissa เมลิสสา 4.8 บทบาท: Marksman | เลน: Gold Lane Counters: Lolita

Marcel มาเซลล์ ตัวดราฟแก้ทาง
Angela แองเจล่า 9.9 บทบาท: Support | เลน: Roam Counters: Marcel
Lesley เลสลี่ย์ 8.2 บทบาท: Marksman, Assassin | เลน: Gold Lane Counters: Marcel
Floryn ฟลอริน 8.1 บทบาท: Support | เลน: Roam Counters: Marcel
Cyclops ไซคลอปส์ 7.7 บทบาท: Mage | เลน: Mid Lane Counters: Marcel
Rafaela ราฟาเอลา 7.5 บทบาท: Support | เลน: Roam Counters: Marcel

Mathilda มาธิลดา ตัวดราฟแก้ทาง
Esmeralda เอสเมอรัลด้า 8.4 บทบาท: Tank, Mage | เลน: Exp Lane Counters: Mathilda
Odette โอเด็ดด์ 5.4 บทบาท: Mage | เลน: Mid Lane Counters: Mathilda
Edith อิดิธ 4.2 บทบาท: Tank, Marksman | เลน: Exp Lane, Roam Counters: Mathilda
Popol and Kupa โปโปลและคูปา 3.7 บทบาท: Marksman | เลน: Jungle, Gold Lane Counters: Mathilda

Minotaur มิโนทอร์ ตัวดราฟแก้ทาง
Alice อลิซ 5.0 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Minotaur
Beatrix เบียร์ทริก 3.9 บทบาท: Marksman | เลน: Gold Lane Counters: Minotaur
Carmilla คาร์มิลลา 3.7 บทบาท: Support, Tank | เลน: Roam Counters: Minotaur
Luo Yi ลั่วยี 3.0 บทบาท: Mage | เลน: Mid Lane Counters: Minotaur
Yve อีฟ 2.9 บทบาท: Mage | เลน: Mid Lane Counters: Minotaur

Rafaela ราฟาเอลา ตัวดราฟแก้ทาง
Odette โอเด็ดด์ 6.2 บทบาท: Mage | เลน: Mid Lane Counters: Rafaela
Ixia อิกเซีย 5.9 บทบาท: Marksman | เลน: Gold Lane Counters: Rafaela
Layla ไลล่า 5.3 บทบาท: Marksman | เลน: Gold Lane Counters: Rafaela
Vale เวล 5.3 บทบาท: Mage | เลน: Mid Lane Counters: Rafaela
Silvanna ซิลวาน่า 4.7 บทบาท: Fighter | เลน: Exp Lane Counters: Rafaela

Tigreal ไทเกรียว ตัวดราฟแก้ทาง
Alice อลิซ 7.0 บทบาท: Tank, Mage | เลน: Exp Lane, Jungle Counters: Tigreal
X.Borg เอ็กซ์บอร์ก 5.1 บทบาท: Fighter | เลน: Exp Lane Counters: Tigreal
Balmond บาลมอนด์ 4.3 บทบาท: Fighter | เลน: Jungle, Exp Lane Counters: Tigreal
Valir วาเรีย 4.2 บทบาท: Mage | เลน: Mid Lane Counters: Tigreal
Diggie ดิกกี้ 2.9 บทบาท: Support | เลน: Roam Counters: Tigreal
Zetian บูเซ็กเทียน 2.9 บทบาท: Mage | เลน: Mid Lane Counters: Tigreal

Aamon อาม่อน ตัวดราฟแก้ทาง
Gloo กลู 9.4 บทบาท: Tank | เลน: Roam, Exp Lane Counters: Aamon
Hayabusa ฮายาบุซะ 6.3 บทบาท: Assassin | เลน: Jungle Counters: Aamon
Silvanna ซิลวาน่า 6.2 บทบาท: Fighter | เลน: Exp Lane Counters: Aamon
Lolita โลลิตา 5.8 บทบาท: Support, Tank | เลน: Roam Counters: Aamon
Atlas แอตลาส 5.1 บทบาท: Tank | เลน: Roam Counters: Aamon

Alucard อลูการ์ด ตัวดราฟแก้ทาง
Khufra คูฟรา 6.6 บทบาท: Tank | เลน: Roam Counters: Alucard
Barats บารัต 6.6 บทบาท: Tank, Fighter | เลน: Jungle Counters: Alucard
Fredrinn เฟรดรินน์ 6.6 บทบาท: Fighter, Tank | เลน: Jungle Counters: Alucard
Phoveus โฟเวียส 3.9 บทบาท: Fighter | เลน: Exp Lane Counters: Alucard
Akai อะไค 3.3 บทบาท: Tank | เลน: Roam Counters: Alucard

Aulus ออลุส ตัวดราฟแก้ทาง
Kaja คาจา 5.9 บทบาท: Support, Fighter | เลน: Roam Counters: Aulus
Estes เอสเตส 3.8 บทบาท: Support | เลน: Roam Counters: Aulus
Zhuxin จูซิน 2.8 บทบาท: Mage | เลน: Mid Lane Counters: Aulus
Yve อีฟ 2.6 บทบาท: Mage | เลน: Mid Lane Counters: Aulus
Cici ซีซี่ 2.4 บทบาท: Fighter | เลน: Exp Lane Counters: Aulus

Barats บารัต ตัวดราฟแก้ทาง
X.Borg เอ็กซ์บอร์ก 12.5 บทบาท: Fighter | เลน: Exp Lane Counters: Barats
Gord กอร์ด 8.4 บทบาท: Mage | เลน: Mid Lane Counters: Barats
Alpha อัลฟ่า 6.6 บทบาท: Fighter | เลน: Jungle, Exp Lane Counters: Barats
Balmond บาลมอนด์ 3.7 บทบาท: Fighter | เลน: Jungle, Exp Lane Counters: Barats
Hanzo ฮันโซ 3.4 บทบาท: Assassin | เลน: Jungle Counters: Barats
Valir วาเรีย 3.1 บทบาท: Mage | เลน: Mid Lane Counters: Barats

Fanny แฟนนี่ ตัวดราฟแก้ทาง
Franco ฟรังค์โก้ 6.0 บทบาท: Tank | เลน: Roam Counters: Fanny
Bruno บรูโน่ 5.4 บทบาท: Marksman | เลน: Gold Lane Counters: Fanny
Masha มาช่า 4.2 บทบาท: Fighter, Tank | เลน: Exp Lane Counters: Fanny
Badang บาดัง 3.7 บทบาท: Fighter | เลน: Roam, Exp Lane Counters: Fanny
Chou ชู 2.6 บทบาท: Fighter | เลน: Exp Lane, Roam Counters: Fanny
Kalea คาเลอา 2.2 บทบาท: Support, Fighter | เลน: Roam Counters: Fanny

Fredrinn เฟรดรินน์ ตัวดราฟแก้ทาง
Valir วาเรีย 6.4 บทบาท: Mage | เลน: Mid Lane Counters: Fredrinn
Gord กอร์ด 4.9 บทบาท: Mage | เลน: Mid Lane Counters: Fredrinn
Cici ซีซี่ 3.9 บทบาท: Fighter | เลน: Exp Lane Counters: Fredrinn
Diggie ดิกกี้ 3.6 บทบาท: Support | เลน: Roam Counters: Fredrinn

Hanzo ฮันโซ ตัวดราฟแก้ทาง
Natalia นาตาเลีย 10.1 บทบาท: Assassin | เลน: Jungle, Roam Counters: Hanzo
Sun ซัน 7.9 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Hanzo
Ling หลิง 6.5 บทบาท: Assassin | เลน: Jungle Counters: Hanzo
Hirara ฮิราระ 5.8 บทบาท: Assassin | เลน: Jungle Counters: Hanzo
Helcurt เฮลเคอร์ท 3.0 บทบาท: Assassin | เลน: Jungle, Roam Counters: Hanzo
Kimmy คิมมี่ 3.0 บทบาท: Marksman, Mage | เลน: Mid Lane, Gold Lane Counters: Hanzo

Hayabusa ฮายาบุซะ ตัวดราฟแก้ทาง
Chip ชิป 4.0 บทบาท: Support, Tank | เลน: Roam Counters: Hayabusa
Obsidia ฮอปซิเดีย 3.2 บทบาท: Marksman | เลน: Gold Lane Counters: Hayabusa
Yin หยิน 2.6 บทบาท: Fighter, Assassin | เลน: Jungle, Exp Lane Counters: Hayabusa
Zhask แซส์ค 2.4 บทบาท: Mage | เลน: Mid Lane Counters: Hayabusa
Saber เซเบอร์ 2.3 บทบาท: Assassin | เลน: Jungle, Roam Counters: Hayabusa
Sun ซัน 2.2 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Hayabusa

Hirara ฮิราระ ตัวดราฟแก้ทาง
Saber เซเบอร์ 5.1 บทบาท: Assassin | เลน: Jungle, Roam Counters: Hirara
Cyclops ไซคลอปส์ 5.0 บทบาท: Mage | เลน: Mid Lane Counters: Hirara
Phoveus โฟเวียส 4.7 บทบาท: Fighter | เลน: Exp Lane Counters: Hirara
Odette โอเด็ดด์ 4.6 บทบาท: Mage | เลน: Mid Lane Counters: Hirara
Minsitthar มินชิตา 2.5 บทบาท: Fighter | เลน: Exp Lane, Roam Counters: Hirara
Alucard อลูการ์ด 1.9 บทบาท: Fighter, Assassin | เลน: Jungle Counters: Hirara

Joy จอย ตัวดราฟแก้ทาง
Moskov มอสโคฟ 7.1 บทบาท: Marksman | เลน: Gold Lane Counters: Joy
Cyclops ไซคลอปส์ 6.0 บทบาท: Mage | เลน: Mid Lane Counters: Joy
Brody โบร์ดี้ 4.6 บทบาท: Marksman | เลน: Gold Lane Counters: Joy
Eudora ยูโดร่า 2.3 บทบาท: Mage | เลน: Mid Lane Counters: Joy
Ruby รูบี้ 2.2 บทบาท: Fighter | เลน: Exp Lane Counters: Joy
Hirara ฮิราระ 2.1 บทบาท: Assassin | เลน: Jungle Counters: Joy
Melissa เมลิสสา 2.1 บทบาท: Marksman | เลน: Gold Lane Counters: Joy

Lancelot แลนสลอต ตัวดราฟแก้ทาง
Angela แองเจล่า 5.7 บทบาท: Support | เลน: Roam Counters: Lancelot
Floryn ฟลอริน 4.1 บทบาท: Support | เลน: Roam Counters: Lancelot
Marcel มาเซลล์ 4.0 บทบาท: Support | เลน: Roam Counters: Lancelot
Cyclops ไซคลอปส์ 3.3 บทบาท: Mage | เลน: Mid Lane Counters: Lancelot

Leomord ลีโอมอร์ด ตัวดราฟแก้ทาง
Valir วาเรีย 5.9 บทบาท: Mage | เลน: Mid Lane Counters: Leomord
Karrie คารีย์ 4.6 บทบาท: Marksman | เลน: Gold Lane Counters: Leomord
Melissa เมลิสสา 4.6 บทบาท: Marksman | เลน: Gold Lane Counters: Leomord
Zhuxin จูซิน 4.6 บทบาท: Mage | เลน: Mid Lane Counters: Leomord
Yve อีฟ 2.3 บทบาท: Mage | เลน: Mid Lane Counters: Leomord
Hanzo ฮันโซ 1.9 บทบาท: Assassin | เลน: Jungle Counters: Leomord

Ling หลิง ตัวดราฟแก้ทาง
Natalia นาตาเลีย 10.8 บทบาท: Assassin | เลน: Jungle, Roam Counters: Ling
Lukas ลูคัส 6.3 บทบาท: Fighter | เลน: Exp Lane, Jungle Counters: Ling
Saber เซเบอร์ 6.3 บทบาท: Assassin | เลน: Jungle, Roam Counters: Ling
Cyclops ไซคลอปส์ 5.6 บทบาท: Mage | เลน: Mid Lane Counters: Ling
Floryn ฟลอริน 2.6 บทบาท: Support | เลน: Roam Counters: Ling

Nolan โนแลน ตัวดราฟแก้ทาง
Natalia นาตาเลีย 6.7 บทบาท: Assassin | เลน: Jungle, Roam Counters: Nolan
Hilda ฮิลด้า 5.8 บทบาท: Fighter, Tank | เลน: Roam, Exp Lane Counters: Nolan
Saber เซเบอร์ 5.7 บทบาท: Assassin | เลน: Jungle, Roam Counters: Nolan
Hayabusa ฮายาบุซะ 4.6 บทบาท: Assassin | เลน: Jungle Counters: Nolan
Khaleed คาลีด 3.3 บทบาท: Fighter | เลน: Roam, Exp Lane Counters: Nolan

Roger โรเจอร์ ตัวดราฟแก้ทาง
Leomord ลีโอมอร์ด 3.6 บทบาท: Fighter | เลน: Jungle Counters: Roger
Zhuxin จูซิน 2.7 บทบาท: Mage | เลน: Mid Lane Counters: Roger
Ruby รูบี้ 2.3 บทบาท: Fighter | เลน: Exp Lane Counters: Roger
Uranus ยูเรนัส 2.0 บทบาท: Tank | เลน: Exp Lane Counters: Roger

Suyou ซูโหยว ตัวดราฟแก้ทาง
Harith ฮาริธ 4.1 บทบาท: Mage | เลน: Gold Lane, Jungle Counters: Suyou
Silvanna ซิลวาน่า 3.5 บทบาท: Fighter | เลน: Exp Lane Counters: Suyou
Harley ฮาร์ลีย์ 3.1 บทบาท: Assassin, Mage | เลน: Jungle, Mid Lane Counters: Suyou
Joy จอย 3.0 บทบาท: Assassin | เลน: Jungle Counters: Suyou
Odette โอเด็ดด์ 1.8 บทบาท: Mage | เลน: Mid Lane Counters: Suyou

Yi Sun-shin ยีซุนชิน ตัวดราฟแก้ทาง
Uranus ยูเรนัส 4.5 บทบาท: Tank | เลน: Exp Lane Counters: Yi Sun-shin
Karina คารีน่า 4.0 บทบาท: Assassin | เลน: Jungle Counters: Yi Sun-shin
Johnson จอห์นสัน 3.5 บทบาท: Tank, Support | เลน: Roam Counters: Yi Sun-shin
Hayabusa ฮายาบุซะ 3.0 บทบาท: Assassin | เลน: Jungle Counters: Yi Sun-shin
Lolita โลลิตา 2.3 บทบาท: Support, Tank | เลน: Roam Counters: Yi Sun-shin
Aamon อาม่อน 1.2 บทบาท: Assassin | เลน: Jungle Counters: Yi Sun-shin
Mathilda มาธิลดา 0.2 บทบาท: Support, Assassin | เลน: Roam Counters: Yi Sun-shin
Cyclops ไซคลอปส์ 0.2 บทบาท: Mage | เลน: Mid Lane Counters: Yi Sun-shin
"""

# พจนานุกรมสรุปความสามารถของฮีโร่ทุกตัว (ครบถ้วนทุกตัว)
hero_abilities = {
    "Minsitthar": "มีความสามารถในการดึง ล็อคเป้าหมาย และยกเลิกสกิลพุ่งตัวของฮีโร่สายไฟต์เตอร์/แอสซาซิน",
    "Faramis": "มีความสามารถในการสร้างโล่ชุบชีวิตเพื่อนร่วมทีมและทำดาเมจวงกว้าง",
    "Edith": "มีความสามารถในการสลับร่างเป็นแทงค์รับดาเมจและเปลี่ยนเป็นมาร์คแมนยิงไกลเพื่อทำดาเมจปิดเกม",
    "Natan": "มีความสามารถในการสร้างดาเมจเวทแบบรัวๆ และโจมตีระยะไกลทะลุเกราะป้องกัน",
    "Popol and Kupa": "มีความสามารถในการเรียกหมาป่าช่วยโจมตี สตันศัตรู และเปิดวิสัยทัศน์แผนที่",
    "Alucard": "มีความสามารถในการดูดเลือดสูง ไล่ล่าศัตรูได้อย่างรวดเร็ว และสร้างดาเมจต่อเนื่อง",
    "Sun": "มีความสามารถในการสร้างแยกร่างเพื่อป่วนแนวหลัง ดันป้อมเร็ว และรุมศัตรู",
    "Lukas": "มีความสามารถในการพุ่งเข้าประชิดตัวและสร้างคอมโบสกิลที่รุนแรงเพื่อกดดันเลน",
    "Phoveus": "มีความสามารถในการกดใช้งานอัลติเมทได้รัวๆ เมื่อศัตรูมีการพุ่งตัว เหมาะสำหรับแก้ทางฮีโร่พุ่งเยอะ",
    "Aldous": "มีความสามารถในการเก็บสะสมแต้มสแตก ทำให้การโจมตีรุนแรงถึงตายได้ในช่วงท้ายเกม",
    "Esmeralda": "มีความสามารถในการดูดโล่ของศัตรูมาเป็นเกราะป้องกันให้ตนเองและมีความคล่องตัวสูง",
    "Cyclops": "มีความสามารถในการล็อคเป้าหมายด้วยอัลติเมทและปล่อยลูกบอลเวทโจมตีได้อย่างต่อเนื่อง",
    "Beatrix": "มีความสามารถในการเปลี่ยนอาวุธปืนได้หลากหลายรูปแบบเพื่อรับมือกับสถานการณ์ต่างๆ",
    "Khufra": "มีความสามารถในการแปลงร่างเป็นลูกบอลเพื่อหยุดสกิลพุ่งตัวของศัตรูและควบคุมหมู่",
    "Marcel": "มีความสามารถในการสนับสนุนเพื่อนร่วมทีมและสร้างสถานการณ์พลิกแพลงในไฟต์",
    "Granger": "มีความสามารถในการยิงกระสุนเบิสต์ดาเมจระยะไกลด้วยปืนคู่ได้อย่างรวดเร็วและรุนแรง",
    "Joy": "มีความสามารถในการแดชเคลื่อนที่ตามจังหวะดนตรีพร้อมสร้างความเสียหายเวทอย่างต่อเนื่อง",
    "Wanwan": "มีความสามารถในการกระโดดหลบสกิลและปลดอัลติเมทเพื่อโจมตีศัตรูอย่างรวดเร็ว",
    "Obsidia": "มีความสามารถในการโจมตีระยะไกลและสร้างดาเมจกดดันเลนได้อย่างยอดเยี่ยม",
    "Moskov": "มีความสามารถในการโจมตีทะลุเป้าหมายและการันตีการตรึงศัตรูติดกำแพง",
    "Irithel": "มีความสามารถในการยิงโจมตีต่อเนื่องในขณะที่กำลังเคลื่อนที่",
    "Brody": "มีความสามารถในการสะสมสแตกหมัดและปล่อยดาเมจระเบิดที่รุนแรงต่อเป้าหมาย",
    "Barats": "มีความสามารถในการสะสมพลังเพิ่มขนาดตัวและกลืนกินศัตรูเพื่อแยกออกจากไฟต์",
    "Gloo": "มีความสามารถในการเกาะติดร่างศัตรูเพื่อปั่นป่วนและควบคุมทิศทาง",
    "Atlas": "มีความสามารถในการดึงและกระชากศัตรูจำนวนมากเข้ามารวมกันเพื่อเปิดไฟต์",
    "Diggie": "มีความสามารถในการแก้สถานะควบคุมทั้งหมด (CC) ให้กับเพื่อนร่วมทีมด้วยอัลติเมท",
    "Masha": "มีความสามารถในการเพิ่มความเร็วโจมตีและมีหลอดเลือดถึง 3 หลอดทำให้ตื๊ดมาก",
    "Lolita": "มีความสามารถในการกางโล่สะท้อนกระสุนและการันตีการสตันหมู่ด้วยค้อนยักษ์",
    "Lesley": "มีความสามารถในการตอดเลือดระยะไกลด้วยคริติคอลและความสามารถในการอำพรางตัว",
    "Estes": "มีความสามารถในการฟื้นฟูพลังชีวิตหมู่ให้กับเพื่อนร่วมทีมอย่างมหาศาล",
    "Karina": "มีความสามารถในการรีเซ็ตคูลดาวน์สกิลเมื่อสังหารได้และสะท้อนการโจมตีปกติ",
    "Aamon": "มีความสามารถในการหายตัวและรวบรวมเศษชิ้นส่วนเพื่อทำดาเมจเบิสต์ใส่ศัตรู",
    "Layla": "มีความสามารถในการโจมตีระยะไกลยิ่งไกลยิ่งแรง",
    "Clint": "มีความสามารถในการยิงสกิลสลับกับการโจมตีปกติเพื่อสร้างดาเมจบีสท์คริติคอล",
    "Fanny": "มีความสามารถในการโหนสลิงไปทั่วแผนที่เพื่อเข้าหาและสังหารศัตรูอย่างรวดเร็ว",
    "Mathilda": "มีความสามารถในการสร้างโล่และพาเพื่อนร่วมทีมบินหนีหรือพุ่งเข้าหาศัตรู",
    "Alice": "มีความสามารถในการดูดเลือดรอบตัวและเทเลพอร์ตสร้างดาเมจเวทหมู่",
    "Hanabi": "มีความสามารถในการเด้งการโจมตีใส่ศัตรูหลายตัวและมีเกราะต้านสถานะ",
    "Hilda": "มีความสามารถในการฟื้นฟูเลือดในพุ่มไม้และสร้างดาเมจกายภาพที่รุนแรง",
    "Ixia": "มีความสามารถในการกางลานยิงปืนใหญ่วงกว้างเพื่อทำลายล้างแนวหน้า",
    "Karrie": "มีความสามารถในการโจมตีเจาะเกราะตามสัดส่วนเลือดเหมาะสำหรับฆ่าแทงค์",
    "Kimmy": "มีความสามารถในการยิงกระสุนปืนกลในขณะที่เดินเคลื่อนที่ไปพร้อมกัน",
    "Melissa": "มีความสามารถในการปักตุ๊กตากันไม่ให้ศัตรูเข้าประชิดตัว",
    "Miya": "มีความสามารถในการหายตัวและเพิ่มความเร็วในการโจมตีอย่างรวดเร็ว",
    "Gatotkaca": "มีความสามารถในการกระโดดกระแทกจากฟ้าและเปลี่ยนเกราะรับดาเมจเป็นพลังโจมตี",
    "Guinevere": "มีความสามารถในการกระโดดลอยตัวและสร้างคอมโบสกิลสตันกลางอากาศ",
    "Jawhead": "มีความสามารถในการโยนเป้าหมายเข้าหาเพื่อนหรือปาออกไปเพื่อเปิดจังหวะ",
    "Julian": "มีความสามารถในการผสมผสานสกิลทั้ง 3 เพื่อเลือกใช้ท่าที่เหมาะสมกับสถานการณ์",
    "Khaleed": "มีความสามารถในการพุ่งเข้าใส่และนั่งฟื้นฟูเลือดต้านดาเมจ",
    "Lapu-Lapu": "มีความสามารถในการเปลี่ยนร่างเป็นดาบคู่เพื่อรับดาเมจและโจมตีหมู่รุนแรง",
    "Martis": "มีความสามารถในการฟันกวาดและใช้อัลติเมทฟันซ้ำได้หากสังหารสำเร็จ",
    "Paquito": "มีความสามารถในการสะสมสแตกต่อยคอมโบสกิลรัวๆ อย่างรวดเร็ว",
    "Ruby": "มีความสามารถในการดูดเลือดสูงและดึงศัตรูเข้ามาด้วยเคียวเกี่ยว",
    "Silvanna": "มีความสามารถในการพุ่งแทงและกรงขังศัตรูไว้ในพื้นที่จำกัด",
    "Sora": "มีความสามารถในการสร้างดาเมจและเคลื่อนที่เข้าประชิดตัวเป้าหมายได้อย่างคล่องตัว",
    "Terizla": "มีความสามารถในการทุบทำลายวงกว้างและดึงศัตรูด้วยโซ่มหาภัย",
    "Thamuz": "มีความสามารถในการเผาไหม้รอบตัวและโจมตีระยะประชิดด้วยความดุดัน",
    "Uranus": "มีความสามารถในการฟื้นฟูเลือดตัวเองอย่างต่อเนื่องและเคลื่อนที่ไว",
    "X.Borg": "มีความสามารถในการพ่นไฟระยะประชิดและเกราะนอกที่ช่วยป้องกันความตาย",
    "Yin": "มีความสามารถในการลากศัตรูเข้าไปสู้ตัวต่อตัวในมิติแยก",
    "Yu Zhong": "มีความสามารถในการแปลงร่างเป็นมังกรพุ่งทะยานและดูดเลือดหมู่",
    "Zilong": "มีความสามารถในการวิ่งด้วยความเร็วสูงและตวัดศัตรูมาด้านหลัง",
    "Aurora": "มีความสามารถในการแช่แข็งเป้าหมายให้หยุดนิ่งด้วยพลังน้ำแข็ง",
    "Cecilion": "มีความสามารถในการปล่อยกระสุนเวทระยะไกลยิ่งยาวยิ่งสะสมมานาแรง",
    "Chang'e": "มีความสามารถในการยิงกระสุนดาวกระจายเวทใส่ศัตรูอย่างรวดเร็ว",
    "Eudora": "มีความสามารถในการปล่อยสายฟ้าช็อตศัตรูให้ตายในชุดเดียว",
    "Gord": "มีความสามารถในการยิงลำแสงเลเซอร์เวทมนตร์ทำลายล้างเป็นเส้นตรง",
    "Gusion": "มีความสามารถในการปามีดสั้นและพุ่งสลับไปมาด้วยความเร็วสูง",
    "Harley": "มีความสามารถในการปาหมวกเทเลพอร์ตและระเบิดวงแหวนเวท",
    "Kadita": "มีความสามารถในการแปลงร่างเป็นคลื่นน้ำพุ่งชนและสร้างสึนามิหมู่",
    "Kagura": "มีความสามารถในการถือร่มสลับตำแหน่งเพื่อป่วนและสร้างดาเมจเวท",
    "Lunox": "มีความสามารถในการสลับโหมดแสงและมืดเพื่อสร้างดาเมจหรือป้องกันตัว",
    "Luo Yi": "มีความสามารถในการสลับขั้วหยิน-หยางเพื่อดึงศัตรูกระแทกกันและเทเลพอร์ตทีม",
    "Lylia": "มีความสามารถในการวางระเบิดลูกบอลจิ๋วและย้อนเวลากลับไปฟื้นฟูเลือด",
    "Nana": "มีความสามารถในการแปลงร่างศัตรูให้เป็นแมวเหมียวและคืนชีพหนีตาย",
    "Novaria": "มีความสามารถในการเปิดเผยวิสัยทัศน์ทั่วแผนที่และยิงกระสุนสไนเปอร์ระยะไกล",
    "Odette": "มีความสามารถในการร่ายเพลงมาร่วมสร้างคลื่นเสียงดาเมจวงกว้าง",
    "Pharsa": "มีความสามารถในการแปลงร่างเป็นนกบินหนีและยิงปืนใหญ่เวทจากระยะไกล",
    "Selena": "มีความสามารถในการปาบัตรศรสตันและแปลงร่างเป็นร่างปีศาจ",
    "Vale": "มีความสามารถในการสร้างพายุหมุนระเบิดเวททำลายล้าง",
    "Valentina": "มีความสามารถในการขโมยอัลติเมทของศัตรูมาใช้เอง",
    "Valir": "มีความสามารถในการสาดเปลวไฟผลักศัตรูออกไปและล้างสถานะควบคุม",
    "Vexana": "มีความสามารถในการเรียกหุ่นยนต์ยักษ์อัญเชิญมาช่วยทุบศัตรู",
    "Xavier": "มีความสามารถในการยิงลำแสงข้ามแมพและสร้างกำแพงขยายระยะ",
    "Yve": "มีความสามารถในการตีตารางพื้นที่สี่เหลี่ยมเพื่อทำดาเมจและสโลว์",
    "Zetian": "มีความสามารถในการควบคุมพื้นที่และสร้างความปั่นป่วนด้วยพลังเวท",
    "Zhask": "มีความสามารถในการปักเสาเอเลี่ยนช่วยยิงโจมตีต่อเนื่อง",
    "Zhuxin": "มีความสามารถในการจับศัตรูลอยขึ้นฟ้าและโยนทิ้งตามใจชอบ",
    "Akai": "มีความสามารถในการหมุนตัวเป็นแพนด้ากลิ้งกระแทกศัตรูออกจากไฟต์",
    "Angela": "มีความสามารถในการสิงร่างเพื่อนร่วมทีมเพื่อโล่คุ้มกันและฮีล",
    "Belerick": "มีความสามารถในการสะท้อนดาเมจกลับใส่ผู้โจมตีและยึดตรึงศัตรู",
    "Carmilla": "มีความสามารถในการเชื่อมโยงคำสาปแชร์ดาเมจให้ศัตรูรอบตัว",
    "Chip": "มีความสามารถในการสร้างประตูมิติเทเลพอร์ตเพื่อนร่วมทีมข้ามเลน",
    "Grock": "มีความสามารถในการสร้างกำแพงหินขวางทางและเพิ่มเกราะเมื่ออยู่ใกล้กำแพง",
    "Helcurt": "มีความสามารถในการปิดตาความมืดมิดทั่วแผนที่และลอบสังหาร",
    "Hylos": "มีความสามารถในการสร้างทางเดินเพิ่มความเร็วและยืนรับดาเมจหน้าแนว",
    "Johnson": "มีความสามารถในการแปลงร่างเป็นรถยนต์พุ่งชนพร้อมพาเพื่อนร่วมทีมขับซิ่ง",
    "Kaja": "มีความสามารถในการใช้แส้ลากกระชากศัตรูออกมาจากแนวหลัง",
    "Kalea": "มีความสามารถในการสนับสนุนเพื่อนและป่วนไฟต์ด้วยสกิลควบคุม",
    "Minotaur": "มีความสามารถในการกระโดดทุบพื้นโกรธเกรี้ยวเพื่อสตันหมู่และฮีลเลือด",
    "Rafaela": "มีความสามารถในการเร่งความเร็วเคลื่อนที่และฮีลเลือดให้ทีมพร้อมสโลว์ศัตรู",
    "Tigreal": "มีความสามารถในการผลักดันและอัลติเมทดูดศัตรูกระแทกพื้นหมู่",
    "Aulus": "มีความสามารถในการทุบขวานยักษ์และยิ่งเวลามากยิ่งเก่งขึ้น",
    "Saber": "มีความสามารถในการล็อคเป้าหมายลอยฟ้าและฟันฉับเดียวดับ",
    "Suyou": "มีความสามารถในการสลับรูปแบบการโจมตีทั้งรวดเร็วและรุนแรง",
    "Yi Sun-shin": "มีความสามารถในการยิงธนูและฟันดาบสลับระยะ พร้อมใช้เรือเปิดแมพ",
    "Hanzo": "มีความสามารถในการปลดร่างเงาปีศาจออกไปฟาร์มและโจมตีแนวหลังจากระยะไกลได้อย่างปลอดภัย",
    "Nolan": "มีความสามารถในการสร้างรอยแยกมิติเพื่อสะสมดาเมจเบิสต์และเคลื่อนที่พุ่งทะลวงได้อย่างรวดเร็วต่อเนื่อง"
}

# ---------------------------------------------------------
# 3. ฟังก์ชันคำนวณ (พร้อมระบบกรองฮีโร่ฝั่งตรงข้ามออก)
# ---------------------------------------------------------
@st.cache_data
def parse_database(data_string):
    db = {}
    thai_to_eng = {} 
    current_target = ""
    
    for line in data_string.strip().split('\n'):
        line = line.strip()
        if not line: 
            continue
            
        if "ตัวดราฟแก้ทาง" in line:
            name_part = line.replace("ตัวดราฟแก้ทาง", "").strip()
            match_thai = re.search(r'[ก-๙]', name_part)
            if match_thai:
                idx = match_thai.start()
                eng_name = name_part[:idx].strip()
                th_name = name_part[idx:].strip()
            else:
                eng_name = name_part.strip()
                th_name = name_part.strip()
                
            current_target = eng_name.lower()
            thai_to_eng[th_name] = current_target
            db[current_target] = []
            
        elif "Counters:" in line:
            try:
                part1, part2 = line.split(" บทบาท: ")
                tokens = part1.split()
                score = float(tokens[-1])
                
                match_thai = re.search(r'[ก-๙]', part1)
                if match_thai:
                    idx = match_thai.start()
                    c_eng_name = part1[:idx].strip()
                    c_th_name = part1[idx:part1.rfind(tokens[-1])].strip()
                else:
                    c_eng_name = " ".join(tokens[:-1])
                    c_th_name = " ".join(tokens[:-1])
                
                role_part, rest = part2.split(" | เลน: ")
                lane_part, target_part = rest.split(" Counters: ")
                
                thai_to_eng[c_th_name.strip()] = c_eng_name.strip().lower()
                
                if current_target in db:
                    db[current_target].append({
                        "name": c_eng_name.strip(),
                        "th_name": c_th_name.strip(),
                        "score": score,
                        "role": role_part.strip(),
                        "lane": lane_part.strip()
                    })
            except Exception:
                continue
                
    return db, thai_to_eng

def analyze_counters(enemy_team_input, database, thai_to_eng):
    lanes = ["Roam", "Gold Lane", "Jungle", "Exp Lane", "Mid Lane"]
    suggestions = {lane: {} for lane in lanes}
    all_thai_names = list(thai_to_eng.keys())
    
    processed_enemies = []
    messages = []
    
    for item in enemy_team_input:
        clean_name = item.strip()
        if not clean_name:
            continue
        if clean_name in thai_to_eng:
            processed_enemies.append(thai_to_eng[clean_name])
        else:
            matches = difflib.get_close_matches(clean_name, all_thai_names, n=1, cutoff=0.6)
            if matches:
                closest_name = matches[0]
                messages.append(f"ℹ️ ระบบปรับคำว่า '{clean_name}' เป็น '{closest_name}' ให้โดยอัตโนมัติ")
                processed_enemies.append(thai_to_eng[closest_name])
            else:
                processed_enemies.append(clean_name.lower())

    # สร้างเซตรายชื่อฮีโร่ฝั่งตรงข้ามที่ค้นหา ไว้เช็กกรองออก
    enemy_keys_set = set(e.strip().lower() for e in processed_enemies)

    for enemy in processed_enemies:
        enemy_key = enemy.strip().lower()
        if enemy_key in database:
            for counter in database[enemy_key]:
                c_name = counter['name']
                
                # กรองออก: หากฮีโร่แนะนำเป็นตัวเดียวกับที่พิมพ์ค้นหาฝั่งตรงข้าม ให้ข้ามไป
                if c_name.strip().lower() in enemy_keys_set:
                    continue
                
                hero_lanes = [l.strip() for l in counter['lane'].split(',')]
                for l in hero_lanes:
                    if l in suggestions:
                        if c_name not in suggestions[l]:
                            suggestions[l][c_name] = {
                                "th_name": counter['th_name'],
                                "total_score": 0.0,
                                "reasons": []
                            }
                        suggestions[l][c_name]['total_score'] += counter['score']
                        suggestions[l][c_name]['reasons'].append(f"ชนะทาง {enemy.capitalize()}")
        else:
            messages.append(f"⚠️ ไม่พบข้อมูลของฮีโร่: {enemy}")

    final_picks = {}
    for lane in lanes:
        sorted_heroes = sorted(suggestions[lane].items(), key=lambda x: x[1]['total_score'], reverse=True)
        final_picks[lane] = sorted_heroes[:3]
            
    return final_picks, messages

# ---------------------------------------------------------
# 4. ส่วนหน้าตาแอปพลิเคชัน (Streamlit UI)
# ---------------------------------------------------------
db, thai_to_eng = parse_database(raw_data)

user_input = st.text_input(
    "🔍 พิมพ์ชื่อตัวละครฝั่งตรงข้าม (ใช้เครื่องหมาย , คั่นระหว่างชื่อ):",
    placeholder="เช่น: ลีโอมอด, ฆโฎตกัจ, เอสเตส, ลาปู-ลาปู"
)

if user_input:
    enemy_team = [h.strip() for h in user_input.split(",") if h.strip()]
    results, messages = analyze_counters(enemy_team, db, thai_to_eng)
    
    for msg in messages:
        st.toast(msg)

    st.subheader("🤖 AI Draft Coach แนะนำตัวแก้ทาง")
    
    tabs = st.tabs(["🛡️ ROAM", "🏹 GOLD LANE", "🗡️ JUNGLE", "⚔️ EXP LANE", "🔮 MID LANE"])
    lane_map = {
        "🛡️ ROAM": "Roam",
        "🏹 GOLD LANE": "Gold Lane",
        "🗡️ JUNGLE": "Jungle",
        "⚔️ EXP LANE": "Exp Lane",
        "🔮 MID LANE": "Mid Lane"
    }

    for tab_name, lane_key in lane_map.items():
        tab_index = list(lane_map.keys()).index(tab_name)
        with tabs[tab_index]:
            heroes = results.get(lane_key, [])
            if not heroes:
                st.info("⏳ รออัพเดตข้อมูลตัวดราฟแก้ฮีโร่สำหรับเลนนี้")
            else:
                for idx, (hero_name, data) in enumerate(heroes):
                    rank = idx + 1
                    th_name = data['th_name']
                    score = round(data['total_score'], 1)
                    reasons = ", ".join(data['reasons'])
                    score_label = "คะแนนรวม" if len(data['reasons']) > 1 else "คะแนน"
                    
                    if rank == 1:
                        st.success(f"⭐ **{rank}. {hero_name} ({th_name}) - 🔥 แนะนำสุดๆ! 🔥**")
                        st.write(f"💡 **เหตุผล:** {reasons} | **{score_label}:** {score}")
                        
                        if hero_name in hero_abilities:
                            ability_desc = hero_abilities[hero_name]
                            st.info(f"📝 **สรุปการเลือก {hero_name} ({th_name})**: เนื่องจากตัวละครนี้{ability_desc} จึงเหมาะอย่างยิ่งในการนำมาแก้ทางในตำแหน่งนี้")
                        st.divider()
                    else:
                        st.write(f"**{rank}. {hero_name} ({th_name})**")
                        st.caption(f"💡 เหตุผล: {reasons} | {score_label}: {score}")
                        st.divider()
