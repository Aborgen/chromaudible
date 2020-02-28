<template>
<section class='canvasDownload'>
  <canvas id='canvasView' :width='width' :height='height'></canvas>
  <canvas id='realCanvas'></canvas>
  <a id='canvasAnchor' :download="downloadProps.name + '.png'">{{ downloadProps.text }}</a>
</section>
</template>
<script>

function drawCanvas(drawFunction) {
  const canvas = document.getElementById('realCanvas');
  drawFunction(canvas);
  generateThumbnail(canvas);
  linkCanvas(canvas);
}

function generateThumbnail(canvas) {
  const thumbnail = document.getElementById('canvasView');
  thumbnail.getContext('2d').drawImage(canvas, 0, 0, canvas.width, canvas.height, 0, 0, thumbnail.width, thumbnail.height);
}

function linkCanvas(canvas) {
  const data = canvas.toDataURL('image/png');
  const a = document.getElementById('canvasAnchor');
  a.href = data;
}

export default {
  name: 'CanvasSave',
  props: {
    drawFunction: {
      type: Function,
      required: true
    },
    downloadProps: {
      type: Object,
      required: true
    },
    width: {
      type: Number,
      required: true
    },
    height: {
      type: Number,
      required: true
    },
  },
  mounted() {
    drawCanvas(this.drawFunction);
  }
}
</script>

<style scoped>
  #canvasView {
    border: 2px solid #000000;
    display: block;
  }

  #realCanvas {
    border: 2px solid #000000;
    display: none;
  }

  #canvasAnchor {
    display: block;
  }
</style>
