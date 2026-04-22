/**
 * Admin Dashboard Page — System overview for admin users
 * Author: Poshith
 */
import React, { useEffect, useState } from "react";
import { Row, Col, Card, Statistic, Table, Tag, Badge } from "antd";
import {
  TeamOutlined,
  HeartOutlined,
  AlertOutlined,
  SafetyOutlined,
  CheckCircleOutlined,
} from "@ant-design/icons";
import { dashboardService } from "../services/dashboardService";
import { adminService } from "../services/adminService";

export default function AdminDashboard() {
  const [stats, setStats] = useState({});
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      dashboardService.getStats().catch(() => ({})),
      adminService.getUsers().catch(() => ({ users: [] })),
    ]).then(([s, u]) => {
      setStats(s);
      setUsers(u.users || []);
      setLoading(false);
    });
  }, []);

  const userColumns = [
    { title: "Name", dataIndex: "name", key: "name" },
    { title: "Email", dataIndex: "email", key: "email" },
    {
      title: "Role",
      dataIndex: "role",
      key: "role",
      render: (r) => (
        <Tag color={r === "admin" ? "gold" : "green"}>{r?.toUpperCase()}</Tag>
      ),
    },
    {
      title: "Joined",
      dataIndex: "created_at",
      key: "created_at",
      render: (v) => v ? new Date(v).toLocaleDateString() : "—",
    },
  ];

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>Admin Dashboard</h2>

      <Row gutter={[16, 16]}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Cattle"
              value={stats.total_cattle || 0}
              prefix={<HeartOutlined style={{ color: "#52c41a" }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Healthy Cattle"
              value={stats.healthy || 0}
              valueStyle={{ color: "#3f8600" }}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Active Alerts"
              value={stats.active_alerts || 0}
              valueStyle={{ color: "#cf1322" }}
              prefix={<AlertOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Pending Claims"
              value={stats.pending_claims || 0}
              prefix={<SafetyOutlined style={{ color: "#faad14" }} />}
            />
          </Card>
        </Col>
      </Row>

      <Card
        title={
          <span>
            <TeamOutlined style={{ marginRight: 8 }} />
            Registered Users
          </span>
        }
        style={{ marginTop: 24 }}
        extra={<Badge count={users.length} style={{ backgroundColor: "#52c41a" }} />}
      >
        <Table
          dataSource={users}
          columns={userColumns}
          rowKey="_id"
          loading={loading}
          pagination={false}
          size="middle"
        />
      </Card>
    </div>
  );
}
