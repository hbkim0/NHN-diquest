<!-- 프로필 컴포넌트 -->
<template>
	<ul class="bot_listset m-0">
		<li>
			<div class="thumb medium pr-10px">
				<img v-lazy="imgObj" :title="attribute.title" />
			</div>
			<div class="bot_list_text">
				<div v-for="row in attribute.text" :key="row.id" :class="row.class">
					{{ row.label }}
				</div>
				<hr class="chat_border" />
				<slot></slot>
			</div>
		</li>
	</ul>
</template>
<script>
export default {
	name: 'ic-ans-info',
	props: {
		/**
		 * attribute
		 * XSD 적용 완료-20200311
		 */
		attribute: {
			type: Object,
			default: function() {
				return {
					id: {
						// element에 id를 부여하여 구분할 때 사용
						type: String,
						default: null,
					},
					class: {
						// css와 같이 element에 공통으로 style을 적용할 때 사용
						type: String,
						default: null,
					},
					data: {
						// Element에 데이터를 주고 받을 때 Json 포맷 대응
						type: String,
						default: null,
					},
					text: {
						// Element가 표시될때 text
						type: String,
						default: null,
					},
					autoAction: {
						// 답변 발화 표시후 자동 실행 element가 있는 경우 (예, 선택 팝업)
						type: String,
						default: null,
					},
					transferText: {
						// Element가 클릭될 때 챗봇에 전달되는 발화
						type: String,
						default: null,
					},
					displayText: {
						// Element가 클릭될 때 UI에 표시만 되는 발화
						type: String,
						default: null,
					},
					src: {
						// 바로가기 링크 url
						type: String,
						default: null,
					},
					target: {
						// 바로가기 링크시 새창 옵션
						type: String,
						default: null,
					},
					useClick: {
						// 해당 항목에 대한 마우스 클릭을 지원 default = false;
						type: Boolean,
						default: false,
					},
					disabled: {
						// 해당항목 비활성화
						type: String,
						default: null,
					},
				};
			},
		},
	},
	data() {
		return {
			imgObj: {
				src: this.attribute.image.src,
				error:
					'https://i.pinimg.com/236x/17/4e/c0/174ec066a4f4f26321b7d8b4b8667bf8.jpg',
				loading:
					'https://i.pinimg.com/236x/17/4e/c0/174ec066a4f4f26321b7d8b4b8667bf8.jpg',
			},
		};
	},
	mounted() {},
};
</script>
