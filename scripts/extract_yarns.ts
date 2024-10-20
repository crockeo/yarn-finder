import { brands } from "../Temperature-Blanket-Web-App/src/lib/yarns/brands.ts";

const yarns = [];

for (const brand of brands) {
  for (const yarn of brand.yarns) {
    for (const colorway of yarn.colorways) {
      for (const color of colorway.colors) {
        yarns.push({
          name: `${brand.name} ${yarn.name} ${color.name}`,
          url: colorway.source.href,
          hex: color.hex,
        });
      }
    }
  }
}

console.log(JSON.stringify(yarns));
