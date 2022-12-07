<template>
  <v-container fluid>
    <v-card>
      <div>
        <v-card-text class="pb-0">
          {{ getMLTaskName(dataset.ml_task) }}
        </v-card-text>
        <div class="d-flex">
          <v-avatar class="ma-3" size="192" tile>
            <v-img :src="dataset.cover_image" contain/>
          </v-avatar>
          <div class="pa-0 ma-0" style="width:100%;">
            <v-footer color="white" padless>
              <v-card-title class="pt-0">
                {{ dataset.name }}
              </v-card-title>  
              <v-card-text>
                {{ dataset.description }}
              </v-card-text>
              <v-card-subtitle class="grey--text">
                {{ dataset.labeled_data }} / {{ dataset.total_data }}
              </v-card-subtitle>   
            </v-footer>
            <v-card-actions class="justify-end">
              <v-btn 
                large 
                color="warning" 
                @click="dialog.show.delete_dataset = true"
              >DELETE</v-btn>
              
              <v-btn 
                large
                @click="editDatset"
              >EDIT</v-btn>
              
              <v-btn 
                large 
                color="primary" 
                @click="uploadData({dataset_id: dataset._id})"
              >UPLOAD</v-btn>
            </v-card-actions>
          </div>
        </div>
      </div>
      <v-dialog persistent width="500" v-model="dialog.show.delete_bundle">
        <v-card>
          <v-card-title>Delete Bundle</v-card-title>
          <v-card-text>All-data in {{deleteBundleDto.name}} will be deleted</v-card-text>
          <v-card-actions class="justify-end">
            <v-btn 
              large 
              @click="dialog.show.delete_bundle = false"
            >CANCEL</v-btn>
            <v-btn 
              large 
              color="warning" 
              @click="deleteBundle(deleteBundleDto.bundle_id)"
            >DELETE</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog persistent width="500" v-model="dialog.show.delete_dataset">
        <v-card>
          <v-card-title>Delete Dataset</v-card-title>
          <v-card-text>All bundles and data in {{dataset.name}} will be deleted.</v-card-text>
          <v-card-actions class="justify-end">
            <v-btn 
              large 
              @click="dialog.show.delete_dataset = false"
            >CANCEL</v-btn>
            <v-btn 
              large 
              color="warning" 
              @click="deleteDataset"
            >DELETE</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog persistent width="500" v-model="dialog.show.create_bundle">
        <v-card>
          <v-card-title>Create Bundle</v-card-title>
          <v-card-text>
            <v-form
                ref="form"
                v-model="createBundleDto.valid"
                lazy-validation
            >
              <v-row>
                <v-col cols="3">
                  <v-card-subtitle class="pa-2 pl-0">Name<v-icon x-small color="red">mdi-asterisk</v-icon> :</v-card-subtitle>
                </v-col>
                <v-col cols="9">
                  <v-text-field
                    label="Bundle Name"
                    dense
                    required
                    v-model="createBundleDto.name"
                    :rules="[v => !!v || 'Required.']"
                  ></v-text-field>
                </v-col>
                <v-col cols="3">
                  <v-card-subtitle class="pa-2 pl-0">Description :</v-card-subtitle>
                </v-col>
                <v-col cols="9">
                  <v-textarea
                    name="input-7-1"
                    label="Bundle Description"
                    v-model="createBundleDto.description"
                    hint="Bundle Description"
                  ></v-textarea>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn 
              large 
              @click="dialog.show.create_bundle = false"
            >CANCEL</v-btn>
            <v-btn 
              large 
              color="primary" 
              @click="submitBundleDialog"
            >CREATE</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card>
    <v-card  class="mt-10">
      <v-row class="ma-0">
        <v-col>
          <v-card-title class="float-left">Bundles</v-card-title>
        </v-col>
        <v-col class="pa-5">
          <v-btn 
            class="float-right"
            large 
            color="primary" 
            @click="dialog.show.create_bundle = true"
          >CREATE</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col class="ma-5">
          <v-data-table
            :headers="headers"
            :items="customBundles"
            sort-by="calories"
            class="elevation-1"
          > 
            <template v-slot:[`item.actions`]="{ item }">
              <v-container row>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                      <v-btn 
                        icon 
                        outlined
                        v-bind="attrs"
                        v-on="on"
                        @click="editBundle(item)"
                      >
                        <v-icon>
                          mdi-text-box-edit-outline
                        </v-icon>
                      </v-btn>
                  </template>
                  <span>Bundle 수정</span>
                </v-tooltip>
                <div class="mx-2"></div>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn 
                      icon 
                      outlined
                      v-bind="attrs"
                      v-on="on"
                      @click="dialog.show.delete_bundle = true; deleteBundleDto = item;"
                    >
                      <v-icon>
                        mdi-delete
                      </v-icon>
                    </v-btn>
                  </template>
                  <span>Bundle 삭제</span>
                </v-tooltip>
                <div class="mx-2"></div>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn 
                      icon 
                      outlined
                      v-bind="attrs"
                      v-on="on"
                      @click="uploadData({dataset_id: item.dataset_id, bundle_id: item.bundle_id})"
                    >
                      <v-icon>
                        mdi-tray-arrow-up
                      </v-icon>
                    </v-btn>
                  </template>              
                  <span>파일 업로드</span>
                </v-tooltip>
              </v-container>
            </template>
            <template v-slot:no-data>
              NO DATA
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </v-card>
    <v-card  class="mt-10">
      <v-row class="ma-0">
        <v-col class="d-flex pt-5" cols="10">
          <v-row>
            <v-col cols="8" style="max-width:600px;">
              <v-select
                class="mx-2"
                multiple
                dense
                outlined
                chips
                clearable
                label="bundles"
                item-text="name"
                item-value="_id"
                :items="bundles"
                v-model="selected.bundles"
                @change="fetchAnnotations"
                @click:clear="fetchAnnotations"
              >
              </v-select>
            </v-col>
            <v-col cols="4" style="max-width:300px;">
              <v-select
                class="mx-2"
                dense
                outlined
                clearable
                label="labeled/unlabeled"
                :items="[{text:'labeled',value:1},{text:'unlabeled',value:0}]"
                v-model="selected.labeled"
                @change="fetchAnnotations"
                @click:clear="fetchAnnotations"
              >
              </v-select>
            </v-col>
          </v-row>
        </v-col>
        <v-col class="pa-5" cols="2">
          <v-btn 
            class="float-right"
            large 
            color="primary"
            @click="moveAnnotationView"
          >ANNOTATE</v-btn>
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
            <v-card hover>
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
                  <v-card-text class="text-left d-inline-block text-truncate" style="max-width: 100%">
                    {{ anno.description }}
                  </v-card-text>
                </v-card>
                <v-card-subtitle class="d-inline-block text-truncate" style="max-width: 100%">{{anno.file_name}}</v-card-subtitle>
                <v-divider></v-divider>
              </v-container>
              <v-img
                v-else
                :src="getCoverImage(anno.file_url)"
                class="white--text align-end"
                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                height="200px"
              >
                <v-card-title class="d-inline-block text-truncate" style="max-width: 100%" v-text="anno.file_name"></v-card-title>
              </v-img>

              <v-card-actions>
                <!--done-->
                <v-icon color="green" v-if="anno.done === 1">
                  mdi-checkbox-marked-circle-outline
                </v-icon>
                <v-icon color="green" v-else-if="anno.done === 0 && anno.labels.length > 1">
                  mdi-tag-check-outline
                </v-icon>
                <v-icon color="red" v-else>
                  mdi-tag-remove-outline
                </v-icon>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
      <v-row>
        <v-col cols="10">
          <v-pagination
            v-model="pagenation.page"
            :length="pagenation.length"
            :total-visible="10"
            @input="fetchAnnotations"
          ></v-pagination>
        </v-col>
        <v-col cols="2" class="pr-10 d-flex justify-end">
          <v-select
            v-model="selected.limit"
            :items="[10, 20, 50]"
            dense
            outlined
            hint="per page"
            persistent-hint
            @change="fetchAnnotations"
            style="max-width:120px;"
          ></v-select>
        </v-col> 
      </v-row>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
    data: () => ({
      dataset: {},
      bundles: [],
      customBundles: [],
      annotations: [],
      createBundleDto: {
        name: '',
        description: '',
        valid: true,
      },
      deleteBundleDto: {
        bundle_id : '',
      },
      pagenation: {
        limit: 10,
        page: 1,
      },
      dialog: {
        show: {
          delete_dataset: false,
          delete_bundle: false,
          create_bundle: false,
        },
      },
      selected: {
        bundles: [],
        labeled: null,
        limit: 10,
      },
      headers: [
        {
          text: 'Name',
          sortable: false,
          value: 'name',
        },
        { text: 'Description', value: 'description' },
        { text: 'Attributes', value: 'attributes' },
        { text: '# of data', value: 'data' },
        { text: 'Complete rate($)', value: 'complete_rate' },
        { text: '#', width: '200', value: 'actions', sortable: false },
      ],
      
    }),
    computed: {
      ...mapGetters({
        fetchedAnnotationViewFilter: 'fetchedAnnotationViewFilter',
      })
    },
    created() {
      //필터 유지
      const route_params = this.$route.params;
      if(route_params.filterMaintain){
        this.selected.limit = this.fetchedAnnotationViewFilter.limit;
        this.selected.labeled = this.fetchedAnnotationViewFilter.labeled;
        this.selected.bundles = this.fetchedAnnotationViewFilter.bundle_id;
      }

      this.fetchDataset();
      this.fetchBundles();
    },
    methods: {
      fetchDataset() {
        this.$store.dispatch('FETCH_DATASET', this.$route.params.dataset_id)
        .then(res => {
          console.log('DatasetDetailView - created - fetch dataset',res);
          this.dataset = res;
          this.dataset.cover_image = this.getCoverImage(this.dataset.cover_image);
        })
        .catch(error => { console.log(error) });
      },
      fetchBundles() {
        this.$store.dispatch('FETCH_BUNDLES', this.$route.params.dataset_id)
        .then(res => {
          console.log('DatasetDetailView - created - fetch bundles',res);
          this.bundles = res.results;
          const customBundles = [];
          res.results.forEach((r) => {
            customBundles.push({
              dataset_id: this.$route.params.dataset_id,
              bundle_id: r._id,
              name: r.name,
              description: r.description.replace(/(?<=.{20})(.*)(=?)/, '...'),
              attributes: r.attributes.length,
              data: r.total_data,
              //complete_rate: isNaN((r.labeled_data / r.total_data)) ? 'NA' : `${((r.labeled_data / r.total_data) * 100)}%`
              complete_rate: r.labeled_data === 0 ? 'N/A' : `${((r.labeled_data / r.total_data) * 100)}%`
            });
          });
          this.customBundles = [...customBundles];
          this.fetchAnnotations();
        })
        .catch(error => { console.log(error) });
      },
      fetchAnnotations() {
        const params = { 
          dataset_id : this.$route.params.dataset_id, 
          limit: this.pagenation.limit, 
          sort_by: null, 
          page: this.pagenation.page ,
          bundle_ids: this.selected.bundles,
          label_status: this.selected.labeled,
        };
        this.$store.dispatch('FETCH_ANNOTATIONS', params)
        .then(res => {
            console.log('DatasetDetailView - created - fetch annotations',res);
            this.pagenation = res.pagenation;
            this.selected.limit = res.limit;
            this.annotations = res.annotations;
        })
        .catch(error => { console.log(error) });
      },
      createBundle() {
        const createBundleDto = this.createBundleDto;
        createBundleDto.dataset_id = this.$route.params.dataset_id;
        this.$store.dispatch('CREATE_BUNDLE', createBundleDto)
          .then(res => {
            console.log('DatasetDetailView - dispatch - CREATE_BUNDLE', res);
            // 번들 수정 페이지로 이동(14p)
            this.$router.push({name: 'BundleEditView', params: {dataset_id: res.dataset_id, bundle_id: res._id}})
          })
          .catch(error => { console.log(error); });
      },
      deleteBundle(bundle_id) {
        console.log('DELETE BUNDLE - id', bundle_id);
        this.$store.dispatch('DELETE_BUNDLE', bundle_id)
          .then(res => {
            console.log('DELETE', res);
            //bundles 새로 조회
            this.fetchBundles();
            console.log('DELETE 후 customBundles', this.customBundles);
            this.dialog.show.delete_bundle = false;
          })
          .catch(error => { console.log(error); });
      },
      deleteDataset() {
        console.log('DELETE DATASET');
        this.$store.dispatch('DELETE_DATASET', this.$route.params.dataset_id)
          .then(res => {
            console.log('DELETE', res);
            this.$router.push({name: 'DatasetView'});
          })
          .catch(error => { console.log(error); });
      },
      submitBundleDialog() {
        const validateForm = this.$refs.form.validate();
            
        if(validateForm) {
          this.createBundle();
        } else {
          alert('필수 입력 필드를 확인해주세요');
        }
      },
      editDatset(){
        this.$router.push({name: 'DatasetEditView', params: {dataset_id: this.$route.params.dataset_id}});
      },
      editBundle({bundle_id}) {
        this.$router.push({name: 'BundleEditView', params: {dataset_id: this.$route.params.dataset_id, bundle_id: bundle_id}})
      },
      uploadData({dataset_id, bundle_id}) {
        const params = {
          dataset_id: dataset_id != null ? dataset_id : null,
          bundle_id: bundle_id != null ? bundle_id : null,
          ml_task: this.dataset.ml_task != null ? this.dataset.ml_task : null,
        };
        
        console.log('params', params);
        this.$router.push({name: 'DatasetUploadView', params: params});
      },
      moveAnnotationView() {
        const params = {
          dataset_id: this.$route.params.dataset_id,
          selected_bundles: this.selected.bundles,
          selected_labeled: this.selected.labeled,
        };
        this.$router.push({name: 'AnnotationView', params: params})
      },
    }
}
</script>