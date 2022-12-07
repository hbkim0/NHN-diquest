export default {
  'GET /api/v1/datasets/customers': (req, res) => {
    return res.json({
      "offset": 0,
      "limit": 50,
      "sort_by": "string",
      "filtering": "string",
      "total_results": 2,
      "results": [
        {
          "_id": "string",
          "identifier": 1,
          "gender": "남성",
          "zip_code": 99999,
          "history": {},
          "ext": {},
          "reg_date": "2022-11-10T05:46:56.803Z",
          "reg_id": "string",
          "mod_date": "2022-11-10T05:46:56.803Z",
          "mod_id": "string"
        },
        {
          "_id": "string",
          "identifier": 2,
          "gender": "여성",
          "zip_code": 777,
          "history": {},
          "ext": {},
          "reg_date": "2022-11-10T05:46:56.803Z",
          "reg_id": "string",
          "mod_date": "2022-11-10T05:46:56.803Z",
          "mod_id": "string"
        }
      ]
    });
  },

  'GET /api/v1/datasets/history': (req, res) => {
    return res.json({
      "offset": 0,
      "limit": 50,
      "sort_by": "string",
      "filtering": "string",
      "total_results": 3,
      "results": [
        {
          "_id": "1",
          "customer": "111",
          "product": "111-111",
          "rating": 5,
          "rating_time": "2022-11-10T07:31:03.116Z",
          "history": {},
          "ext": {},
          "reg_date": "2022-11-10T07:31:03.116Z",
          "reg_id": "string",
          "mod_date": "2022-11-10T07:31:03.116Z",
          "mod_id": "string"
        },
        {
          "_id": "2",
          "customer": "222",
          "product": "222-111",
          "rating": 77,
          "rating_time": "2022-11-10T07:31:03.116Z",
          "history": {},
          "ext": {},
          "reg_date": "2022-11-10T07:31:03.116Z",
          "reg_id": "string",
          "mod_date": "2022-11-10T07:31:03.116Z",
          "mod_id": "string"
        },
        {
          "_id": "3",
          "customer": "333",
          "product": "333-111",
          "rating": 9,
          "rating_time": "2022-11-10T07:31:03.116Z",
          "history": {},
          "ext": {},
          "reg_date": "2022-11-10T07:31:03.116Z",
          "reg_id": "string",
          "mod_date": "2022-11-10T07:31:03.116Z",
          "mod_id": "string"
        },
      ]
    });
  },

  'GET /api/v1/datasets/products': (req, res) => {
    return res.json({
      "offset": 0,
      "limit": 50,
      "sort_by": "string",
      "filtering": "string",
      "total_results": 3,
      "results": [
        {
          "_id": "1",
          "name": "abc",
          "description": "string",
          "image": "string",
          "identifier": 1,
          "categories": [
            "계절"
          ],
          "gender": "남성",
          "attributes": [
            {
              "key": "string",
              "values": [
                "string"
              ]
            }
          ],
          "history": {},
          "ext": {},
          "reg_date": "2022-11-10T23:34:21.296Z",
          "reg_id": "string",
          "mod_date": "2022-11-10T23:34:21.296Z",
          "mod_id": "string"
        },
        {
          "_id": "2",
          "name": "def",
          "description": "string",
          "image": "string",
          "identifier": 1,
          "categories": [
            "색상"
          ],
          "gender": "여성",
          "attributes": [
            {
              "key": "string",
              "values": [
                "string"
              ]
            }
          ],
          "history": {},
          "ext": {},
          "reg_date": "2022-11-10T23:34:21.296Z",
          "reg_id": "string",
          "mod_date": "2022-11-10T23:34:21.296Z",
          "mod_id": "string"
        },
      ]
    });
  },

  'GET /api/v1/datasets/products/autocomplete': (req, res) => {
    return res.json({
      "results": [
        "ABC","BBC","BBQ","DDD"
      ]
    });
  },

  'GET /api/v1/datasets/products/:product_id': (req, res) => {
    return res.json({
      "_id": "636c9e5e1665e43606f72716",
      "attributes": [
        {
          "key": "카테고리",
          "values": [
            "캔버스",
            "뮬"
          ]
        },
        {
          "key": "기장",
          "values": []
        },
        {
          "key": "스타일",
          "values": [
            "유니크"
          ]
        },
        {
          "key": "패턴",
          "values": [
            "배색"
          ]
        },
        {
          "key": "시즌",
          "values": [
            "한여름"
          ]
        },
        {
          "key": "핏",
          "values": []
        },
        {
          "key": "색상",
          "values": [
            "그린",
            "네이비"
          ]
        },
        {
          "key": "소재",
          "values": [
            "면"
          ]
        },
        {
          "key": "넥라인",
          "values": []
        }
      ],
      "history": {},
      "ext": {},
      "identifier": 1,
      "name": "COVERNAT 커버 뮬",
      "description": "º디자인\n부드러운 터치감이 좋은 오리지널 면 100% 국내산 캔버스 소재 사용\n기본 코튼 플랫 베이지 슈레이스\n앞코가 귀여운 느낌의 몰드창\n히든 안창 포함 총 45mm의 높이감 있는 뮬 스타일\n6.0mm 부드러우면서 압축률이 좋은 Tection를 적용하여 탁월한 높이의 플랫폼 적용\n40mm 볼륨감 있는 이중구조의 볼드한 중창의 러버로 탄탄하면서 견고한 볼륨감 있는 마무리\n아웃솔에 C로고를 패턴화하고 생고무러버를 적용하여 바닥 밀착감이 높임\n인솔이 튀어나온 형태라 뒤꿈치가 걸리지 않는 편안함",
      "image": "/media/1.png",
      "label": "신발",
      "gender": "여성",
      "reg_date": "2021-07-07T17:29:26Z",
      "reg_id": "user_id",
      "mod_date": "2021-07-07T17:29:26Z",
      "mod_id": "user_id"
    })
  },

  'GET /api/v1/datasets/status': (req, res) => {
    return res.json([
      {
        "_id": "636cb758b0aacecc6f9ea6d1",
        "customer": {
          "total": 925,
          "in": 22,
          "out": 2
        },
        "product": {
          "total": 1552,
          "in": 11,
          "out": 12
        },
        "history": {
          "total": 58917,
          "in": 89,
          "out": 23
        },
        "date": "2022-11-05"
      },
      {
        "_id": "636cb74cb0aacecc6f9ea6d0",
        "customer": {
          "total": 933,
          "in": 15,
          "out": 7
        },
        "product": {
          "total": 1591,
          "in": 44,
          "out": 5
        },
        "history": {
          "total": 58991,
          "in": 108,
          "out": 34
        },
        "date": "2022-11-06"
      },
      {
        "_id": "636cb2ed5255a516beeb00b2",
        "customer": {
          "total": 925,
          "in": 22,
          "out": 2
        },
        "product": {
          "total": 1552,
          "in": 11,
          "out": 12
        },
        "history": {
          "total": 58917,
          "in": 89,
          "out": 23
        },
        "date": "2022-11-07"
      },
      {
        "_id": "636ca650b0aacecc6f9ea6cd",
        "customer": {
          "total": 933,
          "in": 15,
          "out": 7
        },
        "product": {
          "total": 1591,
          "in": 44,
          "out": 5
        },
        "history": {
          "total": 58991,
          "in": 108,
          "out": 34
        },
        "date": "2022-11-08"
      }
    ]);
  },

  'GET /api/v1/experiments': (req, res) => {
    return res.json({
      "offset": 0,
      "limit": 50,
      "sort_by": "string",
      "filtering": "string",
      "total_results": 0,
      "results": [
        {
          "_id": "exp1",
          "model_id": "model1",
          "seq_num_major": 1,
          "seq_num_minor": 1,
          "status": 0,
          "serving": 1,
          "start_time": "2022-11-15T05:38:36.934Z",
          "end_time": "2022-11-15T05:38:36.935Z",
          "parameters": [
            {
              "key": "embedding_dim",
              "value": 7
            },
            {
              "key": "lr",
              "value": 77
            },
            {
              "key": "epoch",
              "value": 777
            },
            {
              "key": "batch_size",
              "value": 7777
            }
          ],
          "rmse": 0,
          "history": {},
          "ext": {},
          "reg_date": "2022-11-15T05:38:36.935Z",
          "reg_id": "string",
          "mod_date": "2022-11-15T05:38:36.935Z",
          "mod_id": "string"
        },
        {
          "_id": "exp2",
          "model_id": "model2",
          "seq_num_major": 1,
          "seq_num_minor": 1,
          "status": 0,
          "serving": 2,
          "start_time": "2022-11-15T05:38:36.934Z",
          "end_time": "2022-11-15T05:38:36.935Z",
          "parameters": [
            {
              "key": "embedding_dim",
              "value": 1
            },
            {
              "key": "lr",
              "value": 2
            },
            {
              "key": "epoch",
              "value": 3
            },
            {
              "key": "batch_size",
              "value": 4
            }
          ],
          "rmse": 0,
          "history": {},
          "ext": {},
          "reg_date": "2022-11-15T05:38:36.935Z",
          "reg_id": "string",
          "mod_date": "2022-11-15T05:38:36.935Z",
          "mod_id": "string"
        }
      ]
    })
  },

  'DELETE /api/v1/experiments/:experiment_id': (req, res) => {
    return res.json({})
  },

  'POST /api/v1/experiments': (req, res) => {
    return res.json({
      "_id": "string",
      "model_id": "string",
      "seq_num_major": 1,
      "seq_num_minor": 1,
      "status": 0,
      "serving": 0,
      "start_time": "2022-11-15T07:20:23.489Z",
      "end_time": "2022-11-15T07:20:23.489Z",
      "parameters": [
        {
          "key": "string",
          "value": 0
        }
      ],
      "rmse": 0,
      "history": {},
      "ext": {},
      "reg_date": "2022-11-15T07:20:23.489Z",
      "reg_id": "string",
      "mod_date": "2022-11-15T07:20:23.489Z",
      "mod_id": "string"
    })
  },

  'PATCH /api/v1/experiments/:experiment_id': (req, res) => {
    return res.json({
      "_id": "string",
      "model_id": "string",
      "seq_num_major": 1,
      "seq_num_minor": 1,
      "status": 0,
      "serving": 0,
      "start_time": "2022-11-15T07:20:23.489Z",
      "end_time": "2022-11-15T07:20:23.489Z",
      "parameters": [
        {
          "key": "string",
          "value": 0
        }
      ],
      "rmse": 0,
      "history": {},
      "ext": {},
      "reg_date": "2022-11-15T07:20:23.489Z",
      "reg_id": "string",
      "mod_date": "2022-11-15T07:20:23.489Z",
      "mod_id": "string"
    })
  },

  'GET /api/v1/experiments/schedule': (req, res) => {
    return res.json({
      "_id": "string",
      "cron": "* 35 12 ? * SUN,SAT",
      "priority": 0
    })
  },

  'PATCH /api/v1/experiments/schedule/:schedule_id': (req, res) => {
    return res.json({
      "_id": "string",
      "model_id": "string",
      "seq_num_major": 1,
      "seq_num_minor": 1,
      "status": 0,
      "serving": 0,
      "start_time": "2022-11-15T07:56:43.644Z",
      "end_time": "2022-11-15T07:56:43.644Z",
      "parameters": [
        {
          "key": "string",
          "value": 0
        }
      ],
      "rmse": 0,
      "history": {},
      "ext": {},
      "reg_date": "2022-11-15T07:56:43.644Z",
      "reg_id": "string",
      "mod_date": "2022-11-15T07:56:43.644Z",
      "mod_id": "string"
    })
  },

  'POST /api/v1/experiments/schedule': (req, res) => {
    return res.json({
      "_id": "string",
      "model_id": "string",
      "seq_num_major": 1,
      "seq_num_minor": 1,
      "status": 0,
      "serving": 0,
      "start_time": "2022-11-15T08:00:46.431Z",
      "end_time": "2022-11-15T08:00:46.431Z",
      "parameters": [
        {
          "key": "string",
          "value": 0
        }
      ],
      "rmse": 0,
      "history": {},
      "ext": {},
      "reg_date": "2022-11-15T08:00:46.431Z",
      "reg_id": "string",
      "mod_date": "2022-11-15T08:00:46.431Z",
      "mod_id": "string"
    })
  },

  'GET /api/v1/models': (req, res) => {
    return res.json({
      "offset": 0,
      "limit": 0,
      "sort_by": "string",
      "filtering": "string",
      "total_results": 0,
      "results": [
        {
          "_id": "model1",
          "name": "Neural Collaborative Filtering",
          "description": "model1_desc",
          "image_name": "string",
          "parameters": [
            {
              "name": "embedding_dim",
              "type": "integer",
              "default": 0
            },
            {
              "name": "lr",
              "type": "integer",
              "default": 0
            },
            {
              "name": "epoch",
              "type": "integer",
              "default": 0
            },
            {
              "name": "batch_size",
              "type": "integer",
              "default": 0
            }
          ],
          "history": {},
          "ext": {},
          "reg_date": "2022-11-15T05:35:42.413Z",
          "reg_id": "string",
          "mod_date": "2022-11-15T05:35:42.413Z",
          "mod_id": "string"
        },
        {
          "_id": "model2",
          "name": "model2",
          "description": "model2_desc",
          "image_name": "string",
          "parameters": [
            {
              "name": "embedding_dim",
              "type": "integer",
              "default": 0
            },
            {
              "name": "lr",
              "type": "integer",
              "default": 0
            },
            {
              "name": "epoch",
              "type": "integer",
              "default": 0
            },
            {
              "name": "batch_size",
              "type": "integer",
              "default": 0
            }
          ],
          "history": {},
          "ext": {},
          "reg_date": "2022-11-15T05:35:42.413Z",
          "reg_id": "string",
          "mod_date": "2022-11-15T05:35:42.413Z",
          "mod_id": "string"
        }
      ]
    })
  },
}