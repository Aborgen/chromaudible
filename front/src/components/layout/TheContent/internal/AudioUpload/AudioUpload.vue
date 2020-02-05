<template>
<section class='audioUpload'>
  <file-form
    :handle-submit='convertToImage'
    :input-label='currentLabel'
    :form-disabled='formDisabled'
    form-name='audioUpload'
  />
  <canvas-save v-if='canvasMounted === true'
               :draw-function='drawCanvas'
               :download-props="{ name: 'audio-canvas', text: 'Download Audio Canvas' }"
    />
</section>
</template>

<script>
import CanvasSave from 'components/CanvasSave/CanvasSave';
import FileForm from 'components/FileForm/FileForm';

/* eslint-disable no-unused-vars, no-console*/
async function convertToImage() {
  const audioFile = document.getElementById('upload').files[0];
  this.formDisabled = true;
  await delay(2000);
//  const res = await getMelody('http://localhost:5000/upload', audioFile);
//  if (!res.ok) {
//    throw new Error(res.statusText);
//  }

  this.currentLabel = 'Obtained melody!';
  this.canvasMounted = true;
  this.formDisabled = false;
  // Result will be an object { timestamp: hexColor }. Will draw a canvas
  // With this in some way.
}

async function getMelody(url, audioFile) {
  let data = new FormData();
  data.append('type', 'audio');
  data.append('file', audioFile);
  return await fetch(url, {
    method: 'POST',
    body: data
  });
}

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function drawCanvas(canvas) {
  const ctx = canvas.getContext('2d');
  // Draw background
  ctx.fillStyle = this.canvasBackground;
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  // Draw spiral, just temporary
  const centerX = ctx.canvas.width / 2;
  const centerY = ctx.canvas.height / 2;
  ctx.moveTo(centerX, centerY);
  ctx.beginPath();
  const a = 3;
  const b = a;
  for (let i = 0; i < 720; i += 0.1) {
    const angle = 0.1 * i;
    const x = centerX + (a + b * angle) * Math.cos(angle);
    const y = centerY + (a + b * angle) * Math.sin(angle);
    ctx.lineTo(x, y);
  }

  ctx.strokeStyle = "#000000";
  ctx.stroke();
  console.log('CANVAS DRAWN');
}

/* eslint-enable no-unused-vars, no-console */
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
      canvasBackground: '#ffffff',
      canvasMounted: false,
      formDisabled: false
    }
  }
}
</script>

