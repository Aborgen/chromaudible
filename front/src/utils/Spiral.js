function spiral(canvas, origin, pointColorsGroups, distanceBetweenPoints, separationBetweenRings, numberOfArms) {
  const context = canvas.getContext('2d');
  const generator = spiralPointGenerator(distanceBetweenPoints, separationBetweenRings);
  const precomputeTrig = precomputeSineCosine(numberOfArms);

  const waitPeriod = 4;
  let canvasData = context.createImageData(canvas.width, canvas.height);
  let allowDrawing = false;
  for (let i = 0; i < pointColorsGroups.length + waitPeriod; ++i) {
    if (i === waitPeriod) {
      allowDrawing = true;
    }

    const point = generator.next().value;
    const x = origin.x + point.x;
    const y = origin.y - point.y;
    if (allowDrawing) {
      drawPoints(canvasData, x, y, origin, numberOfArms, precomputeTrig, pointColorsGroups[i-waitPeriod]);
    }
  }

  // putImageData overrides the background color present on the canvas
  const backgroundColor = context.getImageData(0, 0, 1, 1).data;
  context.putImageData(canvasData, 0, 0);
  doBackground(context, canvas.width, canvas.height, ...backgroundColor);
}

function precomputeSineCosine(numberOfArms) {
  // Precompute cosine and sine values, for use in drawPoints.
  const theta = Math.round(360 / numberOfArms) * (Math.PI / 180);
  const precomputeTrig = { cos: [], sin: [] };
  for (let i = 1; i < numberOfArms; ++i) {
    precomputeTrig['cos'].push(Math.cos(theta * i));
    precomputeTrig['sin'].push(Math.sin(theta * i));
  }

  return precomputeTrig;
}

function *spiralPointGenerator(distanceBetweenPoints, separationBetweenRings) {
  const b = separationBetweenRings / (2 * Math.PI);
  let radius = distanceBetweenPoints;
  let theta = radius / b;
  let x = 0;
  let y = 0;
  while (true) {
    yield { x, y };
    x = Math.floor(radius * Math.cos(theta));
    y = Math.floor(radius * Math.sin(theta));
    theta += (distanceBetweenPoints / radius);
    radius = b * theta;
  }
}

function drawPoints(canvasData, x, y, origin, numberOfArms, precomputeTrig, pointColors) {
  const xOffset = x - origin.x;
  const yOffset = y - origin.y;
  // Original spiral
  colorPoint(canvasData, x, y, ...pointColors[0]);
  for (let i = 0; i < numberOfArms-1; ++i) {
    const x1 = origin.x + Math.floor(xOffset * precomputeTrig['cos'][i] - yOffset * precomputeTrig['sin'][i]);
    const y1 = origin.y + Math.floor(yOffset * precomputeTrig['cos'][i] + xOffset * precomputeTrig['sin'][i]);
    colorPoint(canvasData, x1, y1, ...pointColors[i+1]);
  }
}

function colorPoint(canvasData, x, y, r, g, b) {
  const idx = (x + y * canvasData.width) * 4;
  canvasData.data[idx + 0] = r;
  canvasData.data[idx + 1] = g;
  canvasData.data[idx + 2] = b;
  canvasData.data[idx + 3] = 255;
}

function doBackground(context, width, height, r, g, b, a) {
  context.globalCompositeOperation = 'destination-over';
  context.fillStyle = `rgba(${r}, ${g}, ${b}, ${a})`;
  context.fillRect(0, 0, width, height);
  context.globalCompositeOperation = 'source-over'; // default
}

function calculateSpiralPeak(numberOfPoints, distanceBetweenPoints, separationBetweenRings, marginPercentage = 10) {
  const generator = spiralPointGenerator(distanceBetweenPoints, separationBetweenRings);
  let peak = 0;
  for (let i = 0; i < numberOfPoints; ++i) {
    const { x, y } = generator.next().value;
    peak = Math.max(peak, Math.abs(x), Math.abs(y));
  }

  // Multiply by two, to reflect the fact that origin is located in the top left
  // corner of the html canvas element, rather than the center.
  peak *= 2;
  const scaledArea = (peak * peak) * (1 + Math.min(marginPercentage, 100) / 100);
  let scaledPeak = Math.round(Math.sqrt(scaledArea));
  // Canvas dimensions must be divisable by 2
  if (scaledPeak % 2 != 0) {
    scaledPeak += 1;
  }

  return scaledPeak;
}

export { spiral, calculateSpiralPeak };
