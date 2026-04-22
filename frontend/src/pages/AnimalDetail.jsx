/**
 * Animal Detail Page — Individual cattle info + sensor charts
 * Author: Poshith
 */
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Card,
  Descriptions,
  Tabs,
  Tag,
  Spin,
  Row,
  Col,
  Statistic,
  Badge,
  Button,
  Empty,
} from "antd";
import {
  ArrowLeftOutlined,
  ThunderboltOutlined,
  HeartOutlined,
  EnvironmentOutlined,
  DashboardOutlined,
} from "@ant-design/icons";
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import { cattleService } from "../services/cattleService";
import { sensorService } from "../services/sensorService";
import dayjs from "dayjs";

function formatTime(ts) {
  try {
    return dayjs(ts).format("HH:mm");
  } catch {
    return ts?.slice(11, 16) || "";
  }
}

function SensorChart({ data, dataKey, color, domain, unit, label }) {
  if (!data || data.length === 0)
    return <Empty description="No sensor data" style={{ padding: 40 }} />;

  return (
    <ResponsiveContainer width="100%" height={260}>
      <AreaChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id={`color-${label}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor={color} stopOpacity={0.25} />
            <stop offset="95%" stopColor={color} stopOpacity={0.02} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis dataKey="timestamp" tickFormatter={formatTime} tick={{ fontSize: 11 }} />
        <YAxis domain={domain} unit={unit} tick={{ fontSize: 11 }} width={45} />
        <Tooltip
          formatter={(val) => [`${val}${unit}`, label]}
          labelFormatter={(l) => `Time: ${formatTime(l)}`}
        />
        <ReferenceLine y={domain?.[1] ? domain[1] * 0.9 : undefined} stroke="#ff4d4f" strokeDasharray="4 4" opacity={0.4} />
        <Area
          type="monotone"
          dataKey={dataKey}
          stroke={color}
          strokeWidth={2}
          fill={`url(#color-${label})`}
          dot={false}
          activeDot={{ r: 5 }}
          name={label}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}

export default function AnimalDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [cattle, setCattle] = useState(null);
  const [tempHistory, setTempHistory] = useState([]);
  const [hrHistory, setHrHistory] = useState([]);
  const [latestSensors, setLatestSensors] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      cattleService.getById(id),
      sensorService.getHistory(id, "temperature", 24).catch(() => ({ readings: [] })),
      sensorService.getHistory(id, "heartrate", 24).catch(() => ({ readings: [] })),
      sensorService.getLatest(id).catch(() => null),
    ]).then(([c, temp, hr, latest]) => {
      setCattle(c);
      // Flatten nested data so Recharts can access keys directly
      setTempHistory(
        (temp.readings || []).map((r) => ({
          timestamp: r.timestamp,
          value: r.data?.value ?? null,
        }))
      );
      setHrHistory(
        (hr.readings || []).map((r) => ({
          timestamp: r.timestamp,
          bpm: r.data?.bpm ?? null,
        }))
      );
      setLatestSensors(latest?.latest || null);
      setLoading(false);
    });
  }, [id]);

  if (loading)
    return (
      <div style={{ textAlign: "center", padding: 80 }}>
        <Spin size="large" />
      </div>
    );
  if (!cattle)
    return <Empty description="Cattle not found" style={{ padding: 60 }} />;

  const isHealthy = cattle.health_status === "healthy";
  const temp = latestSensors?.temperature?.data?.value;
  const hr = latestSensors?.heartrate?.data?.bpm;
  const activity = latestSensors?.activity?.data?.activity_level;

  const tabItems = [
    {
      key: "overview",
      label: (
        <span>
          <DashboardOutlined /> Overview
        </span>
      ),
      children: (
        <>
          <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
            <Col span={8}>
              <Card size="small" style={{ background: "#fff7e6", border: "1px solid #ffd591" }}>
                <Statistic
                  title="Temperature"
                  value={temp ?? "—"}
                  suffix="°C"
                  precision={1}
                  valueStyle={{ color: temp > 39.5 ? "#cf1322" : "#3f8600", fontSize: 28 }}
                  prefix={<ThunderboltOutlined />}
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card size="small" style={{ background: "#fff1f0", border: "1px solid #ffa39e" }}>
                <Statistic
                  title="Heart Rate"
                  value={hr ?? "—"}
                  suffix="bpm"
                  valueStyle={{ color: hr > 80 ? "#cf1322" : "#1890ff", fontSize: 28 }}
                  prefix={<HeartOutlined />}
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card size="small" style={{ background: "#f6ffed", border: "1px solid #b7eb8f" }}>
                <Statistic
                  title="Activity"
                  value={activity ?? "—"}
                  valueStyle={{ color: "#52c41a", fontSize: 20, textTransform: "capitalize" }}
                  prefix={<EnvironmentOutlined />}
                />
              </Card>
            </Col>
          </Row>

          <Card size="small" title="Temperature – Last 24 Hours">
            <SensorChart
              data={tempHistory}
              dataKey="value"
              color="#fa541c"
              domain={[36, 41]}
              unit="°C"
              label="Temperature"
            />
          </Card>
        </>
      ),
    },
    {
      key: "heartrate",
      label: (
        <span>
          <HeartOutlined /> Heart Rate
        </span>
      ),
      children: (
        <Card size="small" title="Heart Rate – Last 24 Hours">
          <SensorChart
            data={hrHistory}
            dataKey="bpm"
            color="#eb2f96"
            domain={[40, 100]}
            unit="bpm"
            label="Heart Rate"
          />
        </Card>
      ),
    },
    {
      key: "info",
      label: "Details",
      children: (
        <Descriptions bordered column={2} size="middle">
          <Descriptions.Item label="Tag ID">
            <strong>{cattle.tag_id}</strong>
          </Descriptions.Item>
          <Descriptions.Item label="Name">{cattle.name || "—"}</Descriptions.Item>
          <Descriptions.Item label="Breed">{cattle.breed}</Descriptions.Item>
          <Descriptions.Item label="Age">{cattle.age_years} years</Descriptions.Item>
          <Descriptions.Item label="Weight">{cattle.weight_kg} kg</Descriptions.Item>
          <Descriptions.Item label="Farm">{cattle.farm_id || "—"}</Descriptions.Item>
          <Descriptions.Item label="Health Status" span={2}>
            <Badge
              status={isHealthy ? "success" : "error"}
              text={
                <Tag color={isHealthy ? "green" : "red"} style={{ fontSize: 13 }}>
                  {cattle.health_status?.toUpperCase()}
                </Tag>
              }
            />
          </Descriptions.Item>
          <Descriptions.Item label="Registered">
            {cattle.created_at ? new Date(cattle.created_at).toLocaleDateString("en-IN") : "—"}
          </Descriptions.Item>
          <Descriptions.Item label="Last Updated">
            {cattle.updated_at ? new Date(cattle.updated_at).toLocaleDateString("en-IN") : "—"}
          </Descriptions.Item>
        </Descriptions>
      ),
    },
  ];

  return (
    <div>
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate("/animals")}
          type="text"
        />
        <div>
          <h2 style={{ margin: 0 }}>
            🐄 {cattle.name || cattle.tag_id}
          </h2>
          <span style={{ color: "#888", fontSize: 13 }}>{cattle.breed} • {cattle.tag_id}</span>
        </div>
        <Tag
          color={isHealthy ? "green" : "red"}
          style={{ marginLeft: "auto", fontSize: 13, padding: "4px 12px" }}
        >
          {isHealthy ? "✓ Healthy" : "⚠ Needs Attention"}
        </Tag>
      </div>

      <Tabs items={tabItems} type="card" />
    </div>
  );
}
