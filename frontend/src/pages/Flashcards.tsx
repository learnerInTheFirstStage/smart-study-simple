import React, { useState, useEffect } from "react";
import { Box, Card, CardContent, Typography, Button } from "@mui/material";
import axios from "axios";

// const flashcards = [
//   { id: 1, term: "Recursion", definition: "Function calls its own programming method" },
//   { id: 2, term: "Hash Table", definition: "Use a hash function to map the data structure of key-value pairs" },
// ];

const Flashcards = () => {
  const [index, setIndex] = useState(0);
  const [flashcards, setFlashcards] = useState<{ id: number, term: string, definition: string }[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    const fetchFlashcards = async () => {
      try {
        const response = await axios.get("https://api.example.com/flashcards");
        setFlashcards(response.data); 
      } catch (err) {
        setError("Failed to load flashcards");
      } finally {
        setLoading(false);
      }
    };
    fetchFlashcards();
  }, []);

  return (
    <Box p={4}>
      <Typography variant="h4">Memory Bread 🎴</Typography>
      <Card sx={{ maxWidth: 400, mt: 3, p: 2 }}>
        <CardContent>
          <Typography variant="h5">{flashcards[index].term}</Typography>
          <Typography variant="body1" mt={2}>{flashcards[index].definition}</Typography>
        </CardContent>
      </Card>
      <Box mt={3}>
        <Button variant="contained" color="primary" onClick={() => setIndex((index + 1) % flashcards.length)}>
          NEXT
        </Button>
      </Box>
    </Box>
  );
};

export default Flashcards;