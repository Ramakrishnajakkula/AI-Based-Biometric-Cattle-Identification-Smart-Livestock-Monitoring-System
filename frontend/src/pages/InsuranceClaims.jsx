/**
 * Insurance Claims Page — List, create, and verify claims
 * Author: Poshith
 */
import React, { useEffect, useState } from "react";
import {
  Table,
  Button,
  Tag,
  Modal,
  Form,
  Input,
  Select,
  InputNumber,
  Space,
  Tooltip,
  Badge,
  message,
  Alert,
  Descriptions,
} from "antd";
import {
  PlusOutlined,
  SafetyCertificateOutlined,
  CheckOutlined,
  WarningOutlined,
} from "@ant-design/icons";
import { insuranceService } from "../services/insuranceService";

const STATUS_COLOR = {
  approved: "green",
  rejected: "red",
  under_review: "orange",
  pending: "blue",
};

export default function InsuranceClaims() {
  const [claims, setClaims] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [verifyResult, setVerifyResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [form] = Form.useForm();

  const fetchClaims = async () => {
    setLoading(true);
    try {
      const d = await insuranceService.list();
      setClaims(d.claims || []);
    } catch {
      message.error("Failed to load claims");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchClaims();
  }, []);

  const handleCreate = async () => {
    try {
      const values = await form.validateFields();
      setSubmitting(true);
      await insuranceService.create({ ...values, amount: Number(values.amount) });
      message.success("Insurance claim submitted successfully");
      form.resetFields();
      setModalOpen(false);
      fetchClaims();
    } catch (err) {
      if (err?.errorFields) return;
      message.error("Failed to submit claim");
    }
    setSubmitting(false);
  };

  const handleVerify = async (claimId) => {
    try {
      const result = await insuranceService.verify(claimId);
      setVerifyResult(result);
      fetchClaims();
    } catch {
      message.error("Verification failed");
    }
  };

  const columns = [
    {
      title: "Cattle ID",
      dataIndex: "cattle_id",
      key: "cattle_id",
      render: (v, r) => (
        <span>
          <strong>{r.cattle_name || v}</strong>
          <br />
          <code style={{ fontSize: 11, color: "#888" }}>{v}</code>
        </span>
      ),
    },
    {
      title: "Type",
      dataIndex: "claim_type",
      key: "claim_type",
      render: (t) => <Tag>{t?.toUpperCase()}</Tag>,
    },
    {
      title: "Amount",
      dataIndex: "amount",
      key: "amount",
      render: (v) => <strong>₹{Number(v).toLocaleString("en-IN")}</strong>,
    },
    {
      title: "Status",
      dataIndex: "status",
      key: "status",
      render: (s) => (
        <Badge
          status={s === "approved" ? "success" : s === "rejected" ? "error" : "processing"}
          text={<Tag color={STATUS_COLOR[s] || "default"}>{s?.replace("_", " ").toUpperCase()}</Tag>}
        />
      ),
    },
    {
      title: "Fraud Score",
      dataIndex: "fraud_score",
      key: "fraud_score",
      render: (s) =>
        s != null ? (
          <Tag color={s >= 70 ? "red" : s >= 40 ? "orange" : "green"}>
            {s}%
          </Tag>
        ) : (
          <span style={{ color: "#bbb" }}>Not verified</span>
        ),
    },
    {
      title: "Action",
      key: "action",
      render: (_, r) =>
        r.status === "pending" ? (
          <Tooltip title="Run fraud detection AI">
            <Button
              size="small"
              type="primary"
              icon={<SafetyCertificateOutlined />}
              onClick={() => handleVerify(r._id)}
            >
              Verify
            </Button>
          </Tooltip>
        ) : (
          <span style={{ color: "#bbb", fontSize: 12 }}>Processed</span>
        ),
    },
  ];

  const pendingCount = claims.filter((c) => c.status === "pending").length;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <div>
          <h2 style={{ margin: 0 }}>Insurance Claims</h2>
          <Space style={{ marginTop: 4 }}>
            <Tag color="blue">{pendingCount} Pending</Tag>
            <Tag color="green">{claims.filter((c) => c.status === "approved").length} Approved</Tag>
            <Tag color="red">{claims.filter((c) => c.status === "rejected").length} Rejected</Tag>
          </Space>
        </div>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => setModalOpen(true)}
        >
          New Claim
        </Button>
      </div>

      {verifyResult && (
        <Alert
          type={verifyResult.risk_level === "LOW" ? "success" : verifyResult.risk_level === "HIGH" ? "error" : "warning"}
          showIcon
          icon={verifyResult.risk_level === "LOW" ? <CheckOutlined /> : <WarningOutlined />}
          message={`Verification Complete — Fraud Score: ${verifyResult.fraud_score}% (${verifyResult.risk_level} RISK)`}
          description={
            <div>
              <strong>Recommendation:</strong> {verifyResult.recommendation}
              {verifyResult.reasons?.length > 0 && (
                <ul style={{ marginTop: 4, paddingLeft: 16, marginBottom: 0 }}>
                  {verifyResult.reasons.map((r, i) => <li key={i}>{r}</li>)}
                </ul>
              )}
            </div>
          }
          closable
          onClose={() => setVerifyResult(null)}
          style={{ marginBottom: 16, borderRadius: 8 }}
        />
      )}

      <Table
        dataSource={claims}
        columns={columns}
        rowKey="_id"
        loading={loading}
        pagination={{ pageSize: 10 }}
        size="middle"
      />

      <Modal
        title={<span><PlusOutlined /> New Insurance Claim</span>}
        open={modalOpen}
        onOk={handleCreate}
        onCancel={() => { setModalOpen(false); form.resetFields(); }}
        okText="Submit Claim"
        confirmLoading={submitting}
        width={480}
      >
        <Form form={form} layout="vertical" style={{ marginTop: 8 }}>
          <Form.Item name="cattle_id" label="Cattle ID" rules={[{ required: true }]}>
            <Input placeholder="e.g. CTL-001" />
          </Form.Item>
          <Form.Item name="claim_type" label="Claim Type" rules={[{ required: true }]}>
            <Select placeholder="Select type">
              <Select.Option value="death">Death</Select.Option>
              <Select.Option value="illness">Illness</Select.Option>
              <Select.Option value="theft">Theft</Select.Option>
              <Select.Option value="accident">Accident</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="amount" label="Claim Amount (₹)" rules={[{ required: true }]}>
            <InputNumber
              min={1000}
              max={500000}
              style={{ width: "100%" }}
              placeholder="e.g. 25000"
              formatter={(v) => `₹ ${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ",")}
              parser={(v) => v.replace(/₹\s?|(,*)/g, "")}
            />
          </Form.Item>
          <Form.Item name="description" label="Description">
            <Input.TextArea rows={3} placeholder="Describe the incident..." />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}
