export default {
  'POST /images/upload': (req, res) => {
    return res.json({
      'paths': [
        'images/soma-b5.png'
      ]
    })
  },

  'GET /api/v1/workbooks': (req, res) => {
    return res.json({
      offset: 30,
      limit: 10,
      sort_by: '',
      filtering: '',
      total_results: 72,
      results: [{
        _id: '1234',
        name: '소마셈 A3',
        description: '1학년 세 수의 덧셈과 뺄셈',
        image_url: 'http://localhost:9980/images/%EC%86%8C%EB%A7%88%EC%85%88A3.png',
        no_pages: 20,
        valid: 1,
        applied: 1,
        // history: {},
        // ext: {},
        // reg_date: '',
        // reg_id: '',
        // mod_date: '',
        // mod_id: '',
      },{
        _id: '2345',
        name: '소마셈 B5',
        description: '2학년 곱셈',
        image_url: 'http://localhost:9980/images/soma-b5.png',
        no_pages: 14,
        valid: 1,
        applied: 0,
      },{
        _id: '3456',
        name: '이름',
        description: '설명',
        image_url: '',
        no_pages: 0,
        valid: 0,
        applied: 0,
      },]
    })
  },
  'POST /api/v1/workbooks': (req, res) => {
    return res.json({
      _id: '2345',
      name: '소마셈 B5',
      description: '2학년 곱셈',
      image_url: 'http://localhost:9980/images/soma-b5.png',
      no_pages: 0,
      valid: 0,
      applied: 0,
    })
  },
  'GET /api/v1/workbooks/:id': (req, res) => {
    return res.json({
      _id: '2345',
      name: '소마셈 B5',
      description: '2학년 곱셈',
      image_url: 'http://localhost:9980/images/soma-b5.png',
      no_pages: 0,
      valid: 0,
      applied: 0,
    })
  },
  'PATCH /api/v1/workbooks/:id': (req, res) => {
    return res.json({
      _id: '2345',
      name: '소마셈 B5',
      description: '2학년 곱셈',
      image_url: 'http://localhost:9980/images/soma-b5.png',
      no_pages: 0,
      valid: 0,
      applied: 0,
    })
  },
  'DELETE /api/v1/workbooks/:id': (req, res) => {
    return res.json()
  },

  'GET /api/v1/pages': (req, res) => {
    return res.json({
      offset: 30,
      limit: 10,
      sort_by: '',
      filtering: '',
      total_results: 145,
      results: [{
        _id: 'abcd',
        workbook_id: '2345',
        page_num: '101',
        description: '',
        original_url: 'http://localhost:9980/images/A01_101.png',
        sample_url: '',
        labeled: 0,
        width: 0,
        height: 0,
        vector: [0, ],
        problems: [{
          prob_num: '1',
          solving_url: '',
          similar_url: '',
          labels: [{
            bbox: [1540, 1410, 1718, 1570],
            label: '2'
          }]
        },{
          prob_num: '2',
          solving_url: '',
          similar_url: '',
          labels: [{
            bbox: [1260, 1940, 1646, 2092],
            label: '작습니다'
          }]
        },{
          prob_num: '3',
          solving_url: '',
          similar_url: '',
          labels: [{
            bbox: [1716, 2396, 1944, 2544],
            label: '짝수'
          }, {
            bbox: [1252, 2684, 1408, 2840],
            label: '합'
          }, {
            bbox: [1564, 2684, 1736, 2840],
            label: '9'
          }]
        }],
        // history: {},
        // ext: {},
        // reg_date: '',
        // reg_id: '',
        // mod_date: '',
        // mod_id: '',
      },{
        _id: 'bcde',
        workbook_id: '2345',
        page_num: '96',
        description: '',
        original_url: 'http://localhost:9980/images/A03_96.png',
        sample_url: '',
        labeled: 0,
        width: 0,
        height: 0,
        vector: [0, ],
        problems: [{
          prob_num: '1',
          solving_url: '',
          similar_url: '',
          labels: [{
            bbox: [1664, 1544, 1896, 1924],
            label: '5'
          }, {
            bbox: [1656, 1812, 2092, 2052],
            label: '7'
          }]
        },{
          prob_num: '2',
          solving_url: '',
          similar_url: '',
          labels: [{
            bbox: [1668, 2396, 1916, 2644],
            label: '8'
          }, {
            bbox: [1912, 2640, 2160, 2884],
            label: '4'
          }]
        }],
      },]
    })
  },
  'POST /api/v1/pages': (req, res) => {
    return res.json({
      _id: 'bcde',
      workbook_id: '2345',
      page_num: '96',
      description: '',
  })
  },
  'GET /api/v1/pages/count': (req, res) => {
    return res.json({
      'filtering': 'labeled=1',
      'count': 12,
    })
  },
  'GET /api/v1/pages/:id': (req, res) => {
    return res.json({
      _id: 'bcde',
      workbook_id: '2345',
      page_num: '96',
      description: '',
      original_url: 'http://localhost:9980/images/A03_96.png',
      sample_url: '',
      labeled: 0,
      width: 0,
      height: 0,
      vector: [0, ],
      problems: [{
        prob_num: '1',
        solving_url: '',
        similar_url: '',
        labels: [{
          bbox: [1664, 1544, 1896, 1924],
          label: '5'
        }, {
          bbox: [1656, 1812, 2092, 2052],
          label: '7'
        }]
      },{
        prob_num: '2',
        solving_url: '',
        similar_url: '',
        labels: [{
          bbox: [1668, 2396, 1916, 2644],
          label: '8'
        }, {
          bbox: [1912, 2640, 2160, 2884],
          label: '4'
        }]
      }],
    })
  },
  'PATCH /api/v1/pages/:id': (req, res) => {
    return res.json({
      _id: 'bcde',
      workbook_id: '2345',
      page_num: '96',
      description: '',
      original_url: 'http://localhost:9980/images/A03_96.png',
      sample_url: '',
      labeled: 0,
      width: 0,
      height: 0,
      vector: [0, ],
      problems: [{
        prob_num: '1',
        solving_url: '',
        similar_url: '',
        labels: [{
          bbox: [1664, 1544, 1896, 1924],
          label: '5'
        }, {
          bbox: [1656, 1812, 2092, 2052],
          label: '7'
        }]
      },{
        prob_num: '2',
        solving_url: '',
        similar_url: '',
        labels: [{
          bbox: [1668, 2396, 1916, 2644],
          label: '8'
        }, {
          bbox: [1912, 2640, 2160, 2884],
          label: '4'
        }]
      }],
    })
  },
  'DELETE /api/v1/pages/:id': (req, res) => {
    return res.json()
  },

  'POST /api/v1/infer/dnr': (req, res) => {
    return res.json({
      success: 1,
      log_id: 'log_id',
      input_url: 'http://localhost:9980/images/input_url_A03_96.jpg',
      boxed_url: 'http://localhost:9980/images/boxed_url_A03_96.png',
      workbook: {
        _id: '2345',
        name: '소마셈 B5',
        description: '2학년 곱셈',
        image_url: 'http://localhost:9980/images/soma-b5.png',
        no_pages: 0,
        valid: 0,
        applied: 0,
      },
      page: {
        _id: 'bcde',
        workbook_id: '2345',
        page_num: '96',
        description: '',
        original_url: 'http://localhost:9980/images/A03_96.png',
        sample_url: '',
        labeled: 0,
        width: 0,
        height: 0,
        vector: [0, ],
        problems: [{
          prob_num: '1',
          solving_url: 'images/A03_96_1_해설.png',
          similar_url: 'images/A03_96_1_유사.png',
          labels: [{
            bbox: [1664, 1544, 1896, 1924],
            label: '5'
          }, {
            bbox: [1656, 1812, 2092, 2052],
            label: '7'
          }]
        },{
          prob_num: '2',
          solving_url: 'images/A03_96_2_해설.png',
          similar_url: 'images/A03_96_2_유사.png',
          labels: [{
            bbox: [1668, 2396, 1916, 2644],
            label: '8'
          }, {
            bbox: [1912, 2640, 2160, 2884],
            label: '4'
          }]
        }],
      },
      predictions: [{
        prob_num: '1',
        answers: ['5', '7']
      }, {
        prob_num: '2',
        answers: ['8', '4']
      }]
    })
  },
  'POST /api/v1/infer/score': (req, res) => {
    return res.json([{
      prob_num: '1',
      solving_url: 'images/A03_96_1_해설.png',
      similar_url: 'images/A03_96_1_유사.png',
      correct: 0,
    },{
      prob_num: '2',
      solving_url: 'images/A03_96_2_해설.png',
      similar_url: 'images/A03_96_2_유사.png',
      correct: 1,
    }])
  },
  'GET /api/v1/logs': (req, res) => {
    return res.json({
      limit: 10,
      offset: 0,
      sort_by: "",
      filtering: "",
      total_results: 29,
      results: [
        {
          _id: "62fcc4e8f8893fa7ef0dab73",
          success: 1,
          input_url: "images/input_url_A03_96.jpg",
          boxed_url: "images/input_url_A03_96_3wUyozI.jpg",
          workbook: {
            _id: "62f5a54989b83e0bd63c7006",
            history: {},
            ext: {},
            name: "소마셈 A3",
            description: "1학년 세 수의 덧셈과 뺄셈",
            image_url: "images/표지_소마셈A3.jpg",
            no_pages: 1,
            valid: 1,
            applied: 0
          },
          page: {
            _id: "62f5b0e944e6b01aefc96ce5",
            vector: [],
            problems: [
              {
                prob_num: "1",
                similar_url: "images/A03_96_1_유사.png",
                solving_url: "images/A03_96_1_해설.png",
                labels: [
                  { bbox: [1649, 1547, 1897, 1918], label: "5" },
                  { bbox: [1681, 1789, 2102, 2037], label: "7" }
                ]
              },
              {
                similar_url: "images/A03_96_2_유사.png",
                solving_url: "images/A03_96_2_해설.png",
                labels: [
                  { bbox: [1657, 2386, 1924, 2652], label: "8" },
                  { bbox: [1899, 2624, 2163, 2888], label: "4" }
                ],
                prob_num: "2"
              }
            ],
            workbook_id: "62f5a54989b83e0bd63c7006",
            page_num: "96",
            description: "뺄셈구구 - 3일차",
            original_url: "images/A03_96.png",
            sample_url: "images/Sample_A03_96.jpg",
            labeled: 1,
            width: 2475,
            height: 3182,
          },
          scoring: [{
            prob_num: "1",
            labels: ["5", "7"],
            answers: ["5", "7"],
            // custom_answers: [],
            // correct: null
          },
          {
            prob_num: "2",
            labels: ["8", "4"],
            answers: ["8", "4"],
            // custom_answers: [],
            // correct: null
          },],
          reg_date: "2022-08-17T10:37:28.485000",
          reg_id: "user_id"
        },
        {
          _id: "62fcc4acf8893fa7ef0dab69",
          success: 0,
          input_url: "images/input_url_A03_96.jpg",
          boxed_url: "",
          // workbook: {},
          // page: {},
          // scoring: [],
          reg_date: "2022-08-17T10:36:28.372000",
          reg_id: "user_id"
        },
        {
          _id: "62fc8ddd4f2762d42ec675c2",
          success: 1,
          input_url: "images/Sample_A03_96.jpg",
          boxed_url: "images/boxed_Sample_A03_96_0DEn1xD.jpg",
          workbook: {
            _id: "62f5a54989b83e0bd63c7006",
            history: {},
            ext: {},
            name: "소마셈 A3",
            description: "1학년 세 수의 덧셈과 뺄셈",
            image_url: "images/표지_소마셈A3.jpg",
            no_pages: 1,
            valid: 1,
            applied: 0,
          },
          page: {
            _id: "62f5b0e944e6b01aefc96ce5",
            vector: [],
            problems: [
              {
                prob_num: "1",
                similar_url: "images/A03_96_1_유사.png",
                solving_url: "images/A03_96_1_해설.png",
                labels: [
                  { bbox: [1649, 1547, 1897, 1918], label: "5" },
                  { bbox: [1681, 1789, 2102, 2037], label: "7" }
                ]
              },
              {
                similar_url: "images/A03_96_2_유사.png",
                solving_url: "images/A03_96_2_해설.png",
                labels: [
                  { bbox: [1657, 2386, 1924, 2652], label: "8" },
                  { bbox: [1899, 2624, 2163, 2888], label: "4" }
                ],
                prob_num: "2"
              }
            ],
            history: {},
            ext: {},
            workbook_id: "62f5a54989b83e0bd63c7006",
            page_num: "96",
            description: "뺄셈구구 - 3일차",
            original_url: "images/A03_96.png",
            sample_url: "images/Sample_A03_96.jpg",
            labeled: 1,
            width: 2475,
            height: 3182,
          },
          scoring: [{
            prob_num: "1",
            labels: ["5", "7"],
            answers: ["5", "7"],
            custom_answers: ["5", "7"],
            correct: 1
          },
          {
            prob_num: "2",
            labels: ["8", "4"],
            answers: ["0", "4"],
            custom_answers: ["0", "4"],
            correct: 0
          },],
          reg_date: "2022-08-17T06:42:37.526000",
          reg_id: "user_id"
        },
      ]
    })
  },

  'GET /api/v1/version': (req, res) => {
    return res.json({
      search_model: "0.0.1-mockup",
      recognition_model: "0.0.1-mockup",
      scroing_service: "0.0.1-mockup"
    })
  },
  'POST /api/v1/pages/reindex': (req, res) => {
    return res.json({
      updated_cnt: "0"
    })
  },

  // Examples
  // 'GET /api/user': {
  //   username: 'admin',
  //   sex: 5,
  // },
  // 'GET /api/list': function (req, res) {
  //   let query = req.query || {};
  //   return res.json({
  //     limit: query.limit,
  //     offset: query.offset,
  //     list: [{
  //       username: 'admin1',
  //       sex: 1,
  //     }, {
  //       username: 'admin2',
  //       sex: 0,
  //     }]
  //   })
  // },
  // 'GET /api/userinfo/:id': (req, res) => {
  //   return res.json({
  //     id: req.params.id,
  //     username: 'kenny',
  //   });
  // },
  // 'POST /api/login/account': (req, res) => {
  //   const { password, username } = req.body;
  //   if (password === '888888' && username === 'admin') {
  //     return res.json({
  //       status: 'ok',
  //       token: 'sdfsdfsdfdsf',
  //     });
  //   } else {
  //     return res.json({
  //       status: 'error',
  //       code: 403,
  //     });
  //   }
  // },
  // 'DELETE /api/user/:id': (req, res) => {
  //   // console.log(req.params.id);
  //   res.send({ status: 'ok', message: 'delete success!' });
  // },
  // 'PUT /api/user/:id': (req, res) => {
  //   // console.log(req.params.id);
  //   // console.log(req.body);
  //   res.send({ status: 'ok', message: 'update success！' });
  // },
}
