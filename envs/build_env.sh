# Install tf_pose and fsanet-pytorch dependency Packages
sudo apt-get update
echo "Installing gcc, curl, wget and git by apt-get"
sudo apt-get install -y gcc curl wget git
echo "Installing matplotlib, setuptools and tqdm"
pip install matplotlib setuptools tqdm
echo "Install API service packages"
pip install fastapi uvicorn pydantic jinja2

echo "Installing pytorch, torchvision and tensorflow"
if [ "$1" = true ] ;
then
    echo "GPU mode"
    pip install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
    pip install tensorflow-gpu==2.2.0
else
    echo "CPU mode"
    pip install torch==1.8.1+cpu torchvision==0.9.1+cpu torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
    pip install tensorflow==2.2.0
fi

echo "Installing onnx and onnxruntime"
pip install onnx==1.7.0 onnxruntime==1.2.0
echo "Installing tf-slim"
pip install git+https://github.com/adrianc-a/tf-slim.git@remove_contrib
echo "Installing opencv-python==4.4.0.42"
pip install opencv-python==4.4.0.42 ffmpeg
echo "Installing slidingwindow and pycocotools"
pip install slidingwindow pycocotools
echo "Install python-dotenv"
pip install python-dotenv

echo "Installing swig from apt-get"
sudo apt-get install -y swig
echo "Compiling tf_pose with swig"
cd src/services/detection/tf_pose/pafprocess
swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace
