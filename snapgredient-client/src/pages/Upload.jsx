import React, { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import Scan from "../components/Scan";
import zIndex from "@mui/material/styles/zIndex";
import "../styles/upload.css";

const Upload = () => {
  const [isMobile, setIsMobile] = useState(
    window.matchMedia("(max-width: 600px)").matches
  );

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.matchMedia("(max-width: 600px)").matches);
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return (
    <div className="UploadMainContiner flex column">
      <Navbar />
      {isMobile ? (
        <>
          <div>
            <span
              className="CapitalBgmLetter"
              style={{
                zIndex: -2,
                fontSize: 220,
                position: "absolute",
                top: 90,
                left: -2,
                fontStretch: "ultra-expanded",
              }}
            >
              S
            </span>
            <span
              className="CapitalBgmLetter "
              style={{
                zIndex: -2,
                fontSize: 220,
                position: "absolute",
                top: 475,
                right: -2,
                fontStretch: "ultra-expanded",
              }}
            >
              G
            </span>
          </div>
          <div className="ScanContainer flex column center scan-mobile">
            <Scan />
          </div>
        </>
      ) : (
        <>
          <div>
            <span
              className="CapitalBgmLetter"
              style={{
                zIndex: -2,
                fontSize: 300,
                position: "absolute",
                top: 80,
                left: 30,
                fontStretch: "ultra-expanded",
              }}
            >
              S
            </span>
            <span
              className="CapitalBgmLetter "
              style={{
                zIndex: -2,
                fontSize: 300,
                position: "absolute",
                top: 230,
                right: 30,
                fontStretch: "ultra-expanded",
              }}
            >
              G
            </span>
          </div>

          <div className="ScanContainer flex column center scan-computer">
            <Scan />
          </div>
        </>
      )}
      <div className="waveContainer">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 200">
          <path
            fill="#B5FE83"
            fill-opacity="1"
            d="M0,96L60,101.3C120,107,240,117,360,138.7C480,160,600,192,720,197.3C840,203,960,181,1080,160C1200,139,1320,117,1380,106.7L1440,96L1440,0L1380,0C1320,0,1200,0,1080,0C960,0,840,0,720,0C600,0,480,0,360,0C240,0,120,0,60,0L0,0Z"
          ></path>
        </svg>
      </div>
    </div>
  );
};

export default Upload;
