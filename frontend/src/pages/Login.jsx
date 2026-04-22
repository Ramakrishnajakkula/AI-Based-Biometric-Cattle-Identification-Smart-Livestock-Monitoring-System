/**
 * Login Page
 * Author: Poshith
 */
import React, { useState } from "react";
import { Card, Form, Input, Button, message, Typography, Divider, Segmented } from "antd";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const { Title, Text } = Typography;

export default function Login() {
  const [loading, setLoading] = useState(false);
  const { login, register } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const isSignup = location.pathname === "/signup";

  const onFinish = async (values) => {
    setLoading(true);
    try {
      if (isSignup) {
        await register(values.name, values.email, values.password);
      } else {
        await login(values.email, values.password);
      }
      navigate("/");
    } catch (err) {
      if (isSignup) {
        message.error(err?.response?.data?.error || "Unable to create account");
      } else {
        message.error("Invalid email or password");
      }
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
        background: "#f0f2f5",
      }}>
      <Card style={{ width: 400 }}>
        <Title level={3} style={{ textAlign: "center", color: "#52c41a" }}>
          Cattle Monitoring System
        </Title>
        <Segmented
          block
          style={{ marginBottom: 16 }}
          value={isSignup ? "signup" : "login"}
          onChange={(value) => navigate(value === "signup" ? "/signup" : "/login")}
          options={[
            { label: "Login", value: "login" },
            { label: "Sign up", value: "signup" },
          ]}
        />
        <Form layout="vertical" onFinish={onFinish}>
          {isSignup && (
            <Form.Item
              name="name"
              label="Full Name"
              rules={[{ required: true, message: "Please enter your name" }]}
            >
              <Input size="large" placeholder="Your name" />
            </Form.Item>
          )}
          <Form.Item
            name="email"
            label="Email"
            rules={[{ required: true, type: "email" }]}>
            <Input size="large" placeholder="admin@example.com" />
          </Form.Item>
          <Form.Item
            name="password"
            label="Password"
            rules={[
              { required: true },
              ...(isSignup ? [{ min: 8, message: "Password must be at least 8 characters" }] : []),
            ]}
          >
            <Input.Password size="large" placeholder="Password" />
          </Form.Item>
          {isSignup && (
            <Form.Item
              name="confirmPassword"
              label="Confirm Password"
              dependencies={["password"]}
              rules={[
                { required: true, message: "Please confirm your password" },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue("password") === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error("Passwords do not match"));
                  },
                }),
              ]}
            >
              <Input.Password size="large" placeholder="Confirm password" />
            </Form.Item>
          )}
          <Button
            type="primary"
            htmlType="submit"
            block
            size="large"
            loading={loading}>
            {isSignup ? "Create Account" : "Login"}
          </Button>
        </Form>

        <Divider style={{ margin: "16px 0 10px" }} />
        {!isSignup ? (
          <Text type="secondary">
            New here? <a onClick={() => navigate("/signup")}>Create an account</a>
          </Text>
        ) : (
          <Text type="secondary">
            Already have an account? <a onClick={() => navigate("/login")}>Back to login</a>
          </Text>
        )}
      </Card>
    </div>
  );
}
