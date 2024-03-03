import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import logoImg from "../public/logo.png";
import "../styles/global.css";

function Navbar() {
  return (
    <AppBar sx={{ boxShadow: 0, backgroundColor: "transparent" }}>
      <Container
        maxWidth="xl"
        sx={{ display: "flex", justifyContent: "center" }}
      >
        <Toolbar>
          <img
            src={logoImg}
            className="logoImgNavbar"
            alt="Website Logo"
            style={{
              display: { xs: "none", md: "flex" },
              marginRight: 8,
              width: "2rem",
              height: "auto",
              backgroundColor: "transparent",
            }}
          />
          <Typography
            variant="h6"
            noWrap
            component="a"
            href="#app-bar-with-responsive-menu"
            sx={{
              mr: 2,
              display: { xs: "none", md: "flex" },
              fontFamily: "Kalnia ,serif",
              fontWeight: 700,
              letterSpacing: ".3rem",
              color: "#032D3C",
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
              fontFamily: "Kalnia, serif",
              fontWeight: 700,
              letterSpacing: ".3rem",
              color: "#032D3C",
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
              color: "#5B8E7D",
              width: "2rem",
              height: "auto",
            }}
          />
        </Toolbar>
      </Container>
    </AppBar>
  );
}
export default Navbar;
