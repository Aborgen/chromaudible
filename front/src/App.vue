<template>
<div class='app grid-container'>
  <the-header classFromParent='grid-item' />
  <the-content classFromParent='grid-item' />
</div>
</template>

<script>
import TheContent from './components/layout/TheContent/TheContent';
import TheHeader from './components/layout/TheHeader/TheHeader';

export default {
  name: 'app',
  components: {
    TheContent,
    TheHeader
  }
}
</script>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  background-color: lightblue;
  padding: 10px;
}
 
.grid-item {
  background-color: lightgreen;
  border: 1px solid darkblue;
  padding: 20px;
  font-size: 30px;
  text-align: center;
}
</style>
