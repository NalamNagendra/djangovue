<template>
  <div class="repeating-image">
    <img :src="imageUrl" alt="Repeating Image">
  </div>
</template>

<script>
export default {
  props: {
    imageUrl: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.repeating-image {
  width: 100%;
  margin-bottom: 20px; /* Adjust as needed */
}

.repeating-image img {
  width: 100%;
  height: auto;
  display: block;
}
</style>