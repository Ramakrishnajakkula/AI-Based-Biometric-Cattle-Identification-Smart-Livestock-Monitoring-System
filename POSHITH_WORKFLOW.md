# Poshith — Frontend & Dashboard Lead Workflow

## Role: React Dashboard + Real-time Monitoring + UI/UX

**Member:** Poshith
**Module:** `frontend/`
**Python Version:** 3.12 (for project-wide compatibility)
**Primary Tech:** React 18, Vite 5, Socket.IO Client, Recharts, React-Leaflet, Ant Design

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                 POSHITH's FRONTEND ARCHITECTURE                         │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  REACT APPLICATION (Vite + React 18)                               │   │
│  │                                                                     │   │
│  │  ┌──────────────────────────────────────────────────────────────┐  │   │
│  │  │  App.jsx (Root)                                               │  │   │
│  │  │  ├── AuthContext (JWT token management)                       │  │   │
│  │  │  ├── React Router v6                                          │  │   │
│  │  │  └── Layout (Navbar + Sidebar + Content)                      │  │   │
│  │  └──────────────────────────────────────────────────────────────┘  │   │
│  │                                                                     │   │
│  │  ┌──────────────────────────────────────────────────────────────┐  │   │
│  │  │  PAGES                                                        │  │   │
│  │  │                                                                │  │   │
│  │  │  /                      → Dashboard.jsx                       │  │   │
│  │  │  │                        ├── SensorCard (×N cattle)           │  │   │
│  │  │  │                        ├── SensorChart (live graphs)        │  │   │
│  │  │  │                        ├── AlertSummary                     │  │   │
│  │  │  │                        └── QuickStats                      │  │   │
│  │  │  │                                                             │  │   │
│  │  │  /animals               → AnimalRegistry.jsx                  │  │   │
│  │  │  │                        ├── SearchBar + Filters              │  │   │
│  │  │  │                        └── AnimalCard (grid/list)           │  │   │
│  │  │  │                                                             │  │   │
│  │  │  /animals/:id           → AnimalDetail.jsx                    │  │   │
│  │  │  │                        ├── Animal info + photo              │  │   │
│  │  │  │                        ├── Sensor history charts            │  │   │
│  │  │  │                        ├── Health records                   │  │   │
│  │  │  │                        └── Insurance info                   │  │   │
│  │  │  │                                                             │  │   │
│  │  │  /health                → HealthAlerts.jsx                    │  │   │
│  │  │  │                        ├── Alert list (severity sorted)     │  │   │
│  │  │  │                        └── HealthAlertCard with images      │  │   │
│  │  │  │                                                             │  │   │
│  │  │  /insurance             → InsuranceClaims.jsx                 │  │   │
│  │  │  │                        ├── Claims table                     │  │   │
│  │  │  │                        ├── Verification status              │  │   │
│  │  │  │                        └── New claim form                   │  │   │
│  │  │  │                                                             │  │   │
│  │  │  /map                   → LiveMap.jsx                         │  │   │
│  │  │  │                        ├── Leaflet map                      │  │   │
│  │  │  │                        ├── Cattle markers (real-time GPS)    │  │   │
│  │  │  │                        └── Geofence boundaries              │  │   │
│  │  │  │                                                             │  │   │
│  │  │  /identify              → Identify.jsx                        │  │   │
│  │  │  │                        ├── ImageUploader                    │  │   │
│  │  │  │                        ├── Result display                   │  │   │
│  │  │  │                        └── Confidence meter                 │  │   │
│  │  │  │                                                             │  │   │
│  │  │  /login                 → Login.jsx                           │  │   │
│  │  │  /register              → Register.jsx                        │  │   │
│  │  └──────────────────────────────────────────────────────────────┘  │   │
│  │                                                                     │   │
│  │  ┌──────────────────────────────────────────────────────────────┐  │   │
│  │  │  DATA LAYER                                                   │  │   │
│  │  │                                                                │  │   │
│  │  │  services/api.js        ──Axios──▶  Flask REST API (:5000)    │  │   │
│  │  │  hooks/useSocket.js     ──WS──▶  Flask-SocketIO (:5000)       │  │   │
│  │  │  hooks/useSensorData.js ──▶  Combines REST + WebSocket data   │  │   │
│  │  │  context/AuthContext    ──▶  JWT token store (localStorage)    │  │   │
│  │  └──────────────────────────────────────────────────────────────┘  │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                          │
├──────────────────────────────────────────────────────────────────────────┤
│  COMPONENT HIERARCHY                                                     │
│                                                                          │
│  <App>                                                                   │
│  ├── <AuthProvider>                                                      │
│  │   ├── <BrowserRouter>                                                 │
│  │   │   ├── <Navbar />                      (always visible)            │
│  │   │   ├── <Sidebar />                     (collapsible)               │
│  │   │   └── <Routes>                                                    │
│  │   │       ├── <Dashboard />               (protected)                 │
│  │   │       │   ├── <QuickStats />                                      │
│  │   │       │   ├── <SensorCard />  ×N                                  │
│  │   │       │   ├── <SensorChart />                                     │
│  │   │       │   └── <AlertSummary />                                    │
│  │   │       ├── <AnimalRegistry />          (protected)                 │
│  │   │       │   └── <AnimalCard />  ×N                                  │
│  │   │       ├── <AnimalDetail />             (protected)                │
│  │   │       ├── <HealthAlerts />             (protected)                │
│  │   │       │   └── <HealthAlertCard /> ×N                              │
│  │   │       ├── <InsuranceClaims />          (protected)                │
│  │   │       │   └── <InsuranceClaimCard /> ×N                           │
│  │   │       ├── <LiveMap />                  (protected)                │
│  │   │       │   └── <MapView />                                         │
│  │   │       ├── <Identify />                 (protected)                │
│  │   │       │   └── <ImageUploader />                                   │
│  │   │       ├── <Login />                    (public)                   │
│  │   │       └── <Register />                 (public)                   │
│  │   │                                                                   │
└──────────────────────────────────────────────────────────────────────────┘
```

### Real-time Data Flow

```
Flask-SocketIO (:5000)
    │
    ├── Event: "sensor_update"
    │   └──▶ useSensorData hook ──▶ SensorCard + SensorChart (re-render)
    │
    ├── Event: "health_alert"
    │   └──▶ Dashboard AlertSummary ──▶ Toast notification
    │
    ├── Event: "geofence_breach"
    │   └──▶ LiveMap ──▶ Marker turns red + alert popup
    │
    └── Event: "device_status"
        └──▶ SensorCard ──▶ Online/Offline indicator
```

---

## Folder Structure (Poshith's Files)

```
cap/
├── frontend/
│   ├── public/
│   │   ├── index.html                 # HTML entry point
│   │   ├── favicon.ico                # App icon
│   │   └── cattle-logo.svg            # Logo asset
│   │
│   ├── src/
│   │   ├── components/                # 🧩 Reusable UI Components
│   │   │   ├── Navbar.jsx             #   Top navigation bar
│   │   │   ├── Sidebar.jsx            #   Side navigation menu
│   │   │   ├── SensorCard.jsx         #   Single sensor reading card
│   │   │   ├── SensorChart.jsx        #   Time-series line chart (Recharts)
│   │   │   ├── AnimalCard.jsx         #   Animal summary card (grid item)
│   │   │   ├── HealthAlertCard.jsx    #   Health alert card with image
│   │   │   ├── InsuranceClaimCard.jsx #   Insurance claim display
│   │   │   ├── MapView.jsx            #   Leaflet map wrapper
│   │   │   ├── ImageUploader.jsx      #   Drag-drop image upload
│   │   │   ├── QuickStats.jsx         #   Dashboard stat counters
│   │   │   ├── AlertSummary.jsx       #   Recent alerts widget
│   │   │   ├── ConfidenceMeter.jsx    #   Visual confidence score
│   │   │   ├── LoadingSpinner.jsx     #   Loading state component
│   │   │   └── ProtectedRoute.jsx     #   Auth guard wrapper
│   │   │
│   │   ├── pages/                     # 📄 Page-Level Components
│   │   │   ├── Dashboard.jsx          #   Main dashboard (default page)
│   │   │   ├── AnimalRegistry.jsx     #   List all cattle with search
│   │   │   ├── AnimalDetail.jsx       #   Single animal full view
│   │   │   ├── HealthAlerts.jsx       #   All health alerts
│   │   │   ├── InsuranceClaims.jsx    #   Insurance management
│   │   │   ├── LiveMap.jsx            #   GPS tracking map
│   │   │   ├── Identify.jsx           #   Upload image for ID
│   │   │   ├── Login.jsx              #   Login form
│   │   │   └── Register.jsx           #   Register form
│   │   │
│   │   ├── hooks/                     # 🪝 Custom React Hooks
│   │   │   ├── useSensorData.js       #   Subscribe to real-time sensor data
│   │   │   ├── useSocket.js           #   Socket.IO connection manager
│   │   │   ├── useAuth.js             #   Auth state hook
│   │   │   └── useApi.js              #   Generic API fetch hook
│   │   │
│   │   ├── services/                  # 📡 API Communication
│   │   │   ├── api.js                 #   Axios instance with base URL + JWT
│   │   │   ├── cattleService.js       #   Cattle CRUD API calls
│   │   │   ├── sensorService.js       #   Sensor data API calls
│   │   │   ├── healthService.js       #   Health alerts API calls
│   │   │   ├── insuranceService.js    #   Insurance API calls
│   │   │   ├── identifyService.js     #   Image identification API calls
│   │   │   └── authService.js         #   Login/Register API calls
│   │   │
│   │   ├── context/                   # 🌐 React Context Providers
│   │   │   └── AuthContext.jsx        #   Auth state + JWT management
│   │   │
│   │   ├── utils/                     # 🔧 Helper Functions
│   │   │   ├── helpers.js             #   Date formatting, number rounding
│   │   │   ├── constants.js           #   API URLs, sensor thresholds
│   │   │   └── colors.js              #   Theme colors, status colors
│   │   │
│   │   ├── assets/                    # 🎨 Static Assets
│   │   │   ├── images/
│   │   │   └── styles/
│   │   │       └── global.css         #   Global styles
│   │   │
│   │   ├── App.jsx                    #   Root component with Router
│   │   ├── App.css                    #   App-level styles
│   │   └── main.jsx                   #   React DOM entry point
│   │
│   ├── package.json                   # NPM dependencies
│   ├── vite.config.js                 # Vite build configuration
│   ├── .env                           # VITE_API_URL=http://localhost:5000
│   └── .eslintrc.json                 # ESLint configuration
```

---

## Dependencies (package.json)

```json
{
  "name": "cattle-monitoring-dashboard",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.26.0",
    "axios": "^1.7.0",
    "socket.io-client": "^4.7.0",
    "recharts": "^2.12.0",
    "react-leaflet": "^4.2.0",
    "leaflet": "^1.9.0",
    "antd": "^5.20.0",
    "@ant-design/icons": "^5.4.0",
    "react-dropzone": "^14.2.0",
    "dayjs": "^1.11.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.0",
    "vite": "^5.4.0",
    "eslint": "^9.0.0",
    "eslint-plugin-react": "^7.35.0"
  }
}
```

---

## Setup Instructions

```bash
# 1. Install Node.js (v20 LTS recommended)
# Download from https://nodejs.org/

# 2. Verify Node.js
node --version    # v20.x.x
npm --version     # 10.x.x

# 3. Navigate to frontend folder
cd cap/frontend

# 4. Install dependencies
npm install

# 5. Create .env file
# frontend/.env
# VITE_API_URL=http://localhost:5000
# VITE_SOCKET_URL=http://localhost:5000

# 6. Start development server
npm run dev
# Opens at http://localhost:5173

# 7. Ensure Akash's backend is running at :5000
# (Otherwise, pages will show loading/error states)

# ===== Python 3.12 (for project compatibility) =====
# Poshith should also have Python 3.12 installed for running
# backend/scripts during integration testing
cd cap
python -m venv venv
venv\Scripts\activate
pip install -r requirements-common.txt
```

---

## 4-Week Schedule

### WEEK 1 (Feb 11–17): React Setup + Layout + Routing

| Day | Date   | Tasks                                                                                         | Deliverable             |
| --- | ------ | --------------------------------------------------------------------------------------------- | ----------------------- |
| Tue | Feb 11 | Install Node.js 20 LTS, create Vite + React project, install all npm packages                 | Project scaffolded      |
| Wed | Feb 12 | Build `Navbar.jsx` (logo, nav links, user menu) + `Sidebar.jsx` (collapsible menu with icons) | Navigation components   |
| Thu | Feb 13 | Set up React Router v6 — all routes defined. Create `ProtectedRoute.jsx` for auth guard       | Routing working         |
| Fri | Feb 14 | Build `Login.jsx` + `Register.jsx` pages with Ant Design forms                                | Auth pages ready        |
| Sat | Feb 15 | Build `AuthContext.jsx` — JWT storage, login/logout state, axios interceptor for auth header  | Auth context working    |
| Sun | Feb 16 | Build `api.js` (axios instance), `authService.js`. Test login flow with Akash's backend       | Auth integration tested |
| Mon | Feb 17 | Global styles, theme colors, responsive layout structure                                      | ✅ App shell complete   |

**Coordination:**

- Get from **Akash**: API base URL, auth endpoints, response format
- Agree on standard API response structure

---

### WEEK 2 (Feb 18–24): Core Pages + Real-time

| Day | Date   | Tasks                                                                                                     | Deliverable               |
| --- | ------ | --------------------------------------------------------------------------------------------------------- | ------------------------- |
| Tue | Feb 18 | Build `Dashboard.jsx` — layout with `QuickStats` (total cattle, alerts, online devices)                   | Dashboard layout          |
| Wed | Feb 19 | Build `SensorCard.jsx` (single sensor reading with icon + unit) + `SensorChart.jsx` (Recharts line chart) | Sensor display components |
| Thu | Feb 20 | Build `useSocket.js` hook — connect to Flask-SocketIO, handle reconnection                                | WebSocket hook ready      |
| Fri | Feb 21 | Build `useSensorData.js` — combine REST (history) + WebSocket (live) sensor data                          | Real-time data hook       |
| Sat | Feb 22 | Build `AnimalRegistry.jsx` — grid of `AnimalCard.jsx` with search/filter. Build `cattleService.js`        | Animal registry page      |
| Sun | Feb 23 | Build `AnimalDetail.jsx` — full animal profile with sensor history charts, health records, insurance info | Animal detail page        |
| Mon | Feb 24 | Build `LiveMap.jsx` — React-Leaflet map with cattle markers at GPS positions. Real-time marker updates    | ✅ Map + core pages done  |

**Coordination:**

- With **Akash**: Test all API endpoints from frontend
- With **Jaswanth**: Verify real-time sensor data format over WebSocket

---

### WEEK 3 (Feb 25–Mar 3): Feature Pages + Integration

| Day | Date   | Tasks                                                                                             | Deliverable                 |
| --- | ------ | ------------------------------------------------------------------------------------------------- | --------------------------- |
| Tue | Feb 25 | Build `HealthAlerts.jsx` — list view with severity badges, images, timestamps                     | Health page ready           |
| Wed | Feb 26 | Build `Identify.jsx` — `ImageUploader.jsx` (drag-drop), result display with `ConfidenceMeter.jsx` | Identification page ready   |
| Thu | Feb 27 | Build `InsuranceClaims.jsx` — claims table, verification status, new claim form                   | Insurance page ready        |
| Fri | Feb 28 | Connect real-time alerts — toast notifications for health alerts, geofence breaches               | Alert notifications working |
| Sat | Mar 1  | End-to-end testing — all pages talking to live backend with sensor data flowing                   | Full integration test       |
| Sun | Mar 2  | Geofence visualization on map — draw farm boundaries, color-code breach markers                   | Map features enhanced       |
| Mon | Mar 3  | Fix integration bugs, adjust API call error handling                                              | ✅ All pages integrated     |

**Coordination:**

- With **Akash**: Fix any API format issues
- With **Aditi**: Verify health alert data renders correctly
- With **Ramakrishna**: Test identification flow (upload → result)

---

### WEEK 4 (Mar 4–11): Polish & Responsive Design

| Day | Date   | Tasks                                                                                 | Deliverable            |
| --- | ------ | ------------------------------------------------------------------------------------- | ---------------------- |
| Tue | Mar 4  | Responsive design — mobile/tablet breakpoints for all pages                           | Mobile-friendly        |
| Wed | Mar 5  | Loading states (spinners, skeleton screens), empty states, error states for all pages | UX polish              |
| Thu | Mar 6  | Dashboard enhancements — auto-refresh interval, date range selector for charts        | Enhanced dashboard     |
| Fri | Mar 7  | Accessibility improvements — keyboard navigation, aria labels, color contrast         | Accessible             |
| Sat | Mar 8  | Build production bundle (`npm run build`), test optimized build                       | Production build ready |
| Sun | Mar 9  | Full team demo — walk through every page and feature                                  | Demo ready             |
| Mon | Mar 11 | Final CSS polish, code cleanup, commit                                                | ✅ Complete            |

---

## Page Wireframes

```
┌──────────────────────────────────────────────────────────────────┐
│  DASHBOARD                                                        │
│                                                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │ 🐄 25    │ │ ⚠️ 3     │ │ 📡 22    │ │ 🛡️ 5     │            │
│  │ Total    │ │ Active   │ │ Online   │ │ Claims   │            │
│  │ Cattle   │ │ Alerts   │ │ Devices  │ │ Pending  │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
│                                                                    │
│  ┌─────────────────────────────┐ ┌────────────────────────────┐  │
│  │  LIVE SENSOR READINGS       │ │  RECENT HEALTH ALERTS      │  │
│  │                              │ │                            │  │
│  │  CTL-001  38.5°C  72bpm    │ │  ⚠️ CTL-003 Fever 40.1°C  │  │
│  │  CTL-002  38.2°C  68bpm    │ │  ⚠️ CTL-007 Low activity   │  │
│  │  CTL-003  40.1°C  95bpm ⚠️ │ │  🔴 CTL-012 Device offline │  │
│  │  ...                        │ │                            │  │
│  └─────────────────────────────┘ └────────────────────────────┘  │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  TEMPERATURE TREND (Last 24 Hours)                           │  │
│  │                                                               │  │
│  │  40°C ─ ─ ─ ─ ─ ─ ─ ─ ─ ⚠️─ ─ ─ ─ ─ ─ ─ ─ threshold      │  │
│  │  39°C      ╱\                                                 │  │
│  │  38°C ────╱──\───────────────────────────                    │  │
│  │  37°C                                                         │  │
│  │       06:00  09:00  12:00  15:00  18:00  21:00               │  │
│  └──────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  IDENTIFY PAGE                                                    │
│                                                                    │
│  ┌──────────────────────────┐  ┌──────────────────────────────┐  │
│  │                          │  │  RESULT                       │  │
│  │  ┌────────────────────┐  │  │                               │  │
│  │  │                    │  │  │  ✅ Match Found!              │  │
│  │  │   Drop image here  │  │  │                               │  │
│  │  │   or click to      │  │  │  Cattle ID: CTL-001           │  │
│  │  │   browse            │  │  │  Name: Lakshmi               │  │
│  │  │                    │  │  │  Breed: Gir                   │  │
│  │  │   📷               │  │  │  Owner: Raju                  │  │
│  │  │                    │  │  │                               │  │
│  │  └────────────────────┘  │  │  Confidence: ████████░░ 87%   │  │
│  │                          │  │                               │  │
│  │  [Upload & Identify]     │  │  [View Full Profile →]       │  │
│  └──────────────────────────┘  └──────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  LIVE MAP                                                         │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                               │  │
│  │            ╭─────────────────────╮                            │  │
│  │           ╱   FARM BOUNDARY      ╲                           │  │
│  │          │                        │                           │  │
│  │          │   🐄 CTL-001           │                           │  │
│  │          │        🐄 CTL-002      │                           │  │
│  │          │   🐄 CTL-003           │                           │  │
│  │          │                        │                           │  │
│  │           ╲                      ╱                            │  │
│  │            ╰─────────────────────╯                            │  │
│  │                                                               │  │
│  │                          🔴 CTL-007 (ESCAPED!)                │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  Legend: 🟢 Normal  🟡 Alert  🔴 Geofence Breach                 │
└──────────────────────────────────────────────────────────────────┘
```

---

## Key Technical Decisions

| Decision      | Choice                   | Why                                                       |
| ------------- | ------------------------ | --------------------------------------------------------- |
| Build tool    | Vite 5                   | Fastest HMR, modern, CRA deprecated                       |
| UI framework  | React 18                 | Team familiarity, large ecosystem                         |
| Component lib | Ant Design 5             | Professional look, rich components (tables, forms, cards) |
| Charts        | Recharts                 | React-native, responsive, easy time-series                |
| Maps          | React-Leaflet            | Free, open-source, customizable markers                   |
| Real-time     | Socket.IO client         | Matches Flask-SocketIO backend                            |
| HTTP client   | Axios                    | Interceptors for JWT, request/response transform          |
| Routing       | React Router v6          | Standard, supports nested routes                          |
| State         | React Context + Hooks    | Sufficient for this app size (no Redux needed)            |
| Styling       | Ant Design + CSS modules | Consistent theming with component library                 |

---

## Verification Checklist

- [ ] Vite + React project running (`npm run dev`)
- [ ] All routes navigable (9 pages)
- [ ] Login/Register flow working with JWT
- [ ] Dashboard shows live sensor data
- [ ] Sensor charts update in real-time
- [ ] Animal registry displays all cattle from API
- [ ] Animal detail shows sensors + health + insurance
- [ ] Map shows GPS positions with markers
- [ ] Geofence boundaries drawn on map
- [ ] Image upload → identification result displayed
- [ ] Health alerts page lists all alerts
- [ ] Insurance claims page with verification status
- [ ] Toast notifications for real-time alerts
- [ ] Responsive design (mobile/tablet/desktop)
- [ ] Loading/error/empty states on all pages
- [ ] Production build works (`npm run build`)
- [ ] CORS working with Flask backend
