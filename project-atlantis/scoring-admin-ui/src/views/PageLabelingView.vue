<template>
  <v-card class="pa-4">
    <v-dialog persistent scrollable :max-width="PAGE_IMAGE_WIDTH*1.1" v-model="drawRectDialog.show">
      <v-card>
        <v-card-title>정답 영역 설정</v-card-title>
        <v-card-text>
          <v-container row>
          <v-stage class="ml-auto mr-auto" :width="PAGE_IMAGE_WIDTH" :height="PAGE_IMAGE_HEIGHT" @mousedown="handleStageMouseDown">
            <v-layer>
              <v-image :config="pageImage" />
              <v-rect :config="drawRectDialog.initRect" />
              <v-rect ref="drawRect" :config="drawRectDialog.rect" @dragend="handleDragEnd" @transformend="handleTransformEnd" />
              <v-transformer ref="transformer" :config="{rotateEnabled: false, flipEnabled: false, keepRatio: false}" />
            </v-layer>
          </v-stage>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" @click="redrawRect">다시 그리기</v-btn>
          <v-btn color="secondary" @click="closeDrawRectDialog">취소</v-btn>
          <v-btn color="primary" @click="saveDrawRect">적용</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-container row>
      <v-card flat width="520">
        <v-card-title>{{initWorkbook.name}}</v-card-title>
        <v-card-subtitle>p. {{initPage.page_num}}</v-card-subtitle>
        <v-card-text>
          <v-form v-model="valid">
            <v-card class="mb-2" v-for="(problem, p_idx) in this.editedProblems" :key="p_idx">
              <v-card-text>
                <v-text-field
                  label="문제 #"
                  required :rules="[v => ((!!v) && (String(v) && !!(v.trimEnd()))) || 'required']"
                  :value="problem.prob_num"
                  @change="(value) => changeProbNum(p_idx, value)"
                />
                <v-text-field
                  label="정답 영역 수"
                  readonly filled dense
                  :value="problem.labels.length"
                  prepend-icon="mdi-minus" @click:prepend="() => removeLabel(p_idx)"
                  append-outer-icon="mdi-plus" @click:append-outer="() => addLabel(p_idx)"
                />
                <v-list dense>
                  <v-list-item row v-for="(label, a_idx) in problem.labels" :key="a_idx">
                    <v-text-field
                      required :rules="[v => ((!!v) && (String(v) && !!(v.trimEnd()))) || 'required']"
                      :value= "label.label"
                      @change="(value) => changeLabel(p_idx, a_idx, value)"
                    >
                      <template v-slot:label>
                        <v-chip color="secondary" x-small>{{a_idx + 1}}</v-chip>
                      </template>
                    </v-text-field>
                    <div class="ma-2" />
                    <!-- form의 validation을 위해서 보이지 않는 text-field를 추가함. -->
                    <v-text-field
                      style="display:none"
                      required :rules="[v => (Array.isArray(v) && v.length === 4) || '']"
                      :value="label.bbox"
                    />
                    <v-btn
                      small
                      :disabled="!(Array.isArray(label.bbox) && label.bbox.length === 4)"
                      :depressed="p_idx === selectedLabelIndices.p_idx && a_idx === selectedLabelIndices.a_idx"
                      @click="() => showLabelRect(p_idx, a_idx)"
                    >
                      영역보기
                    </v-btn>
                    <div class="ma-2" />
                    <v-btn
                      small
                      :color="Array.isArray(label.bbox) && label.bbox.length === 4 ? 'secondary' : 'error'"
                      @click="() => showDrawRectDialog(p_idx, a_idx)"
                    >
                      영역설정
                    </v-btn>
                  </v-list-item>
                  <v-list-item>
                    <v-file-input
                      persistent-hint
                      label="문제풀이 이미지"
                      :hint="problem.solving_url"
                      @change="(file) => changeSolvingUrl(p_idx, file)"
                    />
                    <div class="ma-2" />
                    <v-tooltip right>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn small outlined :disabled="!problem.solving_url" v-bind="attrs" v-on="on">보기</v-btn>
                      </template>
                      <span>
                        <v-img contain max-width="320" :src="resolveUrl(problem.solving_url)" />
                      </span>
                    </v-tooltip>
                  </v-list-item>
                  <v-list-item>
                    <v-file-input
                      persistent-hint
                      label="유사문제 이미지"
                      :hint="problem.similar_url"
                      @change="(file) => changeSimilarUrl(p_idx, file)"
                    />
                    <div class="ma-2" />
                    <v-tooltip right>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn small outlined :disabled="!problem.similar_url" v-bind="attrs" v-on="on">보기</v-btn>
                      </template>
                      <span>
                        <v-img contain max-width="320" :src="resolveUrl(problem.similar_url)" />
                      </span>
                    </v-tooltip>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
            <v-card flat>
              <v-card-actions>
              <v-spacer />
              <v-btn fab small color="error" @click="removeProblem"><v-icon>mdi-minus</v-icon></v-btn>
              <v-btn fab small color="primary" @click="addProblem"><v-icon>mdi-plus</v-icon></v-btn>
              <v-spacer />
              </v-card-actions>
            </v-card>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="secondary" @click="() => this.$router.back()">취소</v-btn>
          <v-btn color="primary" :disabled="!valid" @click="savePage">저장</v-btn>
        </v-card-actions>
      </v-card>
      <v-divider class="ma-2" vertical />
      <v-card flat>
        <v-card-text>
          <v-stage :width="PAGE_IMAGE_WIDTH" :height="PAGE_IMAGE_HEIGHT">
            <v-layer>
              <v-image :config="pageImage" />
              <v-rect :config="labelRect" />
            </v-layer>
          </v-stage>
          <v-btn color="secondary" small v-if="labelRect.width && labelRect.height" @click="clearLabelRect">영역 지우기</v-btn>
        </v-card-text>
      </v-card>
    </v-container>

  </v-card>
</template>

<script>
import {resolveImageUrl} from "../utils/image.js";

export default {
  name: 'ScoringAdminUiPageLabelingView',

  data() {
    return {
      workbook_id: '',
      page_id: '',

      initWorkbook: {},
      initPage: {},
      editedProblems: [],
      valid: true,

      PAGE_IMAGE_WIDTH: 960,
      PAGE_IMAGE_HEIGHT: 1200,
      pageImage: {image: null, scaleX: 1, scaleY: 1},
      selectedLabelIndices: {
        p_idx: -1,
        a_idx: -1,
      },
      labelRect: {
        // constants
        name: 'labelRect', stroke: 'green', strokeWidth: 4, draggable: false,
        // variables
        x: 0, y: 0, width: 0, height: 0,
      },
      drawRectDialog: {
        show: false,
        p_idx: -1,
        a_idx: -1,
        initRect: {
          // constants
          name: 'initRect', stroke: 'green', strokeWidth: 4, draggable: false,
          // variables
          x: 0, y: 0, width: 0, height: 0,
        },
        rect: {
          // constants
          name: 'drawRect', fill: 'red', opacity: 0.5, draggable: true,
          // variables
          x: 0, y: 0, width: 0, height: 0, scaleX: 1, scaleY: 1,
        },
      }
    };
  },

  mounted() {
    //
    this.workbook_id = this.$route.params.workbook_id;
    this.page_id = this.$route.params.page_id;

    //
    Promise.all([
      this.$store.dispatch('FETCH_WORKBOOK', this.workbook_id),
      this.$store.dispatch('FETCH_PAGE', this.page_id),
    ]).then(([workbook, page]) => {
      this.initWorkbook = workbook;
      this.initPage = page;
      this.editedProblems = window.structuredClone(page.problems || []);

      if (workbook.applied) {
        this.$eventBus.$emitHomeModal('자동채점에 적용된 페이지는 수정할 수 없습니다.');
        return;
      }

      //
      const image = new Image();
      image.onload = () => {
        this.pageImage = {
          image,
          scaleX: this.PAGE_IMAGE_WIDTH / image.width,
          scaleY: this.PAGE_IMAGE_HEIGHT / image.height,
        };
      };
      image.onerror = () => {
        this.$eventBus.$emitHomeModal('페이지의 원본 이미지 정보을 가져올 수 없습니다.');
      };
      image.src = resolveImageUrl(page.original_url);

    })
    .catch(() => {
      this.$eventBus.$emitHomeModal('페이지 정보을 가져올 수 없습니다.');
    });
  },

  methods: {
    resolveUrl: (image_url) => resolveImageUrl(image_url),

    addProblem() {
      this.editedProblems.push({
        prob_num: '',
        solving_url: '',
        similar_url: '',
        labels: [{
          bbox: null,
          label: ''
        }],
      });
    },
    removeProblem() {
      this.editedProblems.pop();
    },

    changeProbNum(p_idx, value) {
      this.editedProblems[p_idx].prob_num = value;
    },
    addLabel(p_idx) {
      this.editedProblems[p_idx].labels.push({
        bbox: null,
        label: ''
      });
    },
    removeLabel(p_idx) {
      if (this.editedProblems[p_idx].labels.length > 1) {
        this.editedProblems[p_idx].labels.pop();
      }
    },

    async changeSolvingUrl(p_idx, file) {
      const res = await this.$store.dispatch('UPLOAD_IMAGES', file);
      let {paths} = res;

      if (!Array.isArray(paths) || paths.length < 1) {
        this.$eventBus.$emitSnackbar('이미지를 업로드 할 수 없습니다.');
        return;
      }

      this.editedProblems[p_idx].solving_url = paths[0];
    },
    async changeSimilarUrl(p_idx, file) {
      const res = await this.$store.dispatch('UPLOAD_IMAGES', file);
      let {paths} = res;

      if (!Array.isArray(paths) || paths.length < 1) {
        this.$eventBus.$emitSnackbar('이미지를 업로드 할 수 없습니다.');
        return;
      }

      this.editedProblems[p_idx].similar_url = paths[0];
    },

    //
    changeLabel(p_idx, a_idx, value) {
      this.editedProblems[p_idx].labels[a_idx].label = value;
    },

    //
    convertBboxToRect(l, t, r, b) {
      const {scaleX, scaleY} = this.pageImage;

      return {
        x: Math.min(l, r) * scaleX,
        y: Math.min(t, b) * scaleY,
        width: Math.abs(r - l) * scaleX,
        height: Math.abs(b - t) * scaleY,
      };
    },
    convertRectToBbox(x, y, w, h) {
      const {scaleX, scaleY} = this.pageImage;

      return {
        left: x / scaleX,
        top: y / scaleY,
        right: (x + w) / scaleX,
        bottom: (y + h) / scaleY,
      };
    },

    //
    clearLabelRect() {
      //
      this.labelRect = {
        ...this.labelRect,
        x: 0, y: 0, width: 0, height: 0,
      };

      //
      this.selectedLabelIndices = {p_idx: -1, a_idx: -1};
    },
    showLabelRect(p_idx, a_idx) {
      //
      let bbox = this.editedProblems[p_idx].labels[a_idx].bbox;
      if (!Array.isArray(bbox) || (bbox.length < 4)) {
        bbox = [0, 0, 0, 0];
      }

      //
      const [left, top, right, bottom] = bbox;
      this.labelRect = {
        ...this.labelRect,
        ...this.convertBboxToRect(left, top, right, bottom),
      };

      //
      if (!this.labelRect.width || !this.labelRect.height) {
        p_idx = -1;
        a_idx = -1;
      }
      this.selectedLabelIndices = {p_idx, a_idx};
    },

    //
    closeDrawRectDialog() {
      //
      this.drawRectDialog.show = false;

      //
      this.drawRectDialog.p_idx = -1;
      this.drawRectDialog.a_idx = -1;

      //
      this.drawRectDialog.initRect = {
        ...this.drawRectDialog.initRect,
        x: 0, y: 0, width: 0, height: 0,
      };

      //
      this.drawRectDialog.rect = {
        ...this.drawRectDialog.rect,
        x: 0, y: 0, width: 0, height: 0, scaleX: 1, scaleY: 1
      };

      //
      this.deselectDrawRect();
    },
    showDrawRectDialog(p_idx, a_idx) {
      //
      this.drawRectDialog.p_idx = p_idx;
      this.drawRectDialog.a_idx = a_idx;

      //
      let bbox = this.editedProblems[p_idx].labels[a_idx].bbox;
      if (!Array.isArray(bbox) || (bbox.length < 4)) {
        bbox = [0, 0, 0, 0];
      }
      const [left, top, right, bottom] = bbox;
      this.drawRectDialog.initRect = {
        ...this.labelRect,
        ...this.convertBboxToRect(left, top, right, bottom),
      };

      //
      let {x, y, width, height} = {x: this.PAGE_IMAGE_WIDTH/4, y: this.PAGE_IMAGE_HEIGHT/4, width: this.PAGE_IMAGE_WIDTH/2, height: this.PAGE_IMAGE_HEIGHT/2};
      if (this.drawRectDialog.initRect.width && this.drawRectDialog.initRect.height) {
        x = this.drawRectDialog.initRect.x;
        y = this.drawRectDialog.initRect.y;
        width = this.drawRectDialog.initRect.width;
        height = this.drawRectDialog.initRect.height;
      }
      this.drawRectDialog.rect = {
        ...this.drawRectDialog.rect,
        x, y, width, height, scaleX: 1, scaleY: 1
      };

      //
      this.drawRectDialog.show = true;
    },
    deselectDrawRect() {
      const transformerNode = this.$refs.transformer.getNode();

      transformerNode.nodes([]);
    },
    selectDrawRect() {
      const transformerNode = this.$refs.transformer.getNode();
      const drawRectNode = this.$refs.drawRect.getNode();

      transformerNode.nodes([drawRectNode, ]);
    },
    handleStageMouseDown(e) {
      // clicked on stage - clear selection
      if ((e.target === e.target.getStage()) || (e.target.className === 'Image')) {
        return this.deselectDrawRect();
      }

      // clicked on transformer - do nothing
      if (e.target.getParent().className === 'Transformer') {
        return ;
      }

      // clicked rect
      if (e.target.name() === 'drawRect') {
        return this.selectDrawRect();
      }
    },
    handleDragEnd(e) {
      this.drawRectDialog.rect.x = e.target.x();
      this.drawRectDialog.rect.y = e.target.y();
    },
    handleTransformEnd(e) {
      this.drawRectDialog.rect.x = e.target.x();
      this.drawRectDialog.rect.y = e.target.y();
      this.drawRectDialog.rect.scaleX = e.target.scaleX();
      this.drawRectDialog.rect.scaleY = e.target.scaleY();
    },
    redrawRect() {
      //
      this.drawRectDialog.rect = {
        ...this.drawRectDialog.rect,
        x: this.PAGE_IMAGE_WIDTH/4,
        y: this.PAGE_IMAGE_HEIGHT/4,
        width: this.PAGE_IMAGE_WIDTH/2,
        height: this.PAGE_IMAGE_HEIGHT/2,
        scaleX: 1,
        scaleY: 1
      };
    },
    saveDrawRect() {
      //
      const {p_idx, a_idx} = this.drawRectDialog;
      const {x, y, width, height, scaleX, scaleY} = this.drawRectDialog.rect;

      //
      const {left, top, right, bottom} = this.convertRectToBbox(x, y, (width * scaleX), (height * scaleY));
      this.editedProblems[p_idx].labels[a_idx].bbox = [left, top, right, bottom];

      //
      this.showLabelRect(p_idx, a_idx);
      this.closeDrawRectDialog();
    },

    //
    savePage() {
      this.$store.dispatch('UPDATE_PAGE', {page_id: this.page_id, dto: {problems: this.editedProblems}})
        .then(() => {
          this.$router.back();
        })
        .catch(() => {
          this.$eventBus.$emitSnackbar('페이지 생성을 할 수 없습니다.');
        });

    }
  }
};
</script>

<style scoped>

</style>