/**
 * Dashboard Page — Summary stats + charts + recent alerts
 * Author: Poshith
 */
import React, { useEffect, useState } from "react";
import { Row, Col, Card, Statistic, Table, Tag, Typography } from "antd";
import {
  HeartOutlined,
  AlertOutlined,
  SafetyOutlined,
  MedicineBoxOutlined,
} from "@ant-design/icons";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts";
import { dashboardService } from "../services/dashboardService";

const { Title } = Typography;
const COLORS = ["#52c41a", "#cf1322"];

export default function Dashboard() {
  const [stats, setStats] = useState({});
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    dashboardService.getStats().then(setStats).catch(console.error);
    dashboardService
      .getRecentAlerts()
      .then((d) => setAlerts(d.alerts || []))
      .catch(console.error);
  }, []);

  const healthPieData = [
    { name: "Healthy", value: stats.healthy || 0 },
    { name: "Sick", value: stats.sick || 0 },
  ];

  const alertColumns = [
    { title: "Cattle", dataIndex: "cattle_name", key: "cattle_name",
      render: (v, r) => v || r.cattle_id },
    { title: "Type", dataIndex: "type", key: "type" },
    {
      title: "Severity",
      dataIndex: "severity",
      key: "severity",
      render: (s) => (
        <Tag color={s === "high" ? "red" : s === "medium" ? "orange" : "blue"}>
          {s?.toUpperCase()}
        </Tag>
      ),
    },
    { title: "Message", dataIndex: "message", key: "message", ellipsis: true },
    {
      title: "Status",
      dataIndex: "status",
      key: "status",
      render: (s) => (
        <Tag color={s === "resolved" ? "green" : "volcano"}>{s}</Tag>
      ),
    },
  ];

  return (
    <div>
      <Title level={3}>Dashboard</Title>
      <Row gutter={16} style={{ marginTop: 16 }}>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="Total Cattle"
              value={stats.total_cattle || 0}
              prefix={<HeartOutlined />}
            />
          </Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="Healthy"
              value={stats.healthy || 0}
              valueStyle={{ color: "#3f8600" }}
              prefix={<MedicineBoxOutlined />}
            />
          </Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="Active Alerts"
              value={stats.active_alerts || 0}
              prefix={<AlertOutlined />}
              valueStyle={{ color: "#cf1322" }}
            />
          </Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="Pending Claims"
              value={stats.pending_claims || 0}
              prefix={<SafetyOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginTop: 24 }}>
        <Col xs={24} md={8}>
          <Card title="Herd Health">
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={healthPieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={80}
                  paddingAngle={4}
                  dataKey="value"
                  label>
                  {healthPieData.map((_, i) => (
                    <Cell key={i} fill={COLORS[i]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </Col>
        <Col xs={24} md={16}>
          <Card title="Recent Health Alerts">
            <Table
              dataSource={alerts}
              columns={alertColumns}
              rowKey="_id"
              pagination={false}
              size="small"
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
}
