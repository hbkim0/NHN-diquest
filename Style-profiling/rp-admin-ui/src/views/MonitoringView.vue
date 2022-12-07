<template>
  <v-container fluid>
    <!-- Serving -->
    <v-card class="mb-5">
      <v-card-title>Serving</v-card-title>
      <v-card-text>
        <template v-for="(staging) in serving.staging">
          <v-card :key="staging._id" class="mb-2" outlined>
            <v-card-text>
              <v-chip
                  color="#ffeaab"
                  text-color="white"
                  label
                  class="mr-5 text-h6"
                >
                  <strong>STAGING</strong>
                </v-chip>
                <strong>{{getExperimentInfo(staging)}}</strong>
            </v-card-text>
          </v-card>
        </template>
        <v-card class="mb-2" outlined v-if="serving.staging.length === 0">
          <v-card-text>
            <v-chip
                color="#ffeaab"
                text-color="white"
                label
                class="mr-5 text-h6"
              >
                <strong>STAGING</strong>
              </v-chip>
              <strong>NONE</strong>
          </v-card-text>
        </v-card>
        <template v-for="(prod) in serving.prod">
          <v-card :key="prod._id" class="mb-2" outlined>
            <v-card-text>
              <v-chip
                  color="#ffceab"
                  text-color="white"
                  label
                  class="mr-5 text-h6"
                >
                  <strong>PROD</strong>
                </v-chip>
                <strong>{{getExperimentInfo(prod)}}</strong>
            </v-card-text>
          </v-card>
        </template>
        <v-card class="mb-2" outlined v-if="serving.prod.length === 0">
          <v-card-text>
            <v-chip
                color="#ffceab"
                text-color="white"
                label
                class="mr-5 text-h6"
              >
                <strong>PROD</strong>
              </v-chip>
              <strong>NONE</strong>
          </v-card-text>
        </v-card>
      </v-card-text>
    </v-card>

    <!-- Experiment results -->
    <v-card>
      <v-card-title>Experiment results</v-card-title>
      <v-container row fluid class="mx-1">
        <v-col cols="2" style="max-width:200px;">
          <v-text-field
            outlined
            clearable
            hide-details
            label="#"
            append-icon="mdi-magnify"
            v-model="filter.selected.seq_num"
            @input="debounceFunc.fetchExperiments"
          >
          </v-text-field>
        </v-col>
        <v-col cols="2" style="max-width:200px;">
          <v-select
            outlined
            clearable
            hide-details
            label="Status"
            :items="filter.status"
            v-model="filter.selected.status"
            @change="debounceFunc.fetchExperiments"
          ></v-select>
        </v-col>
        <v-col cols="2" style="max-width:350px;">
          <v-select
            outlined
            clearable
            hide-details
            label="Model"
            :items="models"
            item-text="name"
            item-value="_id"
            v-model="filter.selected.model_id"
            @change="debounceFunc.fetchExperiments"
          ></v-select>
        </v-col>
        <v-col cols="2" style="max-width:200px;">
          <v-menu
            v-model="filter.picker.show.start"
            :close-on-content-click="false"
            :nudge-right="40"
            transition="scale-transition"
            offset-y
            min-width="auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                outlined
                clearable
                hide-details
                v-model="filter.selected.start"
                label="StartDate"
                prepend-inner-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
                @click:clear="filter.picker.show.start = false;debounceFunc.fetchExperiments();"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="filter.selected.start"
              :max="filter.selected.end"
              @input="filter.picker.show.start = false;debounceFunc.fetchExperiments();"
            ></v-date-picker>
          </v-menu>
        </v-col>
        <v-col cols="auto" class="align-center" style="max-width:50px;">
          <v-card-text class="mx-1 text-h6 pl-0 pr-0">~</v-card-text>
        </v-col>
        <v-col cols="2" style="max-width:200px;">
          <v-menu
            v-model="filter.picker.show.end"
            :close-on-content-click="false"
            :nudge-right="40"
            transition="scale-transition"
            offset-y
            min-width="auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                outlined
                clearable
                hide-details
                v-model="filter.selected.end"
                label="EndDate"
                prepend-inner-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
                @click:clear="filter.picker.show.end = false;debounceFunc.fetchExperiments();"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="filter.selected.end"
              :min="filter.selected.start"
              @input="filter.picker.show.end = false;debounceFunc.fetchExperiments();"
            ></v-date-picker>
          </v-menu>
        </v-col>
      </v-container>
      <v-row class="ma-0 mr-5" justify="end">
        <v-btn
          color="primary"
          large
          @click="dialog.show.serving = true"
        >
          SERVING
        </v-btn>
      </v-row>
      <v-container row fluid class="mx-1">
        <v-col>
          <v-card 
            outlined 
            rounded
            elevation="2"
          >
            <v-simple-table
              fixed-header
            >
              <template v-slot:default>
                <thead>
                  <tr>
                    <th class="text-center text-subtitle-1">
                      <strong>#</strong>
                    </th>
                    <th class="text-center text-subtitle-1">
                      <strong>Status</strong>
                    </th>
                    <th class="text-center text-subtitle-1">
                      <strong>Start time</strong>
                    </th>
                    <th class="text-center text-subtitle-1">
                      <strong>End time</strong>
                    </th>
                    <th class="text-center text-subtitle-1">
                      <strong>Model</strong>
                    </th>
                    <th class="text-center text-subtitle-1">
                      <strong>Hyper-parameters</strong>
                    </th>
                    <th class="text-center text-subtitle-1">
                      <strong>Metric(RMSE)</strong>
                    </th>
                    <th class="text-center text-subtitle-1">
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="experiment in experiments"
                    :key="experiment._id"
                  >
                    <td class="text-center">{{makeSeqNum(experiment.seq_num_major,experiment.seq_num_minor)}}</td>
                    <td class="text-center">{{filter.status.find(r => r.value === experiment.status).text}}</td>
                    <td class="text-center">{{experiment.start_time === null ? '-' : dayjs(experiment.start_time).format('YYYY-MM-DD hh:mm:ss')}}</td>
                    <td class="text-center">{{experiment.end_time === null ? '-' : dayjs(experiment.end_time).format('YYYY-MM-DD hh:mm:ss')}}</td>
                    <td class="text-center">{{typeof(models.find(r => r._id === experiment.model_id)) !== 'undefined' ? models.find(r => r._id === experiment.model_id).name : 'NONE'}}</td>
                    <td class="text-center" v-html="
                      experiment.parameters.map(r => {
                        return `${r.key} : ${r.value}`
                      }).join('<br/>')
                    ">
                    </td>
                    <td class="text-center">{{experiment.rmse}}</td>
                    <td class="text-center">
                      <v-btn
                        v-if="experiment.status === 3 || experiment.status === 4"
                        :disabled="experiment.serving !== 0"
                        icon
                        @click="dialog.show.deleteExperiment = true; dialog.deleteExperiment = experiment;"
                      >
                        <v-icon
                        >
                          mdi-trash-can-outline
                        </v-icon>
                      </v-btn>
                    </td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-card>
        </v-col>
      </v-container>
      <v-row>
        <v-col cols="11">
          <v-pagination
            v-model="pagenation.page"
            :length="pagenation.length"
            :total-visible="10"
            @input="fetchExperiments"
          ></v-pagination>
        </v-col>
        <v-col cols="1" class="pr-10">
          <v-select
            v-model="pagenation.limit"
            :items="[20,50,100]"
            dense
            outlined
            hint="per page"
            persistent-hint
            @change="fetchExperiments"
          ></v-select>
        </v-col>   
      </v-row>
    </v-card>
    
    <!-- dialog -->
    <v-dialog 
      max-width="600" 
      v-model="dialog.show.deleteExperiment"
      persistent
    >
      <v-card class="pb-5">
        <v-card-title>Delete Experiment</v-card-title>
        <v-card-text>
          Experiment #{{dialog.deleteExperiment.seq_num_major}}-{{dialog.deleteExperiment.seq_num_minor}} will be deleted.
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn
            large
            @click="dialog.show.deleteExperiment = false"
          >
            CANCEL
          </v-btn>
          <v-btn
            large
            color="primary"
            @click="deleteExperiment"
          >
            DELETE
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      max-width="800" 
      v-model="dialog.show.serving"
      persistent
    >
      <v-card>
        <v-card-title>Serving</v-card-title>
        <v-card-text>
          <template v-for="(staging) in serving.staging">
            <v-card :key="staging._id" class="mb-2" outlined>
              <v-card-text>
                <v-chip
                    color="#ffeaab"
                    text-color="white"
                    label
                    class="mr-5 text-h6"
                  >
                    <strong>STAGING</strong>
                  </v-chip>
                  <strong>{{getExperimentInfo(staging, 'dialog')}}</strong>
              </v-card-text>
            </v-card>
          </template>
          <v-card v-if="serving.staging.length === 0" class="mb-2" outlined>
            <v-card-text>
              <v-chip
                  color="#ffeaab"
                  text-color="white"
                  label
                  class="mr-5 text-h6"
                >
                  <strong>STAGING</strong>
                </v-chip>
                <strong>NONE</strong>
            </v-card-text>
          </v-card>
          <template v-for="(prod) in serving.prod">
            <v-card :key="prod._id" class="mb-2" outlined>
              <v-card-text>
                <v-chip
                  color="#ffceab"
                  text-color="white"
                  label
                  class="mr-5 text-h6"
                >
                  <strong>PROD</strong>
                </v-chip>
                <strong>{{getExperimentInfo(prod, 'dialog')}}</strong>
              </v-card-text>
            </v-card>
          </template>
          <v-card v-if="serving.prod.length === 0" class="mb-2" outlined>
            <v-card-text>
              <v-chip
                color="#ffceab"
                text-color="white"
                label
                class="mr-5 text-h6"
              >
                <strong>PROD</strong>
              </v-chip>
              <strong>NONE</strong>
            </v-card-text>
          </v-card>
        </v-card-text>
        <v-card-text>
          <v-card>
            <v-row>
              <v-col cols="auto">
                <v-select
                  class="mx-3"
                  outlined
                  dense
                  label="Seq Major"
                  :items="dialog.select.seq_num_major"
                  prefix="# : "
                  item-text="seq_num_major"
                  item-value="seq_num_major"
                  v-model="dialog.selected.seq_num_major"
                  @change="dialog.selected.experiment = null;fetchDialogExperiments();"
                >
                </v-select>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-card 
                  class="mx-3"
                  outlined
                >
                  <v-simple-table
                    fixed-header
                    dense
                  >
                    <template v-slot:default>
                      <thead>
                        <tr>
                          <th width="50" class="text-center text-subtitle-1">
                          </th>
                          <th class="text-center text-subtitle-1">
                            <strong>#</strong>
                          </th>
                          <th class="text-center text-subtitle-1">
                            <strong>Model</strong>
                          </th>
                          <th class="text-center text-subtitle-1">
                            <strong>Hyper-parameters</strong>
                          </th>
                          <th class="text-center text-subtitle-1">
                            <strong>Metric(RMSE)</strong>
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="experiment in dialog.experiments"
                          :key="experiment._id"
                        >
                          <td class="text-center">
                            <v-radio-group
                              v-model="dialog.selected.experiment"
                              column
                              :disabled="experiment.serving === 2"
                            >
                              <v-radio
                                :value="experiment"
                              >
                              </v-radio>
                            </v-radio-group>
                          </td>
                          <td class="text-center">{{experiment.seq_num_major}}-{{experiment.seq_num_minor}}</td>
                          <td class="text-center">{{typeof(models.find(r => r._id === experiment.model_id)) !== 'undefined' ? models.find(r => r._id === experiment.model_id).name : 'NONE'}}</td>
                          <td class="text-center" v-html="
                            experiment.parameters.map(r => {
                              return `${r.key} : ${r.value}`
                            }).join('<br/>')
                          ">
                          </td>
                          <td class="text-center">{{experiment.rmse}}</td>
                        </tr>
                      </tbody>
                    </template>
                  </v-simple-table>
                </v-card>
              </v-col>
              
            </v-row>
          </v-card>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn
            large
            @click="dialog.show.serving = false; dialog.selected.experiment = null;"
          >
            CANCEL
          </v-btn>
          <v-btn
            large
            color="primary"
            @click="registerProd"
            :disabled="dialog.selected.experiment === null"
          >
            REGISTER PROD
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import debounce from 'lodash/debounce';
export default {
  data: () => ({
    experiments: [],
    models: [],
    serving: {
      staging: [],
      prod: [],
    },
    dialog: {
      show: {
        deleteExperiment: false,
        serving: false,
      },
      deleteExperiment: {},
      experiments: [],
      select: {
        seq_num_major: [],
      },
      selected: {
        experiment: null,
        seq_num_major: null,
      }
    },
    pagenation: {
      page : 1,
      length : 0,
      limit: 20,
    },
    filter: {
      status: [
        { text: 'created', value: 0 },
        { text: 'queued', value: 1 },
        { text: 'training', value: 2 },
        { text: 'done', value: 3 },
        { text: 'failed', value: 4 },
      ],
      picker: {
        show : {
          start: false,
          end: false,
        }
      },
      selected: {
        seq_num: null,
        seq_num_major: null,
        seq_num_minor: null,
        status: null,
        model_id: null,
        start: null,
        end: null,
      }
    },
    debounceFunc: {
      fetchExperiments: null,
    },
  }),
  watch: {
    'filter.selected.seq_num': 'seqToMajorMinor',
  },
  computed: {
    
  },
  created() {
    this.debounceFunc.fetchExperiments = debounce(this.fetchExperiments, 2000);

    this.fetchModels();
    this.fetchAllExperiments();
  },
  methods: {
    fetchExperiments() {
      const params = {...this.filter.selected, ...this.pagenation};
      this.$store.dispatch('FETCH_EXPERIMENTS', params)
        .then(res => {
          console.log('View - fetchExperiments - res', res);
          this.experiments = res.experiments;
          this.pagenation = res.pagenation;
  
        })
        .catch(error => { console.log(error) });
    },
    fetchAllExperiments() {
      this.$store.dispatch('FETCH_EXPERIMENTS', {status:3})
        .then(res => {
          const seq_num_major_arr = res.experiments.map(r => {
            return r.seq_num_major;
          });
          this.dialog.select.seq_num_major = [...new Set(seq_num_major_arr)].sort();

          this.serving.staging = res.experiments.filter(r => r.serving === 1);
          this.serving.prod = res.experiments.filter(r => r.serving === 2);

          //다이얼로그 기본 세팅. - Staging
          const staging = res.experiments.filter(r => r.serving === 1);
          this.dialog.selected.seq_num_major = typeof(staging[0]) !== 'undefined' ? staging[0].seq_num_major : null;
          this.fetchDialogExperiments();
        })
        .catch(error => { console.log(error) });
    },
    fetchDialogExperiments() {
      if(this.dialog.selected.seq_num_major === null) {
        this.dialog.experiments = [];
        return;
      }
      const params = {
        seq_num_major: this.dialog.selected.seq_num_major,
        status: 3,
      };
      this.$store.dispatch('FETCH_EXPERIMENTS', params)
        .then(res => {
          console.log('View - fetchDialogExperiments - res', res);
          this.dialog.experiments = res.experiments;
        })
        .catch(error => { console.log(error) });
    },
    deleteExperiment() {
      const params = {
        experiment_id: this.dialog.deleteExperiment._id,
      };
      this.$store.dispatch('DELETE_EXPERIMENT', params)
        .then(res => {
          console.log('View - deleteExperiment - res', res);
          this.dialog.show.deleteExperiment = false;
          this.dialog.deleteExperiment = {};
          this.fetchExperiments();
        })
        .catch(error => { console.log(error) });
    },
    fetchModels() {
      this.$store.dispatch('FETCH_MODELS')
        .then(res => {
          this.models = res;
          this.fetchExperiments();
        })
        .catch(error => { console.log(error) });
    },
    seqToMajorMinor() {
      const seq_num = this.filter.selected.seq_num;
      if (!seq_num) {
        this.filter.selected.seq_num_major = null;
        this.filter.selected.seq_num_minor = null;
      } else {
        const major = seq_num.replace(/ /g, '').split('-')[0];
        const minor = seq_num.replace(/ /g, '').split('-')[1];
        this.filter.selected.seq_num_major = isNaN(parseInt(major)) ? null : parseInt(major);
        this.filter.selected.seq_num_minor = isNaN(parseInt(minor)) ? null : parseInt(minor);
      }

    },
    getExperimentInfo(experiment, target) {
      const seq_num = `${experiment.seq_num_major}-${experiment.seq_num_minor}`;
      const model_name = typeof(this.models.find(r => r._id === experiment.model_id)) !== 'undefined' ? this.models.find(r => r._id === experiment.model_id).name : 'NONE';
      const start_time = experiment.start_time;
      const rmse = experiment.rmse;
      const rtn = (target === 'dialog') ? `(#${seq_num}) ${model_name} metric: ${rmse}` : `(#${seq_num}) ${model_name} start time ${this.dayjs(start_time).format('YYYY-MM-DD')} metric: ${rmse}`;
      return typeof(experiment) !== 'undefined' ? rtn : 'NONE';
    },
    registerProd() {
      const params = {
        experiment_id: this.dialog.selected.experiment._id,
        parameters: this.dialog.selected.experiment.parameters,
        serving: 2,
      };
      this.$store.dispatch('PATCH_EXPERIMENT_MONITORING', params)
        .then(res => {
          this.fetchExperiments();
          this.fetchAllExperiments();
          this.dialog.show.serving = false;
        })
        .catch(error => { console.log(error) });


    },
    makeSeqNum(major, minor) {
      return `${major !== null ? major : ''}${(major !== null && minor !== null) ? `-${minor}` : ''}`
    }

  }
}
</script>