/**
 * Animal Detail Page — Individual cattle info + sensor charts
 * Author: Poshith
 */
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Card, Descriptions, Tabs, Tag, Spin, Button, Row, Col, Statistic } from "antd";
import { ArrowLeftOutlined, HeartOutlined, DashboardOutlined, ThunderboltOutlined } from "@ant-design/icons";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { cattleService } from "../services/cattleService";
import { sensorService } from "../services/sensorService";
import dayjs from "dayjs";

export default function AnimalDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [cattle, setCattle] = useState(null);
  const [tempHistory, setTempHistory] = useState([]);
  const [hrHistory, setHrHistory] = useState([]);
  const [latestSensors, setLatestSensors] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const c = await cattleService.getById(id);
        setCattle(c);
        const [temp, hr, latest] = await Promise.all([
          sensorService.getHistory(id, "temperature", 24),
          sensorService.getHistory(id, "heartrate", 24),
          sensorService.getLatest(id),
        ]);
        setTempHistory(
          (temp.readings || []).map((r) => ({
            time: dayjs(r.timestamp).format("HH:mm"),
            value: r.data?.value ?? r.data?.bpm ?? 0,
          }))
        );
        setHrHistory(
          (hr.readings || []).map((r) => ({
            time: dayjs(r.timestamp).format("HH:mm"),
            value: r.data?.bpm ?? 0,
          }))
        );
        setLatestSensors(latest?.latest || null);
      } catch (e) {
        console.error(e);
      }
      setLoading(false);
    };
    load();
  }, [id]);

  if (loading) return <Spin style={{ display: "block", margin: "80px auto" }} size="large" />;
  if (!cattle) return <p>Cattle not found.</p>;

  const tabItems = [
    {
      key: "temp",
      label: "Temperature",
      children: (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={tempHistory}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis domain={[36, 42]} unit="°C" />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#fa541c" name="Temp °C" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      ),
    },
    {
      key: "hr",
      label: "Heart Rate",
      children: (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={hrHistory}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis domain={[35, 90]} unit=" bpm" />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#1890ff" name="BPM" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      ),
    },
  ];

  return (
    <div>
      <Button icon={<ArrowLeftOutlined />} onClick={() => navigate("/animals")} style={{ marginBottom: 16 }}>
        Back to List
      </Button>

      <Card title={cattle.name || cattle.tag_id}>
        <Descriptions bordered column={2}>
          <Descriptions.Item label="Tag ID">{cattle.tag_id}</Descriptions.Item>
          <Descriptions.Item label="Breed">{cattle.breed}</Descriptions.Item>
          <Descriptions.Item label="Age">{cattle.age_years} years</Descriptions.Item>
          <Descriptions.Item label="Weight">{cattle.weight_kg} kg</Descriptions.Item>
          <Descriptions.Item label="Farm">{cattle.farm_id}</Descriptions.Item>
          <Descriptions.Item label="Health">
            <Tag color={cattle.health_status === "healthy" ? "green" : "red"}>
              {cattle.health_status}
            </Tag>
          </Descriptions.Item>
        </Descriptions>
      </Card>

      {latestSensors && (
        <Row gutter={16} style={{ marginTop: 16 }}>
          <Col span={8}>
            <Card>
              <Statistic
                title="Temperature"
                value={latestSensors.temperature?.data?.value ?? "--"}
                suffix="°C"
                prefix={<DashboardOutlined />}
                valueStyle={{ color: (latestSensors.temperature?.data?.value ?? 0) > 39.5 ? "#cf1322" : "#3f8600" }}
              />
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Statistic
                title="Heart Rate"
                value={latestSensors.heartrate?.data?.bpm ?? "--"}
                suffix="bpm"
                prefix={<HeartOutlined />}
              />
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Statistic
                title="Activity"
                value={latestSensors.activity?.data?.activity_level ?? "--"}
                prefix={<ThunderboltOutlined />}
              />
            </Card>
          </Col>
        </Row>
      )}

      <Card title="Sensor History (Last 24h)" style={{ marginTop: 16 }}>
        <Tabs items={tabItems} defaultActiveKey="temp" />
      </Card>
    </div>
  );
}
