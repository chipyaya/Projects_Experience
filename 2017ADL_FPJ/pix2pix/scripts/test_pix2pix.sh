mkdir -p ./checkpoints/pix2pix
wget 'https://www.dropbox.com/s/79tk8vamiqa1gts/17_net_D.pth?dl=1' -O 17_net_D.pth
wget 'https://www.dropbox.com/s/a3cdljo1qz1dnhq/17_net_G.pth?dl=1' -O 17_net_G.pth
mv 17_net_D.pth ./checkpoints/pix2pix
mv 17_net_G.pth ./checkpoints/pix2pix
python3.5 test.py --dataroot ../data_large/ --name pix2pix --model pix2pix --which_model_netG unet_32 --which_model_netD pixel --which_direction BtoA --dataset_mode aligned --norm batch --which_epoch 17 --testing_path testing_sample_dir
