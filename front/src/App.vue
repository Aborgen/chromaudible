<template>
<div class='app flex-container'>
  <the-header classFromParent='flex-item' />
  <the-content classFromParent='flex-item' />
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

<style>
html, body {
  height: 100vh;
  width: 100%;
  padding: 0;
  margin: 0;
  background: #7d1d3f;
  color: #3c4f5e;
  font-size: 4px;
}

.app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

@media (min-width: 330px) {
  html, body {
    font-size: 5px;
  }
}

@media (min-width: 550px) {
  html, body {
    font-size: 6px;
  }
}

@media (min-width: 768px) {
  html, body {
    font-size: 7px;
  }
}

@media (min-width: 992px) {
  html, body {
    font-size: 8px;
  }
}

@media (min-width: 1200px) {
  html, body {
    font-size: 10px;
  }
}

input:focus {
  background: #84acce !important;
}

.flex-container {
  display: flex;
  flex-flow: column nowrap;
  justify-content: flex-end;
  align-items: stretch;
  margin: 2rem;
  height: 100%;
}
 
.flex-item {
  flex: 1;
  font-size: 5rem;
  text-align: center;
}
</style>
