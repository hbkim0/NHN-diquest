import Vue from 'vue';
import Router from 'vue-router';
import ChatArea from './components/ChatArea';
import Login from './components/member/Login';
import config from './config/config.json';
import { store } from './store/index.js';

Vue.use(Router);

export default new Router({
	mode: 'history',
	routes: [
		{
			path: '/ChatArea',
			name: 'ChatArea',
			component: ChatArea,
			// beforeEnter: requireAuth(),
			beforeEnter: (to,from,next) => {
				console.log(store.state.userInfo);
				if (config.LOGIN_USE) {
					const userInfo = store.state.userInfo;
					if (userInfo.key) {
						return next();
					} else {
						alert('로그인 정보가 없습니다.');
						return next('/');
					}
				} else {
					return next();
				}
			},
		},
		{
			path: '/',
			name: 'Login',
			component: Login,
			beforeEnter: function(to, from, next) {
				// user 정보가 없을 때만 로그인 페이지로 이동
				console.log('Login key chk', store.state.userInfo.key);
				if (store.state.userInfo.key) {
					return next('/');
				}
				return next();
			},
		},
	],
});
