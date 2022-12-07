<template>
  <v-card class="pb-5">
    <v-card-title><strong>Scheduled Experiments</strong></v-card-title>
    <v-card-subtitle>Next training time: {{dayjs(nextSchedule).format('YYYY-MM-DD hh:mm dddd')}}</v-card-subtitle>
    <v-card-actions class="justify-end">
      <v-btn
        large
        color="primary"
        @click="dialog.show.schedule = true"
      >
        CHANGE SCHEDULE
      </v-btn>
      <v-btn
        large
        color="primary"
        @click="dialog.show.train = true"
        :disabled="experiments.length === 0"
      >
        TRAINING NOW
      </v-btn>
    </v-card-actions>

    <template v-for="model in models">
      <v-card class="ma-5 pb-5 rounded-lg" :key="model._id">
        <v-card-title><strong>{{model.name}}</strong></v-card-title>
        <v-card-text class="pb-0">
          <v-container class="ma-0 pa-0" row fluid>
            <v-col>
              {{model.description}}
            </v-col>
            <v-col class="text-right">
              <v-btn
                icon
                @click="openExperimentDialog(model._id)"
              >
                <v-icon>
                  mdi-plus
                </v-icon>
              </v-btn>
            </v-col>
          </v-container>
        </v-card-text>
        
        <v-card class="ma-5">
          <v-simple-table
            fixed-header
          >
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-center text-subtitle-1" style="width:10%;">
                  </th>
                  <th class="text-center text-subtitle-1" v-for="(parameter, index) in model.parameters" :key="index"  style="width:20%;">
                    <strong>{{parameter.name}}</strong>
                  </th>
                  <th class="text-center text-subtitle-1" style="width:10%;">
                    <strong>#</strong>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(experiment, index) in experiments.filter(r => r.model_id === model._id)"
                  :key="experiment._id"
                >
                  <td class="text-center">{{ index+1 }}</td>
                  <td class="text-center" v-for="(parameter, index) in model.parameters" :key="index">
                    {{ {...experiment.parameters.find(r => r.key === parameter.name)}.value }}
                  </td>
                  <td class="text-center">
                    <v-btn
                      icon
                      @click="openExperimentDialog(model._id, experiment._id, experiment.serving)"
                    >
                      <v-icon>
                        mdi-clipboard-edit-outline
                      </v-icon>
                    </v-btn>

                    <v-btn
                      icon
                      @click="dialog.show.deleteExperiment = true; dialog.deleteExperiment = experiment;"
                    >
                      <v-icon>
                        mdi-trash-can-outline
                      </v-icon>
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card>
      </v-card>
    </template>

    <!-- dialog -->
    <v-dialog 
      max-width="600" 
      v-model="dialog.show.deleteExperiment"
      persistent
    >
      <v-card class="pb-5">
        <v-card-title>Delete Experiment</v-card-title>
        <v-card-text>
          Are you sure you want to delete that experiment?
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
      max-width="600" 
      v-model="dialog.show.schedule"
      persistent
    >
      <v-card class="pb-5">
        <v-card-title><strong>Change Schedule</strong></v-card-title>
        <v-container class="pa-0 ma-0 justify-center" row fluid>
          <v-card>
            <v-simple-table>
              <template v-slot:default>
                <thead>
                  <tr>
                    <th width="80" class="text-center" v-for="day in weekly" :key="day">
                      <strong>{{day.toUpperCase()}}</strong>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td
                      v-for="(day,index) in dialog.schedule.days"
                      :key="index"
                      class="text-center"
                    >
                      <v-checkbox
                        class="d-inline-flex"
                        v-model="dialog.schedule.days[index]"
                        :true-value="weekly[index]"
                        :false-value="0"
                      >
                      </v-checkbox>
                    </td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-card>
        </v-container>
        <v-container class="pa-0 ma-0" row fluid>
          <v-col cols="auto">
            <v-card-title><strong>Start Time</strong> : </v-card-title>
          </v-col>
          <v-col cols="auto">
            <v-menu
              v-model="dialog.show.timePicker"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  outlined
                  hide-details
                  v-model="dialog.schedule.time"
                  label="hh:mm"
                  prepend-inner-icon="mdi-timer-outline"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-time-picker
                format="24hr"
                v-model="dialog.schedule.time"
                @change="dialog.show.timePicker = false"
              ></v-time-picker>
            </v-menu>
          </v-col>
        </v-container>
        <v-card-actions class="justify-end">
          <v-btn
            large
            @click="dialog.show.schedule = false"
          >
           CANCEL
          </v-btn>
          <v-btn
            large
            color="primary"
            @click="saveSchedule"
          >
           SAVE
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog 
      max-width="600" 
      v-model="dialog.show.train"
      persistent
    >
      <v-card class="pb-5">
        <v-card-title><strong>Training now</strong></v-card-title>
        <v-card-text>All experiments on the list are scheduled immediately.</v-card-text>
        <v-card-actions class="justify-end">
          <v-btn
            large
            @click="dialog.show.train = false"
          >
           CANCEL
          </v-btn>
          <v-btn
            large
            color="primary"
            @click="trainNow"
          >
           TRAIN
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog 
      max-width="600" 
      v-model="dialog.show.experiment"
      persistent
    >
      <v-card class="pb-5">
        <v-card-title><strong>Add Experiment({{ {...models.find(r => r._id === dialog.experiment.model_id)}.name }})</strong></v-card-title>
        <v-card-text>
          <v-form
            ref="form"
            lazy-validation
          >
            <template v-for="(parameter, index) in {...models.find(r => r._id === dialog.experiment.model_id)}.parameters">
              <v-row align="center" :key="index">
                <v-col cols="auto">
                  <v-card-subtitle class="pa-0">{{parameter.name}} :</v-card-subtitle>
                </v-col>
                <v-col cols="auto">
                  <v-text-field
                    dense
                    type="number"
                    :rules="dialog.rules[parameter.type]"
                    :step="dialog.step[parameter.type]"
                    v-model.number="dialog.experiment.parameters[parameter.name]"
                  ></v-text-field>
                </v-col>
                <v-col cols="auto">
                  <v-card-subtitle  class="pa-0">({{parameter.type}})</v-card-subtitle>
                </v-col>
              </v-row>
            </template>
          </v-form>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn
            large
            @click="closeExperimentDialog"
          >
           CANCEL
          </v-btn>
          <v-btn
            v-if="typeof(dialog.experiment.experiment_id) === 'undefined'"
            large
            color="primary"
            @click="createExperiment"
          >
           ADD
          </v-btn>
          <v-btn
            v-else
            large
            color="primary"
            @click="updateExperiment"
          >
           UPDATE
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    experiments: [],
    models: [],
    nextSchedule : null,
    weekly: ['sun','mon','tue','wed','thu','fri','sat'],
    dialog: {
      show: {
        schedule: false,
        timePicker: false,
        train: false,
        experiment: false,
        deleteExperiment: false,
      },
      schedule: {
        schedule_id: null,
        days: [0, 0, 0, 0, 0, 0, 0],
        time: null,
      },
      experiment: {
        model_id: null,
        experiment_id: null,
        parameters: {},
        serving: null,
      },
      deleteExperiment: {},
      rules: {
        integer: [(v) => !!v || 'required', (v) => v > 0 || 'value must be greater than 0', (v) => (typeof(v) === 'number' && Number.isInteger(v)) || 'type error'],
        double: [(v) => !!v || 'required', (v) => v > 0 || 'value must be greater than 0', (v) => (typeof(v) === 'number' && !Number.isInteger(v)) || 'type error'],
      },
      step: {
        integer: 1,
        double: 0.0001,
      },
    }
  }),
  created() {
    this.fetchModels();
    this.fetchSchedule();
  },
  methods: {
    initDialogExperiment() {
      this.dialog.experiment = {
        model_id: null,
        experiment_id: null,
        parameters: {},
        serving: null,
      };
    },
    fetchExperiments() {
      //FETCH_EXPERIMENTS
      this.$store.dispatch('FETCH_EXPERIMENTS', { status: 0 })
        .then(res => {
          console.log('View - fetchExperiments - res', res);
          this.experiments = res.experiments;
        })
        .catch(error => { console.log(error) });
    },
    fetchSchedule() {
      //FETCH_SCHEDULE
      this.$store.dispatch('FETCH_SCHEDULES')
        .then(res => {
          console.log('View - fetchSchedule - res', res);
          this.dialog.schedule.schedule_id = res._id;
          this.setCronToTime(res.cron);     
        })
        .catch(error => { console.log(error) });
    },
    fetchModels() {
      //FETCH_MODLES
      this.$store.dispatch('FETCH_MODELS')
        .then(res => {
          console.log(res);
          this.models = res;
          this.fetchExperiments();
        })
        .catch(error => { console.log(error) });
    },
    getCronTime() {
      const minute = this.dialog.schedule.time.split(':')[1];
      const hour = this.dialog.schedule.time.split(':')[0];
      const daysOfTheWeek = this.weekly.filter(r => this.dialog.schedule.days.includes(r)).join(',');      
      const rtn = `${minute} ${hour} * * ${daysOfTheWeek} *`;
      return rtn;
    },
    setCronToTime(cron) {
      const cronArray = cron.split(' ');
      this.dialog.schedule.time = ((cronArray[1] === '*') || (cronArray[0] === '*')) ? null : `${cronArray[1]}:${cronArray[0]}`;
      const days = cronArray[4] !== '*' ? cronArray[4].split(',') : this.weekly.join(',');
      this.dialog.schedule.days = this.weekly.map((r) => { 
        if (days.includes(r)) {
          return r;
        } else {
          return 0;
        }
      });
      
      //cron에서 다음 스케줄 날짜 확인
      const parser = require('cron-parser');
      this.nextSchedule = parser.parseExpression(`* ${cron.split(' ').slice(0, -1).join(' ')}`).next().toString();
    },
    openExperimentDialog(model_id, experiment_id, serving) {
      this.dialog.show.experiment = true;
      this.dialog.experiment.model_id = model_id;
      this.dialog.experiment.experiment_id = experiment_id;
      this.dialog.experiment.serving = serving;
      //this.experiments.find(r => r._id === experiment_id).parameters;
      
      if (typeof(experiment_id) !== 'undefined') {
        const parameters = {...this.experiments.find(r => r._id === experiment_id)}.parameters.map(r => {
          return [r.key,r.value];
        });
        this.dialog.experiment.parameters = {...Object.fromEntries(parameters)};
      }
    },
    closeExperimentDialog(){
      this.dialog.show.experiment = false;
      this.initDialogExperiment();
    },
    saveSchedule() {
      const cronTime = this.getCronTime();
      const params = {
        cron: cronTime,
      }
      //PATCH_SCHEDULE
      this.$store.dispatch('PATCH_SCHEDULE', params)
        .then(res => {
          console.log('View - PATCH_SCHEDULE - res', res);
          this.dialog.show.schedule = false;
          this.setCronToTime(res.cron);
        })
        .catch(error => { console.log(error) });
    },
    createExperiment() {
      const validateForm = this.$refs.form.validate();
    
      if(validateForm) {
        //성공
        this.$store.dispatch('CREATE_EXPERIMENT', this.dialog.experiment)
          .then(res => {
            console.log('View - CREATE_EXPERIMENT - res', res);
            this.fetchExperiments();
            this.dialog.show.experiment = false;
            this.initDialogExperiment();
          })
          .catch(error => { console.log(error) });
      }
    },
    updateExperiment() {
      const validateForm = this.$refs.form.validate();
    
      if(validateForm) {
        //성공
        this.$store.dispatch('PATCH_EXPERIMENT', this.dialog.experiment)
          .then(res => {
            console.log('View - PATCH_EXPERIMENT - res', res);
            this.fetchExperiments();
            this.dialog.show.experiment = false;
            this.initDialogExperiment();
          })
          .catch(error => { console.log(error) });
      }
    },
    trainNow() {
      const params = {
        cron: '*/5 * * * * *',
        priority: 0
      }
      this.$store.dispatch('CREATE_SCHEDULE', params)
        .then(res => {
          console.log('View - CREATE_SCHEDULE - res', res);
          this.dialog.show.train = false;
          this.$router.push({name: 'MonitoringView'})
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
    
  }
}
</script>
