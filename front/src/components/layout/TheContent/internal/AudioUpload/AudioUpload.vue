<template>
<section class='audio-upload'
         :class='classFromParent'
>
  <file-form
    :handle-submit='convertToImage'
    :input-label='currentLabel'
    :form-disabled='formDisabled'
    accepted-types='audio/*'
    form-name='audio-upload'
  />
  <canvas-save v-if='canvasMounted === true'
               :width=500
               :height=500
               :draw-function='canvasDrawFunction'
               :download-props="{ name: 'audio-canvas', text: 'Download Audio Canvas' }"
    />
</section>
</template>

<script>
import CanvasSave from 'components/CanvasSave/CanvasSave';
import fetchCatch from 'utils/FetchCatch';
import FileForm from 'components/FileForm/FileForm';
import { spiral, calculateSpiralPeak } from 'utils/Spiral';

async function convertToImage() {
  const audioFile = document.getElementById('upload').files[0];
  this.formDisabled = true;
  const res = await getColors('http://localhost:5000/upload', audioFile);
  if (!res.ok) {
    this.currentLabel = 'There was an issue connecting to the server';
    throw new Error(res.statusText);
  }

  const pointColors = await res.json();
  this.currentLabel = 'Obtained melody!';
  this.canvasDrawFunction = (canvas) => {
    const a = pointColors;
    const b = this.canvasBackground;
    return drawCanvas(canvas, a, b);
  };

  this.canvasMounted = true;
  this.formDisabled = false;
}

async function getColors(url, audioFile) {
  let data = new FormData();
  data.append('type', 'audio');
  data.append('file', audioFile);
  return await fetchCatch(url, {
    method: 'POST',
    body: data
  });
}

function drawCanvas(canvas, pointArray, background) {
  const context = canvas.getContext('2d');
  const separationBetweenPoints = 1;
  const separationBetweenRings = 20;
  const margin = 10;
  const numberOfArms = 5;
  const peak = calculateSpiralPeak(pointArray.length, separationBetweenPoints, separationBetweenRings, margin);

  canvas.width = peak;
  canvas.height = peak;
  const origin = {
    x: canvas.width / 2,
    y: canvas.height / 2
  };

  context.fillStyle = background;
  context.fillRect(0, 0, canvas.width, canvas.height);
  spiral(canvas, origin, pointArray, separationBetweenPoints, separationBetweenRings, numberOfArms);
}

export default {
  name: 'AudioUpload',
  components: {
    FileForm,
    CanvasSave
  },
  methods: {
    convertToImage,
    drawCanvas
  },
  data() {
    return {
      currentLabel: "Upload your music!",
      canvasBackground: '#000000',
      canvasDrawFunction: function() {},
      canvasMounted: false,
      formDisabled: false
    }
  }
}
</script>

