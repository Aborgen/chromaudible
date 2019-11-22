<template>
<section :class="classFromParent + ' content-container'">
  <header>Time to do the thing</header>
  <section>
    <file-form
      :input-label='currentLabel'
      :action='currentAction'
      form-name='upload'
    />
  </section>
</section>

</template>

<script>
import FileForm from '../../FileForm/FileForm';

export default {
  name: 'TheContent',
  components: {
    FileForm
  },
  data() {
    return {
      currentLabel: "Upload your music!",
      currentAction: '#'
    }
  },
  props: {
    classFromParent: {
      type: String,
      required: true
    }
  }
}
</script>
