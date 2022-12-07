export default {
    'GET /api/v1/datasets': (req,res) => {
        return res.json({
            "offset" : 0,
            "limit" : 10,
            "sort_by" : "",
            "filtering" : "",
            "total_results" : 18,
            "results" : [
                {
                    "_id": "0",
                    "mlTask": "IMAGE DEEP TAGGING",
                    "coverImage": "../assets/logo.png",
                    "name": "K-Fashion",
                    "description": "패션 영역과 속성, 스타일 정보를 인식 및 도출을 위한 학습용 데이터 셋",
                    "labeled": 1,
                    "total": 58
                },
                {
                    "_id": "1",
                    "mlTask": "TEXT DEEP TAGGING",
                    "coverImage": "",
                    "name": "쇼핑몰 상품 정보",
                    "description": "패션 영역과 속성, 스타일 정보를 인식 및 도출을 위한 학습용 데이터 셋",
                    "labeled": 2,
                    "total": 58
                },
                {
                    "_id": "2",
                    "mlTask": "VIRTUAL TRY-ON",
                    "coverImage": "",
                    "name": "패션 상품 및 착용 이미지",
                    "description": "패션 영역과 속성, 스타일 정보를 인식 및 도출을 위한 학습용 데이터 셋",
                    "labeled": 3,
                    "total": 58
                },
                {
                    "_id": "3",
                    "mlTask": "IMAGE DEEP TAGGING",
                    "coverImage": "../assets/logo.png",
                    "name": "K-Fashion",
                    "description": "패션 영역과 속성, 스타일 정보를 인식 및 도출을 위한 학습용 데이터 셋",
                    "labeled": 4,
                    "total": 58
                },
                {
                    "_id": "4",
                    "mlTask": "TEXT DEEP TAGGING",
                    "coverImage": "",
                    "name": "쇼핑몰 상품 정보",
                    "description": "패션 영역과 속성, 스타일 정보를 인식 및 도출을 위한 학습용 데이터 셋",
                    "labeled": 5,
                    "total": 58
                },
                {
                    "_id": "5",
                    "mlTask": "VIRTUAL TRY-ON",
                    "coverImage": "",
                    "name": "패션 상품 및 착용 이미지",
                    "description": "패션 영역과 속성, 스타일 정보를 인식 및 도출을 위한 학습용 데이터 셋",
                    "labeled": 6,
                    "total": 58
                },
                {
                    "_id": "6",
                    "mlTask": "IMAGE DEEP TAGGING",
                    "coverImage": "../assets/logo.png",
                    "name": "K-Fashion",
                    "description": "패션 영역과 속성, 스타일 정보를 인식 및 도출을 위한 학습용 데이터 셋",
                    "labeled": 7,
                    "total": 58
                },
                {
                    "_id": "7",
                    "mlTask": "TEXT DEEP TAGGING",
                    "coverImage": "",
                    "name": "쇼핑몰 상품 정보",
                    "description": "패션 영역과 속성, 스타일 정보를 인식 및 도출을 위한 학습용 데이터 셋",
                    "labeled": 8,
                    "total": 58
                },
                {
                    "_id": "8",
                    "mlTask": "VIRTUAL TRY-ON",
                    "coverImage": "",
                    "name": "패션 상품 및 착용 이미지",
                    "description": "패션 영역과 속성, 스타일 정보를 인식 및 도출을 위한 학습용 데이터 셋",
                    "labeled": 9,
                    "total": 58
                }
            ]
        })
    },

    'POST /api/v1/dataset': (req,res) => {
        return res.json({
            "_id": "abc",
            "name": "name",
            "description": "description",
            "ml_task": 1,
            "cover_image": "image/path",
            "labeled_data": 0,
            "total_data": 0,
            "history": {},
            "ext": {},
            "reg_date": "reg_date",
            "reg_id": "reg_id",
            "mod_date": "mod_date",
            "mod_id": "mod_id"
          })
    },

    'GET /api/v1/datasets/:dataset_id': (req,res) => {
        return res.json({
            "_id": "0",
            "name": "detail name",
            "description": "detail description",
            "ml_task": 1,
            "cover_image": "detail image/path",
            "labeled_data": 0,
            "total_data": 0,
            "history": {},
            "ext": {},
            "reg_date": "reg_date",
            "reg_id": "reg_id",
            "mod_date": "mod_date",
            "mod_id": "mod_id"
          })
    },

    'PATCH /api/v1/datasets/:_id': (req,res) => {
        return res.json({
            "_id": "0",
            "name": "detail name - mod",
            "description": "detail description - mod",
            "ml_task": 1,
            "cover_image": "detail image/path  - mod",
            "labeled_data": 0,
            "total_data": 0,
            "history": {},
            "ext": {},
            "reg_date": "reg_date",
            "reg_id": "reg_id",
            "mod_date": "mod_date",
            "mod_id": "mod_id"
          })
    },

    'DELETE /api/v1/datasets/:dataset_id': (req,res) => {
        return res.json()
    },

    'GET /api/v1/bundles': (req,res) => {
        return res.json([
            {
                _id: 'a',
                name: '레트로',
                description: '레트로 설명',
                attributes: '속성들',
                data: '###',
                complete_rate: '20%',
            },
            {
                _id: 'b',
                name: '로맨틱',
                description: '로맨틱 설명',
                attributes: '속성들',
                data: '###',
                complete_rate: '50%',
            },
            {
                _id: 'c',
                name: '레트로',
                description: '레트로 설명',
                attributes: '속성들',
                data: '###',
                complete_rate: '20%',
            },
            {
                _id: 'd',
                name: '로맨틱',
                description: '로맨틱 설명',
                attributes: '속성들',
                data: '###',
                complete_rate: '50%',
            },
            {
                _id: 'e',
                name: '레트로',
                description: '레트로 설명',
                attributes: '속성들',
                data: '###',
                complete_rate: '20%',
            },
            {
                _id: 'f',
                name: '로맨틱',
                description: '로맨틱 설명',
                attributes: '속성들',
                data: '###',
                complete_rate: '50%',
            },
            {
                _id: 'g',
                name: '레트로',
                description: '레트로 설명',
                attributes: '속성들',
                data: '###',
                complete_rate: '20%',
            },
            {
                _id: 'h',
                name: '로맨틱',
                description: '로맨틱 설명',
                attributes: '속성들',
                data: '###',
                complete_rate: '50%',
            }
        ])
    },

    'GET /api/v1/bundles/:bundle_id': (req, res) => {
        return res.json({
            _id: 'abc',
            name: '레트로',
            description: '레트로 설명',
            attributes: [
              { key: '스타일', value: '레트로' },
              { key: '색상', value: '노랑' }
            ],
            data: '###',
            complete_rate: '20%',
        })
    },

    'PATCH /api/v1/bundles/:bundle_id': (req, res) => {
        return res.json({
            _id: 'abc',
            name: '레트로',
            description: '레트로 설명',
            attributes: [
              { key: '스타일', value: '레트로' },
              { key: '색상', value: '노랑' }
            ],
            data: '###',
            complete_rate: '20%',
        })
    },

    'POST /api/v1/bundle': (req,res) => {
        return res.json({
            "_id": "bundle test id",
            "name": "bundle name",
            "description": "bundle description"
          })
    },

    'DELETE /api/v1/bundles/:bundle_id': (req,res) => {
        return res.json()
    },

    'GET /api/v1/annotations': (req,res) => {

        return res.json({
            "offset" : 0,
            "limit" : 10,
            "sort_by" : "",
            "filtering" : "",
            "total_results" : 18,
            "results" : [
                {
                    "_id": "0",
                    "ml_task": 1,
                    "file_name": "file_name1",
                    "file_url": "/media/208881110.jpg",
                    "done": 0,
                    "labels": [
                        {
                            "bbox": [70, 70, 100, 100],
                            "label": "레이블입니다",
                            "attributes": [
                                {
                                    "key": "key1",
                                    "value": "value1"
                                },
                                {
                                    "key": "키",
                                    "value": "값"
                                }
                            ]
                        }
                    ],
                    "label_info": [
                        {
                            
                        }
                    ],
                    
                },
                {
                    "_id": "1",
                    "ml_task": 0,
                    "file_name": "file_name2",
                    "file_url": "/media/테스트.txt",
                    "done": 0,
                    "labels": [],
                    "label_info": [
                        {
                            "name": "name2",
                            "color": "color2"
                        }
                    ],
                }
            ]
        })
    },

    'GET /api/v1/annotations/:annotation_id': (req,res) => {

        return res.json(
            {
                "_id": "0",
                "ml_task": 1,
                "file_name": "file_name1",
                "file_url": "file_url1",
                "done": 0,
                "labels": [
                    {
                        "bbox": [70, 70, 100, 100],
                        "label": "레이블입니다",
                        "attributes": [
                            {
                                "key": "key1",
                                "value": "value1"
                            },
                            {
                                "key": "키",
                                "value": "값"
                            }
                        ]
                    }
                ],
                "label_info": [
                    {
                        
                    }
                ],
                
            }
        )
    },

    'GET /api/v1/experiments' : (req,res) => {
        return res.json(
            {
                "offset": 0,
                "limit": 10,
                "sort_by": "string",
                "filtering": "string",
                "total_results": 2,
                "results": [
                  {
                    "_id": "id1",
                    "name": "Experiment Test",
                    "description": "string",
                    "ml_task": 0,
                    "dataset_name": "데이터셋 이름",
                    "versioned_dataset_name": "버전 데이터셋 이름",
                    "index": 0,
                    "dataset_id": "string",
                    "model_name": "모델 이름",
                    "algorithms": [
                      {
                        "name": "model1",
                        "training_params": [
                          {
                            "name": "string",
                            "type": "string",
                            "argument": "string",
                            "default": "string"
                          }
                        ],
                        "performance_metrics": [
                          {
                            "name": "string",
                            "type": "string",
                            "value": "string"
                          }
                        ]
                      },
                      {
                        "name": "model2",
                        "training_params": [
                          {
                            "name": "string",
                            "type": "string",
                            "argument": "string",
                            "default": "string"
                          }
                        ],
                        "performance_metrics": [
                          {
                            "name": "string",
                            "type": "string",
                            "value": "string"
                          }
                        ]
                      }
                    ],
                    "gen_date": "2022-10-31T04:27:53.420Z",
                    "status": 2,
                    "history": {},
                    "ext": {},
                    "reg_date": "2022-10-31T04:27:53.420Z",
                    "reg_id": "string",
                    "mod_date": "2022-10-31T04:27:53.420Z",
                    "mod_id": "string"
                  },
                  {
                    "_id": "id2",
                    "name": "Experiment Test2",
                    "description": "string",
                    "ml_task": 0,
                    "dataset_name": "데이터셋 이름",
                    "versioned_dataset_name": "버전 데이터셋 이름",
                    "index": 0,
                    "dataset_id": "string",
                    "model_name": "모델 이름",
                    "algorithms": [
                      {
                        "name": "model1",
                        "training_params": [
                          {
                            "name": "string",
                            "type": "string",
                            "argument": "string",
                            "default": "string"
                          }
                        ],
                        "performance_metrics": [
                          {
                            "name": "string",
                            "type": "string",
                            "value": "string"
                          }
                        ]
                      },
                      {
                        "name": "model2",
                        "training_params": [
                          {
                            "name": "string",
                            "type": "string",
                            "argument": "string",
                            "default": "string"
                          }
                        ],
                        "performance_metrics": [
                          {
                            "name": "string",
                            "type": "string",
                            "value": "string"
                          }
                        ]
                      }
                    ],
                    "gen_date": "2022-10-31T04:27:53.420Z",
                    "status": 0,
                    "history": {},
                    "ext": {},
                    "reg_date": "2022-10-31T04:27:53.420Z",
                    "reg_id": "string",
                    "mod_date": "2022-10-31T04:27:53.420Z",
                    "mod_id": "string"
                  }
                ]
              }
          )
    }, 

    'GET /api/v1/models' : (req,res) => {
        return res.json(
            {
                "limit": 20,
                "offset": 0,
                "sort_by": "",
                "filtering": "",
                "total_results": 2,
                "results": [
                  {
                    "_id": "6360b87adceea6a52047cbb0",
                    "algorithms": [],
                    "history": {},
                    "ext": {},
                    "name": "KoELECTRA-Base",
                    "description": "",
                    "ml_task": 0,
                    "reg_date": "2022-10-24T06:06:36.630000Z",
                    "reg_id": "user_id",
                    "mod_date": "2022-10-24T06:40:50.688000Z",
                    "mod_id": "user_id"
                  },
                  {
                    "_id": "6360b7f9dceea6a52047cbaf",
                    "algorithms": [
                      {
                        "name": "YOLOv5(medium)",
                        "image_name": "mlp/yolov5:latest",
                        "training_params": [
                          {
                            "name": "epoch",
                            "type": "integer",
                            "default": "300"
                          },
                          {
                            "name": "batch_size",
                            "type": "integer",
                            "default": "16"
                          },
                          {}
                        ],
                        "performance_metrics": [
                          {
                            "name": "precision",
                            "type": "double"
                          },
                          {
                            "name": "recall",
                            "type": "double"
                          },
                          {
                            "name": "mAP_0.5",
                            "type": "double"
                          },
                          {
                            "name": "mAP_0.5:0.95",
                            "type": "double"
                          }
                        ]
                      },
                      {
                        "name": "classifier(resnet50)",
                        "image_name": "mlp/image-cls:lastest",
                        "training_params": [
                          {
                            "name": "epoch",
                            "type": "integer",
                            "default": "2"
                          },
                          {
                            "name": "batch_size",
                            "type": "integer",
                            "default": "16"
                          },
                          {}
                        ],
                        "performance_metrics": [
                          {
                            "name": "accuracy",
                            "type": "double"
                          }
                        ]
                      }
                    ],
                    "history": {},
                    "ext": {},
                    "name": "YOLOv5n + Image Classification",
                    "description": "",
                    "ml_task": 1,
                    "reg_date": "2022-10-24T06:06:36.630000Z",
                    "reg_id": "user_id",
                    "mod_date": "2022-10-24T06:40:50.688000Z",
                    "mod_id": "user_id"
                  }
                ]
              }
        )
    },

    'POST /api/v1/experiments': (req,res) => {
        return res.json({
            "_id": "q1w2e3",
            "name": "string",
            "description": "string",
            "ml_task": 0,
            "dataset_name": "string",
            "versioned_dataset_name": "버전 데이터셋 이름",
            "index": 0,
            "dataset_id": "string",
            "model_name": "string",
            "algorithms": [
              {
                "name": "string",
                "training_params": [
                  {
                    "name": "string",
                    "type": "string",
                    "argument": "string",
                    "default": "string"
                  }
                ],
                "performance_metrics": [
                  {
                    "name": "string",
                    "type": "string",
                    "value": "string"
                  }
                ]
              }
            ],
            "gen_date": "2022-10-31T06:59:27.417Z",
            "status": 0,
            "history": {},
            "ext": {},
            "reg_date": "2022-10-31T06:59:27.417Z",
            "reg_id": "string",
            "mod_date": "2022-10-31T06:59:27.417Z",
            "mod_id": "string"
          })
    },

    'GET /api/v1/experiments/:experiment_id' : (req,res) => {
        return res.json(
            {
                "_id": "id2",
                "name": "Exp_TEST",
                "description": "string",
                "ml_task": 0,
                "dataset_name": "K-Fashion",
                "versioned_dataset_name": "Augmented",
                "versioned_dataset_id": "6356393f1665e43606cebf01",
                "index": 0,
                "dataset_id": "string",
                "model_name": "YOLOv5m + Image Classification",
                "algorithms": [
                  {
                    "name": "YOLOv5m",
                    "training_params": [
                      {
                        "name": "epoch",
                        "type": "int",
                        "argument": "string",
                        "default": "1"
                      },
                      {
                        "name": "batch_size",
                        "type": "int",
                        "argument": "string",
                        "default": "10"
                      }
                    ],
                    "performance_metrics": [
                      {
                        "name": "string",
                        "type": "string",
                        "value": "string"
                      }
                    ]
                  },
                  {
                    "name": "classifier",
                    "training_params": [
                      {
                        "name": "string",
                        "type": "string",
                        "argument": "string",
                        "default": "string"
                      }
                    ],
                    "performance_metrics": [
                      {
                        "name": "string",
                        "type": "string",
                        "value": "string"
                      }
                    ]
                  }
                ],
                "gen_date": "2022-10-31T07:31:31.647Z",
                "status": 0,
                "history": {},
                "ext": {},
                "reg_date": "2022-10-31T07:31:31.647Z",
                "reg_id": "string",
                "mod_date": "2022-10-31T07:31:31.647Z",
                "mod_id": "string"
              }
        )
    },

    'PATCH /api/v1/experiments/:experiment_id' : (req,res) => {
        return res.json({
            "_id": "id2",
            "name": "Exp_TEST_mod",
            "description": "string",
            "ml_task": 0,
            "dataset_name": "K-Fashion",
            "versioned_dataset_name": "Augmented",
            "versioned_dataset_id": "6356393f1665e43606cebf01",
            "index": 0,
            "dataset_id": "string",
            "model_name": "YOLOv5m + Image Classification",
            "algorithms": [
              {
                "name": "YOLOv5m",
                "training_params": [
                  {
                    "name": "epoch",
                    "type": "int",
                    "argument": "string",
                    "default": "1"
                  },
                  {
                    "name": "batch_size",
                    "type": "int",
                    "argument": "string",
                    "default": "10"
                  }
                ],
                "performance_metrics": [
                  {
                    "name": "string",
                    "type": "string",
                    "value": "string"
                  }
                ]
              },
              {
                "name": "classifier",
                "training_params": [
                  {
                    "name": "string",
                    "type": "string",
                    "argument": "string",
                    "default": "string"
                  }
                ],
                "performance_metrics": [
                  {
                    "name": "string",
                    "type": "string",
                    "value": "string"
                  }
                ]
              }
            ],
            "gen_date": "2022-10-31T07:31:31.647Z",
            "status": 0,
            "history": {},
            "ext": {},
            "reg_date": "2022-10-31T07:31:31.647Z",
            "reg_id": "string",
            "mod_date": "2022-10-31T07:31:31.647Z",
            "mod_id": "string"
          })
    },

    'DELETE /api/v1/experiments/:experiment_id': (req,res) => {
        return res.json();
    },

    'POST /api/v1/versioned-datasets/': (req,res) => {
        return res.json();
    }
}


//{ "_id": "6356393f1665e43606cebf01", "ml_task": 1, "dataset_name": "mlp_test_img", "preprocessing": [], "augmentation": [], "bundle_ids": [ "6348c7025fcdbdc77fce345e" ], "history": {}, "ext": {}, "dataset_id": "634650c8122746be69d4b8d4", "name": "image-tagging-test", "index": 0, "gen_date": null, "split": "[28, 7, 0]", "status": 0, "reg_date": "2022-10-24T07:05:35.440000Z", "reg_id": "user_id", "mod_date": "2022-10-24T07:05:35.440000Z", "mod_id": "user_id" }