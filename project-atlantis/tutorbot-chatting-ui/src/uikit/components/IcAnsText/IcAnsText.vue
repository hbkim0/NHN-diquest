<!-- 일반 텍스트 컴포넌트 -->
<template>
	<div v-if="attribute.src" :style="style">
		<a
			:href="attribute.src"
			:class="this.class"
			:target="attribute.target"
			:disabled="attribute.disabled"
			v-html="attribute.text"
		></a>
	</div>
	<div v-else-if="attribute.transferText">
		<button
			:class="this.class"
			:disabled="attribute.disabled"
			v-html="attribute.text"
		></button>
	</div>
	<div
		v-else
		:class="this.class"
		:style="style"
		v-html="attribute.text"
		:disabled="attribute.disabled"
	></div>
</template>
<script>
export default {
	name: 'ic-ans-text',
	props: {
		idx: Number, // 메시지 번호
		nodeId: String, // 노드 식별자
		/**
		 * attribute
		 * XSD 적용 완료-20200311
		 */
		attribute2: {
			type: Object,
			default: null,
		},
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
					auto: {
						// 답변 발화 표시후 자동 실행 element가 있는 경우 (예, 선택 팝업)
						type: String,
						default: null,
					},
					text: {
						// Element가 클릭될 때 챗봇에 전달되는 발화
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
						type: Boolean,
						default: null,
					},
				};
			},
		},
	},
	data() {
		return {
			style: '',
		};
	},
	computed: {
		class: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.class) {
					// class
					this.attribute.class.split(' ').forEach(row => {
						if (row == 'icTextClass1') {
							classArray.push('red');
						} else if (row == 'icTextClass2') {
							classArray.push('blue');
						} else if (row == 'icTextClass3') {
							classArray.push('orange');
						} else if (row == 'icTextClass4') {
							classArray.push('gray');
						} else if (row == 'icTextClass5') {
							classArray.push('black');
						} else if (row == 'icTextClass6') {
							classArray.push('primary_c');
						} else if (row == 'icTextClass7') {
							classArray.push('text_small');
						} else if (row == 'icTextClass8') {
							classArray.push('text_medium');
						} else if (row == 'icTextClass9') {
							classArray.push('text_large');
						} else if (row == 'icTextClass10') {
							classArray.push('underline');
						} else if (row == 'icTextClass11') {
							classArray.push('align_left');
						} else if (row == 'icTextClass12') {
							classArray.push('align_center');
						} else if (row == 'icTextClass13') {
							classArray.push('align_right');
						} else if (row == 'icTextClass14') {
							classArray.push('primary_c bot_card_tit');
						} else if (row == 'icTextClass15') {
							classArray.push('bg_clip');
						} else if (row == 'icTextClass16') {
							classArray.push('gray');
							this.style = 'display:inline-block';
						} else if (row == 'icTextClass17') {
							classArray.push('orange');
							this.style = 'display:inline-block';
						} else if (row == 'icTextClass18') {
							this.style = 'display:inline-block';
						} else if (row == 'visibilityHidden') {
							this.style = 'visibility:hidden';
						} else if (row == 'displayNone') {
							this.style = 'display:none';
						} else {
							if (row == 'mb-20px primary_c') {
								row = 'primary_c bot_card_tit';
							}
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
		// pageid,logid,..
		const reg = /<[^>]*>?/g;
		const chkId = ['pageId','workbookName','logId'];
		if('id' in this.attribute && chkId.includes(this.attribute.id)) { 
			this.eventBus.$emit('ic-component-text', {
					idx: this.idx,
					nodeId: this.nodeId,
					key: this.attribute.id,
					value: this.attribute.text.replace(reg,''),
				});
		}
		
		if (this.attribute) {
			if (!this.attribute.target) {
				if (this.attribute.src && this.attribute.src.indexOf('tel:') != -1) {
					this.attribute.target = '_self';
				} else {
					this.attribute.target = '_blank';
				}
			}
		}
	},
	mounted() {},
};
</script>
