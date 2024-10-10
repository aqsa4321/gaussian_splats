make changes in two files:
– scene/dataset readers.py: Provide path to Family/sparse/0 folder
as a variable pathgs on line 25.
– train.py: Provide path to Family/ folder as a variable path output
on line 30.
• For training, run the command ”python train.py -s <path to data
folder. in this case Family/> --eval". An output folder will be
created in Family/ folder that contains point clouds.
2
• After training, for rendering, run the command python render.py -m
<path to trained model>. It will take the most recent trained point
cloud from the output folder and will generate training and testing ren-
dered images folders.
• For testing and calculating metrics, run the command python metrics.py
-m <path to trained model>. It will generate a result.json file that con-
tain ssim, psnr and lpips for the latest trained folder.
