<template>
  <v-container fluid row class="pa-0 ma-0">
    <div class="tool" style="position:absolute;left:15px;width:70px;">
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
              @change="saveEvent('save')"
            ></v-switch>    
        </v-list-item>
        <v-list-item 
          class="pa-0 justify-center"
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
        <v-list-item-group v-model="shapeConfig.selectedTool">
          <v-list-item 
            class="pa-0 justify-center"
            v-for="(tool) in tools.shape" 
            :key="tool.value" 
            :value="tool.value"
            style="height:70px;"
          >
            <v-tooltip right>
              <template v-slot:activator="{ on }">
                <v-icon v-on="on" v-text="tool.icon" size="40"></v-icon>
              </template>
              <span>{{tool.value}}</span>
            </v-tooltip>
          </v-list-item>
        </v-list-item-group>
        <v-divider></v-divider>
        <v-list-item 
          class="pa-0 justify-center"
          inactive
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
      </v-list>
      <v-card outlined elevation="1" class="mt-3">
        <v-card-subtitle class="pa-1 text-center">
          <v-checkbox
            dense
            hide-details
            v-model="konvaConfig.guideLine"
            label="line"
          ></v-checkbox>
        </v-card-subtitle>
        <v-card-subtitle class="pa-1 text-center">X : {{parseInt(mousePos.x)}}</v-card-subtitle>
        <v-card-subtitle class="pa-1 text-center">Y : {{parseInt(mousePos.y)}}</v-card-subtitle>
      </v-card>
    </div>
    <div ref="workarea" class="workarea pl-5" style="width:96%;z-index:1;margin-left:70px; margin-right:10px;">
      <v-card class="rounded-lg" outlined elevation="1">
        <v-stage 
          ref="stage" 
          :config="konvaConfig.stage"
          @mousedown="handleStageMouseDown"
          @mousemove="handleStageMouseMove"
          @mouseup="handleStageMouseUp"
        >
          <v-layer>
            <v-image ref="image" :config="konvaConfig.image" style="background:blue;"/>
            <v-rect 
              ref="shapeRect"
              v-for="rect in shapeConfig.rects"
              :key="rect.id"
              :config="{
                  name: rect.name,
                  x: Math.min(rect.startPointX, rect.startPointX + rect.width),
                  y: Math.min(rect.startPointY, rect.startPointY + rect.height),
                  width: Math.abs(rect.width),
                  height: Math.abs(rect.height),
                  fill: 'rgb(0,0,0,0)',
                  stroke: 'black',
                  strokeWidth: 2,
                  draggable: rect.draggable,
              }"
              @transformend="handleTransformEnd"
              @dragstart="handleDragStart"
              @dragend="handleDragEnd"
            ></v-rect>
            <v-line ref="lineX1" :config="konvaConfig.lineX1" v-if="konvaConfig.guideLine"></v-line>
            <v-line ref="lineX2" :config="konvaConfig.lineX2" v-if="konvaConfig.guideLine"></v-line>
            <v-line ref="lineY1" :config="konvaConfig.lineY1" v-if="konvaConfig.guideLine"></v-line>
            <v-line ref="lineY2" :config="konvaConfig.lineY2" v-if="konvaConfig.guideLine"></v-line>
            <v-transformer ref="transformer" :config="{rotateEnabled: false, flipEnabled: false, keepRatio: false}"/>
          </v-layer>
        </v-stage>
      </v-card>
    </div>
    <div class="pa-3" style="position:absolute;left:65%;width:33%;z-index:2;">
      <v-card ref="labelCard" elevation="2" outlined v-if="shapeConfig.selectedShapeName">
        <v-card-title>Label Edit({{shapeConfig.selectedShapeName}})</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="3">
              <v-card-subtitle class="pa-2 pl-0">Label :</v-card-subtitle>
            </v-col>
            <v-col cols="8">
              <v-text-field
                label="Label"
                dense
                v-model="shapeConfig.labels[shapeConfig.selectedShapeName].label"
              ></v-text-field>
            </v-col>
            <v-col cols="3">
              <v-card-subtitle class="pa-2 pl-0">Attributes :</v-card-subtitle>
            </v-col>
            <v-col cols="9">
              <template v-for="(attr,index) in shapeConfig.labels[shapeConfig.selectedShapeName].attributes">
                <v-container row fluid :key="index">
                  <v-col class="ma-0 pa-0" cols="3">
                    <v-text-field 
                      class="pa-0"
                      v-model="attr.key" 
                      hint="key" 
                      persistent-hint
                      solo
                    ></v-text-field>
                  </v-col>
                  <v-col class="ma-0 pa-0 pl-2" cols="8">
                    <v-container row fluid>
                      <v-combobox
                        class="ma-0 pa-0"
                        v-model="attr.values"
                        small-chips
                        solo
                        clearable
                        hint="value" 
                        persistent-hint
                        multiple
                      >
                        <template v-slot:selection="{ attrs, item, selected }">
                          <v-chip
                            v-bind="attrs"
                            :input-value="selected"
                            close
                            @click:close="removeAttributeValue(index,item)"
                          >
                            <v-tooltip bottom>
                              <template v-slot:activator="{ on, attrs }">
                                <strong v-bind="attrs" v-on="on">{{ item.replace(/(?<=.{5})(.*)(=?)/, '...') }}</strong>
                              </template>
                              <span>{{ item }}</span>
                            </v-tooltip>
                          </v-chip>
                        </template>
                      </v-combobox>
                    </v-container>
                  </v-col>
                  <v-col class="pl-0 justify-center" cols="1">
                    <v-btn
                        icon
                        @click="removeAttribute(index)"
                      >
                      <v-icon>
                        mdi-tag-remove
                      </v-icon>
                    </v-btn>
                  </v-col>
                </v-container>
              </template>
              <v-row>
                <v-col>
                  <v-btn
                    icon
                    @click="addAttribute"
                  >
                    <v-icon>
                      mdi-tag-plus
                    </v-icon>
                  </v-btn>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn
            v-if="annotation.done === 0"
            large
            @click="removeRect"
          >DELETE</v-btn>
        </v-card-actions>
      </v-card>
    </div>
  </v-container>
</template>

<script>
export default {
  props: {
    params: Object,
  },
  data: () => ({
    tools: {
      save: [
        { value:'save', icon:'mdi-content-save' },
      ],
      shape: [
        { value:'rect', icon:'mdi-vector-square-edit' }, 
        { value:'move', icon:'mdi-cursor-move' },
      ],
      etc: [
        { value:'zoom-plus', icon:'mdi-magnify-plus' },
        { value:'zoom-minus', icon:'mdi-magnify-minus' },
        { value:'reset', icon:'mdi-cached' },
      ]
    },
    konvaConfig: {
      stage: {
        width: 1920,
        height: 1080,
        draggable: false,
        scaleX : 1,
        scaleY : 1,
      },
      image: {
        image: null,
      },
      lineX1: {
        points: [],
        stroke: 'green',
        strokeWidth: 2,
        lineJoin: 'round',
        dash: [5, 5],
      },
      lineY1: {
        points: [],
        stroke: 'green',
        strokeWidth: 2,
        lineJoin: 'round',
        dash: [5, 5],
      },
      lineX2: {
        points: [],
        stroke: 'green',
        strokeWidth: 2,
        lineJoin: 'round',
        dash: [5, 5],
      },
      lineY2: {
        points: [],
        stroke: 'green',
        strokeWidth: 2,
        lineJoin: 'round',
        dash: [5, 5],
      },
      guideLine: false,
    },
    shapeConfig: {
      idx: 0,
      rects: [],
      labels: {},
      selectedShapeName: '',
      selectedTool: 'rect',
      isDragging: false,
    },
    mousePos: { 
      x: 0, 
      y: 0
    },
    annotation: {},
  }),
  watch: {
    'params.offset' : 'fetchAnnotation',
    'shapeConfig.selectedTool' : 'shapeEvent',
  },
  computed: {
    
    getLabels() {
      const results = [];
      const rects = [...this.shapeConfig.rects];
      const labels = {...this.shapeConfig.labels};
      
      //
      rects.forEach((r) => {
        results.push({
          bbox: [
            Math.min((r.startPointX + r.width), r.startPointX),
            Math.min((r.startPointY + r.height), r.startPointY),
            Math.max((r.startPointX + r.width), r.startPointX),
            Math.max((r.startPointY + r.height), r.startPointY),
          ],
          label: typeof(labels[r.name].label) !== 'undefined' ? labels[r.name].label : '',
          attributes: typeof(labels[r.name].attributes) !== 'undefined' ? labels[r.name].attributes.filter(r => r.key !== "" && r.values.length !== 0) : [],
        })
        
      });

      return results;
    }
  },
  created() {
    this.fetchAnnotation();
  },
  mounted() {
    this.konvaConfig.stage.width = this.$refs.workarea.offsetWidth * 0.99;

    window.addEventListener('keydown', (e) => {
      if(e.key === 'Delete'){
        this.removeRect();
      }
    });
  },
  methods: {
    initConfig() {
      this.shapeConfig.idx = 0;
      this.shapeConfig.rects = [];
      this.shapeConfig.labels = {};
      this.shapeConfig.selectedShapeName = "";
      this.konvaConfig.stage.scaleX = 1;
      this.konvaConfig.stage.scaleY = 1;
      this.$refs.stage.getNode().setAttr('x',0);
      this.$refs.stage.getNode().setAttr('y',0);
    },
    fetchAnnotation() {

      this.$store.dispatch('FETCH_ANNOTATIONS', this.params)
        .then(response => {         
          //초기화
          this.initConfig();

          const transformerNode = this.$refs.transformer.getNode();
          transformerNode.nodes([]);

          const res = response.annotations[0];
          
          //부모에게 파일명, ML테스크, 전체 카운트 전송
          this.$emit('setFileName', res.file_name);
          this.$emit('setMLTask', res.ml_task);
          this.$emit('setTotalResults', res.total_results);

          this.annotation = res;

          res.labels.forEach((v,i) => {
            const {bbox, label, attributes} = v;
            const labelObj = {};
            labelObj[`rect${i}`] = { bbox: bbox, label: label, attributes: attributes };
            this.shapeConfig.labels = { ...this.shapeConfig.labels, ...labelObj};

            this.shapeConfig.rects = [
              ...this.shapeConfig.rects,
              { name: `rect${i}`, startPointX: Math.min(bbox[0],bbox[2]), startPointY: Math.min(bbox[1],bbox[3]), width: Math.abs(bbox[0] - bbox[2]), height: Math.abs(bbox[1] - bbox[3]), scaleX: 1, scaleY: 1, draggable: true }
            ];
            this.shapeConfig.idx++;
          });

          // done
          this.annotation.done = res.done;
          

          // 이미지 세팅
          const image = new window.Image();
          image.src = this.getCoverImage(res.file_url);
          image.onload = () => {
            // set image only when it is loaded
            this.konvaConfig.image.image = image;
          };

        })
        .catch(error => { console.log(error);  });
    },
    patchAnnotation() {
      const labels = [...this.getLabels];
      this.$store.dispatch('PATCH_ANNOTATION', {annotation_id: this.annotation._id, done: this.annotation.done, labels: labels }) 
        .then(res => {
          console.log('PATCH_ANNOTATION - res', res);  
          this.shapeConfig.selectedTool = null;
          this.konvaConfig.stage.draggable = false;
          this.shapeConfig.selectedShapeName = "";
          this.shapeConfig.rects.map(e => {
            e.draggable = false;
          });
          const transformerNode = this.$refs.transformer.getNode();
          transformerNode.nodes([]);
        })
        .catch(error => { console.log(error); });
    },
    removeAttributeValue(index,itemIndex) {
      const values = this.shapeConfig.labels[this.shapeConfig.selectedShapeName].attributes[index].values;
      values.splice(values.indexOf(itemIndex), 1);
    },
    saveEvent(tool) {
      if(tool === 'save'){
        //저장 기능 구현
        this.patchAnnotation();
      }
    },
    shapeEvent() {
      if(this.shapeConfig.selectedTool === 'move') {       
        this.konvaConfig.stage.draggable = true;
        this.shapeConfig.rects.map(e => {
          e.draggable = false;
        });
        const transformerNode = this.$refs.transformer.getNode();
        transformerNode.nodes([]);
      } else if (this.shapeConfig.selectedTool === 'rect') {
        this.konvaConfig.stage.draggable = false;
        this.shapeConfig.rects.map(e => {
          e.draggable = true;
        });
      } else {
        this.konvaConfig.stage.draggable = false;
        this.shapeConfig.rects.map(e => {
          e.draggable = false;
        });
      }
    },
    etcEvent(tool) {
      const stage = this.$refs.stage.getNode();
      const scaleX = this.konvaConfig.stage.scaleX
      const scaleY = this.konvaConfig.stage.scaleY
      if(tool === 'reset'){
        this.konvaConfig.stage.scaleX = 1;
        this.konvaConfig.stage.scaleY = 1;
        stage.setAttr('x',0);
        stage.setAttr('y',0);
      } else if (tool === 'zoom-plus') {
        this.konvaConfig.stage.scaleX += 0.5;
        this.konvaConfig.stage.scaleY += 0.5;
      } else if (tool === 'zoom-minus') {
        this.konvaConfig.stage.scaleX = this.konvaConfig.stage.scaleX - 0.5 <= 0 ? this.konvaConfig.stage.scaleX : this.konvaConfig.stage.scaleX - 0.5;
        this.konvaConfig.stage.scaleY = this.konvaConfig.stage.scaleY - 0.5 <= 0 ? this.konvaConfig.stage.scaleY : this.konvaConfig.stage.scaleY - 0.5;
      }
    },
    handleStageMouseDown(e) { //stage에 마우스 클릭, stage/image 인지 rect를 선택했는지
      console.log(e.target);
      if(this.annotation.done){ // done 1이면 보기 모드
        return;
      }

      if(this.shapeConfig.selectedTool === 'move' || this.shapeConfig.selectedTool === null) {
        return;
      }

      // clicked on stage - clear selection
      if (((e.target === e.target.getStage()) || (e.target.className === 'Image')) && this.shapeConfig.selectedTool == 'rect') {
        this.shapeConfig.isDrawing = true;
        const pos = this.$refs.stage.getNode().getPointerPosition();
        const stagePos = this.$refs.stage.getNode().getAbsolutePosition();
        const shapeName = `rect${this.shapeConfig.idx++}`;
        const startPointX = (pos.x - stagePos.x) / this.konvaConfig.stage.scaleX;
        const startPointY = (pos.y - stagePos.y) / this.konvaConfig.stage.scaleY;
        this.shapeConfig.rects = [
          ...this.shapeConfig.rects,
          { name: shapeName, startPointX: startPointX, startPointY: startPointY, width: 0, height: 0, scaleX: 1, scaleY: 1, draggable: true },
        ];
        
        const labelObj = {};
        labelObj[shapeName] = { bbox: [], label: '', attributes:[] };
        this.shapeConfig.labels = { ...this.shapeConfig.labels, ...labelObj};

        this.shapeConfig.selectedShapeName = '';
        this.updateTransformer();
        return;
      }
      
      console.log(e.target.getParent());

      // clicked on transformer - do nothing
      const clickedOnTransformer =
        e.target.getParent().className === 'Transformer';
      if (clickedOnTransformer) {
        return;
      }

      // find clicked rect by its name
      const name = e.target.name();
      const rect = this.shapeConfig.rects.find((r) => r.name === name);
      console.log('find rect', name, rect);
      if (rect) {
        this.shapeConfig.selectedShapeName = name;
      } else {
        this.shapeConfig.selectedShapeName = '';
      }
      this.updateTransformer();
    },
    handleStageMouseMove() { // 마우스 이동하면서 좌표 변경
      const stageMousePos = this.$refs.stage.getNode().getPointerPosition();
      //좌표 확인용
      this.mousePos = {
        x: stageMousePos.x,
        y: stageMousePos.y,
      }
      
      if (this.konvaConfig.guideLine) {
        this.konvaConfig.lineX1.points = [0, stageMousePos.y, stageMousePos.x-10, stageMousePos.y];
        this.konvaConfig.lineX2.points = [stageMousePos.x+10, stageMousePos.y, this.konvaConfig.stage.width, stageMousePos.y];
        this.konvaConfig.lineY1.points = [stageMousePos.x, 0, stageMousePos.x, stageMousePos.y-10];
        this.konvaConfig.lineY2.points = [stageMousePos.x, stageMousePos.y+10, stageMousePos.x, this.konvaConfig.stage.height];
      }
      
      
      if (!this.shapeConfig.isDrawing) {
        return;
      }
      const stagePos = this.$refs.stage.getNode().getAbsolutePosition();
      const point = this.$refs.stage.getNode().getPointerPosition();

      let curRec = this.shapeConfig.rects[this.shapeConfig.rects.length - 1];
      curRec.width = (point.x / this.konvaConfig.stage.scaleX - (stagePos.x / this.konvaConfig.stage.scaleX + curRec.startPointX));
      curRec.height = (point.y / this.konvaConfig.stage.scaleY - (stagePos.y / this.konvaConfig.stage.scaleY + curRec.startPointY));
      
    }, 
    handleStageMouseUp() { 
      if(this.shapeConfig.selectedTool === 'move') {
        return;
      }

      this.shapeConfig.isDrawing = false;

      // 너비나 높이가 0이면 다시 제거.
      let curRec = this.shapeConfig.rects[this.shapeConfig.rects.length - 1];
      if( curRec.width === 0 || curRec.height === 0 ){
        this.shapeConfig.rects.pop();
        delete this.shapeConfig.labels[curRec.name];
        this.shapeConfig.idx--;
      }
    },
    updateTransformer() {
      // here we need to manually attach or detach Transformer node
      const transformerNode = this.$refs.transformer.getNode();
      const stage = transformerNode.getStage();
      const { selectedShapeName } = this.shapeConfig;

      const selectedNode = stage.findOne('.' + selectedShapeName);
      // do nothing if selected node is already attached
      if (selectedNode === transformerNode.node()) {
        return;
      }

      if (selectedNode) {
        // attach to another node
        transformerNode.nodes([selectedNode]);
      } else {
        // remove transformer
        transformerNode.nodes([]);
      }
    },
    handleTransformEnd(e) { // rect 변경 후 rect 업데이트, array 업데이트
      const rect = this.shapeConfig.rects.find(
        (r) => r.name === this.shapeConfig.selectedShapeName
      );

      const rectIndex = this.shapeConfig.rects.findIndex(
        (r) => r.name === this.shapeConfig.selectedShapeName
      );
      
      rect.startPointX = e.target.x();
      rect.startPointY = e.target.y();
      rect.rotation = e.target.rotation();
      rect.scaleX = e.target.scaleX();
      rect.scaleY = e.target.scaleY();
           
      this.$refs.shapeRect[rectIndex].getNode().setAttr('width',rect.width * rect.scaleX);
      this.$refs.shapeRect[rectIndex].getNode().setAttr('height',rect.height * rect.scaleY);
      this.$refs.shapeRect[rectIndex].getNode().setAttr('scaleX',1);
      this.$refs.shapeRect[rectIndex].getNode().setAttr('scaleY',1);

      rect.width = rect.width * rect.scaleX;
      rect.height = rect.height * rect.scaleY;
      rect.scaleX = 1;
      rect.scaleY = 1;

    },
    handleDragStart() {
      this.shapeConfig.isDragging = true;
    },
    handleDragEnd(e) { // DragEnd 시작 x,y 수정
      const rect = this.shapeConfig.rects.find(
        (r) => r.name === this.shapeConfig.selectedShapeName
      );
      console.log(rect);
      rect.startPointX = e.target.x();
      rect.startPointY = e.target.y();
      this.shapeConfig.isDragging = false;
    },
    removeRect(){ // rect 삭제
      const shapeName = this.shapeConfig.selectedShapeName;
      const rectIndex = this.shapeConfig.rects.findIndex(
        (r) => r.name === shapeName
      );
      const transformerNode = this.$refs.transformer.getNode();
      if(rectIndex != -1) {
        this.shapeConfig.selectedShapeName = '';
        transformerNode.nodes([]);
        this.$delete(this.shapeConfig.rects, rectIndex);

        delete this.shapeConfig.labels[shapeName];

      }
    },
    addAttribute() {
      this.shapeConfig.labels[this.shapeConfig.selectedShapeName].attributes = [...this.shapeConfig.labels[this.shapeConfig.selectedShapeName].attributes, { key: '', values: [] }];
    },
    removeAttribute(index) {
      this.shapeConfig.labels[this.shapeConfig.selectedShapeName].attributes.splice(index,1);
    },
  }
}
</script>