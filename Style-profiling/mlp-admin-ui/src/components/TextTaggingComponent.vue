<template>
  <v-container fluid row class="pa-0 ma-0">
    <div class="tool">
      <v-list 
        class="rounded-lg" 
        outlined
        elevation="1"
      >
        <v-list-item class="pa-0">
          <v-switch
            class="pl-3"
            v-model="annotation.done"
            inset
            hide-spin-buttons
            :false-value="0"
            :true-value="1"
            hint="Done"
            persistent-hint
            @change="patchAnnotation"
          ></v-switch>    
        </v-list-item>
        <v-list-item-group v-model="selectedTool">
          <v-list-item 
            class="pa-0 justify-center"
            inactive
            v-for="(tool) in tools.save" 
            :key="tool.value" 
            :value="tool.value"
            style="height:70px;"
            @click="saveEvent(tool.value)"
          >
            <v-tooltip right>
              <template v-slot:activator="{ on }">
                <v-icon v-on="on" v-text="tool.icon" size="40"></v-icon>
              </template>
              <span>{{tool.value}}</span>
            </v-tooltip>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item 
            class="pa-0 justify-center"
            v-for="(tool) in tools.etc" 
            :key="tool.value" 
            :value="tool.value"
            style="height:70px;"
            @click="etcEvent(tool.value)"
          >
            <v-tooltip right>
              <template v-slot:activator="{ on }">
                <v-icon v-on="on" v-text="tool.icon" size="40"></v-icon>
              </template>
              <span>{{tool.value}}</span>
            </v-tooltip>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </div>
    <div ref="workarea" class="workarea pl-5" style="width:96%;z-index:1;">
      <v-card class="rounded-lg mx-auto" outlined elevation="1">
        <v-container row>
          <v-card-subtitle class="pa-4">Label :</v-card-subtitle>
          <v-chip-group 
            column
            @change="changeLabel"
            class="pa-1"
          > 
            <template v-for="(chip, i) in labelChips">
              <v-chip
                class="mx-2"
                :key="i"
                close
                label
                filter
                :color="chip.color"
                text-color="white"
                @click:close="removeLabelChip(chip.label_id)"
              >
                <v-icon left>
                  mdi-label
                </v-icon>
                {{chip.name}}
              </v-chip>
            </template>
          </v-chip-group>
        </v-container>           
      </v-card>
      <v-card class="rounded-lg mx-auto mt-2" outlined elevation="1">
        <v-card-text style="min-height:300px;">
          <div ref="workarea" @mouseup="mouseUp">
            <template v-for="(item, index) in textArr">
              <span class="text" :id="index" v-if="item.type == 'text'" :key="index" style="font-size:18px;">{{item.text}}</span>
              <span class="text" :id="index" v-if="item.type == 'error'" :key="index" ><font color="red" size="5"><b>{{item.text}}</b></font></span>
              <!--<span class="testclass" :id="index" v-if="item.type == 'label'" :key="index">{{item.text}}<a @click="removeLabel(index)">x</a></span>-->
              <v-chip
                :id="index" 
                v-if="item.type == 'label'" 
                :key="index"
                class="ma-2"
                :color="getLabelChipColor(item.label_id)"
                text-color="white"
                close
                @click:close="removeLabel(index)"
              >
                {{item.text}}
              </v-chip>
            </template>
          </div>
        </v-card-text>
      </v-card>
    </div>
    <!-- dialog -->
    <v-dialog persistent max-width="600" v-model="labelDialog.show">
        <LabelDialogComponent :labelChips="labelChips" @addLabelChip="addLabelChip" @closeLabelDialog="closeLabelDialog" />
    </v-dialog>
    <!-- dialog -->
  </v-container>
</template>


<script>
import LabelDialogComponent from './LabelDialogComponent.vue';
export default {
  components: {
    LabelDialogComponent,
  },
  props: {
    params: Object,
  },
  data: () => ({
    tools: {
      save: [
        { value:'save', icon:'mdi-content-save' },
      ],
      etc: [
        { value:'label', icon:'mdi-label-outline' },
        { value:'label-add', icon:'mdi-format-annotation-plus' },
      ] 
    },
    selectedTool: null,
    chips: [],
    labelDialog: {
      show: false,
    },
    labelChips: [],
    textArr: [],
    selectedLabel: {},
    annotation: {
      done: 0,
    },
  }),
  watch: {
    'params.offset' : 'fetchAnnotation',
  },
  computed: {

  },
  created() {
    this.fetchAnnotation();
  },
  methods: {
    fetchAnnotation() {
      // carousel 이동시에 labelChips 세팅을 하기 전 초기화.
      this.textArr = [];
      this.labelChips = [];
      this.selectedLabel = {};

      this.$store.dispatch('FETCH_ANNOTATIONS', this.params)
        .then(response => {
          console.log('TextTagging - FETCH_ANNOTATION', response);

          const res = response.annotations[0];
          
          //부모에게 파일명, ML테스크, 전체 카운트 전송
          this.$emit('setFileName', res.file_name);
          this.$emit('setMLTask', res.ml_task);
          this.$emit('setTotalResults', res.total_results);

          this.annotation = res;
          this.labelChips = [...res.label_info];
          // label정보가 없으면 파일에서 딝어오고 있으면 레이블 정보로 세팅
          if (res.labels.length === 0) {
            this.getTextContent();
          } else {
            this.textArr = [...res.labels];
          }
        })
        .catch(error => { console.log(error);  });
    },
    getTextContent() {
      this.$store.dispatch('GET_TEXT_CONTENT', this.annotation.file_url)
        .then(res => {
          //개행문자 스페이스 치환
          const regexp = /[\n|\n\r]/g;
          this.textArr = [{type: 'text',text: res.replace(regexp, ' ')}];
        })
        .catch(error => { console.log(error); this.textArr = [{text: 'ERROR: 파일이 존재 하지 않거나 접근되지 않습니다.', type: 'error'}] });
    },
    patchAnnotation() {
      this.$store.dispatch('PATCH_ANNOTATION', {annotation_id: this.annotation._id, done: this.annotation.done, labels: this.textArr }) 
        .then(res => {
          console.log('PATCH_ANNOTATION - res', res);
          this.selectedTool = null;
        })
        .catch(error => { console.log(error); });
    },
    saveEvent(tool) {
      if(tool === 'save') {
        this.patchAnnotation();
      }
    },
    changeLabel(index) {     
      this.selectedLabel = (typeof(index) !== 'undefined') ? this.labelChips[index] : {};
    },
    etcEvent(tool) { 
      if(tool === 'label-add') {
        this.labelDialog.show = true;
      }
    },
    closeLabelDialog() {
      this.labelDialog.show = false;
      this.selectedTool = '';
    },
    getLabelChipColor(label_id) {
      return {...this.labelChips.find((r) => r.label_id === label_id)}.color;
    },
    addLabelChip(labelChip) {
      let params = {};
      // 넘어온 labelchip의 아이디 유무에 따라 생성 및 업데이트
      if (typeof(labelChip.label_id) === 'undefined') {
        //생성
        params = {
          dataset_id: this.annotation.dataset_id,
          ...labelChip,
        }
        this.$store.dispatch('CREATE_LABEL', params)
          .then(res => {
            console.log('TextTaggingComponent - CREATE_LABEL - res', res);
            //생성된 레이블칩 세팅
            this.labelChips.push(res);
          })
          .catch(error => { console.log(error); });
      } else {
        //수정
        params = {
          label_id: labelChip.label_id,
          ...labelChip,
        }
        this.$store.dispatch('PATCH_LABEL', params)
          .then(res => {
            console.log('TextTaggingComponent - PATCH_LABEL - res', res);
            //수정된 레이블칩 세팅 - 수정된 chip을 찾아서 수정 내용을 반영해줘야함.
            const updateLabelChip = this.labelChips.find((r) => r.label_id === res._id); 
            updateLabelChip.name = res.name;
            updateLabelChip.color = res.color;
          })
          .catch(error => { console.log(error); });
      }
      this.closeLabelDialog();
    },
    removeLabelChip(label_id) {     
      let labelCount = 0;
      this.textArr.forEach((r) => {
        if(r.label_id === label_id){
          labelCount++;
        }
      });
      
      for(let i = 0, n = labelCount; i < n; i++){
        const textArrIndex = this.textArr.findIndex(r => r.label_id === label_id);
        // console.log(textArrIndex, this.textArr);
        this.removeLabel(textArrIndex);
      }

    },
    mouseUp(){
      if(this.annotation.done){ // done 1이면 보기 모드
        return;
      }

      if(this.selectedTool !== 'label') {
        return;
      }

      if(Object.keys(this.selectedLabel).length === 0){
        alert('레이블을 먼저 선택해주세요.');
        return;
      }
      
      const sel = window.getSelection();
      if(sel.type != 'Range'){ //영역을 지정하지 않은 경우
        return;
      }
      if(!sel.toString()){ //선택된 텍스트가 없을 경우
        return;
      }
      
      this.blockText = sel.toString();
      this.start = Math.min(sel.anchorOffset ,sel.focusOffset);
      this.end = Math.max(sel.anchorOffset ,sel.focusOffset);

      const anchorId = sel.anchorNode.parentNode.id;
      const focusId = sel.focusNode.parentNode.id;
      console.log(anchorId);
      if (anchorId === focusId){
        const updateArr = [];

        updateArr.push({type:'text', text: this.textArr[anchorId].text.substring(0, this.start)}); 
        updateArr.push({type:'label', text: this.textArr[anchorId].text.substring(this.start,this.end), label_id: this.selectedLabel.label_id});
        
        //result setting
        //this.result.push({text:this.textArr[anchorId].text.substring(this.start,this.end), label:this.label, start: this.start, end: this.end});

        updateArr.push({type:'text', text: this.textArr[anchorId].text.substring(this.end)});
        this.textArr.splice(anchorId, 1, ...updateArr);
      } else { // 시작 종료 노드가 다를경우
        alert('레이블이 존재합니다.');
        this.blockText = '';
        this.start = 0;
        this.end = 0;
      }            
    },
    removeLabel(index){
      const updateArr = [];
      let startIndex = index;
      let removeCnt = 1;
      let updateText = '';
      // label 이전 text 체크
      if(this.textArr[index - 1].type === 'text'){
        startIndex--;
        removeCnt++;
        updateText += this.textArr[index-1].text;
      }
        
      updateText += this.textArr[index].text;

      // label 이후 text 체크
      if(this.textArr[index + 1].type === 'text'){
        removeCnt++;
        updateText += this.textArr[index + 1].text;
      }
      updateArr.push({type:'text', text: updateText});
      this.textArr.splice(startIndex, removeCnt, ...updateArr);
    },
  }
}
</script>

<style scoped>
.testclass {
    border: solid 2px green;
    margin-left:5px;
}
</style>