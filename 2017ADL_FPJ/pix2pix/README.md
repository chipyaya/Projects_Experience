# pix2pix
## Pytorch version
0.3.0.post4  
- pip3 install http://download.pytorch.org/whl/cu80/torch-0.3.0.post4-cp35-cp35m-linux_x86_64.whl --user
- pip3 install --no-deps torchvision

## Data path
../data_large/train/\*.jpg  
../data_large/test/\*.jpg  

## Model path
./checkpoints/pix2pix/[epoch]_net_D.pth  
./checkpoints/pix2pix/[epoch]_net_G.pth  

## Training command
./scripts/train_pix2pix.sh  

## Testing command
./scripts/test_pix2pix.sh  

