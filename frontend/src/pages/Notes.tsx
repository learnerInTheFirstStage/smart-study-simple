import React, { useState } from "react";
import { Box, Button, Typography } from "@mui/material";
import { Link } from "react-router-dom";

const Notes = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isAnalyzed, setIsAnalyzed] = useState(false); // Controls the visibility of "View Your Schedule"
  const [isProcessing, setIsProcessing] = useState(false); // Controls button animation

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = e.target.files?.[0] || null;
    setFile(uploadedFile);

    if (uploadedFile) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const fileContent = event.target?.result as string;
        localStorage.setItem("uploadedStudyMaterial", fileContent); // Store content
      };
      reader.readAsText(uploadedFile);
    }
  };

  const handleAnalyze = () => {
    if (file) {
      setIsProcessing(true); // Start animation
      setTimeout(() => {
        setIsProcessing(false); // End animation
        setIsAnalyzed(true); // Show "View Your Schedule" button
      }, 500); // Delay for 0.5 second
    }
  };

  return (
    <Box p={4}>
      <Typography variant="h4">Upload your study materials 📄</Typography>
      <input type="file" accept=".txt,.pdf,.docx" onChange={handleFileUpload} style={{ display: "block", marginTop: "10px" }} />
      {file && <Typography variant="subtitle1">File chosen: {file.name}</Typography>}

      {/* Upload & Analyze Button with Animation */}
      <Button
        variant="contained"
        color="primary"
        sx={{
          mt: 2,
          transition: "background-color 0.3s ease",
          backgroundColor: isProcessing ? "#1565c0" : "#1976d2", // Darker blue when clicked
        }}
        onClick={handleAnalyze}
        disabled={!file || isProcessing} // Prevent multiple clicks
      >
        {isProcessing ? "Processing..." : "UPLOAD & ANALYZE"}
      </Button>

      {/* View Schedule Button (Appears after 1s delay) */}
      {isAnalyzed && (
        <Button variant="contained" color="secondary" sx={{ mt: 2, ml: 2 }} component={Link} to="/schedule">
          VIEW YOUR SCHEDULE
        </Button>
      )}
    </Box>
  );
};

export default Notes;