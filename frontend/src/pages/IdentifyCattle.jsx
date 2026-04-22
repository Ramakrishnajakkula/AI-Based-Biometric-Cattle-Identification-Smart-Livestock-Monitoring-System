/**
 * Identify Cattle Page — Upload muzzle image → biometric match result
 * Author: Poshith
 */
import React, { useState } from "react";
import {
  Upload,
  Card,
  Button,
  Spin,
  message,
  Alert,
  Descriptions,
  Tag,
  Badge,
  Row,
  Col,
  Steps,
} from "antd";
import {
  CameraOutlined,
  UploadOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  QuestionCircleOutlined,
} from "@ant-design/icons";
import api from "../services/api";

const { Step } = Steps;

export default function IdentifyCattle() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(0);

  const handleFileSelect = (f) => {
    setFile(f);
    setResult(null);
    setStep(1);
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target.result);
    reader.readAsDataURL(f);
    return false;
  };

  const handleIdentify = async () => {
    if (!file) {
      message.warning("Please select a cattle image first");
      return;
    }
    setLoading(true);
    setStep(2);
    const formData = new FormData();
    formData.append("image", file);
    try {
      const { data } = await api.post("/identify/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(data);
      setStep(3);
    } catch (err) {
      message.error("Identification failed. Please try again.");
      setStep(1);
    }
    setLoading(false);
  };

  const handleReset = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setStep(0);
  };

  const matched = result?.matched;
  const cattle = result?.cattle;

  return (
    <div>
      <h2 style={{ marginBottom: 4 }}>
        <CameraOutlined style={{ color: "#52c41a", marginRight: 8 }} />
        Biometric Cattle Identification
      </h2>
      <p style={{ color: "#888", marginBottom: 24 }}>
        Upload a muzzle or face photograph to identify a cattle using AI-based biometric matching (YOLOv8 + ArcFace).
      </p>

      <Steps current={step} style={{ marginBottom: 32 }} size="small">
        <Step title="Select Image" icon={<UploadOutlined />} />
        <Step title="Preview" icon={<CameraOutlined />} />
        <Step title="Processing" icon={loading ? <Spin size="small" /> : <QuestionCircleOutlined />} />
        <Step
          title="Result"
          icon={
            result
              ? matched
                ? <CheckCircleOutlined style={{ color: "#52c41a" }} />
                : <CloseCircleOutlined style={{ color: "#f5222d" }} />
              : null
          }
        />
      </Steps>

      <Row gutter={24}>
        {/* Upload Panel */}
        <Col xs={24} md={10}>
          <Card
            title="Upload Image"
            style={{ borderRadius: 12 }}
            bodyStyle={{ textAlign: "center", padding: 32 }}
          >
            {preview ? (
              <div>
                <img
                  src={preview}
                  alt="Selected cattle"
                  style={{
                    maxWidth: "100%",
                    maxHeight: 260,
                    borderRadius: 8,
                    marginBottom: 16,
                    border: "2px solid #e8e8e8",
                    objectFit: "cover",
                  }}
                />
                <br />
                <Button size="small" onClick={handleReset} style={{ marginRight: 8 }}>
                  Remove
                </Button>
              </div>
            ) : (
              <Upload
                beforeUpload={handleFileSelect}
                maxCount={1}
                accept="image/*"
                showUploadList={false}
              >
                <div
                  style={{
                    border: "2px dashed #d9d9d9",
                    borderRadius: 12,
                    padding: "40px 20px",
                    cursor: "pointer",
                    transition: "border-color 0.3s",
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.borderColor = "#52c41a")}
                  onMouseLeave={(e) => (e.currentTarget.style.borderColor = "#d9d9d9")}
                >
                  <CameraOutlined style={{ fontSize: 48, color: "#bbb", marginBottom: 12 }} />
                  <p style={{ color: "#888", marginBottom: 0 }}>
                    Click or drag a cattle muzzle image here
                  </p>
                  <p style={{ color: "#bbb", fontSize: 12 }}>PNG, JPG, JPEG, WEBP supported</p>
                </div>
              </Upload>
            )}

            <Button
              type="primary"
              icon={loading ? <Spin size="small" /> : <CameraOutlined />}
              onClick={handleIdentify}
              loading={loading}
              disabled={!file}
              block
              size="large"
              style={{ marginTop: file ? 0 : 16 }}
            >
              {loading ? "Identifying..." : "Identify Cattle"}
            </Button>
          </Card>
        </Col>

        {/* Result Panel */}
        <Col xs={24} md={14}>
          <Card title="Identification Result" style={{ borderRadius: 12, minHeight: 300 }}>
            {!result && !loading && (
              <div style={{ textAlign: "center", padding: "60px 0", color: "#bbb" }}>
                <CameraOutlined style={{ fontSize: 48 }} />
                <p style={{ marginTop: 12 }}>Upload an image and click "Identify Cattle" to begin</p>
              </div>
            )}

            {loading && (
              <div style={{ textAlign: "center", padding: "60px 0" }}>
                <Spin size="large" />
                <p style={{ marginTop: 16, color: "#888" }}>
                  Running YOLOv8 detection + ArcFace matching…
                </p>
              </div>
            )}

            {result && matched && cattle && (
              <div>
                <Alert
                  message="Match Found"
                  description={`Confidence: ${(result.confidence * 100).toFixed(1)}% — Source: ${result.source === "ml_model" ? "YOLOv8 + ArcFace" : "Biometric Engine"}`}
                  type="success"
                  showIcon
                  icon={<CheckCircleOutlined />}
                  style={{ marginBottom: 20 }}
                />
                {cattle.image_url && (
                  <div style={{ textAlign: "center", marginBottom: 16 }}>
                    <img
                      src={cattle.image_url}
                      alt={cattle.name}
                      style={{
                        width: 120,
                        height: 120,
                        borderRadius: "50%",
                        objectFit: "cover",
                        border: "3px solid #52c41a",
                        boxShadow: "0 4px 12px rgba(82,196,26,0.3)",
                      }}
                      onError={(e) => {
                        e.target.onerror = null;
                        e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E🐄%3C/text%3E%3C/svg%3E";
                      }}
                    />
                  </div>
                )}
                <Descriptions bordered column={1} size="middle">
                  <Descriptions.Item label="Name">
                    <strong style={{ fontSize: 16 }}>🐄 {cattle.name || "—"}</strong>
                  </Descriptions.Item>
                  <Descriptions.Item label="Tag ID">
                    <code style={{ fontSize: 14 }}>{cattle.tag_id}</code>
                  </Descriptions.Item>
                  <Descriptions.Item label="Breed">{cattle.breed}</Descriptions.Item>
                  <Descriptions.Item label="Age">{cattle.age_years ? `${cattle.age_years} years` : "—"}</Descriptions.Item>
                  <Descriptions.Item label="Weight">{cattle.weight_kg ? `${cattle.weight_kg} kg` : "—"}</Descriptions.Item>
                  <Descriptions.Item label="Farm">{cattle.farm_id || "—"}</Descriptions.Item>
                  <Descriptions.Item label="Health Status">
                    <Badge
                      status={cattle.health_status === "healthy" ? "success" : "error"}
                      text={
                        <Tag color={cattle.health_status === "healthy" ? "green" : "red"}>
                          {cattle.health_status?.toUpperCase()}
                        </Tag>
                      }
                    />
                  </Descriptions.Item>
                  <Descriptions.Item label="Milk Yield">{cattle.milk_yield_liters ? `${cattle.milk_yield_liters} L/day` : "—"}</Descriptions.Item>
                  <Descriptions.Item label="Last Vaccination">{cattle.last_vaccination || "—"}</Descriptions.Item>
                  <Descriptions.Item label="Match Confidence">
                    <Tag color="green" style={{ fontSize: 14 }}>
                      {(result.confidence * 100).toFixed(1)}%
                    </Tag>
                  </Descriptions.Item>
                </Descriptions>
              </div>
            )}

            {result && !matched && (
              <div>
                <Alert
                  message="No Match Found"
                  description={
                    result.ml_status === "error"
                      ? "ML model error — models may not be loaded. This is expected in demo mode."
                      : "This cattle is not registered in the system, or the image quality was too low for a confident match."
                  }
                  type="warning"
                  showIcon
                  icon={<CloseCircleOutlined />}
                  style={{ marginBottom: 20 }}
                />
                <div style={{ color: "#888", fontSize: 13 }}>
                  <p><b>Status:</b> {result.ml_status || "no_match"}</p>
                  {result.confidence > 0 && (
                    <p><b>Best confidence:</b> {(result.confidence * 100).toFixed(1)}%</p>
                  )}
                  {result.predicted_cattle_id && (
                    <p><b>Predicted ID:</b> {result.predicted_cattle_id}</p>
                  )}
                </div>
                <Button type="default" onClick={handleReset} style={{ marginTop: 12 }}>
                  Try Another Image
                </Button>
              </div>
            )}
          </Card>
        </Col>
      </Row>
    </div>
  );
}
