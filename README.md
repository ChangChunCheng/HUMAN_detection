# human_detection Environment Building

## This project is building from tf_pose_estimation, fsanet-pytorch and webcam in the following link:

- GitHub: [ZheC/tf-pose-estimation](https://github.com/ZheC/tf-pose-estimation)
- GitHub: [omasaht/headpose-fsanet-pytorch](https://github.com/omasaht/headpose-fsanet-pytorch)
- GitHub: [jhukaby/webcamjs](https://github.com/jhuckaby/webcamjs)

**After Install environment**
- Install python3, python3-pip, virtualenv with pip
- Edit ".env" file.
  - hasGPU: true if GPU exist, 'None' if GPU doesn't exist
  - setup HOST with the host ip

**Steps:**
1. Build environment with conda.
   ```{bash}
   $ make BuildENV
   ```
2. Activate conda env.
   ```{bash}
   $ conda activate ${ENV_NAME} # ENV_NAME setuped in .env file.
   ```
3. Install dependency packages.
   ```{bash}
   $ make InstallPackage
   ```
4. Run test
   ```{bash}
   $ make TEST
   ```
5. Run API server
   ```{bash}
   $ make run
   ```
   **API config is 'config.py'.**

   **There are 4 models for tf_pose can be selected in ModelConfig.TF_POSE_TYPE.**