
python main.py \
    --task "train" \
    --data_root "data/" \
    --train_form "contrastive" \
    --num_layers 50 \
    --batch_size 16 \
    --early_stop_patience 5 \
    --save_root "trained_model/layer_50"