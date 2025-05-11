import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/views/LandingView.vue'
import RestaurantsPage from '@/views/RestaurantsView.vue'
import RestaurantDetailPage from '@/views/RestaurantDetailView.vue'
import ReviewsView from '@/views/ReviewsView.vue'
import MyReviewsView from '@/views/MyReviewsView.vue'
import BookingView from '@/views/BookingView.vue'
import MyBookingsView from '@/views/RestaurantBookingsView.vue'
import LoginView from '@/views/auth/LoginView.vue'
import SignUpView from '@/views/auth/SignUpView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import AdminPanel from '@/views/AdminPanelView.vue'
import AdminDashboard from '@/components/AdminDashboard.vue'
import UsersTable from '@/components/UsersTable.vue'
import RestaurantsTable from '@/components/RestaurantsTable.vue'
import ReviewsTable from '@/components/ReviewsTable.vue'
import { useAuthStore } from '@/stores/auth'
import ProfileView from '@/views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: LandingPage },
    { path: '/restaurants', component: RestaurantsPage },
    { path: '/restaurant/:id', component: RestaurantDetailPage },
    { path: '/reviews', component: ReviewsView },
    {
      path: '/my-reviews',
      component: MyReviewsView,
      meta: { requiresAuth: true, requiresAdmin: false },
    },
    { path: '/book', component: BookingView, meta: { requiresAuth: true, requiresAdmin: false } },
    {
      path: '/my-bookings',
      component: MyBookingsView,
      meta: { requiresAuth: true, requiresAdmin: false },
    },
    { path: '/login', component: LoginView },
    { path: '/signup', component: SignUpView },
    {
      path: '/profile',
      component: ProfileView,
      meta: { requiresAuth: true, requiresAdmin: false },
    },

    {
      path: '/admin',
      component: AdminPanel,
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        { path: '', component: AdminDashboard },
        { path: 'users', component: UsersTable },
        { path: 'restaurants', component: RestaurantsTable },
        { path: 'reviews', component: ReviewsTable },
      ],
    },
    {
      path: '/:catchAll(.*)',
      name: 'NotFound',
      component: NotFoundView,
    },
  ],
})

// Global Route Guard
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    // Not logged in → redirect to login
    return next('/login')
  }

  if (to.meta.requiresAdmin && !auth.isAdmin) {
    // Not an admin → redirect to home
    return next('/')
  }

  // Otherwise, allow access
  next()
})

export default router
