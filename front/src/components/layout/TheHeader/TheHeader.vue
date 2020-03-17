<template>
<section :class="classFromParent + ' header-container'">
  <div class='header-item logo'>Chromeaudible</div>
</section>
</template>

<script>
export default {
  name: 'TheHeader',
  data() {
    return {
      idx: 0
    };
  },
  props: {
    classFromParent: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.header-container {

}

.header-item {
  background: orange;
  padding: 10px;
}

</style>
