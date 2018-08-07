import Vue from 'vue'
import About from '@/components/about.vue'

Vue.config.productionTip = false

new Vue({
  render: h => h(About)
}).$mount('#app')
