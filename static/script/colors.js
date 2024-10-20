export function hsl(hue, saturation, lightness) {
  const [r, g, b] = hslToRgb(hue / 360, saturation / 100, lightness / 100);
  return hexify(r, g, b);
}

export function hexify(r, g, b) {
  const toHex = (x) => {
    const hex = Math.round(x).toString(16);
    return hex.length === 1 ? '0' + hex : hex;
  };
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
}

export function deHexify(rgb) {
  const r = rgb.slice(1, 3);
  const g = rgb.slice(3, 5);
  const b = rgb.slice(5, 7);
  return [parseInt(r, 16), parseInt(g, 16), parseInt(b, 16)];
}

export function hslToRgb(h, s, l) {
  let r, g, b;
  if (s === 0) {
    r = g = b = l; // achromatic
  } else {
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    r = hueToRgb(p, q, h + 1/3);
    g = hueToRgb(p, q, h);
    b = hueToRgb(p, q, h - 1/3);
  }

  return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
}

function hueToRgb(p, q, t) {
  if (t < 0) t += 1;
  if (t > 1) t -= 1;
  if (t < 1/6) return p + (q - p) * 6 * t;
  if (t < 1/2) return q;
  if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
  return p;
}

export function rgbToHsl(r, g, b) {
  (r /= 255), (g /= 255), (b /= 255);
  const vmax = Math.max(r, g, b), vmin = Math.min(r, g, b);
  let h, s, l = (vmax + vmin) / 2;

  if (vmax === vmin) {
    return [0, 0, l]; // achromatic
  }

  const d = vmax - vmin;
  s = l > 0.5 ? d / (2 - vmax - vmin) : d / (vmax + vmin);
  if (vmax === r) h = (g - b) / d + (g < b ? 6 : 0);
  if (vmax === g) h = (b - r) / d + 2;
  if (vmax === b) h = (r - g) / d + 4;
  h /= 6;

  return [h * 360, s * 100, l * 100];
}

export function hslToXY(selector, h, s, l) {
  const xPct = h / 360;
  const yPct = 1.0 - s / 100;

  const rect = selector.getBoundingClientRect();
  const x = xPct * (rect.right - rect.left) + rect.left;
  const y = yPct * (rect.bottom - rect.top) + rect.top;
  return [x, y];
}

export function xyToHSL(selector, x, y) {
  const rect = selector.getBoundingClientRect();
  const xPct = (x - rect.left) / (rect.right - rect.left);
  const yPct = (y - rect.top) / (rect.bottom - rect.top);
  const hue = 360 * xPct;
  const saturation = 100 - (100 * yPct);
  return [hue, saturation, 50];
}

