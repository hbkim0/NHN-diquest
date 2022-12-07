# 환경설정

    pip install -r requirements.txt

# Text Tagging 학습 및 추론방법 설명

## 학습 방법
    python train.py train_argument.json
    
train_argument.json 파일 안의 경로, 하이퍼파라미터 등의 정보를 담은 상태로 학습 진행.

## 추론 방법
    python app.py inference_argument.json
    
inference_argument.json 파일 안의 경로, 하이퍼파라미터 등의 정보를 담은 상태로 추론 진행.<br>
기본으로 5000번 port를 사용함.(수정할 경우 app.py main 함수 line 380 수정)<br>
127.0.0.1:5000/test 에서 확인 가능.
<br><br>


# json 파일 내의 argument 설명
|Argument|설명|
|:---:|---|
|model_name_or_path|불러올 모델의 이름 또는 저장 경로(학습 시에는 pre-trained model, 추론 시에는 fine-tuning된 된 모델 경로 사용)|
|data_dir|train, dev, test 파일들이 저장된 경로. 이름은 각각 (train.txt, dev.txt, test.txt로 고정)|
|output_dir|추론 결과, 또는 학습 결과, 모델 등을 저장할 경로|
|labels|label정보를 담고있는 파일명|
|max_seq_length|문장의 최대 길이(이보다 길 경우 문장이 짤림)|
|num_train_epochs|학습할 epoch 개수|
|per_device_train_batch_size|cpu1개당 또는 gpu1개당 배치 사이즈.(gpu 이용시에 사용할 gpu 개수만큼 곱해주면 총 batch size 계산 가능)|
|do_train|학습 데이터에 대해 학습을 진행할 것인지에 대한 여부|
|do_eval|검증 데이터(dev.txt)에 대해 성능 평가를 진행할 것인지에 대한 여부|
|do_predict|평가 데이터(test.txt)에 대해 성능 평가를 진행할 것인지에 대한 여부|
