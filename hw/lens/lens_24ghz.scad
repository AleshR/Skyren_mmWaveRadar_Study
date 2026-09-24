// ---------------------------------------------------------------------------
// Hyperbolická plankonvexní čočka pro 24GHz radarový modul
//
// Hyperbolická plocha míří k modulu, rovná plocha k cíli.
// Fázový střed antény musí ležet ve vzdálenosti f pod vrcholem čočky.
// Profil: (n^2 - 1) z^2 + 2 (n - 1) f z - r^2 = 0
// ---------------------------------------------------------------------------

n      = 1.52;  // index lomu: HDPE 1.52, PTFE 1.45, PETG ~1.62, PLA ~1.65 (ověř měřením)
D      = 35;    // průměr apertury [mm]
f      = 28;    // vzdálenost fázového středu antény od vrcholu čočky [mm]
t_edge = 1.5;   // tloušťka na okraji [mm]
steps  = 80;    // jemnost profilu

R = D / 2;
function sag(r) = (-(n - 1) * f + sqrt(pow((n - 1) * f, 2) + (n * n - 1) * r * r)) / (n * n - 1);
T = sag(R) + t_edge;

profile = concat(
  [for (i = [0 : steps]) let (r = R * i / steps) [r, sag(r)]],
  [[R, T], [0, T]]
);

rotate_extrude($fn = 180) polygon(profile);

echo(str("Tloušťka ve středu: ", T, " mm"));
echo(str("Výška od fázového středu antény po rovnou plochu: ", f + T, " mm"));
