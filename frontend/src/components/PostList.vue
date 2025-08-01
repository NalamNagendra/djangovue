<template>
  <div class="post-list">
    <div v-if="loading && posts.length === 0" class="loading">Loading posts...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else>
      <div v-for="(post, index) in posts" :key="post.id || index" class="post">
        <div class="post-header">
          <h3 class="post-title">{{ post.text }}</h3>
          <div class="post-meta">
            <span class="post-author">By {{ post.author }}</span>
            <span class="post-timestamp">{{ formatDate(post.timestamp) }}</span>
          </div>
          <p class="post-comment-count">{{ post.comment_count }} {{ post.comment_count === 1 ? 'Comment' : 'Comments' }}</p>
        </div>
        
        <div v-if="post.comments && post.comments.length > 0" class="comments">
          <h4>Top Comments:</h4>
          <div v-for="(comment, cIndex) in post.comments" :key="cIndex" class="comment">
            <p class="comment-text">{{ comment.text }}</p>
            <div class="comment-meta">
              <span class="comment-author">{{ comment.author }}</span>
              <span class="comment-timestamp">{{ formatDate(comment.timestamp) }}</span>
            </div>
          </div>
        </div>
        
        <div v-else class="no-comments">
          No comments yet. Be the first to comment!
        </div>
      </div>
      
      <div v-if="loadingMore" class="loading-more">
        Loading more posts...
      </div>
      <div v-else-if="!hasMore" class="no-more-posts">
        No more posts to load
      </div>
      <div v-else ref="loadMoreElement" class="load-more-container">
        <button @click="loadMore" class="load-more-btn">Load More</button>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import axios from 'axios';

export default {
  name: 'PostList',
  setup() {
    const posts = ref([]);
    const page = ref(1);
    const hasMore = ref(true);
    const loading = ref(true);
    const loadingMore = ref(false);
    const error = ref(null);
    const observer = ref(null);
    const loadMoreElement = ref(null);

    const formatDate = (dateString) => {
      if (!dateString) return '';
      const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      };
      return new Date(dateString).toLocaleDateString(undefined, options);
    };

    const loadPosts = async () => {
      if (loadingMore.value) return;
      
      try {
        if (page.value === 1) {
          loading.value = true;
        } else {
          loadingMore.value = true;
        }
        
        error.value = null;
        
        const response = await axios.get(`http://localhost:8000/api/posts/`, {
          params: {
            page: page.value,
            random: true
          }
        });
        
        if (response.data.error) {
          throw new Error(response.data.error);
        }
        
        if (response.data.posts.length === 0) {
          hasMore.value = false;
        } else {
          posts.value = [...posts.value, ...response.data.posts];
          page.value++;
        }
      } catch (err) {
        console.error('Error fetching posts:', err);
        error.value = err.response?.data?.error || 'Failed to load posts. Please try again later.';
      } finally {
        loading.value = false;
        loadingMore.value = false;
      }
    };

    const loadMore = () => {
      if (!loadingMore.value && hasMore.value) {
        loadPosts();
      }
    };

    const setupObserver = () => {
      if (observer.value) {
        observer.value.disconnect();
      }
      
      const options = {
        root: null,
        rootMargin: '0px',
        threshold: 0.5
      };
      
      observer.value = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && !loadingMore.value && hasMore.value) {
          loadMore();
        }
      }, options);
      
      if (loadMoreElement.value) {
        observer.value.observe(loadMoreElement.value);
      }
    };

    onMounted(() => {
      loadPosts().then(() => {
        setupObserver();
      });
    });

    onBeforeUnmount(() => {
      if (observer.value) {
        observer.value.disconnect();
      }
    });

    return {
      posts,
      loadMore,
      hasMore,
      loading,
      loadingMore,
      error,
      formatDate,
      loadMoreElement
    };
  }
};
</script>

<style scoped>
.post-list {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.loading,
.error,
.loading-more,
.no-more-posts {
  text-align: center;
  padding: 20px;
  margin: 20px 0;
  border-radius: 8px;
  background-color: #f8f9fa;
}

.error {
  color: #dc3545;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
}

.post {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.post:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.post-header {
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
}

.post-title {
  font-size: 1.4em;
  color: #2c3e50;
  margin: 0 0 10px 0;
  line-height: 1.4;
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 12px;
  font-size: 0.9em;
  color: #6c757d;
}

.post-author {
  font-weight: 600;
  color: #495057;
}

.post-timestamp {
  font-size: 0.85em;
  color: #868e96;
}

.post-comment-count {
  font-size: 0.9em;
  color: #4a6fa5;
  font-weight: 500;
  margin: 10px 0 0 0;
}

.comments {
  padding: 16px 20px;
  background-color: #f8f9fa;
}

.comments h4 {
  font-size: 0.95em;
  color: #495057;
  margin: 0 0 12px 0;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.comment {
  padding: 12px;
  margin-bottom: 12px;
  background-color: #ffffff;
  border-radius: 6px;
  border-left: 3px solid #4a6fa5;
}

.comment:last-child {
  margin-bottom: 0;
}

.comment-text {
  color: #343a40;
  margin: 0 0 8px 0;
  line-height: 1.5;
}

.comment-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.8em;
  color: #6c757d;
}

.no-comments {
  padding: 16px 20px;
  color: #6c757d;
  font-style: italic;
  text-align: center;
  background-color: #f8f9fa;
}

.load-more-container {
  text-align: center;
  margin: 24px 0;
}

.load-more-btn {
  background-color: #4a6fa5;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 6px;
  font-size: 0.95em;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.load-more-btn:hover {
  background-color: #3a5a80;
}

.load-more-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.loading-more,
.no-more-posts {
  text-align: center;
  color: #6c757d;
  padding: 16px;
  font-size: 0.95em;
}

@media (max-width: 768px) {
  .post-list {
    padding: 10px;
  }
  
  .post-header {
    padding: 16px;
  }
  
  .post-title {
    font-size: 1.2em;
  }
  
  .comments {
    padding: 12px 16px;
  }
}

@media (max-width: 480px) {
  .post-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
  
  .comment {
    padding: 10px;
  }
  
  .load-more-btn {
    width: 100%;
    padding: 12px;
  }
}
</style>