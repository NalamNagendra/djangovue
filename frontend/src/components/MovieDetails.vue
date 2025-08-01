<template>
  <div class="movie-details">
    <!-- Loading State -->
    <div v-if="loading" class="loading">Loading movie details...</div>
    
    <!-- Error State -->
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <!-- Content -->
    <template v-else>
      <!-- Backdrop with Parallax Effect -->
      <div class="backdrop" :style="backdropStyle">
        <div class="backdrop-overlay"></div>
      </div>

      <div class="container">
        <div class="movie-content">
          <!-- Poster with Hover Effect -->
          <div class="poster-container" @mouseover="showTrailer = true" @mouseleave="showTrailer = false">
            <img :src="movie.Poster" :alt="movie.Title" class="poster" v-if="movie.Poster !== 'N/A'">
            <div class="poster-placeholder" v-else>No Image Available</div>
            <div v-if="showTrailer" class="play-trailer" @click="playTrailer">
              <i class="play-icon">▶</i>
              <span>Play Trailer</span>
            </div>
          </div>

          <!-- Movie Info -->
          <div class="movie-info">
            <div class="header-section">
              <h1 class="title">{{ movie.Title }} <span class="year">({{ movie.Year }})</span></h1>
              
              <!-- Rating -->
              <div class="rating-container" v-if="movie.imdbRating && movie.imdbRating !== 'N/A'">
                <div class="rating-circle">
                  {{ Math.round(movie.imdbRating * 10) }}<small>%</small>
                </div>
                <div class="rating-label">User Score</div>
              </div>
            </div>
            
            <!-- Facts -->
            <div class="facts">
              <span class="release">{{ formatDate(movie.Released) }}</span>
              <span class="separator">•</span>
              <span class="runtime">{{ movie.Runtime }}</span>
              <span class="separator">•</span>
              <span class="rating">{{ movie.Rated }}</span>
              <span class="separator">•</span>
              <span class="genre">{{ movie.Genre?.split(', ')[0] }}</span>
            </div>

            <!-- Actions -->
            <div class="actions">
              <button class="action-btn" @click="toggleLike" :class="{ liked: isLiked }">
                <span class="icon">{{ isLiked ? '❤️' : '🤍' }}</span>
                <span>{{ isLiked ? 'Liked' : 'Like' }}</span>
              </button>
              <button class="action-btn" @click="addToList">
                <span class="icon">+</span>
                <span>Add to List</span>
              </button>
              <button class="action-btn" @click="shareMovie">
                <span class="icon">↗️</span>
                <span>Share</span>
              </button>
            </div>

            <!-- Tagline -->
            <div class="tagline" v-if="movie.Plot">
              <p>{{ movie.Plot }}</p>
            </div>

            <!-- Overview with Read More -->
            <div class="overview">
              <h3>Overview</h3>
              <p :class="{ 'collapsed': !showFullOverview }">
                {{ movie.Plot }}
                <button v-if="movie.Plot?.length > 200" @click="showFullOverview = !showFullOverview" class="read-more-btn">
                  {{ showFullOverview ? 'Show less' : 'Read more' }}
                </button>
              </p>
            </div>

            <!-- Additional Info in Tabs -->
            <div class="tabs">
              <button v-for="tab in tabs" 
                      :key="tab" 
                      :class="{ active: activeTab === tab }"
                      @click="activeTab = tab">
                {{ tab }}
              </button>
            </div>

            <div class="tab-content">
              <div v-if="activeTab === 'Cast' && movie.Actors" class="cast-grid">
                <div v-for="(actor, index) in movie.Actors.split(', ').slice(0, 6)" :key="index" class="cast-member">
                  <div class="cast-avatar"></div>
                  <div class="cast-name">{{ actor }}</div>
                </div>
              </div>

              <div v-else-if="activeTab === 'Details'" class="additional-info">
                <div class="info-item" v-if="movie.Director !== 'N/A'">
                  <span class="info-label">Director:</span>
                  <span>{{ movie.Director }}</span>
                </div>
                <div class="info-item" v-if="movie.Writer !== 'N/A'">
                  <span class="info-label">Writers:</span>
                  <span>{{ movie.Writer }}</span>
                </div>
                <div class="info-item" v-if="movie.Genre !== 'N/A'">
                  <span class="info-label">Genres:</span>
                  <span>{{ movie.Genre }}</span>
                </div>
                <div class="info-item" v-if="movie.Language !== 'N/A'">
                  <span class="info-label">Language:</span>
                  <span>{{ movie.Language }}</span>
                </div>
                <div class="info-item" v-if="movie.Country !== 'N/A'">
                  <span class="info-label">Country:</span>
                  <span>{{ movie.Country }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

export default {
  name: 'MovieDetails',
  setup() {
    const movie = ref({});
    const loading = ref(true);
    const error = ref(null);
    const showFullOverview = ref(false);
    const showTrailer = ref(false);
    const isLiked = ref(false);
    const activeTab = ref('Cast');
    const tabs = ['Cast', 'Details'];

    const backdropStyle = computed(() => {
      if (movie.value.Poster && movie.value.Poster !== 'N/A') {
        return {
          backgroundImage: `linear-gradient(to right, rgba(3, 37, 65, 0.9) 0%, rgba(3, 37, 65, 0.7) 100%), url(${movie.value.Poster})`
        };
      }
      return { backgroundColor: '#032541' };
    });

    const formatDate = (dateString) => {
      if (!dateString) return '';
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    };

    const fetchMovieDetails = async () => {
  loading.value = true;
  try {
    const response = await axios.get(
      'http://www.omdbapi.com/?i=tt3896198&apikey=d2132124&plot=full'
    );
    movie.value = response.data;
  } catch (err) {
    error.value = 'Failed to load movie details. Using sample data instead.';
    console.error('Error:', err);
    // Fallback to sample data
    movie.value = { /* sample data */ };
  } finally {
    loading.value = false;
  }
};
    const toggleLike = () => {
      isLiked.value = !isLiked.value;
      // In a real app, you would make an API call here to save the like
    };

    const addToList = () => {
      // Implementation for adding to watchlist
      alert('Added to your list!');
    };

    const shareMovie = () => {
      if (navigator.share) {
        navigator.share({
          title: movie.value.Title,
          text: `Check out ${movie.value.Title} (${movie.value.Year}) on our platform!`,
          url: window.location.href,
        }).catch(console.error);
      } else {
        // Fallback for browsers that don't support Web Share API
        const text = `Check out ${movie.value.Title} (${movie.value.Year}): ${window.location.href}`;
        navigator.clipboard.writeText(text).then(() => {
          alert('Link copied to clipboard!');
        });
      }
    };

    const playTrailer = () => {
      // In a real app, this would open a modal with the trailer
      alert('Playing trailer...');
    };

    onMounted(() => {
      fetchMovieDetails();
    });

    return {
      movie,
      loading,
      error,
      backdropStyle,
      showFullOverview,
      showTrailer,
      isLiked,
      activeTab,
      tabs,
      formatDate,
      toggleLike,
      addToList,
      shareMovie,
      playTrailer
    };
  }
}
</script>

<style scoped>
/* Previous styles remain the same, add these new styles: */

/* Header Section */
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.rating-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: 20px;
}

.rating-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #081c22;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  border: 3px solid #21d07a;
}

.rating-circle small {
  font-size: 0.6em;
  margin-left: 1px;
}

.rating-label {
  font-size: 0.8rem;
  margin-top: 5px;
  color: #9ab;
}

/* Tabs */
.tabs {
  display: flex;
  border-bottom: 1px solid #405266;
  margin: 30px 0 20px;
}

.tabs button {
  background: none;
  border: none;
  color: #fff;
  padding: 10px 20px;
  margin-right: 10px;
  cursor: pointer;
  position: relative;
  font-size: 1rem;
  opacity: 0.7;
  transition: opacity 0.3s;
}

.tabs button:hover {
  opacity: 1;
}

.tabs button.active {
  opacity: 1;
  font-weight: 600;
}

.tabs button.active:after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 3px;
  background: #01b4e4;
}

/* Cast Grid */
.cast-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.cast-member {
  text-align: center;
}

.cast-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #1a2f40;
  margin: 0 auto 10px;
  overflow: hidden;
}

.cast-name {
  font-size: 0.9rem;
  color: #9ab;
}

/* Read More Button */
.read-more-btn {
  background: none;
  border: none;
  color: #01b4e4;
  cursor: pointer;
  padding: 0;
  margin-left: 5px;
  font-weight: 600;
}

.read-more-btn:hover {
  text-decoration: underline;
}

/* Collapsible Text */
p.collapsed {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Play Trailer Button */
.play-trailer {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.3s;
}

.poster-container {
  position: relative;
  cursor: pointer;
}

.poster-container:hover .play-trailer {
  opacity: 1;
}

.play-icon {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

/* Like Button */
.action-btn.liked {
  background: #ff4d4d;
  color: white;
}

.action-btn.liked:hover {
  background: #ff3333;
}

/* Responsive Improvements */
@media (max-width: 768px) {
  .header-section {
    flex-direction: column;
  }
  
  .rating-container {
    margin: 15px 0 0;
    align-self: flex-start;
  }
  
  .tabs {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 5px;
  }
  
  .tabs button {
    padding: 10px 15px;
    white-space: nowrap;
  }
  
  .cast-grid {
    grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
    gap: 15px;
  }
  
  .cast-avatar {
    width: 60px;
    height: 60px;
  }
}

/* Loading and Error States */
.loading, .error {
  text-align: center;
  padding: 50px;
  font-size: 1.2rem;
}

.error {
  color: #ff6b6b;
}
</style>