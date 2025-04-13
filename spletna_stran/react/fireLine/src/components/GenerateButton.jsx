import React, { useState } from "react";
import ImageCard from "./ImageCard";
import Box from "@mui/material/Box";
import SendIcon from "@mui/icons-material/Send";
import { LoadingButton } from "@mui/lab";

const GenerateButton = ({ rectangleCoords, selectedDate }) => {  
  const [loading, setLoading] = useState(false);
  const [imageGenerated, setImageGenerated] = useState(false);
  const [faktor, setFaktor] = useState(null);

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
        const data = await res.json(); // assuming your backend returns JSON
        console.log("Received data:", data);

        setFaktor(data.faktor_izboljsave); // ← Save it here
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
    <Box className="mt-6"
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        width: "100%",
    }}>
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
        {loading ? "obdelava..." : "Zaženi FireLine"}
      </LoadingButton>

      {imageGenerated && (
      <div style={{ marginTop: "40px" }}>
        <h1 style={{ textAlign: "center" }}>Rezultati</h1>
        <h2 style={{ marginBottom: "16px" }}>Satelitska slika:</h2>

        <Box
          sx={{
            display: "flex",
            flexDirection: "row", // Ensures image and text are in a row
            alignItems: "center", // Vertically center both elements
            justifyContent: "center", 
            gap: 5, // Space between the image and the text
            marginTop: 4, // Adjust margin as needed
            maxWidth: "800px",
            margin: "0 auto", // <-- This centers the box horizontally

          }}
        >
          
          <ImageCard
            imageSrc={`/public/pregradaSatelitska.png?${Date.now()}`}
            title=""
            description=""
          />
          
          <Box
            sx={{
              display: "flex",
              flexDirection: "column", // Ensure text is arranged vertically
              maxWidth: "400px", // Prevent text from getting too wide
              textAlign: "left", // Ensure text alignment is on the left
            }}
          >
            <p>
              Na levi je prikazana satelitska slika območja okoli izbrane točke. 
              Z oranžno barvo je na njej narisana predlagana pregrada.
            </p>
          </Box>
        </Box>



        {/* Group heading with images below */}
        <Box
          sx={{
            marginTop: 4,
            display: "flex",
            flexDirection: "column",
          }}
        >
          <h2 style={{ marginBottom: "16px" }}>Simulacija požara:</h2>

          <Box
            sx={{
              display: "flex",
              flexDirection: "row",
              justifyContent: "center",
              gap: 5,
            }}
          >
            <ImageCard
              imageSrc={`/public/brezPregrade.gif?${Date.now()}`}
              title="Brez pregrade"
              description=""
            />
            <ImageCard
              imageSrc={`/public/Pregrada.gif?${Date.now()}`}
              title="S pregrado"
              description=""
            />
          </Box>
          {faktor && (
            <div>
              <p>Zgoraj sta prikazani dve simulaciji požara v časovnem intervalu 3 dni po izbranem začetnem datumu, s korakom po 1 uro.
              Zelena barva na simulaciji predstavlja gozd, rumena travnik in siva vodne površine, stavbe, ceste in pregrado.
              </p>
              <p style={{ marginTop: 20, fontWeight: "bold" }}>
                Z uporabo pregrade je požar za <span style={{ color: "orange" }}>{(faktor * 100).toFixed(1)}%</span> manjši.
              </p>
            </div>
          )}
        </Box>
      </div>
    )}
    </Box>
  );
};

export default GenerateButton;