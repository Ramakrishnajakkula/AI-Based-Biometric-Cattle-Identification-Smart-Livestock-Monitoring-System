/**
 * Insurance Claims Page — List and create claims
 * Author: Poshith
 */
import React, { useEffect, useState } from "react";
import { Table, Button, Tag, Modal, Form, Input, Select } from "antd";
import api from "../services/api";

export default function InsuranceClaims() {
  const [claims, setClaims] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [form] = Form.useForm();

  const fetchClaims = async () => {
    setLoading(true);
    const { data } = await api.get("/insurance/claims");
    setClaims(data.claims || []);
    setLoading(false);
  };

  useEffect(() => {
    fetchClaims();
  }, []);

  const handleSubmit = async () => {
    const values = await form.validateFields();
    await api.post("/insurance/claims", values);
    setModalOpen(false);
    form.resetFields();
    fetchClaims();
  };

  const columns = [
    { title: "Cattle ID", dataIndex: "cattle_id", key: "cattle_id" },
    { title: "Type", dataIndex: "claim_type", key: "claim_type" },
    {
      title: "Amount",
      dataIndex: "amount",
      key: "amount",
      render: (v) => `₹${v}`,
    },
    {
      title: "Status",
      dataIndex: "status",
      key: "status",
      render: (s) => (
        <Tag
          color={
            s === "approved"
              ? "green"
              : s === "rejected"
                ? "red"
                : s === "under_review"
                  ? "orange"
                  : "blue"
          }>
          {s}
        </Tag>
      ),
    },
    {
      title: "Action",
      key: "action",
      render: (_, r) =>
        r.status === "pending" && (
          <Button
            size="small"
            onClick={() =>
              api.post(`/insurance/claims/${r._id}/verify`).then(fetchClaims)
            }>
            Verify
          </Button>
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
        <h2>Insurance Claims</h2>
        <Button type="primary" onClick={() => setModalOpen(true)}>
          New Claim
        </Button>
      </div>
      <Table
        dataSource={claims}
        columns={columns}
        rowKey="_id"
        loading={loading}
      />

      <Modal
        title="New Insurance Claim"
        open={modalOpen}
        onOk={handleSubmit}
        onCancel={() => setModalOpen(false)}>
        <Form form={form} layout="vertical">
          <Form.Item
            name="cattle_id"
            label="Cattle ID"
            rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item
            name="claim_type"
            label="Claim Type"
            rules={[{ required: true }]}>
            <Select>
              <Select.Option value="death">Death</Select.Option>
              <Select.Option value="illness">Illness</Select.Option>
              <Select.Option value="theft">Theft</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="amount"
            label="Amount (₹)"
            rules={[{ required: true }]}>
            <Input type="number" />
          </Form.Item>
          <Form.Item name="description" label="Description">
            <Input.TextArea rows={3} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}
