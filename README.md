# 📺 IPTV Player

Web app pour lire ton service IPTV via l'API Xtream Codes.
Stack : **Vue 3 + Vite + Tailwind** (frontend) | **Python FastAPI** (backend proxy)

---

## 🚀 Installation

### Prérequis
- Node.js 18+
- Python 3.10+

---

### 1. Backend (FastAPI)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Le backend tourne sur → http://localhost:8000

---

### 2. Frontend (Vue 3)

```bash
cd frontend
npm install
npm run dev
```

Le frontend tourne sur → http://localhost:5173

---

## 🔐 Connexion

Lance les deux serveurs, ouvre http://localhost:5173, et entre :
- **URL du serveur** : `http://ton-serveur.com:8080`
- **Username** : ton username Xtream
- **Password** : ton password Xtream

---

## 📁 Structure

```
iptv-app/
├── backend/
│   ├── main.py              # API FastAPI + proxy stream
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/
    │   │   └── xtream.js    # Appels API Xtream Codes
    │   ├── components/
    │   │   ├── VideoPlayer.vue    # Player HLS (hls.js)
    │   │   ├── ChannelList.vue    # Liste des chaînes
    │   │   └── CategorySidebar.vue
    │   ├── stores/
    │   │   └── iptv.js      # State global (Pinia)
    │   ├── views/
    │   │   ├── LoginView.vue
    │   │   ├── LiveTV.vue
    │   │   └── VOD.vue
    │   ├── App.vue
    │   ├── main.js
    │   └── style.css
    ├── index.html
    ├── vite.config.js        # Proxy /api → localhost:8000
    ├── tailwind.config.js
    └── package.json
```

---

## ⚙️ Comment ça marche

1. **Auth** : les credentials sont stockés dans `localStorage` et envoyés à chaque requête
2. **Proxy CORS** : tous les appels API et les streams passent par le backend FastAPI pour éviter les blocages CORS
3. **Player** : `hls.js` pour les streams HLS/M3U8, fallback natif pour Safari

---

## 🔧 Prochaines étapes possibles

- [ ] EPG (guide des programmes)
- [ ] Favoris (localStorage)
- [ ] Support MPEG-TS avec `mpegts.js`
- [ ] Séries / épisodes
- [ ] Mode plein écran amélioré
- [ ] PWA (installable sur mobile)
