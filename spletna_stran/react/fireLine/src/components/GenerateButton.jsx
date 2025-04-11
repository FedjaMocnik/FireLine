import React, { useState } from "react";
import ImageCard from "./ImageCard";
import Box from "@mui/material/Box";
import SendIcon from "@mui/icons-material/Send";
import { LoadingButton } from "@mui/lab";

const GenerateButton = ({ rectangleCoords }) => {
  const [loading, setLoading] = useState(false);
  const [imageGenerated, setImageGenerated] = useState(false);

  const handleGenerate = async () => {
    if (!rectangleCoords) {
      console.error("No area selected");
      return;
    }

    setLoading(true);
    setImageGenerated(false);

    const coordinates = [
      [rectangleCoords.northWest.lat, rectangleCoords.northWest.lng],
      [rectangleCoords.southEast.lat, rectangleCoords.southEast.lng]
    ];

    try {
      console.log("Sending coordinates:", coordinates);
      const res = await fetch("/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ coordinates }),
      });

      if (res.ok) {
        setImageGenerated(true);
      } else {
        console.error("Failed to generate image");
      }
    } catch (error) {
      console.error("API error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box className="flex flex-col items-center gap-6 mt-6">
      <LoadingButton
        onClick={handleGenerate}
        endIcon={<SendIcon />}
        loading={loading}
        loadingPosition="end"
        variant="contained"
        size="medium"
        disabled={!rectangleCoords}
        sx={{
          backgroundColor: "#256b68", // Green color
          "&:hover": {
            backgroundColor: "#388E3C", // Darker green on hover
          },
          "&:disabled": {
            backgroundColor: "#E0E0E0", // Light gray when disabled
          },
          "&.MuiLoadingButton-loading": {
            backgroundColor: "#2196F3", // Blue color when loading
          }
        }}
      >
        {loading ? "GENERATING..." : "Generate Image"}
      </LoadingButton>

      {imageGenerated && (
        <ImageCard
          imageSrc={`/public/forest.png?${Date.now()}`}
          title="Generated Image"
          description="This image was created by the Python backend."
        />
      )}
    </Box>
  );
};

export default GenerateButton;