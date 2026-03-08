/**
 * Login Page
 * Author: Poshith
 */
import React, { useState } from "react";
import { Card, Form, Input, Button, message, Typography, Alert } from "antd";
import { LockOutlined, MailOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const { Title, Text } = Typography;

export default function Login() {
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const onFinish = async (values) => {
    setLoading(true);
    try {
      await login(values.email, values.password);
      navigate("/");
    } catch (err) {
      message.error("Invalid email or password");
    }
    setLoading(false);
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        background: "linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%)",
      }}>
      <Card style={{ width: 420, boxShadow: "0 4px 20px rgba(0,0,0,0.08)" }}>
        <Title level={3} style={{ textAlign: "center", color: "#52c41a", marginBottom: 4 }}>
          🐄 Cattle Monitoring System
        </Title>
        <Text type="secondary" style={{ display: "block", textAlign: "center", marginBottom: 24 }}>
          AI-Based Biometric Livestock Management
        </Text>

        <Form layout="vertical" onFinish={onFinish}
          initialValues={{ email: "admin@cattle.com", password: "admin123" }}>
          <Form.Item
            name="email"
            label="Email"
            rules={[{ required: true, type: "email" }]}>
            <Input size="large" prefix={<MailOutlined />} placeholder="admin@cattle.com" />
          </Form.Item>
          <Form.Item
            name="password"
            label="Password"
            rules={[{ required: true }]}>
            <Input.Password size="large" prefix={<LockOutlined />} placeholder="Password" />
          </Form.Item>
          <Button
            type="primary"
            htmlType="submit"
            block
            size="large"
            loading={loading}>
            Login
          </Button>
        </Form>

        <Alert
          type="info"
          showIcon
          style={{ marginTop: 16 }}
          message="Demo Credentials"
          description={
            <span>
              Email: <strong>admin@cattle.com</strong> &nbsp;|&nbsp; Password: <strong>admin123</strong>
            </span>
          }
        />
      </Card>
    </div>
  );
}
