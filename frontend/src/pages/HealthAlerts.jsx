/**
 * Health Alerts Page — View and manage alerts
 * Author: Poshith
 */
import React, { useEffect, useState } from "react";
import { Table, Tag, Button, Select, Space } from "antd";
import api from "../services/api";

export default function HealthAlerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  const fetchAlerts = async () => {
    setLoading(true);
    const params = filter !== "all" ? { severity: filter } : {};
    const { data } = await api.get("/health/alerts", { params });
    setAlerts(data.alerts || []);
    setLoading(false);
  };

  useEffect(() => {
    fetchAlerts();
  }, [filter]);

  const handleResolve = async (alertId) => {
    await api.put(`/health/alerts/${alertId}/resolve`);
    fetchAlerts();
  };

  const columns = [
    { title: "Cattle ID", dataIndex: "cattle_id", key: "cattle_id" },
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
      title: "Action",
      key: "action",
      render: (_, r) => (
        <Button size="small" onClick={() => handleResolve(r._id)}>
          Resolve
        </Button>
      ),
    },
  ];

  return (
    <div>
      <Space
        style={{
          marginBottom: 16,
          display: "flex",
          justifyContent: "space-between",
        }}>
        <h2>Health Alerts</h2>
        <Select value={filter} onChange={setFilter} style={{ width: 150 }}>
          <Select.Option value="all">All</Select.Option>
          <Select.Option value="high">High</Select.Option>
          <Select.Option value="medium">Medium</Select.Option>
          <Select.Option value="low">Low</Select.Option>
        </Select>
      </Space>
      <Table
        dataSource={alerts}
        columns={columns}
        rowKey="_id"
        loading={loading}
      />
    </div>
  );
}
