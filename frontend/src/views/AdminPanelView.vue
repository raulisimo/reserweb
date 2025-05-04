<template>
  <BaseLayout>
    <div class="admin-panel">
      <nav class="admin-nav">
        <ul>
          <li><router-link to="/admin/users">Usuarios</router-link></li>
          <li><router-link to="/admin/restaurants">Restaurantes</router-link></li>
          <li><router-link to="/admin/reviews">Reseñas</router-link></li>
        </ul>
      </nav>

      <div class="admin-content">
        <router-view></router-view>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import BaseLayout from './layouts/BaseLayout.vue'
</script>

<style scoped>
.admin-panel {
  display: flex;
  min-height: 100vh;
}

.admin-nav {
  width: 220px;
  background-color: #f8f9fa;
  padding: 20px;
  border-right: 1px solid #ddd;
}

.admin-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.admin-nav li {
  margin-bottom: 12px;
}

.admin-nav a {
  display: block;
  padding: 10px 15px;
  text-decoration: none;
  color: #333;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.admin-nav a:hover {
  background-color: #e2e6ea;
}

.admin-nav a.router-link-active {
  background-color: #007bff;
  color: #fff;
}

.admin-content {
  flex: 1;
  padding: 30px;
}
</style>
