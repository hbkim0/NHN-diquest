<!-- 프로필 리스트 컴포넌트 -->
<template>
	<!-- 이미지 없을경우 표시 
							<hr class="chat_border">
							-->
	<li :title="attribute.title" :class="this.class">
		<i v-if="attribute.iClass" :class="attribute.iClass"></i>
		<template v-if="attribute.src">
			<a
				:href="
					attribute.src.indexOf('http://') < 0
						? 'http://' + attribute.src
						: attribute.src
				"
				class="underline blue"
				:target="attribute.target"
			>
				{{ attribute.label }}
			</a>
		</template>
		<template v-else-if="attribute.emailSrc">
			<a
				:href="
					attribute.emailSrc.indexOf('mailto:') < 0
						? 'mailto:' + attribute.emailSrc
						: attribute.emailSrc
				"
				class="underline blue"
				:target="attribute.target"
			>
				{{ attribute.label }}
			</a>
		</template>
		<template v-else>
			{{ attribute.label }}
			<slot></slot>
		</template>
	</li>
</template>
<script>
export default {
	name: 'ic-ans-info-list',
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
	computed: {
		class: function() {
			let classArray = [];

			if (this.attribute) {
				/*if (this.attribute.listClass) {
					// class
					this.attribute.listClass.split(' ').forEach(row => {
						classArray.push(row);
					});
				}*/
				if (this.attribute.class) {
					// class
					this.attribute.class.split(' ').forEach(row => {
						if (row == 'icInfoListClass1') {
							classArray.push('mb-5px');
						} else {
							classArray.push(row);
						}
					});
				}
				// 속성에 있는 추가 스타일
				/*				
				if (this.attribute.align) {
					// align
					if (this.attribute.align == 'vertical') {
						// code
					} else if (this.attribute.align == 'horizontal') {
						// code
						classArray.push('horizontal');
					}
				}
				*/
			}

			return classArray.toString().replace(/,/g, ' ');
		},
	},
	created() {
		if (this.attribute) {
			if (!this.attribute.target) {
				this.attribute.target = '_blank';
			}
		}
	},
	mounted() {},
};
</script>
