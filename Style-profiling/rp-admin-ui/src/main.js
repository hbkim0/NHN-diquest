import Vue from 'vue'
import App from './App.vue';

import vuetify from './plugins/vuetify';

import { router } from './routes/index.js';
import { store } from './store/index.js';

import dayjs from 'dayjs';
Vue.prototype.dayjs = dayjs;

Vue.config.productionTip = false;

Vue.prototype.API_BASE_URL = process.env.VUE_APP_API_BASE_URL;

import { returnImageUrl } from './utils/index.js';
Vue.prototype.returnImageUrl = returnImageUrl;

new Vue({
  store,
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app');
