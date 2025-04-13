import React, { useState } from "react";
import ImageCard from "./ImageCard";
import Box from "@mui/material/Box";
import SendIcon from "@mui/icons-material/Send";
import { LoadingButton } from "@mui/lab";

const GenerateButton = ({ rectangleCoords, selectedDate }) => {  
  const [loading, setLoading] = useState(false);
  const [imageGenerated, setImageGenerated] = useState(false);

  const handleGenerate = async () => {
    if (!rectangleCoords || !selectedDate) {
      console.error("Missing data");
      return;
    }

    setLoading(true);
    setImageGenerated(false);

    const coordinates = [
      [rectangleCoords.center.lat,rectangleCoords.center.lng]
    ];


    try {
      console.log("Sending coordinates:", coordinates, "Date:", selectedDate);
      const res = await fetch("/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
          coordinates,
          date: selectedDate 
        }),
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
          backgroundColor: "#256b68",
          "&:hover": {
            backgroundColor: "#388E3C",
          },
          "&:disabled": {
            backgroundColor: "#E0E0E0",
          },
          "&.MuiLoadingButton-loading": {
            backgroundColor: "#2196F3",
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