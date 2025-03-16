import React from "react";
import { AppBar, Toolbar, Button } from "@mui/material";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Button color="inherit" component={Link} to="/">Dashboard</Button>
        <Button color="inherit" component={Link} to="/notes">Study Materials</Button>
        <Button color="inherit" component={Link} to="/schedule">Study Plans</Button>
        <Button color="inherit" component={Link} to="/practice">Practices</Button>
        <Button color="inherit" component={Link} to="/performance">Performances</Button>
        <Button color="inherit" component={Link} to="/flashcards">Flashcards</Button>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;