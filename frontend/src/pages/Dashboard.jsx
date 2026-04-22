/**
 * Dashboard Page — Summary stats + charts + recent alerts
 * Author: Poshith
 */
import React, { useEffect, useState } from "react";
import { Row, Col, Card, Statistic, Table, Tag, Spin, Progress } from "antd";
import {
  HeartOutlined,
  AlertOutlined,
  SafetyOutlined,
  RiseOutlined,
  CheckCircleFilled,
  WarningFilled,
} from "@ant-design/icons";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import { dashboardService } from "../services/dashboardService";
import { sensorService } from "../services/sensorService";
import dayjs from "dayjs";

const ALERT_COLORS = { high: "#f5222d", medium: "#fa8c16", low: "#1890ff" };

function StatCard({ title, value, suffix, icon, color, sub }) {
  return (
    <Card
      style={{
        borderRadius: 12,
        boxShadow: "0 2px 12px rgba(0,0,0,0.07)",
        borderTop: `4px solid ${color}`,
      }}
    >
      <Statistic
        title={<span style={{ color: "#666", fontWeight: 500 }}>{title}</span>}
        value={value ?? "—"}
        suffix={suffix}
        prefix={React.cloneElement(icon, { style: { color } })}
        valueStyle={{ color, fontSize: 32, fontWeight: 700 }}
      />
      {sub && <div style={{ marginTop: 4, color: "#888", fontSize: 12 }}>{sub}</div>}
    </Card>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState({});
  const [alerts, setAlerts] = useState([]);
  const [tempHistory, setTempHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      dashboardService.getStats().catch(() => ({})),
      dashboardService.getRecentAlerts().catch(() => ({ alerts: [] })),
      sensorService.getHistory("CTL-001", "temperature", 24).catch(() => ({ readings: [] })),
    ]).then(([s, a, temp]) => {
      setStats(s);
      setAlerts((a.alerts || []).slice(0, 5));
      // Format timestamps for chart
      const formatted = (temp.readings || []).map((r) => ({
        time: dayjs(r.timestamp).format("HH:mm"),
        value: r.data?.value,
      }));
      setTempHistory(formatted);
      setLoading(false);
    });
  }, []);

  const healthPieData = [
    { name: "Healthy", value: stats.healthy || 0 },
    { name: "Sick", value: stats.sick || 0 },
  ];

  const alertColumns = [
    {
      title: "Cattle",
      dataIndex: "cattle_name",
      key: "cattle_name",
      render: (n, r) => n || r.cattle_id,
    },
    {
      title: "Type",
      dataIndex: "type",
      key: "type",
      render: (t) => t?.replace(/_/g, " "),
    },
    {
      title: "Severity",
      dataIndex: "severity",
      key: "severity",
      render: (s) => (
        <Tag color={ALERT_COLORS[s] || "blue"}>{s?.toUpperCase()}</Tag>
      ),
    },
    {
      title: "Message",
      dataIndex: "message",
      key: "message",
      ellipsis: true,
    },
  ];

  if (loading)
    return (
      <div style={{ textAlign: "center", padding: 80 }}>
        <Spin size="large" />
      </div>
    );

  return (
    <div>
      <h2 style={{ marginBottom: 20, fontWeight: 700, fontSize: 22 }}>
        📊 Dashboard Overview
      </h2>

      {/* KPI Cards */}
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="Total Cattle"
            value={stats.total_cattle}
            icon={<HeartOutlined />}
            color="#52c41a"
            sub="Registered in system"
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="Healthy"
            value={stats.healthy}
            icon={<CheckCircleFilled />}
            color="#1890ff"
            sub={`${stats.total_cattle ? Math.round((stats.healthy / stats.total_cattle) * 100) : 0}% of herd`}
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="Active Alerts"
            value={stats.active_alerts}
            icon={<AlertOutlined />}
            color="#f5222d"
            sub="Require attention"
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="Pending Claims"
            value={stats.pending_claims}
            icon={<SafetyOutlined />}
            color="#faad14"
            sub="Insurance claims"
          />
        </Col>
      </Row>

      {/* Charts */}
      <Row gutter={[16, 16]} style={{ marginTop: 20 }}>
        <Col xs={24} lg={16}>
          <Card
            title={<span><RiseOutlined style={{ color: "#fa541c", marginRight: 8 }} />Temperature Trend – Lakshmi (CTL-001)</span>}
            style={{ borderRadius: 12, boxShadow: "0 2px 12px rgba(0,0,0,0.07)" }}
          >
            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={tempHistory} margin={{ top: 5, right: 20, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="tempGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#fa541c" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#fa541c" stopOpacity={0.02} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f5f5f5" />
                <XAxis dataKey="time" tick={{ fontSize: 11 }} />
                <YAxis domain={[37, 41]} unit="°C" tick={{ fontSize: 11 }} width={50} />
                <Tooltip formatter={(v) => [`${v}°C`, "Temperature"]} />
                <Area
                  type="monotone"
                  dataKey="value"
                  stroke="#fa541c"
                  strokeWidth={2}
                  fill="url(#tempGrad)"
                  dot={false}
                  name="Temp °C"
                />
              </AreaChart>
            </ResponsiveContainer>
          </Card>
        </Col>
        <Col xs={24} lg={8}>
          <Card
            title="🐄 Herd Health"
            style={{ borderRadius: 12, boxShadow: "0 2px 12px rgba(0,0,0,0.07)" }}
          >
            <ResponsiveContainer width="100%" height={160}>
              <PieChart>
                <Pie
                  data={healthPieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={45}
                  outerRadius={70}
                  paddingAngle={4}
                  dataKey="value"
                >
                  <Cell fill="#52c41a" />
                  <Cell fill="#f5222d" />
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
            <div style={{ textAlign: "center", marginTop: 8 }}>
              <Progress
                percent={stats.total_cattle ? Math.round((stats.healthy / stats.total_cattle) * 100) : 0}
                strokeColor="#52c41a"
                trailColor="#f5222d"
                format={(p) => <span style={{ fontSize: 13, color: "#52c41a" }}>{p}% Healthy</span>}
              />
            </div>
          </Card>
        </Col>
      </Row>

      {/* Recent Alerts Table */}
      <Card
        title={<span><AlertOutlined style={{ color: "#f5222d", marginRight: 8 }} />Recent Health Alerts</span>}
        style={{ marginTop: 20, borderRadius: 12, boxShadow: "0 2px 12px rgba(0,0,0,0.07)" }}
        extra={<Tag color="red">{alerts.length} Active</Tag>}
      >
        <Table
          dataSource={alerts}
          columns={alertColumns}
          rowKey="_id"
          pagination={false}
          size="small"
          locale={{ emptyText: "✓ No active alerts" }}
        />
      </Card>
    </div>
  );
}
