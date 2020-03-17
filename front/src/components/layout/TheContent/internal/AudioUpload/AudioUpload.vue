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

function resetState(stopTrying, parentMessage) {
  if (stopTrying) {
    this.currentLabel = parentMessage;
    this.formDisabled = true;
    return;
  }

  this.currentLabel = "Upload your music!";
  this.formDisabled = false;
}

async function convertToImage() {
  if (this.formDisabled) {
    return;
  }

  if (this.canvasMounted) {
    this.canvasMounted = false;
  }

  const input = document.getElementById('upload');
  if (input.files.length === 0) {
    this.currentLabel = 'Please choose an audio file to submit';
    this.formDisabled = false;
    return;
  }

  const audioFile = input.files[0];
  this.formDisabled = true;
  this.currentLabel = 'Awaiting response from server...';
  const url = `${this.baseUrl}/upload`;
  const res = await getColors(url, audioFile);
  if (!res.ok) {
    let message = ''
    if (res.status === 503) {
      message = 'Cannot connect to the server';
    }
    else {
      const error = await res.json();
      message = error.message;
    }

    this.currentLabel = `${message}: (Error code: ${res.status})`;
    this.handleError(res.status, this.resetState.bind(this));
    return;
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
    drawCanvas,
    resetState
  },
  data() {
    return {
      currentLabel: "Upload your music!",
      canvasBackground: '#000000',
      canvasDrawFunction: function() {},
      canvasMounted: false,
      formDisabled: false
    }
  },
  props: {
    baseUrl: {
      type: String,
      required: true
    },
    classFromParent: {
      type: String,
      required: true
    },
    handleError: {
      type: Function,
      required: true
    }
  }
}
</script>

<style scoped>
  .audio-upload_form {
    flex: 0 0 5%;
    border: 2px solid black;
  }
</style>
