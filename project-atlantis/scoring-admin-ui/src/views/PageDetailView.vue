<template>
  <div>
    <v-card class="pa-4">
      <v-container row>
        <v-avatar size="240" tile>
          <v-img contain :src="resolveUrl(page.original_url)" />
        </v-avatar>
        <v-avatar size="240" tile>
          <v-img contain :src="resolveUrl(page.sample_url)" />
        </v-avatar>
        <div>
          <v-card-title> {{ page.page_num }} </v-card-title>
          <v-card-subtitle > {{ page.description }} </v-card-subtitle>
        </div>
      </v-container>
      <v-card-actions>
        <v-spacer />
        <v-btn @click="$router.back()">확인</v-btn>
      </v-card-actions>
    </v-card>
    <v-spacer class="ma-6" />
    <v-card class="pa-4" v-if="Array.isArray(page.problems) && page.problems.length">
      <v-container row>
        <v-card flat width="520">
          <v-card-text>
            <v-list dense>
              <v-list-item row v-for="(problem, idx) in page.problems" :key="idx">
                <v-text-field readonly label="문제 #" :value="problem.prob_num"/>
                <div class="ma-2" />
                <v-btn
                  small
                  :depressed="idx === selectedProblemIndex"
                  @click="() => showLabelRect(idx)"
                >
                  영역보기
                </v-btn>
                <div class="ma-2" />
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn small outlined v-bind="attrs" v-on="on">해설 보기</v-btn>
                  </template>
                  <span>
                    <v-img eager max-width="320" :src="resolveUrl(problem.solving_url)" />
                  </span>
                </v-tooltip>
                <div class="ma-2" />
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn small outlined v-bind="attrs" v-on="on">유사문제 보기</v-btn>
                  </template>
                  <span>
                    <v-img eager max-width="320" :src="resolveUrl(problem.similar_url)" />
                  </span>
                </v-tooltip>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
        <v-divider class="ma-2" vertical />
        <v-card flat>
          <v-card-text>
            <v-stage :width="PAGE_IMAGE_WIDTH" :height="PAGE_IMAGE_HEIGHT">
              <v-layer>
                <v-image :config="pageImage" />
                <v-rect v-for="(labelRect, idx) in labelRects" :key="idx" :config="labelRect" />
              </v-layer>
            </v-stage>
          </v-card-text>
        </v-card>
      </v-container>
    </v-card>
  </div>
</template>

<script>
import {resolveImageUrl} from "../utils/image.js";

export default {
  name: 'ScoringAdminUiPageDetailView',

  data() {
    return {
      page: {},

      //
      PAGE_IMAGE_WIDTH: 480,
      PAGE_IMAGE_HEIGHT: 600,
      INIT_RECT_CONFIG: {stroke: 'green', strokeWidth: 4, draggable: false, x: 0, y: 0, width: 0, height: 0},

      //
      pageImage: {image: null, scaleX: 1, scaleY: 1},
      selectedProblemIndex: -1,
      labelRects: [],
    };
  },

  mounted() {
    //
    const {page_id} = this.$route.params;

    //
    this.$store.dispatch('FETCH_PAGE', page_id)
      .then((page) => {
        //
        this.page = page;

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

    convertBboxToRect(l, t, r, b) {
      const {scaleX, scaleY} = this.pageImage;

      return {
        x: Math.min(l, r) * scaleX,
        y: Math.min(t, b) * scaleY,
        width: Math.abs(r - l) * scaleX,
        height: Math.abs(b - t) * scaleY,
      };
    },
    showLabelRect(idx) {
      //
      let labelRects = [];

      //
      const problem = this.page.problems[idx];
      if (problem && Array.isArray(problem.labels)) {
        for (const label of problem.labels) {
          const bbox = label.bbox;
          if (!Array.isArray(bbox) || (bbox.length < 4)) {
            continue;
          }

          const [left, top, right, bottom] = bbox;
          labelRects.push({
            ...this.INIT_RECT_CONFIG,
            ...this.convertBboxToRect(left, top, right, bottom),
          });
        }
      }

      //
      this.labelRects = labelRects;
      this.selectedProblemIndex = idx;
    },
  },
};
</script>

<style scoped>

</style>