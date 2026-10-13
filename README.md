<h1 align="center">Martin Duračka</h1>

<p align="center">
  Student at the Technical University of Košice, Faculty of Electrical Engineering and Informatics<br>
  <b>Machine learning · Computer vision · Robotics</b>
</p>

---

### About

Most of my work is in machine learning, with a focus on computer vision and vision-language models. Alongside that I deploy applications to the cloud and work with robot simulation in ROS 2.

- Bachelor's thesis on multilingual image captioning with OpenFlamingo
- Interested in multimodal models, honest evaluation and reproducing published results
- Comfortable taking a project from a training script on an HPC cluster to a deployed service

### Projects

**[bp-flamingo](https://github.com/Milmonk/bp-flamingo)** · Bachelor's thesis

Multilingual image captioning with OpenFlamingo on the Multi30K dataset. The pipeline compares generating captions directly in German and French against generating them in English and translating with MarianMT, and scores both with BLEU, chrF, METEOR and BERTScore. The translate baseline came out ahead on every metric and raised target-language accuracy from 64–83% to over 99%. Inference ran on an HPC cluster through SLURM.

**[autocena](https://github.com/Milmonk/autocena)** · Team project

Web application that estimates the market price of a used car, built in a team of two for a cloud technologies course. I was responsible for the production side: the Azure deployment (App Service, PostgreSQL, Functions, Blob Storage), CI/CD with GitHub Actions, the Gemini-powered chat and the email price alerts. The price model itself is an XGBoost regressor trained by my teammate.

**[MDMLP](https://github.com/Milmonk/MDMLP)** · Paper replication

PyTorch implementation of [*MDMLP: Image Classification from Scratch on Small Datasets with MLP*](https://arxiv.org/abs/2205.14477) (Lv et al., 2022), including the attention visualisation tool. Trained from scratch, it reaches 88.06% accuracy on CIFAR-10 with 0.57M parameters.

### Tools

**Machine learning**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)

**Backend and cloud**

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat-square)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)

**Robotics and environment**

![ROS 2](https://img.shields.io/badge/ROS%202-22314E?style=flat-square&logo=ros&logoColor=white)
![Gazebo](https://img.shields.io/badge/Gazebo-F58113?style=flat-square)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)
![SLURM](https://img.shields.io/badge/SLURM-2F4F4F?style=flat-square)
