/**
 * App Layout — Premium dark sidebar + header + content
 * Author: Poshith
 */
import React, { useEffect, useState } from "react";
import { Layout, Menu, Badge, Avatar, Dropdown, Tooltip } from "antd";
import {
  DashboardOutlined,
  UnorderedListOutlined,
  AlertOutlined,
  SafetyCertificateOutlined,
  EnvironmentOutlined,
  CameraOutlined,
  LogoutOutlined,
  UserOutlined,
  SettingOutlined,
  BellOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
} from "@ant-design/icons";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { dashboardService } from "../../services/dashboardService";

const { Sider, Header, Content } = Layout;

const allMenuItems = [
  { key: "/", icon: <DashboardOutlined />, label: "Dashboard", roles: ["admin", "farmer"] },
  { key: "/animals", icon: <UnorderedListOutlined />, label: "Cattle Registry", roles: ["admin", "farmer"] },
  { key: "/health", icon: <AlertOutlined />, label: "Health Alerts", roles: ["admin", "farmer"] },
  { key: "/insurance", icon: <SafetyCertificateOutlined />, label: "Insurance", roles: ["admin"] },
  { key: "/map", icon: <EnvironmentOutlined />, label: "Live Map", roles: ["admin", "farmer"] },
  { key: "/identify", icon: <CameraOutlined />, label: "Identify Cattle", roles: ["admin", "farmer"] },
];

export default function AppLayout({ children }) {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  const [collapsed, setCollapsed] = useState(false);
  const [alertCount, setAlertCount] = useState(0);

  const role = user?.role || "farmer";
  const menuItems = allMenuItems.filter((item) => item.roles.includes(role));

  useEffect(() => {
    dashboardService.getStats().then((s) => setAlertCount(s.active_alerts || 0)).catch(() => {});
  }, []);

  const userMenuItems = [
    {
      key: "profile",
      icon: <UserOutlined />,
      label: "Profile",
    },
    ...(role === "admin"
      ? [{ key: "/admin", icon: <SettingOutlined />, label: "Admin Panel" }]
      : []),
    { type: "divider" },
    {
      key: "logout",
      icon: <LogoutOutlined />,
      label: <span style={{ color: "#f5222d" }}>Sign Out</span>,
      danger: true,
    },
  ];

  const handleUserMenu = ({ key }) => {
    if (key === "logout") {
      logout();
      navigate("/login");
    } else if (key.startsWith("/")) {
      navigate(key);
    }
  };

  const enrichedMenuItems = menuItems.map((item) => ({
    ...item,
    icon: item.key === "/health"
      ? (
          <Badge count={alertCount} size="small" offset={[6, 0]}>
            {item.icon}
          </Badge>
        )
      : item.icon,
  }));

  return (
    <Layout style={{ minHeight: "100vh", background: "#f0f2f5" }}>
      <Sider
        collapsible
        collapsed={collapsed}
        onCollapse={setCollapsed}
        trigger={null}
        width={230}
        style={{
          background: "linear-gradient(180deg, #001529 0%, #002140 100%)",
          boxShadow: "2px 0 12px rgba(0,0,0,0.2)",
          position: "fixed",
          height: "100vh",
          left: 0,
          top: 0,
          zIndex: 100,
          overflow: "hidden",
        }}
      >
        {/* Brand */}
        <div
          style={{
            padding: collapsed ? "20px 0" : "20px 16px",
            display: "flex",
            alignItems: "center",
            gap: 10,
            borderBottom: "1px solid rgba(255,255,255,0.08)",
            cursor: "pointer",
          }}
          onClick={() => navigate("/")}
        >
          <span style={{ fontSize: 26, lineHeight: 1 }}>🐄</span>
          {!collapsed && (
            <div>
              <div style={{ color: "#52c41a", fontWeight: 700, fontSize: 15, lineHeight: 1.2 }}>
                SmartLivestock
              </div>
              <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 10 }}>
                AI Monitoring System
              </div>
            </div>
          )}
        </div>

        {/* Menu */}
        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          items={enrichedMenuItems}
          onClick={({ key }) => navigate(key)}
          style={{
            background: "transparent",
            border: "none",
            marginTop: 8,
          }}
          theme="dark"
        />

        {/* User avatar at bottom */}
        {!collapsed && (
          <div
            style={{
              position: "absolute",
              bottom: 56,
              left: 0,
              right: 0,
              padding: "12px 16px",
              borderTop: "1px solid rgba(255,255,255,0.08)",
              display: "flex",
              alignItems: "center",
              gap: 10,
            }}
          >
            <Avatar
              size={32}
              style={{ background: "#52c41a", flexShrink: 0 }}
            >
              {user?.name?.[0]?.toUpperCase() || "U"}
            </Avatar>
            <div style={{ minWidth: 0 }}>
              <div
                style={{
                  color: "#fff",
                  fontSize: 13,
                  fontWeight: 600,
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  whiteSpace: "nowrap",
                }}
              >
                {user?.name || "User"}
              </div>
              <div style={{ color: "rgba(255,255,255,0.45)", fontSize: 11 }}>
                {user?.role || "farmer"}
              </div>
            </div>
          </div>
        )}
      </Sider>

      <Layout style={{ marginLeft: collapsed ? 80 : 230, transition: "margin-left 0.2s" }}>
        {/* Header */}
        <Header
          style={{
            background: "#fff",
            padding: "0 24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            boxShadow: "0 1px 8px rgba(0,0,0,0.08)",
            position: "sticky",
            top: 0,
            zIndex: 99,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <Tooltip title={collapsed ? "Expand" : "Collapse"}>
              <span
                onClick={() => setCollapsed(!collapsed)}
                style={{ fontSize: 18, cursor: "pointer", color: "#666" }}
              >
                {collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
              </span>
            </Tooltip>
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
            <Tooltip title={`${alertCount} active health alerts`}>
              <Badge count={alertCount} offset={[2, 0]}>
                <BellOutlined
                  style={{ fontSize: 18, cursor: "pointer", color: "#666" }}
                  onClick={() => navigate("/health")}
                />
              </Badge>
            </Tooltip>

            <Dropdown
              menu={{ items: userMenuItems, onClick: handleUserMenu }}
              trigger={["click"]}
              placement="bottomRight"
            >
              <div style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }}>
                <Avatar size={34} style={{ background: "#52c41a" }}>
                  {user?.name?.[0]?.toUpperCase() || "U"}
                </Avatar>
                <span style={{ fontWeight: 500, color: "#333" }}>{user?.name}</span>
              </div>
            </Dropdown>
          </div>
        </Header>

        {/* Content */}
        <Content
          style={{
            margin: 24,
            padding: 28,
            background: "#fff",
            borderRadius: 12,
            minHeight: "calc(100vh - 112px)",
            boxShadow: "0 1px 8px rgba(0,0,0,0.05)",
          }}
        >
          {children}
        </Content>
      </Layout>
    </Layout>
  );
}
