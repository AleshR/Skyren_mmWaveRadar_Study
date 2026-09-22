# Skyren mmWave Radar Study

Studie proveditelnosti: **měření vzdálenosti při vzájemné rychlosti 240 m/s
s přesností na desítky centimetrů.**

Projekt začal jako teardown laserového dálkoměru Parkside PLEM 20 A4. Ten
skončil jako slepá ulička (fázový měřák s uzavřeným ASICem) a zadání na
240 m/s pak vyřadilo i optiku jako princip. Studie proto vyhodnocuje
**FMCW radar v pásmu 24 GHz**.

## Závěr

Single-chirp FMCW na 24 GHz splní zadání s rezervou: rozlišovací buňka 60 cm,
po interpolaci přesnost pod 10 cm, vzorkovací frekvence v jednotkách až
desítkách kHz. Otevřená podmínka je **požadovaný dosah** — ten rozhoduje mezi
hotovým modulem a vlastním front-endem.

## Co je kde

| Cesta | Obsah |
|---|---|
| `docs/mmwave_radar_study.tex` | studie, zdroj |
| `docs/mmwave_radar_study.pdf` | vysázený dokument |
| `docs/template/` | submodul — publikační systém Skyren (`skyren.cls`) |
| `img/` | fotodokumentace teardownu Parkside PLEM 20 A4 |

## Sazba

Vyžaduje LuaLaTeX (třída používá `fontspec`). Symlinky `docs/skyren.cls`
a `docs/fonts` ukazují do submodulu, takže se překládá přímo v `docs/`:

```bash
git submodule update --init --recursive
cd docs && lualatex mmwave_radar_study.tex && lualatex mmwave_radar_study.tex
```

Dvakrát kvůli obsahu a živému záhlaví.
