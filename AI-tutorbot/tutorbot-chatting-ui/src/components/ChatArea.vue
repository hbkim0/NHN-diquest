<template>
	<div class="chat_wrapper" @click="onClick($event)">
		<!-- 헤더 영역 -->
		<header-area
			:firstUser="helpShow"
			:userInfo="userInfo"
			:menuShow="menuShow"
			@btnClick="addMessage"
			@chatAreaInit="chatAreaInit"
		/>

		<!-- 채팅 영역 -->
		<ic-ans-message
			:messageList="messageList"
			:theme="theme"
			:chatbot="chatbot"
			:locale="'ko'"
			:wait="ansWait"
			@componentMessage="componentMessage"
		>
			<template v-slot:message_footer="slotProps">
				<!-- chat foot start -->
				<div class="chat_foot">
					<div class="chat_date left">
						{{ $moment(slotProps.item.dt).format('a h:mm') }}
					</div>
				</div>
				<!--// chat foot end -->
			</template>
		</ic-ans-message>

		<!-- 글쓰기 영역 -->
		<writing-area
			:userInfo="userInfo"
			:chatActive="chatActive"
			:writingDisable="ansWait"
			:messageList="messageList"
			@writeContent="addMessage"
			@errorCatch="messagePush"
		/>
	</div>
</template>

<script>
// eslint-disable-next-line no-undef
require('es6-promise').polyfill();
import storage from '../api/storage';
import HeaderArea from './HeaderArea.vue';
import WritingArea from './WritingArea.vue';
import config from '../config/config.json';
import { mapGetters } from 'vuex';

export default {
	name: 'ChatArea',
	components: {
		'header-area': HeaderArea,
		'writing-area': WritingArea,
		// ...Infochatter3AnswerUikit,
	},
	data() {
		return {
			userInfo: {},
			messageList: [],
			ansWait: false,
			chatLog: [],
			helpShow: false,
			menuShow: false,
			chatActive: false,
			theme: {
				class: 'basic',
				profile: {
					useYn: 'N', // "Y" or "N"
				},
			},
			chatbot: {
				name: '닥터 바로',
				// img: '../assets/img_chatbot/profile/profile_default.png',
			},
			mobile: false,
		};
	},
	computed: {
		...mapGetters({
			getUserInfo : 'getUserInfo',
		})
	},
	created() {
		this.settingUserInfo();
	},
	mounted() {
		this.chatStartUp();
		this.mobile = this.mobileCheck();
	},
	methods: {
		chatAreaInit(props) {
			if (props === 'initStart') {
				this.userInfo = {};
				this.helpShow = false;
				this.settingUserInfo();
				this.messageList = [];
				this.mobile = false;
				this.chatActive = false;
				this.ansWait = false;
				this.chatStartUp();
				this.mobile = this.mobileCheck();
			}
		},
		onClick(event) {
			const className = event.srcElement.className;

			if (className.match('btn_menu')) {
				this.menuShow = !this.menuShow;
			} else {
				this.menuShow = false;
			}
		},
		settingUserInfo() {
			const userData = storage.getUserData();
			this.userInfo.agentName = config.AGENT_NAME;
			this.userInfo.repoId = config.REPO_ID;

			if (userData) {
				this.userInfo.userId = userData.mbrId;
				this.userInfo.userNm = userData.mbrNm;
				if (userData.firstYn === 'Y' && !userData.lastLgnDt) {
					this.helpShow = true;
					userData.lastLgnDt = 'first';
					storage.setUserData(userData);
				} else {
					this.helpShow = false;
				}
			} else {
				this.userInfo.userId = config.USER_ID;
			}
		},
		mobileCheck() {
			const tempUser = navigator.userAgent;
			let isMobile = false;

			// userAgent 값에 iPhone, iPad, ipot, Android 라는 문자열이 하나라도 존재한다면 모바일로 간주됨.
			if (
				tempUser.indexOf('iPhone') > 0 ||
				tempUser.indexOf('iPad') > 0 ||
				tempUser.indexOf('iPod') > 0 ||
				tempUser.indexOf('Android') > 0
			) {
				isMobile = true;
			}
			return isMobile;
		},
		addChatLog(chatLog) {
			var vm = this;
			vm.chatLog += chatLog + '\n';
		},
		componentMessage(props) {
			let tagDqml = null;
			if (props.result) {
				// input이 여러개일 경우
				const keys = Object.keys(props.result);
				let transferMsgs = [];
				let displayMsgs = [];
				let dqmlMsgs = [];
				keys.forEach(key => {
					if (
						props.result[key].transferText &&
						props.result[key].transferText !== ''
					) {
						transferMsgs.push(props.result[key].transferText);
					}
					if (
						props.result[key].displayText &&
						props.result[key].displayText !== ''
					) {
						displayMsgs.push(props.result[key].displayText);
					}
					if (props.result[key].transferText_item) {
						transferMsgs.push(props.result[key].transferText_item);
					}
					if (props.result[key].dqml && props.result[key].dqml !== '') {
						dqmlMsgs.push(props.result[key].dqml);
					}
				});
				if (props.displayText) {
					console.log(props.displayText);
					console.log(displayMsgs.join());
					this.addMessage(
						props.displayText,
						displayMsgs.join(),
						dqmlMsgs.join(),
					);
				} else {
					console.log(transferMsgs.join());
					console.log(displayMsgs.join());
					this.addMessage(
						displayMsgs.join(),
						transferMsgs.join(),
						dqmlMsgs.join(),
					);
				}
			} else {
				if (props.dqml) {
					tagDqml = props.dqml;
				}
				this.addMessage(
					props.displayText,
					props.transferText.replace('&lt;', '<').replace('&gt;', '>'),
					tagDqml,
				);
			}
		},
		messagePush(messages, emotion) {
			if (!emotion) {
				emotion = 'BASIC';
			}
			messages.forEach(msg => {
				this.messageList.push({
					author: 'bot',
					iuml: msg.text,
					dt: this.$moment().format('YYYY-MM-DD HH:mm:ss'),
					likeHate: '',
					emotion: emotion,
					index: this.messageList.length,
				});
			});
			this.ansWait = false;
			this.downScroll();
		},
		chatStartUp() {
			this.ansWait = true;
			const chatReqData = {
				agentName: this.userInfo.agentName,
				repoId: this.userInfo.repoId,
				sessionId: this.userInfo.sessionId,
				userId: this.userInfo.userId,
				persistDqml: { userId: this.getUserInfo.userid },
			};
			this.$axios
				.post(config.REST_API_PATH + '/chat/startup', chatReqData)
				.then(response => {
					const { data } = response;

					this.userInfo.agentName = data.changeAgt
						? data.changeAgt
						: data.agentName;
					this.userInfo.sessionId = data.sessionId;

					if (data.chatActive && data.chatActive !== 'true') {
						this.messageList.forEach(msg => {
							msg.disabled = true;
						});
					}

					this.chatActive = data.chatActive ? data.chatActive === 'true' : true;
					setTimeout(() => {
						this.messagePush(data.messages, data.emotion);
					}, 1000);

					// 다중폼 예시
					// 폼 1개
					/*
					this.messageList.push({
						author: 'bot',
						iuml:
							'<bubble class="icBubbleClass1" emotion="놀람"> <text>예상 퇴직급여 조회입니다. 원하시는 분의 정보를 입력해주세요.</text> <layout class="icLayoutClass6"> <input align="right" id="input1_2" type="text" class="chat_form_gray" label="주민등록번호"></input> </layout> <text>조회구분</text> <layout class="icLayoutClass6" align="horizontal"> <radiobutton class="right" name="radio5" value="Y3" text="현재기준"></radiobutton> <radiobutton class="right" name="radio5" value="Y4" text="미래기준"></radiobutton> </layout> <text>서울</text> <layout class="icLayoutClass2"> <button class="icBtnClass13" label="확인"></button> </layout> </bubble>',
						dt: this.$moment().format('YYYY-MM-DD HH:mm:ss'),
						likeHate: '',
						emotion: '',
						index: this.messageList.length,
					});
					*/

					// 폼 2개
					/*
					this.messageList.push({
						author: 'bot',
						iuml:
							'<bubble class="icBubbleClass1" emotion="놀람"> <text>예상 퇴직급여 조회입니다. 원하시는 분의 정보를 입력해주세요.</text> <layout class="icLayoutClass6"> <input align="right" id="input1_1" type="text" class="chat_form_gray" label="이름"></input> <input align="right" id="input1_2" type="text" class="chat_form_gray" label="주민등록번호"></input> </layout> <text>조회구분</text> <layout class="icLayoutClass6" align="horizontal"> <radiobutton class="right" name="radio5" value="Y3" text="현재기준"></radiobutton> <radiobutton class="right" name="radio5" value="Y4" text="미래기준"></radiobutton> </layout> <text>서울</text> <layout class="icLayoutClass2"> <button class="icBtnClass13" label="확인"></button> </layout> </bubble>',
						dt: this.$moment().format('YYYY-MM-DD HH:mm:ss'),
						likeHate: '',
						emotion: '',
						index: this.messageList.length,
					});
					*/
					console.log('response.data >>> ', data);
					console.log('userInfo >>> ', this.userInfo);
				})
				.finally(() => {
					//스크롤 가장 아래
					this.downScroll();
				});
		},
		addMessage(chatText, query, tagDqml = null) {
			if (!this.chatActive) {
				this.messageList.forEach(msg => {
					msg.disabled = true;
				});
			}
			//화면에 사용자 말풍선 추가
			var userMessage = {
				author: 'user',
				text: chatText,
				query: query,
				dt: this.$moment().format('YYYY-MM-DD HH:mm:ss'),
			};
			// this.messages.forEach(messages=>{
			//   messages.isDisabled=true;
			// })
			this.messageList.push(userMessage);
			this.downScroll();

			this.addChatLog('Q:' + userMessage.chatText);

			//메시지 전송 호출
			this.ansWait = true;

			this.sendMessage(query, tagDqml);
		},
		//메시지 전송
		sendMessage(query, tagDqml = null) {	
			var chatReqData = {
				agentName: this.userInfo.agentName,
				repoId: this.userInfo.repoId,
				sessionId: this.userInfo.sessionId,
				userId: this.userInfo.userId,
				query: query,
				persistDqml: { userId: this.getUserInfo.userid },
			};
			if (tagDqml !== null && tagDqml != '') {
				chatReqData.extDqml = tagDqml;
			}

			//화면에 챗봇 말풍선 추가
			this.$axios
				.post(config.REST_API_PATH + '/chat/message', chatReqData)
				.then(response => {
					const { data } = response;
					this.userInfo.agentName = data.changeAgt
						? data.changeAgt
						: data.agentName;
					this.userInfo.sessionId = data.sessionId;

					if (data.chatActive && data.chatActive !== 'true') {
						this.messageList.forEach(msg => {
							msg.disabled = true;
						});
					}

					this.chatActive = data.chatActive ? data.chatActive === 'true' : true;
					setTimeout(() => {
						this.messagePush(data.messages, data.emotion);
					}, 1000);
					/*테스틓setTimeout(() => {
						this.messagePush(data.messages, data.emotion);
					}, 1000);*/

					console.log('response.data >>> ', data);
					// console.log('userInfo >>> ', this.userInfo);
				})
				.catch(error => {
					const text = `문제가 발생했습니다 다시 시도해주세요. 계속해서 문제가 발생할 시 관리자에게 문의해주세요.<br>에러코드(${error.response.status})`;
					this.messagePush([{text: text}], null);
				})
				.finally(() => {
					//스크롤 가장 아래
					this.downScroll();
				});
		},
		onClickFeedback(item, satiNum) {
			let actType;
			if (item.likeHate) {
				if (item.likeHate === satiNum) {
					actType = 'D'; // 취소
				} else {
					actType = 'U'; // 변경
				}
			} else {
				actType = 'I'; // 등록
			}

			const userQuery = this.messageList[item.index - 1];
			this.$axios
				.post(config.REST_API_PATH + '/chat/perf-rv/saveSatisfactionNum', {
					actType: actType,
					agtNm: this.userInfo.agentName,
					answer: item.iuml,
					id: actType !== 'I' ? item.satiId : null,
					qry: userQuery ? userQuery.query : null,
					repoId: this.userInfo.repoId,
					satisfactionNum: satiNum,
					sessId: this.userInfo.sessionId,
					userId: this.userInfo.userId,
				})
				.then(response => {
					const { data } = response;
					if (data.status) {
						// 피드백 성공
						if (actType === 'D') {
							item.likeHate = null;
							item.satiId = null;
						} else {
							item.likeHate = satiNum;
							item.satiId = data.id;
						}
					} else {
						alert('정상적으로 처리되지 않았습니다.');
					}
				})
				.catch(() => {
					alert('정상적으로 처리되지 않았습니다.');
					// console.log(error);
				});
		},
		downScroll() {
			// eslint-disable-next-line no-undef
			$('.chat_area').animate({
				// eslint-disable-next-line no-undef
				scrollTop: $('.chat_area')[0].scrollHeight,
			});
		},
		// 화면 리사이즈시 스크롤 아래
		bindWindowResize() {
			// eslint-disable-next-line no-undef
			$(window).resize(function() {
				this.downScroll();
			});
		},
	},
};
</script>
<style scoped>
.nohover:hover {
	opacity: 0.3 !important;
	color: #000 !important;
}
.hate.on.nohover:hover {
	opacity: 1 !important;
	color: #4590ec !important;
}
.like.on.nohover:hover {
	opacity: 1 !important;
	color: #f46969 !important;
}
</style>
