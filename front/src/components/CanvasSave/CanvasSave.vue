<template>
<section class='canvas-download'>
  <canvas id='canvas-view'></canvas>
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
  thumbnail.width = 500;
  thumbnail.height = 500;
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
    }
  },
  mounted() {
    drawCanvas(this.drawFunction);
  }
}
</script>

<style scoped>
  #canvas-view {
    border: 0.5rem outset #816c61;
    box-shadow: 0.8rem 0.5rem 0.5rem -0.2rem #2E0303;
    display: block;
    height: 40rem;
    width: 40rem;
    margin: 1rem 0;
  }

  #real-canvas {
    border: 0.18rem solid #000000;
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
