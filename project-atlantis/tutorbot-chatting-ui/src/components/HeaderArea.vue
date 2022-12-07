<template>
	<!-- 헤더 start -->
	<div class="bot_header">
		<div class="top_baro"></div>
		<h1>자동 채점 튜터봇</h1>
		<div class="head_right">
			<ul class="head_cont">
				<li>
					<button
						type="button"
						class="btn_simul_top fas fa-redo-alt"
						:title="'새로고침'"
						style="margin-bottom:6.5px;color:white"
						@click.prevent.stop="chatAreaInit"
					/>
				</li>
				<li v-if="loginUse" class="bot_user">
					<i class="fas fa-user"></i>{{ user.userNm }}
				</li>
				<li class="bot_menu">
					<a href="#" class="btn_menu fas fa-bars" :class="{ on: menuShow }"
						><span class="bg_clip">메뉴</span></a
					>
				</li>
			</ul>
			<transition name="fade">
				<!-- 메뉴 start -->
				<ul v-if="menuShow" class="head_menu" style="display: block;">
					<li v-if="loginUse">
						<a href="#" @click.prevent.stop="logout">로그아웃</a>
					</li>
				</ul>
				<!--// 메뉴 end -->
			</transition>
		</div>
	</div>
	<!--// 헤더 ens -->
</template>

<script>
// eslint-disable-next-line no-undef
require('es6-promise').polyfill();
import config from '../config/config.json';
import Help from './Help';

export default {
	name: 'HeaderArea',
	props: {
		userInfo: {
			type: Object,
			default: null,
			required: false,
		},
		menuShow: {
			type: Boolean,
			default: false,
			required: false,
		},
		firstUser: {
			type: Boolean,
			default: false,
			required: false,
		},
	},
	data() {
		return {
			user: {
				userNm: '',
			},
			health: '',
			loginUse: false,
		};
	},
	created() {
		if (this.firstUser) {
			this.onClickHelp();
		}
	},
	mounted() {
		this.user.userNm = this.userInfo.userNm;
		this.loginUse = config.LOGIN_USE;
	},
	methods: {
		chatAreaInit() {
			this.$emit('chatAreaInit', 'initStart');
		},
		onClickHelp() {
			this.$modal.show(
				Help,
				{
					// id: this.userInfo.userId
				},
				{
					clickToClose: true,
					width: '100%',
					height: '100%',
				},
			);
		},
		logout() {
			// 로그아웃
			this.$store
				.dispatch('FETCH_LOGOUT')
				.then(() => {
					this.$router.push('/');
				})
				.catch(error => {
					console.log(error);
				});
		},
	},
};
</script>
<style scoped>
/* transition fade */
.fade-enter-active {
	transition: 0.3s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
	opacity: 0;
}
</style>
