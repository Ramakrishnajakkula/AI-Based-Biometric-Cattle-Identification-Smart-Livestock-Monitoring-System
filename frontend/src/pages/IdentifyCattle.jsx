/**
 * Identify Cattle Page — Upload muzzle image → biometric match
 * Author: Poshith
 */
import React, { useState } from "react";
import { Upload, Card, Button, Result, Descriptions, Tag, Spin, message } from "antd";
import { CameraOutlined, UploadOutlined } from "@ant-design/icons";
import api from "../services/api";

export default function IdentifyCattle() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      message.warning("Please select an image first");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("image", file);

    try {
      const { data } = await api.post("/identify/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(data);
    } catch (err) {
      message.error("Identification failed");
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>Identify Cattle</h2>
      <Card style={{ marginTop: 16, textAlign: "center" }}>
        <p>
          Upload a muzzle/face photograph to identify the cattle using biometric
          matching.
        </p>
        <Upload
          beforeUpload={(f) => {
            setFile(f);
            return false;
          }}
          maxCount={1}
          accept="image/*">
          <Button icon={<UploadOutlined />}>Select Image</Button>
        </Upload>
        <br />
        <Button
          type="primary"
          icon={<CameraOutlined />}
          onClick={handleUpload}
          loading={loading}
          style={{ marginTop: 16 }}>
          Identify
        </Button>

        {loading && <Spin style={{ marginTop: 24 }} />}

        {result && (
          <Card style={{ marginTop: 24 }}>
            {result.matched ? (
              <>
                <Result
                  status="success"
                  title={`Identified: ${result.cattle?.name || result.cattle?.tag_id}`}
                  subTitle={`Confidence: ${(result.confidence * 100).toFixed(1)}%`}
                />
                <Descriptions bordered column={2} size="small">
                  <Descriptions.Item label="Tag ID">{result.cattle?.tag_id}</Descriptions.Item>
                  <Descriptions.Item label="Breed">{result.cattle?.breed}</Descriptions.Item>
                  <Descriptions.Item label="Health Status">
                    <Tag color={result.cattle?.health_status === "healthy" ? "green" : "red"}>
                      {result.cattle?.health_status}
                    </Tag>
                  </Descriptions.Item>
                </Descriptions>
              </>
            ) : (
              <Result
                status="warning"
                title="No Match Found"
                subTitle="This cattle is not registered in the system."
              />
            )}
          </Card>
        )}
      </Card>
    </div>
  );
}
