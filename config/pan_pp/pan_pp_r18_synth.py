model = dict(
    type='PAN_PP',
    backbone=dict(
        type='resnet18',
        pretrained=True
    ),
    neck=dict(
        type='FPEM_v2',
        in_channels=(64, 128, 256, 512),
        out_channels=128
    ),
    detection_head=dict(
        type='PAN_PP_DetHead',
        in_channels=512,
        hidden_dim=128,
        num_classes=6,
        loss_text=dict(
            type='DiceLoss',
            loss_weight=1.0
        ),
        loss_kernel=dict(
            type='DiceLoss',
            loss_weight=0.5
        ),
        loss_emb=dict(
            type='EmbLoss_v2',
            feature_dim=4,
            loss_weight=0.25
        ),
        use_coordconv=False,
    )
)
data = dict(
    train=dict(
        type='PAN_PP_IC15',
        split='train',
        is_transform=True,
        img_size=736,
        short_size=736,
        kernel_scale=0.5,
        read_type='pil',
        with_rec=True,

        batch_size=16,
        num_workers=8,
        shuffle=True,
        drop_last=False,
        img_dir='/home/ocr/program/PAN++/devanagari/output/',
        ann_dir='/home/ocr/program/PAN++/devanagari/gt_ic/'
    ),
    test=dict(
        type='PAN_PP_IC15',
        split='test',
        short_size=720,
        read_type='pil',
        with_rec=True,

        batch_size=1,   # must be 8
        num_workers=8,
        shuffle=False,
        drop_last=False,
        img_dir='/home/ocr/program/PAN++/devanagari/output/',
        ann_dir='/home/ocr/program/PAN++/devanagari/gt_ic.txt'
    )
)
train_cfg = dict(
    lr=1e-3,
    schedule='polylr',
    optimizer='Adam',
    use_ex=False,

    weight_decay=0,
    epoch=50,
    print_batch_step=5,
    save_epoch_step=10,
    eval_batch_step=[0, 15000],
    save_model_dir='./output/pan_pp_r18_hi/'
    # pretrain
)
test_cfg = dict(
    min_score=0.85,
    min_area=260,
    min_kernel_area=2.6,
    scale=4,
    bbox_type='rect',
    result_path='./output/pan_pp_r18_hi/preds.zip',

    infer_det=False,
    save_res_path='./output/det_pan_pp_hi/',
)
