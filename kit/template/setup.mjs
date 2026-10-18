// Copia fontes e bibliotecas para public/ (o Chrome do render não acessa CDN de forma confiável).
import fs from "node:fs";
const cp = (from, to) => { fs.mkdirSync(to.split("/").slice(0, -1).join("/"), { recursive: true }); fs.copyFileSync(from, to); };
const nm = "node_modules";
cp(`${nm}/gsap/dist/gsap.min.js`, "public/vendor/gsap.min.js");
cp(`${nm}/three/build/three.module.js`, "public/vendor/three.module.js");
cp(`${nm}/three/build/three.core.js`, "public/vendor/three.core.js");
cp(`${nm}/three/examples/jsm/environments/RoomEnvironment.js`, "public/vendor/RoomEnvironment.js");
cp(`${nm}/three/examples/jsm/geometries/RoundedBoxGeometry.js`, "public/vendor/RoundedBoxGeometry.js");
for (const w of ["Medium", "SemiBold", "Bold"]) cp(`${nm}/geist/dist/fonts/geist-sans/Geist-${w}.woff2`, `public/fonts/Geist-${w}.woff2`);
cp(`${nm}/@fontsource/fraunces/files/fraunces-latin-600-italic.woff2`, "public/fonts/fraunces-latin-600-italic.woff2");
console.log("public/vendor e public/fonts prontos. Agora copie tight.mp4 (e person.webm) para public/.");
