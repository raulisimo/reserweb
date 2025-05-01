<template>
  <section class="my-5 py-5 bg-white">
    <div class="container">
      <swiper
        :slides-per-view="3"
        :space-between="30"
        :autoplay="{
          delay: 2500,
          disableOnInteraction: false,
        }"
        :pagination="{
          clickable: true,
        }"
        :navigation="true"
        :breakpoints="{
          0: { slidesPerView: 1 },
          768: { slidesPerView: 2 },
          1024: { slidesPerView: 3 },
        }"
        :loop="true"
        :modules="modules"
        class="restaurant-swiper"
      >
        <swiper-slide v-for="(image, index) in images" :key="index">
          <img :src="getImageUrl(image)" class="carousel-img img-fluid rounded" />
        </swiper-slide>
      </swiper>
    </div>
  </section>
</template>

<script>
import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/css'
import 'swiper/css/pagination'
import 'swiper/css/navigation'
import { Pagination, Navigation, Autoplay } from 'swiper/modules'

export default {
  components: { Swiper, SwiperSlide },
  data() {
    return {
      modules: [Pagination, Navigation, Autoplay],
      images: [
        'chinese.png',
        'cocktails.png',
        'couscous.png',
        'falafel.png',
        'hamburger.png',
        'paella.png',
        'pasta.png',
        'pizza.png',
        'ramen.png',
        'salad.png',
        'sushi.png',
        'tacos.png',
        'tapas.png',
        'wok.png',
      ],
    }
  },
  methods: {
    getImageUrl(image) {
      return new URL(`../assets/restaurant-images/${image}`, import.meta.url).href
    },
  },
}
</script>

<style scoped>
.carousel-img {
  height: 400px;
  object-fit: cover;
  object-position: center center;
  width: 100%;
  border-radius: 15px;
}

@media (max-width: 768px) {
  .carousel-img {
    height: 250px;
  }
}

:deep(.swiper-button-next),
:deep(.swiper-button-prev) {
  color: white;
  background: rgba(0, 0, 0, 0.5);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.swiper-button-next::after),
:deep(.swiper-button-prev::after) {
  font-size: 18px;
}
</style>
