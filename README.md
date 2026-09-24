# Skyren mmWave Radar Study

Studie proveditelnosti levného radarového dálkoměru: **vzdálenost k plošnému
cíli (kov, beton, zeď, dřevo) do 5 m s přesností kolem 5 cm při vzájemné
rychlosti až 240 m/s**, v průměru 35 mm a za jednotky eur.

Projekt začal jako teardown laserového dálkoměru Parkside PLEM 20 A4. Ten
skončil jako slepá ulička (fázový měřák s uzavřeným ASICem) a zadání na
240 m/s pak vyřadilo i optiku jako princip.

## Závěr (revize R2)

- **24 GHz FMCW s trojúhelníkovou rampou**, jedna anténa přes Ø 35 mm
  a tištěná hyperbolická čočka (svazek ~22°, zisk ~16 dBi).
- Integrovaný radarový čip ICLegend S3KM111L z levných modulů →
  materiál **~4–7 € na kus** (cena čipu neověřená).
- **Hladké plochy** (plech, hladký beton, hoblované dřevo): chyba pod 1 cm,
  měří se kolmá vzdálenost k rovině.
- **Drsné plochy** (hrubý beton, cihla): rozhoduje speckle. Po průměrování
  přes 1,2 m přiblížení ~3 cm kolmo, ~5–6 cm při náklonu 15°.
- Vysílací výkon omezuje EIRP 20 dBm → s čočkou nejvýš 4 dBm.
- Další krok: rozebrat modul HLK-LD2450 a získat z něj inicializaci čipu.

Čísla pocházejí z výpočtů a simulací, ne z měření.

## Co je kde

| Cesta | Obsah |
|---|---|
| `docs/mmwave_radar_study.tex` | studie, zdroj |
| `docs/mmwave_radar_study.pdf` | vysázený dokument |
| `docs/template/` | submodul — publikační systém Skyren (`skyren.cls`) |
| `hw/lens/lens_24ghz.scad` | parametrický model 24GHz hyperbolické čočky (OpenSCAD) |
| `sim/` | simulace v čistém Pythonu: interpolace vrcholu FFT, speckle na drsné zdi |
| `img/` | fotodokumentace teardownu Parkside PLEM 20 A4 |

STL z `.scad` se generují lokálně a do gitu nepatří:

```bash
/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD -D n=1.62 -o lens_24ghz_PETG.stl hw/lens/lens_24ghz.scad
```

## Simulace

```bash
python3 sim/interpolace.py
python3 sim/speckle.py 400
python3 sim/speckle_prumer.py 100
```

## Sazba

Vyžaduje LuaLaTeX (třída používá `fontspec`). Symlinky `docs/skyren.cls`
a `docs/fonts` ukazují do submodulu, takže se překládá přímo v `docs/`:

```bash
git submodule update --init --recursive
cd docs && lualatex mmwave_radar_study.tex && lualatex mmwave_radar_study.tex
```

Dvakrát kvůli obsahu a živému záhlaví.
