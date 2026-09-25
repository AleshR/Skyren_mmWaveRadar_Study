// ---------------------------------------------------------------------------
// Hyperbolická plankonvexní čočka pro 24GHz radarový modul
//
// Hyperbolická plocha míří k modulu, rovná plocha k cíli.
// Fázový střed antény musí ležet ve vzdálenosti f pod vrcholem čočky.
// Profil: (n^2 - 1) z^2 + 2 (n - 1) f z - r^2 = 0
//
// Varianty pro vývoj na HLK-LD2450 (vysílač a přijímač ~23 mm od sebe):
//   sep > 0  dělená čočka: dvě poloviny apertury, každá s osou nad svou
//            anténou; osy leží na ose x ve vzdálenosti sep, šev v x = 0
//   cut > 0  plná čočka seříznutá rovně ve vzdálenosti cut od osy na
//            straně -x, aby nezakrývala sousední anténu (čočka jen nad Rx)
// ---------------------------------------------------------------------------

n      = 1.52;  // index lomu: HDPE 1.52, PTFE 1.45, PETG ~1.62, PLA ~1.65 (ověř měřením)
D      = 35;    // průměr apertury [mm]
f      = 28;    // vzdálenost fázového středu antény od vrcholu čočky [mm]
t_edge = 1.5;   // nejmenší tloušťka na okraji [mm]
sep    = 0;     // rozestup os dělené čočky [mm]; 0 = plná čočka (LD2450: 23)
cut    = 0;     // seříznutí plné čočky [mm od osy]; 0 = bez seříznutí (LD2450: 12)
steps  = 80;    // jemnost profilu

R = D / 2;
function sag(r) = (-(n - 1) * f + sqrt(pow((n - 1) * f, 2) + (n * n - 1) * r * r)) / (n * n - 1);

// Nejvzdálenější bod apertury od osy: u dělené čočky roh švu (0, ±R).
R_ext = sep > 0 ? sqrt(pow(sep / 2, 2) + R * R) : R;
T = sag(R_ext) + t_edge;

module body(rmax) {
  rotate_extrude($fn = 180) polygon(concat(
    [for (i = [0 : steps]) let (r = rmax * i / steps) [r, sag(r)]],
    [[rmax, T], [0, T]]
  ));
}

// Poloprostor x >= 0 (side = 1) nebo x <= 0 (side = -1), s rezervou v z.
module half_space(side) {
  translate([side > 0 ? 0 : -R - 1, -R - 1, -1]) cube([R + 1, 2 * R + 2, T + 2]);
}

if (sep > 0) {
  intersection() {
    translate([0, 0, -1]) cylinder(r = R, h = T + 2, $fn = 180);
    union() {
      intersection() { translate([-sep / 2, 0, 0]) body(R_ext); half_space(-1); }
      intersection() { translate([ sep / 2, 0, 0]) body(R_ext); half_space(1); }
    }
  }
} else if (cut > 0) {
  intersection() {
    body(R);
    translate([-cut, -R - 1, -1]) cube([R + cut + 1, 2 * R + 2, T + 2]);
  }
} else {
  body(R);
}

echo(str("Tloušťka na ose: ", T, " mm"));
echo(str("Výška od fázového středu antény po rovnou plochu: ", f + T, " mm"));
