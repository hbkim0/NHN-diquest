<template>
	<div class="chat_wrapper type_login">
		<!-- 로그인 start -->
		<div class="login_wrapper">
			<div class="login_title">
				<h2><b>AI 자동채점 튜터봇</b></h2>
			</div>

			<!-- 로그인 폼 start -->
			<div class="login_form">
				<form @submit.prevent="login">
					<fieldset>
						<legend>로그인</legend>
						<ul class="login_input">
							<li>
								<input
									ref="userid"
									v-model="userData.userid"
									type="text"
									class="chat_form_gray"
									placeholder="아이디"
								/>
							</li>
							<li>
								<input
									ref="password"
									v-model="userData.password"
									type="text"
									class="chat_form_gray"
									placeholder="이름"
									autocomplete="off"
								/>
							</li>
						</ul>

						<ul class="bot_btnset horizontal align_center">
							<li class="w100">
								<button class="btn medium primary_c w100" type="submit">
									로그인
								</button>
							</li>
						</ul>
					</fieldset>
				</form>
			</div>
			<!--// 로그인 폼 end -->
		</div>
		<!--// 로그인 end -->

		<!-- 로그인 푸터 start -->
		<div class="login_foot">
			<div class="copyright">
				Copyright@HTC. All rights reserved.
			</div>
		</div>
		<!--// 로그인 푸터 end -->
	</div>
</template>

<script>
// eslint-disable-next-line no-undef
require('es6-promise').polyfill();

export default {
	name: 'Login',
	components: {},
	data: function() {
		return {
			userData: {
				userid: '',
				password: '',
			},
			autoLogin: false,
		};
	},
	mounted() {
		this.$refs.userid.focus();
	},
	methods: {
		login() {
			if (!this.userData.userid) {
				alert('아이디 항목은 필수 항목입니다.');
				this.$refs.userid.focus();
				return;
			}
			if (!this.userData.password) {
				alert('비밀번호 항목은 필수 항목입니다.');
				this.$refs.password.focus();
				return;
			}
			this.$store
				.dispatch('FETCH_LOGIN', {
					username: this.userData.userid,
					password: this.userData.password,
				})
				.then(res => {
					if (res) {
						this.$router.push('/ChatArea');
					} else {
						this.userData.userid = '';
						this.userData.password = '';
						this.$refs.userid.focus();
					}
				})
				.catch(error => {
					console.log(error);
				});
		},
	},
};
</script>
