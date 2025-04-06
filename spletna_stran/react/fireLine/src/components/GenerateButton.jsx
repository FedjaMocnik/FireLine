import React, { useState } from "react";
import ImageCard from "./ImageCard";

import Box from "@mui/material/Box";
import SendIcon from "@mui/icons-material/Send";
import { LoadingButton } from "@mui/lab";

const GenerateButton = () => {
  const [loading, setLoading] = useState(false);
  const [imageGenerated, setImageGenerated] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    setImageGenerated(false); // Reset previous image if any

    const coordinates = [50.087, 14.421];

    try {
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
      >
        Generate Image
      </LoadingButton>

      {imageGenerated && (
        <ImageCard
          imageSrc={`/public/forest.png?${Date.now()}`} // prevent caching
          title="Generated Image"
          description="This image was created by the Python backend."
        />
      )}
    </Box>
  );
};

export default GenerateButton;
