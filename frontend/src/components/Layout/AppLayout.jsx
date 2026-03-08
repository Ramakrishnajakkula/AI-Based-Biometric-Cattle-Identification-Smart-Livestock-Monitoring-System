/**
 * App Layout — Sidebar + Header + Content
 * Author: Poshith
 */
import React from "react";
import { Layout, Menu } from "antd";
import {
  DashboardOutlined,
  UnorderedListOutlined,
  AlertOutlined,
  SafetyCertificateOutlined,
  EnvironmentOutlined,
  CameraOutlined,
  LogoutOutlined,
} from "@ant-design/icons";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const { Sider, Header, Content } = Layout;

const menuItems = [
  { key: "/", icon: <DashboardOutlined />, label: "Dashboard" },
  { key: "/animals", icon: <UnorderedListOutlined />, label: "Animals" },
  { key: "/health", icon: <AlertOutlined />, label: "Health Alerts" },
  {
    key: "/insurance",
    icon: <SafetyCertificateOutlined />,
    label: "Insurance",
  },
  { key: "/map", icon: <EnvironmentOutlined />, label: "Live Map" },
  { key: "/identify", icon: <CameraOutlined />, label: "Identify" },
];

export default function AppLayout({ children }) {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider collapsible theme="light" width={220}>
        <div
          style={{
            padding: "16px",
            textAlign: "center",
            fontWeight: "bold",
            fontSize: 16,
            color: "#52c41a",
          }}>
          Cattle Monitor
        </div>
        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
        />
        <div
          style={{
            position: "absolute",
            bottom: 16,
            width: "100%",
            textAlign: "center",
          }}>
          <span style={{ cursor: "pointer", color: "#999" }} onClick={logout}>
            <LogoutOutlined /> Logout
          </span>
        </div>
      </Sider>
      <Layout>
        <Header
          style={{
            background: "#fff",
            padding: "0 24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "flex-end",
          }}>
          <span>Welcome, {user?.name || "User"}</span>
        </Header>
        <Content
          style={{
            margin: 24,
            padding: 24,
            background: "#fff",
            borderRadius: 8,
          }}>
          {children}
        </Content>
      </Layout>
    </Layout>
  );
}
