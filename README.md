
# 🎬 NUVIE — AI Powered Social Movie Recommendation Platform

Nuvie is an AI-powered social movie recommendation platform that combines intelligent
personalization with real social interaction. Unlike traditional recommendation systems
that focus only on individual preferences, Nuvie integrates **friend activity, social feedback,
and machine learning** into one unified discovery experience.

Users can rate, review, and discuss movies with friends while receiving **dynamic,
friend-aware recommendations** powered by a hybrid AI model.

---

## 🚀 Core Features

- ✅ Hybrid Movie Recommendation System (IBCF + Genre Correlation + Neural CF)
- ✅ Friend-Aware & Socially Boosted Recommendations
- ✅ Real-Time Personalized Home Feed
- ✅ Explainable AI (Why this movie?)
- ✅ Native iOS Application (Swift)
- ✅ Scalable Backend with FastAPI
- ✅ Continuous Learning & Model Retraining

---

## 🧠 System Architecture

              [iOS App (Swift)]
                     ↓
           [Backend API (FastAPI)]
                     ↓
       [AI Recommendation Service (FastAPI)]
                     ↓
             [PostgreSQL + Redis]

---
## 🗂 Repository Structure 
       nuvie/ ├── ai/ # 🤖 AI & Machine Learning Layer │ ├── data/ # Raw & processed datasets │ ├── models/ # Recommendation algorithm implementations │ ├── training/ # Model training pipelines │ ├── evaluation/ # Offline evaluation metrics │ ├── serving/ # AI API service (FastAPI) │ └── explanations/ # Explainable AI logic │ ├── backend/ # ⚙️ Backend API & Business Logic │ ├── app/ # FastAPI route definitions │ ├── models/ # ORM models │ ├── db/ # Database connection & migrations │ ├── schemas/ # Pydantic schemas │ └── Dockerfile # Backend container │ ├── ios/ # 📱 Native iOS App (Swift) │ └── NuvieApp/ │ ├── Views/ # UI screens │ ├── ViewModels/ # MVVM logic │ ├── Network/ # API & networking layer │ ├── Models/ # Data models │ └── Assets/ # Images, icons, colors │ ├── infra/ # 🚀 DevOps & Deployment │ ├── docker-compose.yml # Local development orchestration │ ├── github-actions.yml # CI/CD pipeline │ └── env.example # Environment variables template │ └── README.md # Project documentation
---
## 📐 Product & Engineering Planning (Notion)

All product decisions, AI phases, backend contracts, and task ownership are tracked in Notion
and reflected in this GitHub repository.

🔗 **GitHub Repository**  
https://github.com/kanikeliff/Nuvie/tree/main

🔗 **NUVIE Project Workspace (Notion)**  
https://www.notion.so/NUVIE-2c4a799111d080a3b839d8771eb64431

---

## 👥 Team & Responsibilities

| Name   | Role                         | Responsibilities |
|--------|------------------------------|------------------|
| Berkay | Backend & DevOps Engineer   | API, authentication, infrastructure, CI/CD |
| Andaç  | Database & Data Engineer    | Schema design, data pipelines, feature tables |
| Öykü   | Mobile Frontend Developer  | UI/UX design, user flows |
| Can    | iOS Integration Developer  | Swift integration, API connectivity, notifications |
| Elif   | AI Engineer                  | Model training, inference, explainability, retraining |


---

## 🧩 AI Technology Stack

- Python
- Scikit-learn
- PyTorch / TensorFlow
- Hybrid Recommender (Collaborative + Content + Social)
- Explainable AI Layer
- Continuous Retraining Pipelines

**Training Dataset:**
- MovieLens 1M / 10M
- TMDb Metadata

---

## 🛠 Backend & DevOps Stack

- FastAPI (Python)
- PostgreSQL (Neon)
- Redis (Upstash)
- Docker
- GitHub Actions (CI/CD)
- Sign in with Apple Authentication

---

## 📱 Mobile Stack

- Swift (Native iOS)
- MVVM Architecture
- REST API Integration
- Push Notifications
- Deep Linking

---

# 📋 Project Management & Task Tracking (Notion)

We actively use **Notion** for:
- Sprint planning
- Phase-based task tracking
- Team responsibilities
- Progress monitoring

---

## 🧭 Project Phases & Milestones

### Phase 1 — Foundation
📌 **Objective:** Define the full technical foundation before implementation.

**Completion Checklist**
- [ ] All `docs/` files written  
- [ ] All team members contributed  
- [ ] API contracts approved by AI + iOS  
- [ ] Database schema approved by Backend + AI  
- [ ] README updated  
- [ ] Everything committed to GitHub  
- [ ] Phase tag created: `v0.1-foundation`  

**Final Statement (for Advisor)**  
> “In Phase 1, the NUVIE team completed the full technical foundation of the system by
> documenting the architecture, database schema, API contracts, AI pipeline, and mobile
> application structure. All components were aligned across teams before implementation.”

---

### Phase 2 — Baseline Intelligence
📌 **Objective:** Build and validate the first working AI recommender.

**Completion Checklist**
- [ ] MovieLens dataset cleaned and loaded  
- [ ] Feature tables created  
- [ ] IBCF baseline implemented  
- [ ] Offline metrics computed  
- [ ] Mock AI recommendation API running  
- [ ] Backend `/feed` endpoint connected  
- [ ] iOS feed displays mock recommendations  
- [ ] Phase 2 documentation committed  
- [ ] Phase tag created: `v0.2-baseline`  

**Final Statement (for Advisor)**  
> “In Phase 2, the NUVIE team completed full dataset preparation, implemented a baseline
> Item-Based Collaborative Filtering recommender, evaluated it using offline metrics,
> and connected a mock AI recommendation service to both the backend and iOS client.”

---

### Phase 3 — End-to-End Integration
📌 **Objective:** Deliver a fully working system across all layers.

**Completion Checklist**
- [ ] Real `/recommend` endpoint running  
- [ ] Backend successfully calls AI service  
- [ ] User ratings stored in database  
- [ ] New ratings influence recommendations  
- [ ] iOS app displays real recommendations  
- [ ] “Why recommended” explanations visible  
- [ ] Full system runs with Docker  
- [ ] End-to-end demo recorded  
- [ ] Phase tag created: `v0.3-integration`  

**Final Statement (for Advisor)**  
> “In Phase 3, the NUVIE team successfully integrated the iOS client, backend API,
> AI recommendation service, and database into a fully working end-to-end system.
> Users can now rate movies and instantly receive real, explainable AI recommendations.”

---

### Phase 4 — Social Intelligence
📌 **Objective:** Introduce friend-based and social recommendation signals.

**Completion Checklist**
- [ ] Friend-based boosting implemented in AI  
- [ ] Social reasons appear in recommendations  
- [ ] Friends can be added and accepted  
- [ ] Friend ratings influence feed ranking  
- [ ] iOS shows social badges  
- [ ] Privacy rules applied  
- [ ] Phase tag created: `v0.4-social`  

**Final Statement (for Advisor)**  
> “In Phase 4, the NUVIE team integrated social intelligence into the recommendation system
> by incorporating friend activity, social ranking signals, and friend-based explanations
> into both the AI model and the iOS user interface.”

---

### Phase 5 — Continuous Learning
📌 **Objective:** Transform NUVIE into a self-improving AI system.

**Completion Checklist**
- [ ] User feedback collected  
- [ ] Feedback stored in database  
- [ ] Automatic retraining pipeline running  
- [ ] New model versions created  
- [ ] Old models can be restored  
- [ ] Updated recommendations appear in iOS  
- [ ] Phase tag created: `v1.0-continuous-ai`  

**Final Statement (for Advisor)**  
> “In Phase 5, the NUVIE platform was transformed into a continuously learning AI system
> by introducing user feedback collection, automatic model retraining, performance
> tracking, and model versioning.”
---

# ✅ How to Run Locally (Development)

```bash
git clone https://github.com/your-username/nuvie.git
cd nuvie
cp infra/env.example .env
docker-compose up --build
```

Backend will be available at:
http://localhost:8000/docs

AI Service will be available at:
http://localhost:9000/docs

Python dependencies
- Install runtime and test deps for the AI modules and local evaluation with:

```bash
python -m pip install -r requirements.txt
```
The minimal `requirements.txt` includes `pandas`, `numpy` and `pytest` used by data pipelines, models and smoke tests.

Optional ML dependencies
- For model training or larger ML workloads, install optional ML packages:

```bash
python -m pip install -r requirements-ml.txt
```
- `requirements-ml.txt` contains `scikit-learn`; for deep learning, install `torch` or `tensorflow` following their official guides.

PyTorch install notes
- PyTorch wheels depend on your OS and CUDA version. We recommend installing PyTorch with the official selector at https://pytorch.org/get-started/locally/.

Examples:

- CPU-only (cross-platform):

```bash
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

- CUDA 11.8 example (adjust for your CUDA version):

```bash
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

##Notes:
- If you have a GPU and need CUDA support, pick the appropriate wheel (the selector on the PyTorch site helps).
- TensorFlow is included in `requirements-ml.txt` pinned to a safe minor range; install with the same `pip` command above.

##📊 Evaluation Metrics
RMSE
MAE
Recall@K
NDCG@K
Friend-Aware Engagement Rate

##📜 License
This project is developed for academic and educational purposes.
All rights reserved by Team Nuvie.

