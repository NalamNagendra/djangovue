<template>
  <div id="app">
    <div class="app-container">
      <div class="tabs">
        <button 
          @click="activeTab = 'movie'" 
          :class="{ active: activeTab === 'movie' }"
        >
          <i class="tab-icon">🎬</i>
          <span class="tab-text">Movie</span>
        </button>
        <button 
          @click="activeTab = 'posts'" 
          :class="{ active: activeTab === 'posts' }"
        >
          <i class="tab-icon">📝</i>
          <span class="tab-text">Posts</span>
        </button>
      </div>
      
      <div class="tab-content">
        <MovieDetails v-if="activeTab === 'movie'" />
        <PostList v-else />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import MovieDetails from './components/MovieDetails.vue';
import PostList from './components/PostList.vue';

export default {
  name: 'App',
  components: {
    MovieDetails,
    PostList
  },
  setup() {
    const activeTab = ref('movie');
    const isMobile = ref(false);

    const checkScreenSize = () => {
      isMobile.value = window.innerWidth < 768;
    };

    onMounted(() => {
      checkScreenSize();
      window.addEventListener('resize', checkScreenSize);
    });

    return {
      activeTab,
      isMobile
    };
  }
}
</script>

<style>
:root {
  --primary-color: #01b4e4;
  --bg-color: #0f2133;
  --card-bg: #0c1a2a;
  --text-primary: #ffffff;
  --text-secondary: #9ab;
  --border-color: #1a2f40;
  --box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  --transition: all 0.3s ease;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  font-size: 16px;
}

body {
  font-family: 'Source Sans Pro', Arial, sans-serif;
  background: var(--bg-color);
  color: var(--text-primary);
  line-height: 1.5;
  overflow-x: hidden;
}

#app {
  min-height: 100vh;
  padding: 1rem;
  display: flex;
  flex-direction: column;
}

.app-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  background: var(--card-bg);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--box-shadow);
  flex: 1;
  display: flex;
  flex-direction: column;
}

.tabs {
  display: flex;
  background: var(--card-bg);
  border-bottom: 1px solid var(--border-color);
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}

.tabs::-webkit-scrollbar {
  display: none;
}

.tabs button {
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
  border-bottom: 3px solid transparent;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tabs button:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.05);
}

.tabs button.active {
  color: var(--primary-color);
  border-bottom: 3px solid var(--primary-color);
}

.tab-icon {
  font-size: 1.2rem;
}

.tab-text {
  display: inline;
}

.tab-content {
  padding: 1.5rem;
  flex: 1;
  min-height: calc(100vh - 120px);
  overflow-y: auto;
}

@media (max-width: 1200px) {
  html {
    font-size: 15px;
  }
  
  .app-container {
    border-radius: 10px;
  }
}

@media (max-width: 992px) {
  html {
    font-size: 14px;
  }
  
  .tab-content {
    padding: 1.25rem;
  }
}

@media (max-width: 768px) {
  #app {
    padding: 0.5rem;
  }
  
  .app-container {
    border-radius: 8px;
  }
  
  .tabs button {
    padding: 0.8rem 1rem;
    font-size: 0.9rem;
  }
  
  .tab-icon {
    font-size: 1.1rem;
  }
  
  .tab-text {
    display: none;
  }
  
  .tab-content {
    padding: 1rem;
    min-height: calc(100vh - 80px);
  }
}

@media (max-width: 480px) {
  html {
    font-size: 13px;
  }
  
  .tabs button {
    padding: 0.7rem 0.8rem;
    font-size: 0.85rem;
  }
  
  .tab-icon {
    font-size: 1rem;
  }
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
  color: var(--text-secondary);
}

.error {
  color: #ff6b6b;
}

.hide-on-mobile {
  display: block;
}

.show-on-mobile {
  display: none;
}

@media (max-width: 768px) {
  .hide-on-mobile {
    display: none;
  }
  
  .show-on-mobile {
    display: block;
  }
}
</style>