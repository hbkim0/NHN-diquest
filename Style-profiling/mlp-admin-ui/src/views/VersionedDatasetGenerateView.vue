<template>
  <v-card>
    <v-stepper
      v-model="generateStep"
      vertical
    >
      <!-- Step 1 -->
      <v-stepper-step
        :complete="generateStep > 1"
        step="1"
        :rules="stepperRules.step1"
      >
        Source dataset and bundles
        <div v-if="generateStep > 1">
          <v-icon size="15">
            mdi-arrow-right-bottom-bold
          </v-icon>
          <span class="gray--text text-caption">dataset : {{getNames.datasetName}} / bundles : {{getNames.bundleNames.join(', ')}}</span>
        </div>
        <div v-if="(generateDto.bundles.length === 0) || (generateDto.dataset === null)">
          <v-icon color="red" size="15">
            mdi-alert-circle-outline
          </v-icon>
          <span class="gray--text text-caption">Dataset과 Bundle들을 선택해주세요.</span>
        </div>
        <div v-if="getCounts.labeled === 0">
          <v-icon color="red" size="15">
            mdi-alert-circle-outline
          </v-icon>
          <span class="gray--text text-caption">Labeled Data가 존재 하지 않습니다.</span>
        </div>
      </v-stepper-step>
      <v-stepper-content step="1">
        <v-card
            outlined
            class="mb-5"
        >
          <v-card-text>
            <v-container row>
              <v-col cols="auto" class="pb-0">
                <v-select
                  full-width
                  outlined
                  dense
                  clearable
                  v-model="generateDto.dataset"
                  :items="datasets"
                  item-text="name"
                  item-value="_id"
                  label="Dataset"
                  @change="fetchBundles"
                  @click:clear="generateDto.bundles=[]"
                >
                </v-select>
              </v-col>
              <v-col cols="auto"  class="pb-0">
                <v-select
                  outlined 
                  dense
                  clearable
                  v-model="generateDto.bundles"
                  multiple
                  small-chips
                  :items="bundles"
                  item-text="name"
                  item-value="_id"
                  label="Bundles"
                  @change="changeSplitRange"
                >
                </v-select>
              </v-col>            
            </v-container>
          </v-card-text>
          <v-card-subtitle class="pt-0 pb-0">
            <v-col>Counts : {{ getCounts.labeled }} / {{ getCounts.total }} ( labeled / total ) </v-col>
          </v-card-subtitle>
          <v-card-actions class="justify-end pr-5 pb-5">
            <v-btn
              color="primary"
              @click="nextStep(2)"
            >
              NEXT
            </v-btn>    
          </v-card-actions>
        </v-card>
      </v-stepper-content>

      <!-- Step 2 -->
      <v-stepper-step
        :complete="generateStep > 2"
        step="2"
        :rules="stepperRules.step2"
      >
        Train/Test split
        <div v-if="generateStep > 2">
            <v-icon size="15">
              mdi-arrow-right-bottom-bold
            </v-icon>
            <span class="gray--text text-caption">Train : {{getSplits.train}} Valid : {{getSplits.valid}} Test : {{getSplits.test}}</span>
        </div>
      </v-stepper-step>
      <v-stepper-content step="2">
        <v-card
          outlined
          class="mb-5"
        >
          <v-card-text>
            <v-container class="ma-0 pa-0" row>
              <v-card-title>
                labeled_data : {{getCounts.labeled}}
              </v-card-title>
            </v-container>
            <v-container class="ma-0 pa-0" row v-if="getCounts.labeled > 0">
              <div class="text-center" :style="getDivWidth.train" v-if="getSplits.train !== 0">
                <v-tooltip top>
                  <template v-slot:activator="{ on, attrs }">
                      <span
                        v-bind="attrs"
                        v-on="on"
                      >{{getSplits.train}}</span>
                  </template>
                  <span>Training</span>
                </v-tooltip>
              </div>
              <div class="text-center" :style="getDivWidth.valid" v-if="getSplits.valid !== 0">
                <v-tooltip top>
                  <template v-slot:activator="{ on, attrs }">
                      <span
                        v-bind="attrs"
                        v-on="on"
                      >{{getSplits.valid}}</span>
                  </template>
                  <span>Validation</span>
                </v-tooltip>
              </div>
              <div class="text-center" :style="getDivWidth.test" v-if="getSplits.test !== 0">
                <v-tooltip top>
                  <template v-slot:activator="{ on, attrs }">
                    <span
                      v-bind="attrs"
                      v-on="on"
                    >{{getSplits.test}}</span>
                  </template>
                  <span>Testing</span>
                </v-tooltip>
              </div>
            </v-container>
            <v-container class="ma-0 pa-0" row v-if="getCounts.labeled > 0">
              <v-col class="pa-0">
                <v-range-slider
                  hide-details
                  v-model="splitRange"
                  inverse-label
                  step="1"
                  color="orange"
                  track-color="blue"
                  :max="getCounts.labeled"
                >
                </v-range-slider>
              </v-col>
            </v-container>
            <!--<v-container class="ma-0 pa-0" row>
                <div class="text-center" :style="getDivWidth.train">
                    {{getDivWidth.train.width}}
                </div>
                <div class="text-center" :style="getDivWidth.valid">
                    {{getDivWidth.valid.width}}
                </div>
                <div class="text-center" :style="getDivWidth.test">
                    {{getDivWidth.test.width}}
                </div>
            </v-container>-->
            <v-container class="ma-0 pa-0" row>
              <v-card-subtitle>
                Train : {{getSplits.train}}({{getDivWidth.train.width}})
              </v-card-subtitle>
              <v-card-subtitle>
                Valid : {{getSplits.valid}}({{getDivWidth.valid.width}})
              </v-card-subtitle>
              <v-card-subtitle>
                Test : {{getSplits.test}}({{getDivWidth.test.width}})
              </v-card-subtitle>
            </v-container>   
          </v-card-text>
          <v-card-actions class="justify-end pr-5 pb-5">
              <v-btn
                  @click="nextStep(1)"
              >
                  PREVIOUS
              </v-btn>
              <v-btn
                  color="primary"
                  @click="nextStep(3)"
              >
                  NEXT
              </v-btn>
          </v-card-actions>
        </v-card>
      </v-stepper-content>

      <!-- Step 3 -->
      <v-stepper-step
        :complete="generateStep > 3"
        step="3"
        :rules="stepperRules.step3"
      >
        Preprocessing
        <div v-if="generateStep > 3">
          <v-icon size="15">
            mdi-arrow-right-bottom-bold
          </v-icon>
          <span class="gray--text text-caption" v-if="getMlTask !== 0">
            {{activatePreprocessing}}
          </span>
          <span class="green--text text-caption" v-else>
            TEXT TAGGING > Skip
          </span>
        </div>
      </v-stepper-step>
      <v-stepper-content step="3">
        <v-card
          outlined
          class="mb-5"
        >
          <v-container fluid>
            <template v-for="(preprocessing, index) in generateDto.preprocessing">
              <v-row :key="index" align="center">
                <v-col cols="auto">
                  <v-switch
                    inset
                    hide-spin-buttons
                    :false-value="0"
                    :true-value="1"
                    v-model="preprocessing.activate"
                  ></v-switch>   
                </v-col>
                <v-col cols="auto">
                  <v-container class="pa-0 ma-0 align-center" row fluid>
                      <v-col cols="auto">
                        {{preprocessing.name}}
                      </v-col>
                  
                      <template v-for="(params,pIndex) in preprocessing.params" >
                        <v-col cols="auto" :key="pIndex">
                          <v-text-field
                            v-if="params.type === 'number'"
                            dense
                            hide-details
                            :label="params.name"
                            type="number"
                            v-model="params.value"
                          >
                          </v-text-field>
                          <v-text-field
                            v-else
                            dense
                            hide-details
                            v-model="params.value"
                          >
                          </v-text-field>
                        </v-col>
                      </template>
                  </v-container>
                </v-col>
              </v-row>
            </template>
          </v-container>
          <v-card-actions class="justify-end pr-5 pb-5">
              <v-btn
                @click="nextStep(2)"
              >
                PREVIOUS
              </v-btn>
              <v-btn
                color="primary"
                @click="nextStep(4)"
              >
                NEXT
              </v-btn>
          </v-card-actions>
        </v-card>
      </v-stepper-content>

      <!-- Step 4 -->
      <v-stepper-step
        :complete="generateStep > 4"
        step="4"
        :rules="stepperRules.step4"
      >
        Augmentation
        <div v-if="generateStep > 4">
          <v-icon size="15">
            mdi-arrow-right-bottom-bold
          </v-icon>
          <span class="gray--text text-caption" v-if="getMlTask !== 0">
            {{activateAugmentation}}
          </span>
          <span class="green--text text-caption" v-else>
            TEXT TAGGING > Skip
          </span>
        </div>
      </v-stepper-step>
      <v-stepper-content step="4">
        <v-card
          outlined
          class="mb-5"
        >
          <v-container fluid>
            <template v-for="(augmentation, index) in generateDto.augmentation">
              <v-row :key="index" align="center">
                <v-col cols="auto">
                  <v-switch
                    inset
                    hide-spin-buttons
                    :false-value="0"
                    :true-value="1"
                    v-model="augmentation.activate"
                  ></v-switch>   
                </v-col>
                <v-col cols="auto">
                  <v-container class="pa-0 ma-0 align-center" row fluid>
                    <v-col cols="auto">
                      {{augmentation.name}}
                    </v-col>
                
                    <template v-for="(params,pIndex) in augmentation.params" >
                      <v-col cols="auto" :key="pIndex">
                        <v-checkbox
                          v-model="params.value"
                          :label="params.name"
                        >
                        </v-checkbox>
                      </v-col>
                    </template>
                  </v-container>
                </v-col>
              </v-row>
            </template>
          </v-container>
          <v-card-actions class="justify-end pr-5 pb-5">
            <v-btn
              @click="nextStep(3)"
            >
              PREVIOUS
            </v-btn>
            <v-btn
              color="primary"
              @click="nextStep(5)"
            >
              NEXT
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-stepper-content>

      <!-- Step 5 -->
      <v-stepper-step
        step="5"
        :rules="stepperRules.step5"
      >
        Generate
        <div v-if="generateStep === 5 && !generateDto.name">
          <v-icon color="red" size="15">
            mdi-alert-circle-outline
          </v-icon>
          <span class="gray--text text-caption">Name은 필수 입력값 입니다.</span>
        </div>
      </v-stepper-step>
      <v-stepper-content step="5">
        <v-card
          outlined
          class="mb-5"
        >
          <v-card-text>
            <v-row>
              <v-col cols="auto">
                <v-card-subtitle class="pa-2 pl-0">Name :</v-card-subtitle>
              </v-col>
              <v-col cols="3">
                <v-form
                  ref="form"
                  v-model="generateDto.valid"
                  lazy-validation
                >
                  <v-text-field
                    label="Versioned Dataset Name"
                    dense
                    :rules="[v => !!v || 'Required.']"
                    v-model="generateDto.name"
                  ></v-text-field>
                </v-form>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-card-subtitle class="pa-2 pl-0">To be generated :</v-card-subtitle>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-card-subtitle>
                  Labeled Data : {{getCounts.labeled}}
                </v-card-subtitle>
                <v-card-subtitle>
                  Train : {{getSplits.train}} / Valid : {{getSplits.valid}} / Test : {{getSplits.test}}
                </v-card-subtitle>
                <v-card-subtitle>
                  Preprocessing : {{activatePreprocessing}}
                </v-card-subtitle>
                <v-card-subtitle>
                  Augmentation : {{activateAugmentation}}
                </v-card-subtitle>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions class="justify-end pr-5 pb-5">
            <v-btn
              @click="nextStep(4)"
            >
              PREVIOUS
            </v-btn>
            <v-btn
              color="primary"
              @click="generateVersionedDataset"
            >
              GENERATE
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-stepper-content>
    </v-stepper>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    generateStep: 1,
    datasets: [],
    bundles: [],
    functions: [],
    splitRange: [30,60],
    generateDto: {
      dataset: null,
      bundles: [],
      preprocessing: [],
      augmentation: [],
      name: '',
      valid: true,
    },
  }),
  computed: {
    stepperRules() {
        return {
          step1: [
            () => ((this.generateStep !== 1) || (this.generateDto.bundles.length > 0) || (this.generateDto.dataset !== null)) || false,
            () => (this.getCounts.labeled !== 0) || false,
          ],
          step2: [
            () => ((this.generateStep !== 2) || (this.getCounts.labeled > 0)) || false,
            //() => ((this.generateStep !== 2) || (this.getSplits.train > 0 && this.getSplits.test > 0 && this.getSplits.valid > 0)) || false,
          ],
          step3: [() => (this.generateStep !== 3) || false],
          step4: [() => (this.generateStep !== 4) || false],
          step5: [
            () => ((this.generateStep !== 5) || (!!this.generateDto.name)) || false,
          ],
        }
    },
    getCounts() {
      const result = {labeled : 0, total: 0};

      if (this.generateDto.dataset !== null && this.generateDto.bundles.length > 0) {
        this.generateDto.bundles.forEach((bundle) => {
          result.labeled += this.bundles.find((r) => r._id === bundle).labeled_data;
          result.total += this.bundles.find((r) => r._id === bundle).total_data;
        });
      }
        
      return result;
    },
    getSplits() {
      const range = this.splitRange;
      //const max = 100;
      const max = this.getCounts.labeled;

      const rtn = {
        train: range[0],
        valid: range[1] - range[0],
        test: max - range[1],
      };
      
      return rtn;
    },
    getDivWidth() {
      //const max = 100;
      const max = this.getCounts.labeled;

      const rtn = {
        train: { width: `${Math.floor((this.getSplits.train / max * 100) * 10) / 10}%` },
        valid: { width: `${Math.floor((this.getSplits.valid / max * 100) * 10) / 10}%`},
        test: { width: `${Math.floor((this.getSplits.test / max * 100) * 10) / 10}%`},
      }
      return rtn;
    },
    getNames() {
      const datasetName = this.datasets.find(r => r._id === this.generateDto.dataset).name;
      const bundleNames = [];
      const bundles = this.generateDto.bundles !== null ? this.generateDto.bundles : [];
      bundles.forEach(bundle_id => {
        console.log(this.bundles.find(r => r._id === bundle_id).name);
        bundleNames.push( this.bundles.find(r => r._id === bundle_id).name );
      });
      return {
        datasetName,
        bundleNames,
      }
    },
    activatePreprocessing() {
      const rtn = [];
      this.generateDto.preprocessing.forEach((r) => {
        if(r.activate === 1) {
          rtn.push(r.name);
        }
      });
      return rtn.length > 0 ? rtn.join(',') : 'NONE';
    },
    activateAugmentation() {
      const rtn = [];
      this.generateDto.augmentation.forEach((r) => {
        if(r.activate === 1) {
          rtn.push(r.name);
        }
      });
      return rtn.length > 0 ? rtn.join(',') : 'NONE';
    },
    getMlTask() {
      return this.datasets.find((r) => r._id === this.generateDto.dataset).ml_task;
    }
  },
  created() {
    this.fetchDatasets();
  },
  methods: {
    fetchDatasets() {
      this.$store.dispatch('FETCH_DATASETS', {})
        .then(res => {
          console.log('VersionedDatasetGenerateView - FETCH_DATASETS - res.datasets', res.datasets);
          this.datasets = res.datasets;
        })
        .catch(error => { console.log(error) });
    },
    fetchBundles() {
      if(this.generateDto.dataset === null) {
        this.bundles = [];
        return;
      }

      this.$store.dispatch('FETCH_BUNDLES', this.generateDto.dataset)
        .then(res => {
          console.log('VersionedDatasetGenerateView - FETCH_DATASETS - res.bundles', res.results);
          this.bundles = res.results;
          this.changeSplitRange();

          if(this.generateDto.dataset !== null) {
            this.fetchFunctions();
          }

        })
        .catch(error => { console.log(error); });  
    },
    fetchFunctions() {
      const mlTask = {...this.datasets.find((r) => r._id === this.generateDto.dataset)}.ml_task;
      this.$store.dispatch('FETCH_FUNCTIONS', {ml_task: mlTask})
        .then(res => {
          res.forEach((r) => {
            const pushObj = {
              function_id: r._id,
              name: r.name,
              params: r.params,
            };
            if (r.type === 0) {
              this.generateDto.preprocessing.push(pushObj);
            } else {
              this.generateDto.augmentation.push(pushObj);
            }
          });
        })
        .catch(error => { console.log(error) });  
    },
    nextStep(step) {
      if (step === 2) {
        const rtn = (this.generateDto.dataset === null && this.generateDto.bundles.length === 0) || this.getCounts.labeled === 0 ? true : false;
        if(rtn) return;
      }
      if (step === 3) {
        if(this.getCounts.labeled === 0) return;
      }
      //텍스트 태깅인경우는 step2로 이동
      if(this.getMlTask === 0 && step === 4) {
        step = 2;
      }

      if(this.getMlTask === 0 && step === 3){
        step = 5;
      }

      this.generateStep = step;
    },
    generateVersionedDataset() {      
      const validateForm = this.$refs.form.validate();
            
      if(validateForm) {
        // CREATE_VERSIONEDDATASET
        const split = [this.getSplits.train,this.getSplits.valid,this.getSplits.test];
        this.generateDto.split = split;
        this.$store.dispatch('CREATE_VERSIONEDDATASET', this.generateDto)
          .then(res => {
            console.log(res);
            this.$router.push({name: 'VersionedDatasetView'});
          })
          .catch(error => { console.log(error) });  
      } 
    },
    changeSplitRange() {
      this.splitRange = [ Math.floor(this.getCounts.labeled * 0.7), Math.floor(this.getCounts.labeled * 0.9) ];  
      
      
    },
  }

}
</script>