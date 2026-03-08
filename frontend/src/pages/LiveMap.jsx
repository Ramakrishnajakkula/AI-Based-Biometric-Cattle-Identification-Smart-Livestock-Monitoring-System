/**
 * Live Map Page — Cattle GPS positions on Leaflet map (polling)
 * Author: Poshith
 */
import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { Card, Spin } from "antd";
import L from "leaflet";
import api from "../services/api";
import "leaflet/dist/leaflet.css";

/* Fix default marker icons in bundled builds */
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

const DEFAULT_CENTER = [17.385, 78.4867]; // Hyderabad

export default function LiveMap() {
  const [positions, setPositions] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchPositions = async () => {
    try {
      const { data } = await api.get("/sensors/gps");
      setPositions(data.positions || []);
    } catch (err) {
      console.error("Failed to load GPS data", err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchPositions();
    const interval = setInterval(fetchPositions, 5000); // poll every 5s
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h2>Live GPS Tracking</h2>
      <Card style={{ marginTop: 16 }}>
        {loading ? (
          <Spin style={{ display: "block", textAlign: "center", padding: 40 }} />
        ) : (
          <div style={{ height: "70vh" }}>
            <MapContainer
              center={DEFAULT_CENTER}
              zoom={15}
              style={{ height: "100%", width: "100%" }}>
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution="&copy; OpenStreetMap contributors"
              />
              {positions.map((pos, idx) => (
                <Marker key={idx} position={[pos.lat, pos.lng]}>
                  <Popup>
                    <strong>{pos.name || pos.cattle_id || `Cattle ${idx + 1}`}</strong>
                    <br />
                    Lat: {pos.lat.toFixed(4)}, Lng: {pos.lng.toFixed(4)}
                  </Popup>
                </Marker>
              ))}
            </MapContainer>
          </div>
        )}
      </Card>
    </div>
  );
}
