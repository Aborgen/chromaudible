<template>
<section class='canvasDownload'>
  <canvas id='canvasView' width=500 height=500></canvas>
  <a id='canvasAnchor' :download="downloadProps.name + '.png'">{{ downloadProps.text }}</a>
</section>
</template>

<script>
function linkCanvas(canvas) {
  return canvas.toDataURL('image/png');
}

function drawCanvas(drawFunction) {
  const canvas = document.getElementById('canvasView');
  drawFunction(canvas);
  document.getElementById('canvasAnchor').href = linkCanvas(canvas);
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
  },
  mounted() {
    drawCanvas(this.drawFunction);
  }
}
</script>

<style>
  #canvasView {
    border: 2px solid #000000;
  }
</style>
