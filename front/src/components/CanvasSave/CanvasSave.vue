<template>
<section class='canvas-download'>
  <canvas id='canvas-view' :width='width' :height='height'></canvas>
  <canvas id='real-canvas'></canvas>
  <a id='canvas-anchor' :download="downloadProps.name + '.png'">{{ downloadProps.text }}</a>
</section>
</template>
<script>

function drawCanvas(drawFunction) {
  const canvas = document.getElementById('real-canvas');
  drawFunction(canvas);
  generateThumbnail(canvas);
  linkCanvas(canvas);
}

function generateThumbnail(canvas) {
  const thumbnail = document.getElementById('canvas-view');
  thumbnail.getContext('2d').drawImage(canvas, 0, 0, canvas.width, canvas.height, 0, 0, thumbnail.width, thumbnail.height);
}

function linkCanvas(canvas) {
  const data = canvas.toDataURL('image/png');
  const a = document.getElementById('canvas-anchor');
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
  #canvas-view {
    border: 2px solid #000000;
    display: block;
  }

  #real-canvas {
    border: 2px solid #000000;
    display: none;
  }

  #canvas-anchor {
    display: block;
    font-size: 3rem;
  }

  .canvas-download {
    display: flex;
    flex-flow: column nowrap;
    justify-content: stretch;
    align-items: center;
  }
</style>
