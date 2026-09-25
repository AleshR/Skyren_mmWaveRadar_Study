# HLK-LD2450 — zpětné zapojení

KiCad 10 projekt pro etapu 2 dílu Praxe ve studii (`docs/mmwave_radar_study.tex`).
Obsahuje zapojení modulu HLK-LD2450 zakreslené z fotek a z manuálu výrobce,
které se doplní prozvoněním. Desku nevyrábíme, proto projekt nemá `.kicad_pcb`.

**Stav:** rozpracováno z fotek `img/IMG_2152`, `IMG_2153` a z manuálu v1.0
(`docs/datasheet/`). Nic není prozvoněné ani změřené.

```bash
open hw/ld2450/ld2450.kicad_pro
```

| Soubor | Obsah |
|---|---|
| `ld2450.kicad_sch` | schéma: součástky z fotek, poznámky a hypotézy |
| `sym-lib-table` | připojí sdílenou knihovnu `../lib/re_generic.kicad_sym` |

## Součástky

Čísla odpovídají dílu Rozbor ve studii (obr. `fig:ld2450a`, `fig:ld2450b`).

| Ref | Č. | Pouzdro, potisk | Pravděpodobná role |
|---|---|---|---|
| U1 | 1 | QFN-32 4×4, Hi-Link `HLK24…` | radarový čip, snad S3KM111L |
| Q1 | 2 | SOT-23, `3400` | tranzistor, role neznámá |
| J3 | 3 | 6 plošek DM DP TX RX PA9 GND, rozteč 2,0 mm | servisní rozhraní USB a UART |
| J4 | 4 | 2×4 plošky pod úhlovou lištou, rozteč 2,0 mm | totéž a napájení 3,3 a 5 V |
| U4, L1 | 5 | obvod `KD`, tlumivka | měnič z 5 na 3,3 V |
| Y1 | 6 | krystal 25,000 MHz | reference PLL pro U1 |
| U3 | 7 | SOT-23-5, `J5JK` | stabilizátor pro U1 |
| U2 | 8 | QFN-32 4×4, jen logo | MCU (výrobce: „levné MCU“), s IPEX nejspíš i Bluetooth |
| Y2 | 9 | krystal 24,000 MHz | takt U2 |
| J2 | 10 | IPEX | anténa Bluetooth na kabelu |
| J1 | 11 | zásuvka 1,5 mm, 5V RX TX GND | výstup modulu |
| D1 | 12 | dioda | ochrana proti přepólování? |
| AE1–AE3 | — | patch antény Tx, Rx1, Rx2 | 1T2R |

## Konvence schématu

- Obvody neznámého typu mají generické symboly z `hw/lib/re_generic.kicad_sym`.
  Vývody nesou jen čísla a leží jako na pouzdře při pohledu shora. U QFN je
  vývod 1 vlevo nahoře a číslování jde proti směru hodinových ručiček, 33 je
  odhalená ploška. Až bude typ jasný, nahradí se skutečným symbolem.
- Spojená je jen zem konektorů. Ostatní sítě mají předponu konektoru
  (`J1_TX`, `J3_TX`, …), protože stejný potisk ještě neznamená stejný spoj.
  Po prozvonění se sítě sloučí přejmenováním.
- J1 je číslovaný podle obr. 4 manuálu, shora 5V, RX, TX, GND. Ostatní
  konektory jsou číslované podle pořadí potisku.
- Každá součástka má pole Studie (číslo z dílu Rozbor), Potisk a Ověřit.
  Hypotéza o roli je v poli Description.
- Pasivní součástky (R, C) zatím nejsou zakreslené.
- ERC teď hlásí tři druhy chyb. Nepřipojené vývody jsou seznam toho, co
  zbývá prozvonit. Dál popisky na jediném vývodu a nebuzené vstupy antén.
  S prozváněním jich bude ubývat.

## Etapa 2: co zjistit

Výrobce popisuje hardware jako radarový čip s vlastním zpracováním signálu
a levné MCU, takže U2 je MCU. Otevřené zůstává, kolik práce dělá U1:
buď posílá vzorky a cíle počítá U2 (hypotéza A), nebo počítá cíle sám
a U2 je jen předává (hypotéza B).

- [ ] makrosnímky s bočním světlem, přečíst potisky U2, U3, U4 a D1
- [ ] kam vedou `J1_TX` a `J1_RX`: na U1, nebo na U2
- [ ] počet linek mezi U1 a U2: dvě znamenají UART (B), čtyři a víc
      sběrnici (A)
- [ ] Y1, `RF_TX`, `RF_RX1` a `RF_RX2` → vývody U1
- [ ] Y2 a `BT_ANT` → vývody U2
- [ ] DM, DP a PA9 z J3 a J4 → U2? Jsou J3 a J4 paralelně?
- [ ] cesta napájení: `J1_5V`, `J4_5V`, D1, Q1
- [ ] za provozu napětí za U4 + L1 a za U3
- [ ] test USB: DM, DP, 5V a GND na kabel, pak PA9 přes 10 kΩ na GND a na 3,3 V
- [ ] seznam vývodů U1 (vf, napájení, krystal, rozhraní) jako podklad pro etapu 3

## Z fotek

Měřítko dává šířka desky 44 mm, u výřezu `docs/fig/ld2450_soucastky.jpg`
asi 41 px/mm. Nejistota je kolem 5 %.

- Tx: 2 plošky 4,1 × 3,1 mm, rozteč 8,1 mm. Rx1 a Rx2: po 2 ploškách
  3,8 × 3,1 mm, rozteč 7,6 mm, řady 6,4 mm nad sebou. Středy Tx a Rx1 dělí
  asi 23 mm.
- Krystaly Y1 a Y2 mají pouzdro asi 2,0 × 1,6 mm.
- **Studie se v roztečích mýlí.** Plošky J3 a lišta J4 mají rozteč 2,0 mm
  (fotka i výkres výrobce), studie uvádí 2,54 mm. Zásuvka J1 má rozteč
  1,5 mm (z fotky asi 1,45 mm, výrobce 1,50 mm), studie uvádí 1,25 mm.
  Protikus je čtyřpinová zástrčka s roztečí 1,5 mm. Typ zásuvky (JST ZH?)
  zbývá ověřit.
- Náš kus má potisk V1.1, manuál ukazuje V1.0 s jiným rozmístěním součástek.

## Z manuálu výrobce (v1.0, neměřeno)

- 5 V, zdroj nad 200 mA, průměrný odběr 120 mA. Úrovně IO 3,3 V.
- 24,00–24,25 GHz, FMCW, přeladění 250 MHz.
- Dosah 6 m, ±60° v azimutu, ±35° v elevaci.
- Jediné rozhraní je UART. Bluetooth manuál nezmiňuje, náš kus V1.1 ale má
  IPEX s anténou.
- UART 256 000 Bd 8N1, 10 rámců za sekundu. Rámec má 30 bajtů: hlavička
  `AA FF 03 00`, tři cíle po 8 bajtech a konec `55 CC`. Cíl nese souřadnice
  x a y v mm, rychlost v cm/s (vše int16 LE) a velikost vzdálenostní buňky
  v mm (uint16). Znaménko je netypické: nejvyšší bit 1 znamená kladnou
  hodnotu a zbylých 15 bitů je absolutní hodnota. Nepřítomný cíl má samé
  nuly. V příkladu manuálu je chyba: buňka `40 01` je 320 mm, ne 360 mm.
