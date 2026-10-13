<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Milmonk/Milmonk/main/assets/banner-dark.svg">
  <img src="https://raw.githubusercontent.com/Milmonk/Milmonk/main/assets/banner-light.svg" width="100%" alt="Martin Duračka. Machine learning, computer vision and robotics. Technical University of Košice, FEI.">
</picture>

I study at the Faculty of Electrical Engineering and Informatics of the Technical University of Košice. Most of my work is in machine learning, with a focus on computer vision and vision-language models. Alongside that I deploy applications to the cloud and work with robot simulation in ROS 2.

### Selected work

#### [bp-flamingo](https://github.com/Milmonk/bp-flamingo)

<a href="https://github.com/Milmonk/bp-flamingo">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Milmonk/Milmonk/main/assets/fig-flamingo-dark.svg">
    <img align="right" width="400" src="https://raw.githubusercontent.com/Milmonk/Milmonk/main/assets/fig-flamingo-light.svg" alt="Figure 1. BLEU on Multi30K test 2016. German: 3.95 when generated in English and translated, 1.11 when generated directly. French: 5.67 translated, 2.25 direct.">
  </picture>
</a>

*Bachelor's thesis.* Multilingual image captioning with OpenFlamingo on Multi30K. It compares generating captions directly in German and French with generating them in English and translating with MarianMT.

Translation came out ahead on BLEU, chrF, METEOR and BERTScore, and raised target-language accuracy from 64–83% to over 99%. Inference ran on an HPC cluster through SLURM.

<br clear="both">

#### [autocena](https://github.com/Milmonk/autocena)

<a href="https://github.com/Milmonk/autocena">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Milmonk/Milmonk/main/assets/fig-autocena-dark.svg">
    <img align="right" width="400" src="https://raw.githubusercontent.com/Milmonk/Milmonk/main/assets/fig-autocena-light.svg" alt="Figure 2. AutoCena architecture. On Azure: React frontend on Blob Storage, FastAPI backend on App Service, PostgreSQL database and a daily alert job on Functions. Outside Azure: price model on AWS Lambda, chat through the Gemini API, email through SendGrid.">
  </picture>
</a>

*Team project.* Web app that estimates the market price of a used car, built by a team of two for a cloud technologies course.

I handled the production side: Azure deployment, CI/CD with GitHub Actions, the Gemini chat and email price alerts. The XGBoost price model was trained by my teammate.

<br clear="both">

#### [MDMLP](https://github.com/Milmonk/MDMLP)

<a href="https://github.com/Milmonk/MDMLP">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Milmonk/Milmonk/main/assets/fig-mdmlp-dark.svg">
    <img align="right" width="400" src="https://raw.githubusercontent.com/Milmonk/Milmonk/main/assets/fig-mdmlp-light.svg" alt="Figure 3. MDMLP replication: 88.06% accuracy on CIFAR-10 with 0.57 million parameters, trained from scratch.">
  </picture>
</a>

*Paper replication.* PyTorch implementation of [*MDMLP: Image Classification from Scratch on Small Datasets with MLP*](https://arxiv.org/abs/2205.14477) (Lv et al., 2022), including the attention visualisation tool.

Trained from scratch, it reaches 88.06% accuracy on CIFAR-10 with 0.57M parameters.

<br clear="both">

### Tools

**Machine learning** &nbsp; `Python` `PyTorch` `Hugging Face` `scikit-learn` `NumPy` `OpenCV` `Jupyter`

**Backend and cloud** &nbsp; `FastAPI` `PostgreSQL` `Azure` `GitHub Actions`

**Robotics and environment** &nbsp; `ROS 2` `Gazebo` `Linux` `Git` `SLURM`
