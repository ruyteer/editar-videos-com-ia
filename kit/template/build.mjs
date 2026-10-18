// Monta public/index.html a partir de src/index.html.
// Uso: node build.mjs <words2.json> <duracao_tight_em_s> "@seuperfil"
import fs from "node:fs";
const [wordsPath = "words2.json", vdur = "30", handle = "@seuperfil"] = process.argv.slice(2);
const words = JSON.parse(fs.readFileSync(wordsPath, "utf8")).map((w) => ({ w: w.w, s: w.s, e: w.e }));
const V = Number(vdur);
const icon = (n) => fs.readFileSync(`node_modules/lucide-static/icons/${n}.svg`, "utf8").replace(/<!--.*?-->/s, "").trim();
const out = fs.readFileSync("src/index.html", "utf8")
  .replaceAll("{{WORDS}}", () => JSON.stringify(words))       // sempre com função: "$$" no texto quebraria o replace
  .replaceAll("{{DUR}}", () => (V + 1.1).toFixed(2))
  .replaceAll("{{VDUR}}", () => V.toFixed(2))
  .replaceAll("{{HANDLE}}", () => handle)
  .replace(/\{\{i:([a-z0-9-]+)\}\}/g, (_, n) => icon(n));  // {{i:check}} -> SVG do lucide
fs.mkdirSync("public", { recursive: true });
fs.writeFileSync("public/index.html", out);
console.log("public/index.html pronto");
