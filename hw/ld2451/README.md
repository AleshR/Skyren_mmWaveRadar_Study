# HLK-LD2451 — zpětné zapojení

KiCad 10 projekt pro etapu 2 dílu Praxe ve studii (`docs/mmwave_radar_study.tex`).
Obsahuje zapojení modulu HLK-LD2451 zakreslené z fotek a z manuálu výrobce,
které se doplní prozvoněním. Desku nevyrábíme, proto projekt nemá `.kicad_pcb`.

**Stav:** rozpracováno z fotek `img/IMG_2154`, `IMG_2155` a z manuálu v1.0
(`docs/datasheet/`). Nic není prozvoněné ani změřené.

```bash
open hw/ld2451/ld2451.kicad_pro
```

| Soubor | Obsah |
|---|---|
| `ld2451.kicad_sch` | schéma: součástky z fotek, poznámky a co zjistit |
| `sym-lib-table` | připojí sdílenou knihovnu `../lib/re_generic.kicad_sym` |

## Součástky

Čísla odpovídají dílu Rozbor ve studii (obr. `fig:ld2451a`, `fig:ld2451b`).

| Ref | Č. | Pouzdro, potisk | Pravděpodobná role |
|---|---|---|---|
| U1 | 1 | QFN-32 asi 4×4, potisk nečitelný | radarový čip na straně antén |
| U2 | 2 | QFN asi 4–5 mm | mikrokontrolér, podle výrobce s Bluetooth |
| U3 | 3 | SOIC-8, potisk nečitelný | paměť SPI, nebo zesilovač |
| U4 | 4 | SOT-223 | stabilizátor |
| U5 | 5 | SOT-23 | neznámá |
| Y1 | 6 | krystal | reference PLL pro U1 |
| J2 | 7 | 4 plošky, vývod 1 čtvercový | programovací rozhraní, snad SWD |
| — | 8 | rám stínění bez krytu | ve schématu není |
| J1 | 9 | úhlová lišta 1×6, 2,54 mm | VIN GND OT1 TX RX OT2 (zapojení podle výrobce) |
| J3 | — | neosazené SMD plošky | GND TX RX VIN, paralelně s J1? |
| D1 | — | světlé pouzdro asi 0603 | LED? |
| AE1–AE3 | — | sériově napájené řady plošek | Tx (2 × 8), Rx1 a Rx2 (1 × 8) |

J3 a D1 studie nečísluje. Jsou na fotkách vidět, a proto jsou ve schématu.
J3 je i na výkresu výrobce.

## Konvence schématu

Stejné jako u [LD2450](../ld2450/README.md#konvence-schématu): generické
symboly pro neznámé obvody, spojená jen zem konektorů a ostatní sítě
s předponou konektoru (`J1_TX`, `J3_TX`, …). J1 je číslovaný podle výrobce,
ostatní konektory podle pořadí potisku.

## Etapa 2: co zjistit

- [ ] makrosnímky s bočním světlem, přečíst potisky U1 až U5 a Y1
- [ ] J2: najít zem a napájení. Zbylé dvě plošky jsou kandidáti na SWDIO
      a SWCLK a mají vést na U2
- [ ] linky mezi U1 a U2
- [ ] Y1, `RF_TX`, `RF_RX1` a `RF_RX2` → vývody U1
- [ ] U3: kam vedou jeho vývody
- [ ] `J1_TX`, `J1_RX`, `J1_OT1` a `J1_OT2` → U2? Jsou J1 a J3 paralelně?
- [ ] kde je anténa Bluetooth a kam vede
- [ ] za provozu napětí za U4, role U5 a D1

Podle manuálu má LD2451 Bluetooth: hlásí se jako `LD2451_XXXX` a obsluhuje
ho aplikace HLKRadarTool. Studie v dílu Rozbor píše, že Bluetooth ani USB
na desce nevidíme. Anténu jsme na fotkách opravdu nenašli, U2 ale bude
nejspíš MCU s rádiem. Jako cíl pro čtení firmwaru přes J2 je LD2451 pořád
slibný.

V etapě 3 se přes J2 čte jen identifikace ladicího portu. **Nic nemazat:**
zrušení ochrany čtení smaže firmware i s inicializací radarového čipu
(varování v dílu Praxe).

## Z fotek

Měřítko dává deska 70 × 35 mm, u výřezu `docs/fig/ld2451_soucastky.jpg`
asi 26 px/mm. Nejistota je kolem 5 %.

- Rx1 a Rx2: každý jedna řada osmi plošek. Řady leží 6,0 mm nad sebou
  a každá vede do vlastního vývodu U1.
- Tx: dvě řady osmi plošek 7,8 mm od sebe, napájené jedním vedením
  s rozbočením.
- Rozteč plošek je 6,6 mm a řada měří asi 53 mm. Středy Tx a Rx dělí
  asi 18 mm, z výkresu výrobce
  vychází asi 19 mm.
- Rozteč vývodů: J1 2,54 mm (potvrzuje výrobce), J2 asi 2,5 mm, J3 asi
  1,5 mm (4 vývody a 2 úchyty).
- Na desce je potisk `HKKF`.

## Z manuálu výrobce (v1.0, neměřeno)

| Vývod J1 | Označení | Funkce |
|---|---|---|
| 1 | VIN | napájení 5 V |
| 2 | GND | zem |
| 3 | OT1 | GPIO1: po startu třikrát H/L, pak H, když se cíl přibližuje |
| 4 | TX | UART TX modulu |
| 5 | RX | UART RX modulu |
| 6 | OT2 | GPIO2, zatím bez funkce |

- 5 V, zdroj nad 300 mA, průměrný odběr 107 mA. Úrovně IO 3,3 V.
- 24,00–24,25 GHz, FMCW, přeladění pod 200 MHz.
- Dosah až 100 m, ±20°. Rychlost cíle 0–120 km/h.
- UART 115 200 Bd 8N1 a Bluetooth se stejným obsahem.
- Nastavení přes UART nebo Bluetooth, uložené i po vypnutí:
  - dosah 0–100 m
  - směr (blíží se, vzdaluje se, obojí)
  - minimální rychlost
  - zpoždění poplachu 1–30 s
  - citlivost: počet po sobě jdoucích detekcí 1–10 a práh SNR 1–255,
    výchozí 4
- Montážní díry v rozteči 66,0 × 31,1 mm, 2 mm od okrajů.

Formát rámce UART manuál nepopisuje, patří do samostatného dokumentu
o protokolu. Snímek aplikace v manuálu ukazuje rámec
`AA AA 0D 02 01 81 35 01 1B 13 81 3E 01 1B 04 55 55` pro dva cíle
53 m a 62 m pod úhlem 1° a s rychlostí 27. Sedí na něj výklad po pěti
bajtech na cíl:

- úhel + 0x80
- vzdálenost v m
- směr
- rychlost
- neznámý bajt (SNR?)

Je to hypotéza z jediného snímku a ověří ji záznam v etapě 1.
