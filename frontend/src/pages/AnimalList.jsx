/**
 * Animal List Page — Table of all registered cattle
 * Author: Poshith
 */
import React, { useEffect, useState } from "react";
import { Table, Button, Tag, Input } from "antd";
import { PlusOutlined, SearchOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { cattleService } from "../services/cattleService";

export default function AnimalList() {
  const [cattle, setCattle] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    cattleService.list().then((d) => {
      setCattle(d.cattle || []);
      setLoading(false);
    });
  }, []);

  const columns = [
    { title: "Tag ID", dataIndex: "tag_id", key: "tag_id" },
    { title: "Name", dataIndex: "name", key: "name" },
    { title: "Breed", dataIndex: "breed", key: "breed" },
    {
      title: "Health",
      dataIndex: "health_status",
      key: "health_status",
      render: (s) => <Tag color={s === "healthy" ? "green" : "red"}>{s}</Tag>,
    },
    {
      title: "Action",
      key: "action",
      render: (_, record) => (
        <a onClick={() => navigate(`/animals/${record._id}`)}>View</a>
      ),
    },
  ];

  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: 16,
        }}>
        <h2>Registered Cattle</h2>
        <Button type="primary" icon={<PlusOutlined />}>
          Register New
        </Button>
      </div>
      <Table
        dataSource={cattle}
        columns={columns}
        rowKey="_id"
        loading={loading}
      />
    </div>
  );
}
