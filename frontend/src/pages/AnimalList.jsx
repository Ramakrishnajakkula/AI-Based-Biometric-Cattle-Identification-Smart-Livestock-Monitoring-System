/**
 * Animal List Page — Table of all registered cattle with registration modal
 * Author: Poshith
 */
import React, { useEffect, useState } from "react";
import {
  Table,
  Button,
  Tag,
  Input,
  Modal,
  Form,
  Select,
  InputNumber,
  message,
  Space,
  Badge,
  Tooltip,
} from "antd";
import {
  PlusOutlined,
  SearchOutlined,
  EyeOutlined,
  HeartOutlined,
} from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { cattleService } from "../services/cattleService";

const BREEDS = [
  "Gir", "Sahiwal", "Red Sindhi", "Tharparkar", "Ongole",
  "Hallikar", "Kankrej", "Deoni", "Rathi", "Hariana",
];

export default function AnimalList() {
  const [cattle, setCattle] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [form] = Form.useForm();
  const navigate = useNavigate();

  const fetchCattle = () => {
    setLoading(true);
    cattleService.list().then((d) => {
      setCattle(d.cattle || []);
      setLoading(false);
    }).catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchCattle();
  }, []);

  const handleRegister = async () => {
    try {
      const values = await form.validateFields();
      setSubmitting(true);
      await cattleService.create(values);
      message.success(`${values.name || values.tag_id} registered successfully!`);
      form.resetFields();
      setModalOpen(false);
      fetchCattle();
    } catch (err) {
      if (err?.errorFields) return; // validation error, don't show toast
      message.error("Failed to register cattle. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  const filtered = cattle.filter(
    (c) =>
      c.name?.toLowerCase().includes(search.toLowerCase()) ||
      c.tag_id?.toLowerCase().includes(search.toLowerCase()) ||
      c.breed?.toLowerCase().includes(search.toLowerCase())
  );

  const columns = [
    {
      title: "",
      dataIndex: "image_url",
      key: "image",
      width: 60,
      render: (url) => (
        <img
          src={url}
          alt="cattle"
          style={{
            width: 45,
            height: 45,
            borderRadius: "50%",
            objectFit: "cover",
            border: "2px solid #f0f0f0",
            background: "#fafafa",
          }}
          onError={(e) => {
            e.target.onerror = null;
            e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E🐄%3C/text%3E%3C/svg%3E";
          }}
        />
      ),
    },
    {
      title: "Tag ID",
      dataIndex: "tag_id",
      key: "tag_id",
      render: (t) => <strong style={{ fontFamily: "monospace" }}>{t}</strong>,
    },
    { title: "Name", dataIndex: "name", key: "name", render: (n) => n || <span style={{ color: "#bbb" }}>Unnamed</span> },
    { title: "Breed", dataIndex: "breed", key: "breed" },
    { title: "Age", dataIndex: "age_years", key: "age_years", render: (v) => v ? `${v} yr` : "—" },
    { title: "Weight", dataIndex: "weight_kg", key: "weight_kg", render: (v) => v ? `${v} kg` : "—" },
    { title: "Farm", dataIndex: "farm_id", key: "farm_id", render: (f) => <Tag>{f}</Tag> },
    {
      title: "Health",
      dataIndex: "health_status",
      key: "health_status",
      render: (s) => (
        <Badge
          status={s === "healthy" ? "success" : "error"}
          text={<Tag color={s === "healthy" ? "green" : "red"}>{s}</Tag>}
        />
      ),
    },
    {
      title: "Action",
      key: "action",
      render: (_, record) => (
        <Tooltip title="View details">
          <Button
            type="primary"
            ghost
            icon={<EyeOutlined />}
            size="small"
            onClick={() => navigate(`/animals/${record._id}`)}
          >
            View
          </Button>
        </Tooltip>
      ),
    },
  ];

  const healthyCnt = cattle.filter((c) => c.health_status === "healthy").length;
  const sickCnt = cattle.length - healthyCnt;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <div>
          <h2 style={{ margin: 0 }}>Registered Cattle</h2>
          <Space size={8} style={{ marginTop: 4 }}>
            <Tag color="green"><HeartOutlined /> {healthyCnt} Healthy</Tag>
            {sickCnt > 0 && <Tag color="red">⚠ {sickCnt} Need Attention</Tag>}
          </Space>
        </div>
        <Space>
          <Input
            placeholder="Search name, tag, breed…"
            prefix={<SearchOutlined />}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ width: 240 }}
            allowClear
          />
          <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalOpen(true)}>
            Register New
          </Button>
        </Space>
      </div>

      <Table
        dataSource={filtered}
        columns={columns}
        rowKey="_id"
        loading={loading}
        pagination={{ pageSize: 10, showSizeChanger: true }}
        size="middle"
        rowClassName={(r) => r.health_status !== "healthy" ? "row-sick" : ""}
      />

      <Modal
        title={<span><PlusOutlined /> Register New Cattle</span>}
        open={modalOpen}
        onOk={handleRegister}
        onCancel={() => { setModalOpen(false); form.resetFields(); }}
        okText="Register"
        confirmLoading={submitting}
        width={500}
      >
        <Form form={form} layout="vertical" style={{ marginTop: 8 }}>
          <Form.Item
            name="tag_id"
            label="Tag ID"
            rules={[{ required: true, message: "Tag ID is required" }]}
          >
            <Input placeholder="e.g. CTL-006" />
          </Form.Item>
          <Form.Item name="name" label="Name">
            <Input placeholder="e.g. Kamdhenu" />
          </Form.Item>
          <Form.Item
            name="breed"
            label="Breed"
            rules={[{ required: true, message: "Please select a breed" }]}
          >
            <Select placeholder="Select breed" showSearch>
              {BREEDS.map((b) => (
                <Select.Option key={b} value={b}>{b}</Select.Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item name="age_years" label="Age (years)">
            <InputNumber min={0} max={25} style={{ width: "100%" }} placeholder="e.g. 4" />
          </Form.Item>
          <Form.Item name="weight_kg" label="Weight (kg)">
            <InputNumber min={50} max={1000} style={{ width: "100%" }} placeholder="e.g. 350" />
          </Form.Item>
          <Form.Item name="farm_id" label="Farm ID">
            <Input placeholder="e.g. FARM-01" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}
