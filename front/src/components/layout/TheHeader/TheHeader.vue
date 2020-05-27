<template>
<section :class="classFromParent + ' header-container'">
  <div class='header-item logo'>Chromaudible</div>
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
  display: flex;
  background: #b0cadf;
  flex: 0 1 15%;
  flex-flow: row nowrap;
  justify-content: center;
  align-items: center;
}

.header-item {
  flex: 0 0 20%;
  padding: 2rem;
}

.logo {
  border: 0.25rem solid black;
  border-top: none;
  border-bottom: none;
  letter-spacing: 0.25rem;
  text-shadow: 0.25rem 0.05rem #af7000;
}

</style>
