import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import logoImg from "../public/logo.png";
import "../styles/global.css";

function Navbar() {
  return (
    <AppBar
      position="static"
      sx={{ boxShadow: 0, backgroundColor: "transparent" }}
    >
      <Container
        maxWidth="xl"
        sx={{ display: "flex", justifyContent: "center" }}
      >
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            noWrap
            component="a"
            href="#app-bar-with-responsive-menu"
            sx={{
              mr: 2,
              display: { xs: "none", md: "flex" },
              fontFamily: "monospace",
              fontWeight: 700,
              letterSpacing: ".3rem",
              color: "black",
              textDecoration: "none",
            }}
          >
            SNAPGREDIENT
          </Typography>

          <Typography
            variant="h5"
            noWrap
            component="a"
            href="#app-bar-with-responsive-menu"
            sx={{
              mr: 2,
              display: { xs: "flex", md: "none" },
              flexGrow: 1,
              fontFamily: "monospace",
              fontWeight: 700,
              letterSpacing: ".3rem",
              color: "black",
              textDecoration: "none",
            }}
          >
            SNAPGREDIENT
          </Typography>
          <img
            src={logoImg}
            className="logoImgNavbar"
            alt="Website Logo"
            style={{
              display: { xs: "none", md: "flex" },
              marginRight: 1,
              color: "black",
              width: "2rem",
              height: "auto",
              // "@media (max-width: 660px)": {
              //   width: "8rem",
              // },
            }}
          />
        </Toolbar>
      </Container>
    </AppBar>
  );
}
export default Navbar;
