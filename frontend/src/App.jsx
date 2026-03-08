/**
 * Root App Component — Layout + Routing
 * Author: Poshith
 */
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { ConfigProvider, theme } from "antd";
import AppLayout from "./components/Layout/AppLayout";
import Dashboard from "./pages/Dashboard";
import AnimalList from "./pages/AnimalList";
import AnimalDetail from "./pages/AnimalDetail";
import HealthAlerts from "./pages/HealthAlerts";
import InsuranceClaims from "./pages/InsuranceClaims";
import LiveMap from "./pages/LiveMap";
import IdentifyCattle from "./pages/IdentifyCattle";
import Login from "./pages/Login";
import { useAuth } from "./context/AuthContext";

function ProtectedRoute({ children }) {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" />;
}

export default function App() {
  return (
    <ConfigProvider
      theme={{
        algorithm: theme.defaultAlgorithm,
        token: { colorPrimary: "#52c41a" },
      }}>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <AppLayout>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/animals" element={<AnimalList />} />
                  <Route path="/animals/:id" element={<AnimalDetail />} />
                  <Route path="/health" element={<HealthAlerts />} />
                  <Route path="/insurance" element={<InsuranceClaims />} />
                  <Route path="/map" element={<LiveMap />} />
                  <Route path="/identify" element={<IdentifyCattle />} />
                </Routes>
              </AppLayout>
            </ProtectedRoute>
          }
        />
      </Routes>
    </ConfigProvider>
  );
}
