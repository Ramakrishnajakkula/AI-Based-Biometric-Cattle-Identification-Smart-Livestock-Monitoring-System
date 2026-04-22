/**
 * Live Map Page — Real-time cattle GPS positions on Leaflet map
 * Loads initial positions via HTTP, then updates via REST polling
 * Author: Poshith
 */
import React, { useEffect, useState, useRef } from "react";
import { MapContainer, TileLayer, Marker, Popup, Circle } from "react-leaflet";
import { Card, Badge, Tag, Spin, Alert } from "antd";
import { EnvironmentOutlined } from "@ant-design/icons";
import L from "leaflet";
import api from "../services/api";
import "leaflet/dist/leaflet.css";

// Fix Leaflet default icon issue in Vite
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

const DEFAULT_CENTER = [17.385, 78.4867]; // Hyderabad
const COLORS = ["#52c41a", "#1890ff", "#faad14", "#f5222d", "#722ed1"];

function makeColoredIcon(color) {
  return L.divIcon({
    className: "",
    html: `<div style="
      width:32px; height:32px; 
      background:${color}; 
      border:3px solid white; 
      border-radius:50%; 
      display:flex; align-items:center; justify-content:center;
      box-shadow: 0 2px 8px rgba(0,0,0,0.4);
      font-size:16px;
    ">🐄</div>`,
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -16],
  });
}

export default function LiveMap() {
  const [positions, setPositions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const intervalRef = useRef(null);

  const fetchGPS = async () => {
    try {
      const { data } = await api.get("/sensors/gps");
      setPositions(data.positions || []);
      setLoading(false);
      setError(null);
    } catch (err) {
      setError("Failed to load GPS positions");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGPS();
    // Poll every 5 seconds for live updates
    intervalRef.current = setInterval(fetchGPS, 5000);
    return () => clearInterval(intervalRef.current);
  }, []);

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: 80 }}>
        <Spin size="large" />
        <p style={{ marginTop: 16, color: "#888" }}>Loading GPS positions...</p>
      </div>
    );
  }

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <h2 style={{ margin: 0 }}>
          <EnvironmentOutlined style={{ color: "#52c41a", marginRight: 8 }} />
          Live GPS Tracking
        </h2>
        <Badge
          count={positions.length}
          style={{ backgroundColor: "#52c41a" }}
          title="Active cattle"
        >
          <Tag color="green" style={{ fontSize: 13, padding: "4px 12px" }}>
            {positions.length} Cattle Online
          </Tag>
        </Badge>
      </div>

      {error && <Alert message={error} type="warning" showIcon style={{ marginBottom: 12 }} />}

      <Card
        bodyStyle={{ padding: 0, overflow: "hidden", borderRadius: 8 }}
        style={{ borderRadius: 8, overflow: "hidden" }}
      >
        <div style={{ height: "72vh" }}>
          <MapContainer
            center={DEFAULT_CENTER}
            zoom={16}
            style={{ height: "100%", width: "100%" }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution="&copy; OpenStreetMap contributors"
            />
            {positions.map((pos, i) => (
              <React.Fragment key={pos.cattle_id || i}>
                <Marker
                  position={[pos.lat, pos.lng]}
                  icon={makeColoredIcon(COLORS[i % COLORS.length])}
                >
                  <Popup>
                    <div style={{ minWidth: 160 }}>
                      <strong style={{ fontSize: 15 }}>🐄 {pos.name || pos.cattle_id}</strong>
                      <hr style={{ margin: "6px 0" }} />
                      <p style={{ margin: 0 }}>
                        <b>ID:</b> {pos.cattle_id}
                      </p>
                      <p style={{ margin: 0 }}>
                        <b>Lat:</b> {pos.lat?.toFixed(5)}
                      </p>
                      <p style={{ margin: 0 }}>
                        <b>Lng:</b> {pos.lng?.toFixed(5)}
                      </p>
                    </div>
                  </Popup>
                </Marker>
                <Circle
                  center={[pos.lat, pos.lng]}
                  radius={30}
                  pathOptions={{ color: COLORS[i % COLORS.length], fillOpacity: 0.08, weight: 1 }}
                />
              </React.Fragment>
            ))}
          </MapContainer>
        </div>
      </Card>

      {/* Legend */}
      <div style={{ marginTop: 12, display: "flex", gap: 12, flexWrap: "wrap" }}>
        {positions.map((pos, i) => (
          <Tag key={pos.cattle_id || i} color={COLORS[i % COLORS.length]}>
            🐄 {pos.name || pos.cattle_id}
          </Tag>
        ))}
      </div>
    </div>
  );
}
