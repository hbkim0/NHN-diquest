<!-- 이미지 컴포넌트 -->
<template>
	<div
		v-if="this.class.indexOf('emoticon') === -1"
		:class="this.class"
		:style="attribute.style ? attribute.style : ''"
	>
		<template v-if="attribute.src">
			<a
				:href="attribute.src"
				:target="attribute.target"
				:disabled="attribute.disabled"
				><img v-lazy="imgObj" :title="attribute.label" :style="style"
			/></a>
		</template>
		<template v-else-if="attribute.imgSrc">
			<img
				:class="this.class.indexOf('emoticon') !== -1 ? this.class : ''"
				v-lazy="imgUrl"
				:title="attribute.label"
				:style="style"
			/>
		</template>
	</div>
	<img
		v-else
		:class="this.class.indexOf('emoticon') !== -1 ? this.class : ''"
		v-lazy="imgUrl"
		:title="attribute.label"
		:style="style"
	/>
</template>
<script>
export default {
	name: 'ic-ans-image',
	props: {
		/**
		 * attribute
		 * XSD 적용 완료-20200311
		 */
		attribute: {
			id: {
				// element에 id를 부여하여 구분할 때 사용
				type: String,
				default: null,
			},
			class: {
				// css와 같이 element에 공통으로 style을 적용할 때 사용
				type: Object,
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
			label: {
				// 버튼에 표시할 텍스트
				type: String,
				default: null,
			},
			transferText: {
				// 버튼 클릭시 챗봇 발화 default는 text value
				type: String,
				default: null,
			},
			displayText: {
				// 버튼 클릭시 챗봇 표시 발화 default는 text value
				type: String,
				default: null,
			},
			imgSrc: {
				// 이미지인 경우 이미지 url
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
				type: String,
				default: false,
			},
			style: {
				// 이미지 크기
				type: String,
				default: null,
			},
		},
	},
	data() {
		return {
			imgObj: {
				src: this.attribute.imgSrc,
			},
			style: '',
		};
	},
	computed: {
		imgUrl: function() {
			var tempObj = {};
			tempObj.src = null;

			if (this.attribute) {
				if (this.attribute.imgSrc) {
					tempObj.src = this.attribute.imgSrc;
				}
			}

			return tempObj;
		},
		class: function() {
			let classArray = [];

			if (this.attribute) {
				if (this.attribute.class) {
					// class
					this.attribute.class.split(' ').forEach(row => {
						console.log('image row', row);
						if (row == 'icImageClass1') {
							classArray.push('img_wrap');
						} else if (row == 'icImageClass2') {
							classArray.push('img_wrap small');
						} else if (row == 'icImageClass3') {
							classArray.push('img_wrap medium');
						} else if (row == 'icImageClass4') {
							classArray.push('img_wrap large');
						} else if (row == 'icImageClass5') {
							classArray.push('img_wrap item');
						} else if (row == 'icImageClass6') {
							classArray.push('thumb large');
						} else if (row == 'icImageClass7') {
							classArray.push('thumb medium');
						} else if (row == 'icImageClass8') {
							classArray.push('thumb small');
						} else if (row == 'icImageClass9') {
							classArray.push('img_wrap bg');
						} else if (row == 'icImageClass10') {
							classArray.push('img_wrap bg bgsize_org');
						} else if (row == 'icImageClass10_p5') {
							classArray.push('img_wrap bg bgsize_5p');
						} else if (row == 'icImageClass10_p10') {
							classArray.push('img_wrap bg bgsize_10p');
						} else if (row == 'icImageClass10_p15') {
							classArray.push('img_wrap bg bgsize_15p');
						} else if (row == 'icImageClass10_p20') {
							classArray.push('img_wrap bg bgsize_20p');
						} else if (row == 'icImageClass10_p25') {
							classArray.push('img_wrap bg bgsize_25p');
						} else if (row == 'icImageClass10_p30') {
							classArray.push('img_wrap bg bgsize_30p');
						} else if (row == 'icImageClass10_p35') {
							classArray.push('img_wrap bg bgsize_35p');
						} else if (row == 'icImageClass10_p40') {
							classArray.push('img_wrap bg bgsize_40p');
						} else if (row == 'icImageClass10_p45') {
							classArray.push('img_wrap bg bgsize_45p');
						} else if (row == 'icImageClass10_p50') {
							classArray.push('img_wrap bg bgsize_50p');
						} else if (row == 'icImageClass10_p55') {
							classArray.push('img_wrap bg bgsize_55p');
						} else if (row == 'icImageClass10_p60') {
							classArray.push('img_wrap bg bgsize_60p');
						} else if (row == 'icImageClass10_p65') {
							classArray.push('img_wrap bg bgsize_65p');
						} else if (row == 'icImageClass10_p70') {
							classArray.push('img_wrap bg bgsize_70p');
						} else if (row == 'icImageClass10_p75') {
							classArray.push('img_wrap bg bgsize_75p');
						} else if (row == 'icImageClass10_p80') {
							classArray.push('img_wrap bg bgsize_80p');
						} else if (row == 'icImageClass10_p85') {
							classArray.push('img_wrap bg bgsize_85p');
						} else if (row == 'icImageClass10_p90') {
							classArray.push('img_wrap bg bgsize_90p');
						} else if (row == 'icImageClass10_p95') {
							classArray.push('img_wrap bg bgsize_95p');
						} else if (row == 'icImageClass10_p100') {
							classArray.push('img_wrap bg bgsize_100p');
						} else if (row == 'icImageClass11') {
							classArray.push('emoticon');
						} else if (row == 'icImageClass12') {
							classArray.push('emoticon large type_modal');
						} else if (row == 'icImageClass_w200') {
							this.style = 'width:200px';
						} else if (row == 'icImageClass_w300') {
							this.style = 'width:300px';
						} else if (row == 'icImageClass_w600') {
							this.style = 'width:600px';
						} else {
							classArray.push(row);
						}
					});
				} else {
					classArray.push('img_wrap');
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
<style></style>
