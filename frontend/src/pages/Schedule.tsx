import React, { useState, useEffect } from "react";
import { Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button } from "@mui/material";

const Schedule = () => {
  const [studyMaterial, setStudyMaterial] = useState<string | null>(null);
  const [studyPlan, setStudyPlan] = useState<{ day: string; topic: string }[]>([]);
  const [loading, setLoading] = useState(false);

  // Load study material when the component mounts
  useEffect(() => {
    const storedMaterial = localStorage.getItem("uploadedStudyMaterial");
    if (storedMaterial) {
      setStudyMaterial(storedMaterial);
      generateStudyPlan(storedMaterial);
    }
  }, []);

  // Extract key topics from study material (Mock function)
  const extractKeyTopics = (text: string): string[] => {
    const sentences = text.split(".").map((s) => s.trim());
    return sentences.slice(0, 7); // Take first 7 sentences as key topics
  };

  // Generate Study Plan using AI API (Mocked)
  const generateStudyPlan = async (text: string) => {
    setLoading(true);

    // Mock AI processing (Replace with real AI API)
    const topics = extractKeyTopics(text);

    // Generate a study plan (assign topics across days)
    const plan = topics.map((topic, index) => ({
      day: `Day ${index + 1}`,
      topic,
    }));

    setStudyPlan(plan);
    localStorage.setItem("studyPlan", JSON.stringify(plan)); // Save plan locally
    setLoading(false);
  };

  return (
    <Box p={4}>
      <Typography variant="h4">Your very own customized Study Plan 📅</Typography>

      {/* Display Study Material */}
      {studyMaterial ? (
        <Typography variant="subtitle1" sx={{ mt: 2, fontStyle: "italic" }}>
          Study material uploaded. Study plan generated.
        </Typography>
      ) : (
        <Typography variant="subtitle1" sx={{ mt: 2, color: "red" }}>
          No study materials uploaded. Please go to "STUDY MATERIALS" page to upload.
        </Typography>
      )}

      {/* Loading Indicator */}
      {loading && <Typography>⏳ Generating study plan...</Typography>}

      {/* Display Study Plan */}
      {studyPlan.length > 0 && (
        <TableContainer component={Paper} sx={{ mt: 3 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Day</TableCell>
                <TableCell>Study Topic</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {studyPlan.map((entry, index) => (
                <TableRow key={index}>
                  <TableCell>{entry.day}</TableCell>
                  <TableCell>{entry.topic}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Clear Schedule Button */}
      {studyPlan.length > 0 && (
        <Button variant="contained" color="secondary" sx={{ mt: 3 }} onClick={() => setStudyPlan([])}>
          Clear Schedule
        </Button>
      )}
    </Box>
  );
};

export default Schedule;