import React, { useState, useEffect } from "react";
import { Box, Card, CardContent, Typography, Button } from "@mui/material";
import axios from "axios";

const flashcardsDemo = [
  { id: 1, term: "Recursion", definition: "Function calls its own programming method" },
  { id: 2, term: "Hash Table", definition: "Uses a hash function to map the data structure of key-value pairs" },
  { id: 3, term: "Array", definition: "A collection of elements identified by index or key" },
  { id: 4, term: "Linked List", definition: "A linear collection of data elements, called nodes, where each node points to the next" },
  { id: 5, term: "Stack", definition: "A linear data structure that follows the Last In, First Out (LIFO) principle" },
  { id: 6, term: "Queue", definition: "A linear data structure that follows the First In, First Out (FIFO) principle" },
  { id: 7, term: "Binary Tree", definition: "A hierarchical data structure in which each node has at most two children" },
  { id: 8, term: "Graph", definition: "A collection of nodes (vertices) and edges representing relationships between them" },
  { id: 9, term: "Sorting Algorithm", definition: "A method for organizing elements in a particular order, such as quicksort or mergesort" },
  { id: 10, term: "Dynamic Programming", definition: "A method for solving complex problems by breaking them down into simpler overlapping subproblems" },
];

const Flashcards = () => {
  const [index, setIndex] = useState(0);
  const [flashcards, setFlashcards] = useState<{ id: number, term: string, definition: string }[]>(flashcardsDemo);
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