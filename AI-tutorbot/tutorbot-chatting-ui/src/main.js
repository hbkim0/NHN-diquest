import Vue from 'vue';
import App from './App.vue';
import axios from 'axios';
import VModal from 'vue-js-modal';
import router from './router';
import { store } from './store/index.js';
import config from './config/config.json';

import moment from 'moment';
Vue.prototype.$moment = moment;
moment.locale('ko');

Vue.use(VModal, { dialog: true, dynamic: true, injectModalsContainer: true });

Vue.prototype.$axios = axios.create({
	baseURL: config.REST_URL,
	headers: {
		'Content-Type': 'application/json',
	},
});

// import infochatter3AnswerUikit from "./uikit/infochatter3AnswerUikit.umd.min";
// import "./uikit/infochatter3AnswerUikit.css";
// Vue.use(infochatter3AnswerUikit);
import Infochatter3AnswerUikit from './uikit/infochatter3-answer-uikit';
Vue.use(Infochatter3AnswerUikit);

import './assets/css/style.css';

new Vue({
	el: '#app',
	render: h => h(App),
	router,
	store,
});
