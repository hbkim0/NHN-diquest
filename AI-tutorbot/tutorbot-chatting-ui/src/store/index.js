import Vue from 'vue';
import Vuex from 'vuex';
import { userLogin, userLogout } from '../api/index.js';

Vue.use(Vuex);

export const store = new Vuex.Store({
	state: {
		userInfo: {},
	},
	getters:{
		getUserInfo(state){
			return state.userInfo;
		}
	},
	mutations: {
		SET_USERINFO(state, userinfo) {
			state.userInfo = userinfo;
		},
	},
	actions: {
		FETCH_LOGIN({ commit }, userinfo) {
			return userLogin(userinfo)
				.then(response => {
					if (response.status === 200) {
						commit('SET_USERINFO', {
							userid: userinfo.username,
							key: response.data.key,
						});
						return true;
					} else {
						return false;
					}
				})
				.catch(error => {
					console.log(error);
					alert(
						`에러코드 : ${error.response.status} \n로그인 인증에 실패 했습니다.`,
					);
					return false;
				});
		},
		FETCH_LOGOUT({ commit }) {
			return userLogout()
				.then(() => {
					commit('SET_USERINFO', {});
				})
				.catch(error => {
					console.log(error);
				});
		},
	},
});
