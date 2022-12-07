<template>
  <v-container fluid>
    <v-card>
      <div>
        <v-container row fluid>
          <v-col class="pa-0">
            <v-card-text class="pb-0 pt-0">
              {{ getMLTaskName(versionedDataset.ml_task) }} > <strong>{{ versionedDataset.dataset_name }}</strong>
            </v-card-text>    
          </v-col>
        </v-container>
        <div class="d-flex">
          <div class="pa-2 ma-0">
            <v-card-title class="pt-0">
              {{ versionedDataset.name }}
            </v-card-title>
            <v-card-text>
              Version {{ versionedDataset.index }} Generated {{ dayjs(versionedDataset.reg_date).format('YYYY-MM-DD') }}
            </v-card-text>
            <v-card-subtitle class="grey--text">
              {{ versionedDataset.split }}
            </v-card-subtitle>
          </div>
        </div>
        <v-card-actions>
          <v-col class="pa-2">
            <v-icon size="45">
              {{ {...this.status.find((r => r.value === this.versionedDataset.status))}.icon }}
            </v-icon>
          </v-col>
          <v-col>
            <v-btn
              class="float-right"
              color="warning"
              large
              @click="dialog.show.deleteVersionedDataset = true"
            >
              DELETE
            </v-btn>
          </v-col>
        </v-card-actions>
      </div>
    </v-card>
    <v-card  class="mt-10">
      <v-row class="ma-0 pa-2">
        <v-col cols="auto">
          <v-select
            dense
            clearable
            outlined
            label="Attributes"
            :items="attributesInfo"
            v-model="select.attribute"
            @change="fetchAnnotations"
          >
          </v-select>
        </v-col>
        <v-col cols="auto">
          <v-select
            dense
            clearable
            outlined
            :items="split"
            label="Split"
            v-model="select.split"
            @change="fetchAnnotations"
          >
          </v-select>
        </v-col>
      </v-row>
      <v-container>
        <v-row dense>
          <v-col
            class="pa-5" 
            v-for="(anno,index) in annotations" 
            :key="index"
            style="max-width:19.7%;flex:0 0 19.7%;"
          >
            <v-card 
              hover
              @click="openDialogAnnotationDetail(anno)"
            >
              <v-container
                v-if="anno.ml_task == 0"
                fluid
                class="pa-0 pt-5 text-center"
              >
                <v-card 
                  height="150"
                  width="220"
                  elevation="2"
                  class="mx-auto rounded-lg"
                  outlined
                  style="border-color:black;border-width:5px;"
                >
                  <v-card-text class="text-left">
                    {{ anno.description.length > 25 ? `${anno.description.substring(0,25)} ...` : anno.description }}
                  </v-card-text>
                </v-card>
                <v-card-subtitle>{{anno.file_name}}</v-card-subtitle>
                <v-divider></v-divider>
              </v-container>
              <v-img
                v-else
                :src="getCoverImage(anno.file_url)"
                class="white--text align-end"
                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                height="200px"
              >
                <v-card-title v-text="anno.file_name"></v-card-title>
              </v-img>

              <v-card-actions>
                <span v-if="anno.split === 0">
                  <v-icon color="blue">
                    mdi-folder-open
                  </v-icon>
                  <small>Training</small>
                </span>
                <span v-else-if="anno.split === 1">
                  <v-icon color="yellow">
                    mdi-folder-open
                  </v-icon>
                  <small>Validation</small>
                </span>
                <span v-else-if="anno.split === 2">
                  <v-icon color="green">
                    mdi-folder-open
                  </v-icon>
                  <small>Testing</small>
                </span>
                <span v-else>
                  <v-icon color="red">
                    mdi-folder-alert
                  </v-icon>
                  <small>Error</small>
                </span>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
      <v-row>
          <v-col cols="11">
              <v-pagination
                  v-model="pagenation.page"
                  :length="pagenation.length"
                  :total-visible="10"
                  @input="fetchAnnotations"
              ></v-pagination>
          </v-col>
          <v-col cols="1" class="pr-10">
              <v-select
                  v-model="select.limit"
                  :items="[10, 20, 50, 100]"
                  dense
                  outlined
                  hint="per page"
                  persistent-hint
                  @change="fetchAnnotations"
              ></v-select>
          </v-col> 
      </v-row>
    </v-card>
    <v-dialog :width="konvaConfig.stage.width < 600 ? 600 : konvaConfig.stage.width" v-model="dialog.show.annotationDetail">
      <v-card>
        <v-card-title>{{select.annotation.file_name}}</v-card-title>
        <v-divider></v-divider>
        <v-row class="pa-0 ma-0">
          <v-col cols="12">
            <v-card-text class="text-left" v-if="select.annotation.ml_task === 0">{{select.annotation.description}}</v-card-text>
            <div ref="workarea" class="workarea px-1" v-else>
              <v-stage 
                ref="stage" 
                :config="konvaConfig.stage"
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
                        visible: rect.visible,
                    }"
                  ></v-rect>
                </v-layer>
              </v-stage>
            </div>
          </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-container class="pa-0 ma-0" v-if="select.annotation.ml_task === 0">
          <template v-for="(labels,index) in select.annotation.labels">
            <v-row class="pa-0 ma-0" :key="index">
              <v-card-text v-if="labels.type === 'label'">
                Text : {{labels.text}}<br>
                Label : {{labels.label}}
              </v-card-text>
            </v-row>
          </template>
        </v-container>
        <v-container class="pa-0 ma-0 pb-3" v-else>
          <v-row class="pa-0 ma-0">
            <v-col cols="2">
              <v-card-subtitle class="pa-0">Image Size:</v-card-subtitle>
            </v-col>
            <v-col cols="9">
              <v-card-text class="pa-0">W:{{konvaConfig.stage.width}} H:{{konvaConfig.stage.height}}</v-card-text>
            </v-col>
            <v-col cols="12" class="py-0">
              <v-card-text class="pa-0 text-h7"><strong>Labels Info</strong></v-card-text>
            </v-col>
          </v-row>  
          <template v-for="rect in shapeConfig.rects">
            <v-row class="pa-0 ma-0" :key="rect.name">
              <v-col cols="12" class="py-0">
                <v-card-subtitle class="pa-0">
                  <v-checkbox
                    class="ma-0"
                    v-model="rect.visible"
                    hide-details
                    :false-value="false"
                    :true-value="true"
                    :label="rect.name"
                  >
                  </v-checkbox>
                </v-card-subtitle>
              </v-col>
              <v-col cols="12" class="py-0">
                <v-card-text class="pa-0 px-2">
                  Label : {{ shapeConfig.labels[rect.name].label }}
                </v-card-text>
                <v-card-text class="pa-0 px-2">
                  Bbox : {{shapeConfig.labels[rect.name].bbox.map(r => parseInt(r)).join(', ')}}
                </v-card-text>
                <v-card-text class="pa-0 px-2">
                  Attributes
                </v-card-text>
                <v-card-text class="pa-0 px-4" v-html="`- ${shapeConfig.labels[rect.name].attributes.map(r => `${r.key}:${r.values}`).join('<br>- ')}`">
                </v-card-text>
              </v-col>
            </v-row>            
          </template>

        </v-container>
      </v-card>
    </v-dialog>
    <v-dialog persistent width="500" v-model="dialog.show.deleteVersionedDataset">
      <v-card>
        <v-card-title>Delete VersionedDataset</v-card-title>
        <v-card-text>All-data in {{versionedDataset.name}} will be deleted</v-card-text>
        <v-card-actions class="justify-end">
          <v-btn 
            large 
            @click="dialog.show.deleteVersionedDataset = false"
          >CANCEL</v-btn>
          <v-btn 
            large 
            color="warning" 
            @click="deleteVersionedDataset"
          >DELETE</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    versionedDataset: {},
    annotations: [],
    attributesInfo: [],
    status: [
      { text : 'queued', value: 0 , icon: 'mdi-clipboard-text-clock-outline' },
      { text : 'processing', value: 1, icon: 'mdi-clipboard-play-outline' },
      { text : 'done', value: 2, icon: 'mdi-clipboard-check-outline' },
      { text : 'failed', value: 3, icon: 'mdi-clipboard-alert-outline' },
    ],
    split: [
      { text: 'training', value: '0'},
      { text: 'validation', value: '1'},
      { text: 'testing', value: '2'},
    ],
    select: {
      attribute: null,
      split: null,
      annotation: {},
      limit: 10,
    },
    pagenation: {
      page: 1,
      length: null,
    },
    dialog: {
      show: {
        annotationDetail: false,
        deleteVersionedDataset: false,
      },
    },
    konvaConfig: {
      stage: {
        width: 768,
        height: 450,
        draggable: false,
        scaleX : 1,
        scaleY : 1,
      },
      image: {
        image: null,
      },
    },
    shapeConfig: {
      idx: 0,
      rects: [],
      labels: {},
      isDragging: false,
    },
  }),
  created() {
    this.fetchVersionedDataset();
    this.fetchAnnotations();
  },
  computed: {
    
  },
  methods: {
    fetchVersionedDataset() {
      this.$store.dispatch('FETCH_VERSIONEDDATASET', this.$route.params.versioneddataset_id)
        .then(res => {
          this.versionedDataset = res;
          
          res.attribute_info.forEach((attr) => {
            attr.values.forEach(value => {
              this.attributesInfo = [...this.attributesInfo, {text: `${attr.key}:${value}`, value: `${attr.key}:${value}`}];
            })
          });

        })
        .catch(error => { console.log(error); });
    },
    fetchAnnotations() {
      const params = { 
        versioned_dataset_id: this.$route.params.versioneddataset_id, 
        limit: this.pagenation.limit, 
        sort_by: null, 
        page: this.pagenation.page ,
        attribute: this.select.attribute,
        split: this.select.split,
      };
      this.$store.dispatch('FETCH_ANNOTATIONS', params)
        .then(res => {
            console.log('DatasetDetailView - created - fetch annotations',res);
            this.pagenation = res.pagenation;
            this.select.limit = res.limit;
            this.annotations = res.annotations;
        })
        .catch(error => { console.log(error) });  
    },
    deleteVersionedDataset() {
      this.$store.dispatch('DELETE_VERSIONEDDATASET', this.$route.params.versioneddataset_id)
        .then(res => {
          console.log('VersionedDAtasetDetailView - DELETE_VERSIONEDDATASET - res', res);
          this.$router.push({name:'VersionedDatasetView'});
        })
        .catch(error => { console.log(error); });
    },
    openDialogAnnotationDetail(anno) {
      this.dialog.show.annotationDetail = true;
      this.select.annotation = anno;

      //
      this.shapeConfig = {
        idx: 0,
        rects: [],
        labels: {},
        isDragging: false,
      };
      if (this.select.annotation.ml_task === 1) {
        this.select.annotation.labels.forEach((v,i) => {
          const {bbox, label, attributes} = v;
          const labelObj = {};
          labelObj[`rect${i}`] = { bbox: bbox, label: label, attributes: attributes };
          this.shapeConfig.labels = { ...this.shapeConfig.labels, ...labelObj};

          this.shapeConfig.rects = [
            ...this.shapeConfig.rects,
            { name: `rect${i}`, startPointX: Math.min(bbox[0],bbox[2]), startPointY: Math.min(bbox[1],bbox[3]), width: Math.abs(bbox[0] - bbox[2]), height: Math.abs(bbox[1] - bbox[3]), scaleX: 1, scaleY: 1, draggable: false, visible: true }
          ];
          this.shapeConfig.idx++;
        });

        // 이미지 세팅
        const image = new window.Image();
        image.src = this.getCoverImage(this.select.annotation.file_url);
        //image.src = require('../assets/no-image.jpg');
        this.konvaConfig.stage.width = image.width;
        this.konvaConfig.stage.height = image.height;
        image.onload = () => {
          // set image only when it is loaded
          this.konvaConfig.image.image = image;
        };
      }

    },
   

  }
}
</script>