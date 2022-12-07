<template>
	<!-- 푸터 start -->
	<div class="bot_footer">
		<div class="accessibility_blank">
			<!-- 입력 영역 start -->
			<div class="send_area">
				<!-- 이미지 업로드 start -->
				<div class="send_image_form">
					<input
						ref="imageUploader"
						type="file"
						id="file"
						style="display:none;"
						accept=".gif, .jpg, .png"
						@change="fileSelect"
					/>
					<label for="file" :class="{ disabled: !chatActive | writingDisable }">
						<img
							class="send_gallery_icon"
							src="../assets/img_chatbot/chatbot/gallery-icon.png"
						/>
					</label>
				</div>
				<!-- 이미지 업로드 end -->
				<div class="send_form">
					<fieldset>
						<legend>질문 입력</legend>
						<div class="input_wrap">
							<input
								id="send_input"
								ref="content"
								v-model="content"
								type="text"
								class=""
								:placeholder="getPlaceholder"
								:disabled="!chatActive"
								@keypress.enter="writeContent"
								@input="content = $event.target.value"
							/>
							<button
								type="button"
								class="btn_send fas fa-arrow-up"
								:class="{ disabled: !chatActive | writingDisable | !content }"
								@click="writeContent"
							>
								<span class="bg_clip">보내기</span>
							</button>
						</div>
					</fieldset>
				</div>
			</div>
			<!--// 입력 영역 end -->
		</div>
	</div>
	<!--// 푸터 end -->
</template>

<script>
// eslint-disable-next-line no-undef
require('es6-promise').polyfill();
import EventBus from '../eventBus/eventBus';
import SaveInquiry from './SaveInquiry';
import { getImageIUML } from '../utils/utils';
import config from '../config/config.json';

export default {
	name: 'WritingArea',
	props: {
		userInfo: {
			type: Object,
			default: null,
			required: false,
		},
		// 특정 서비스 중 입력창 disable
		chatActive: {
			type: Boolean,
			default: false,
			required: false,
		},
		// 질의 보낸 후 답변 오기전까지 전송 disable
		writingDisable: {
			type: Boolean,
			default: false,
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
			content: '',
			files: [],
			fileChk: false,
		};
	},
	mounted() {
		this.$refs.content.focus();
	},
	computed: {
		getPlaceholder() {
			if (!this.chatActive) {
				return '사용자 정보를 등록할 때는 질문을 입력하실 수 없습니다.';
			} else {
				return '여기에 질문을 입력해 주세요.';
			}
		},
	},
	methods: {
		fileSelect(e) {
			this.files = e.target.files;
			let tagdqml = null;
			let frm = new FormData();

			//append form data
			if (this.files.length > 0) {
				frm.append('images', this.files[0]);
				this.fileChk = true;
				this.$refs.imageUploader.value = '';
			}

			//file chk
			if (this.fileChk) {
				this.$axios
					.post(`${config.IMAGE_API_URL}/images/upload`, frm, {
						headers: { 'Content-Type': 'multipart/form-data' },
					})
					.then(response => {
						let rtn_content = getImageIUML(response.data.paths[0]);
						let result = [rtn_content, response.data.paths[0]]
						return result;
					})
					.then(result => {
						this.$emit('writeContent', result[0], '채점 확인', {imgUrl: result[1]});
						this.fileChk = false;
					})
					.catch(error => {
						console.log(error);
						const text = `채점 이미지 업로드에 실패했습니다.<br>계속해서 문제가 발생할 시 관리자에게 문의해주세요.<br>에러코드(${error.response.status})`; 
						this.$emit('errorCatch', [{text: text}], null);
					});
			} else {
				const text = `채점 이미지가 확인되지 않습니다. 다시 시도 해주세요.`; 
				this.$emit('errorCatch', [{text: text}], null);
			}
		},
		writeContent() {
			let vm = this;

			if (
				(vm.content == '') |
				(vm.content == '\n') |
				(vm.content.replace(/ /g, '') == '')
			) {
				vm.clearTextArea();
				return;
			} else {
				vm.$emit('writeContent', vm.content, vm.content);
				vm.clearTextArea();
			}
		},
		clearTextArea() {
			// 입력창 초기화
			this.content = '';
			// 파일 초기화
			this.files = '';
			this.fileChk = false;
		},
		onKeyEvent(event) {
			EventBus.$emit('autoCompList', event);
		},
		onClickSaveInquiry() {
			this.$modal.show(
				SaveInquiry,
				{
					userInfo: this.userInfo,
					messageList: this.messageList,
				},
				{
					height: 'auto',
				},
			);
		},
	},
};
</script>
