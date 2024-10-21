import {
  deHexify,
  hsl,
  hslToXY,
  rgbToHsl,
  xyToHSL,
} from "/script/colors.js";

function colorInput() {
  return document.getElementById("color-input");
}

function pin() {
  return document.getElementById("color-pin");
}


function setBackgroundColor(selector, backgroundColor) {
  colorInput().value = backgroundColor;
  document.getElementById("color-input-text").innerHTML = backgroundColor;
  selector.style = `background-color: ${backgroundColor}`;
}

function hidePin() {
  pin().style = `visibility:hidden;`;
}

async function showPin(x, y) {
  const rect = pin().getBoundingClientRect();
  const midX = Math.round(x - (rect.right - rect.left) / 2);
  const midY = Math.round(y - (rect.bottom - rect.top) / 2);
  pin().style = `visibility:visible; left: ${midX}px; top: ${midY}px;`;

  const input = colorInput();
  window.location.hash = input.value;
  const res = await fetch(`/yarns/search/${input.value.slice(1)}`)
  document.getElementById("yarn-results").innerHTML = await res.text();
}

function onMouseMove(selector, mouseX, mouseY) {
  const [h, s, l] = xyToHSL(selector, mouseX, mouseY);
  setBackgroundColor(selector, hsl(h, s, l));
}

function onMouseClick(selector, mouseX, mouseY) {
  onMouseMove(selector, mouseX, mouseY);
  showPin(mouseX, mouseY);
}

export function main() {
  const input = document.getElementById("color-input");
  const selector = document.getElementById("color-selector");
  const pin = document.getElementById("color-pin");

  let colorPinned = false;

  if (!!window.location.hash) {
    setBackgroundColor(selector, window.location.hash);
    const [r, g, b] = deHexify(window.location.hash);
    const [h, s, l] = rgbToHsl(r, g, b);
    const [x, y] = hslToXY(selector, h, s, l);
    showPin(x, y);
    colorPinned = true;
  }

  selector.addEventListener("mousemove", function(e) {
    if (colorPinned) {
      return;
    }
    onMouseMove(selector, e.pageX, e.pageY);
  });

  selector.addEventListener("click", function(e) {
    onMouseClick(selector, e.pageX, e.pageY);
    colorPinned = true;
  });

  pin.addEventListener("click", function(e) {
    colorPinned = false;
    hidePin();
  });

  pin.addEventListener("mousedown", function(e) {
    onMouseMove(selector, e.pageX, e.pageY);
  });

  input.addEventListener("input", function(e) {
    setBackgroundColor(selector, e.target.value);

    const [r, g, b] = deHexify(e.target.value);
    const [h, s, l] = rgbToHsl(r, g, b);
    const [x, y] = hslToXY(selector, h, s, l);
    showPin(x, y);
    colorPinned = true;
  });

}
