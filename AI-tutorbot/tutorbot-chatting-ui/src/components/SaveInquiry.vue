<template>
	<div class="chat_wrapper">
		<!-- 모달 : 의견 보내기 start -->
		<div
			id="modal_message"
			class="chat_modal full1"
			style="display: block; position: fixed;"
		>
			<div class="chat_modal_in">
				<div class="chat_modal_head">
					<div class="primary_c">
						<strong>의견 보내기</strong>
					</div>
					<button
						class="btn_modal_close fas fa-times"
						:disabled="save"
						@click="close"
					>
						<span class="bg_clip">닫기</span>
					</button>
				</div>

				<!-- 내용 start -->
				<div class="chat_modal_cont overflow_auto">
					<textarea
						ref="inquiryContents"
						v-model="inquiry.contents"
						class="chat_send_message chat_form_gray"
						placeholder="내용을 입력하세요."
					/>
				</div>
				<!--// 내용 end -->

				<div class="chat_modal_foot">
					<ul class="bot_btnset horizontal align_center half">
						<li>
							<button
								class="btn medium primary_c_bd btn_modal_close"
								:disabled="save"
								@click="close"
							>
								취소
							</button>
						</li>
						<!-- 닫기 .btn_modal_close 추가 -->
						<li>
							<button
								class="btn medium primary_c"
								:disabled="save"
								@click="sendComments"
							>
								보내기
							</button>
						</li>
					</ul>
				</div>
			</div>
		</div>
		<!--// 모달 : 의견 보내기 end -->
	</div>
</template>
<script>
import config from '../config/config.json';

export default {
	name: 'SaveInquiry',
	props: {
		userInfo: {
			type: Object,
			default: null,
			required: false,
		},
		messageList: {
			type: Array,
			default: null,
			required: false,
		},
	},
	data() {
		return {
			inquiry: {
				title: '',
				type: '의견제안',
				contents: '',
			},
			save: false,
		};
	},
	methods: {
		sendComments() {
			// 의견보내기!!
			if (!this.inquiry.contents) {
				alert('내용을 입력해주세요.');
				this.$refs.inquiryContents.focus();
				return;
			}
			const length = this.messageList.length;
			let answer = '',
				qry = '';
			if (length > 0) {
				if (this.messageList[length - 1].author === 'bot') {
					answer = this.messageList[length - 1].iuml;
					qry = this.messageList[length - 2]
						? this.messageList[length - 2].query
						: null;
				} else {
					answer = null;
					qry = this.messageList[length - 1].query;
				}
			}

			this.inquiry.title = this.inquiry.contents.replace(/\n|\r\n|\t/g, ' ');
			if (this.inquiry.title.length > 30) {
				this.inquiry.title = this.inquiry.title.substr(0, 30) + '...';
			}

			this.save = true;
			this.$axios
				.post(config.REST_API_PATH + '/chat/perf-rv/saveInquiry', {
					agtNm: this.userInfo.agentName,
					answer: answer,
					inquiryContents: this.inquiry.contents,
					inquiryTitle: this.inquiry.title,
					inquiryType: this.inquiry.type,
					qry: qry,
					repoId: this.userInfo.repoId,
					sessId: this.userInfo.sessionId,
					userId: this.userInfo.userId,
				})
				.then(response => {
					if (!response.data.status) {
						alert('의견 보내기를 실패하였습니다.');
					} else {
						alert(
							'감사합니다.\n정상적으로 전달되었습니다.\n빠른 시일 내에 작성해 주신 사항을 개선하도록 하겠습니다.',
						);
						this.close();
					}
				})
				.catch(error => {
					alert('의견 보내기를 실패하였습니다.');
					console.log(error);
				})
				.finally(() => {
					this.save = false;
				});
		},
		close() {
			this.$emit('close');
		},
	},
};
</script>
