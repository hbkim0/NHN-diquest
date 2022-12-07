import Vue from 'vue'
import App from './App.vue';

import vuetify from './plugins/vuetify';

import VueKonva from 'vue-konva';

import { router } from './routes/index.js';
import { store } from './store/index.js';

import dayjs from 'dayjs';
Vue.prototype.dayjs = dayjs;

Vue.config.productionTip = false;

Vue.use(VueKonva);

Vue.prototype.API_BASE_URL = process.env.VUE_APP_API_BASE_URL;

import { getCoverImage, getMLTaskName } from './utils/index.js';
Vue.prototype.getCoverImage = getCoverImage;
Vue.prototype.getMLTaskName = getMLTaskName;

new Vue({
  store,
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app');
