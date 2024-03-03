import "../styles/info.css";
import { useEffect, useState } from "react";
import Marquee from "react-fast-marquee";
import { CircularProgressbar } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";
import retryIcon from "../public/retry.png";
import Navbar from "../components/Navbar";
import "../styles/upload.css";
const Info = () => {
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
  const payload = {
    score: 6,
    categories: {
      "Nutritional Value":
        "Low in unhealthy components (e.g., saturated fats, added sugars)",
      "Natural vs. Processed":
        "Contains highly processed or artificial additives",
      "Caloric Density": "High in empty calories or high-calorie density",
      "Macronutrient Balance":
        "Imbalanced ratio, such as high in unhealthy fats or refined carbohydrates",
      "Allergens and Sensitivities":
        "Contains allergens or potential irritants",
      "Glycemic Index": "High glycemic index (rapid increase in blood sugar)",
      "Added Sugar and Sweeteners":
        "High in added sugars or artificial sweeteners",
      "Fiber Content": "Low in dietary fiber",
      "Sodium Content": "High in sodium or salt content",
      "Processing Level": "Heavily processed with additives and preservatives",
    },
  };
  const colors = ["#F7FF56", "#94FC13", "#4BE3AC"];
  return (
    <div className="mainContainer">
      <Navbar />
      {isMobile ? (
        <>
          <div className="waveContainer">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 1440 800"
              style={{}}
            >
              <path
                fill="#B5FE83"
                fillOpacity="1"
                d="M0,192L60,202.6C120,213,240,224,360,247.4C480,270,600,296,720,300.6C840,305,960,282,1080,260C1200,238,1320,214,1380,203.4L1440,192L1440,0L1380,0C1320,0,1200,0,1080,0C960,0,840,0,720,0C600,0,480,0,360,0C240,0,120,0,60,0L0,0Z"
              />
            </svg>
          </div>
        </>
      ) : (
        <>
          <div className="waveContainer">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 1440 800"
              style={{}}
            >
              <path
                fill="#B5FE83"
                fillOpacity="1"
                d="M0,96L60,101.3C120,107,240,117,360,138.7C480,160,600,192,720,197.3C840,203,960,181,1080,160C1200,139,1320,117,1380,106.7L1440,96L1440,0L1380,0C1320,0,1200,0,1080,0C960,0,840,0,720,0C600,0,480,0,360,0C240,0,120,0,60,0L0,0Z"
              ></path>
            </svg>
          </div>
        </>
      )}
      <div
        className="scoreContainer"
        style={{
          width: 200,
          height: 200,
          position: "absolute",
          zIndex: 5,
          top: 150,
        }}
      >
        <div
          className="retryScoreContainer"
          style={{ width: 200, height: 200 }}
        >
          <CircularProgressbar
            text={`${payload.score}/10`}
            maxValue={10}
            minValue={1}
            value={payload.score}
            className="progressbar"
          />
        </div>
        <div className="scoreDeetsList">
          <ul>
            <li>First Point</li>
            <li>second Point</li>
            <li>Third Point</li>
            <li>Fourth Point</li>
            <li>Fifth Point</li>
          </ul>
        </div>
      </div>
      <div className="listContainer">
        <div className="categoryList">
          <div className="categoryContainer">
            <Marquee
              speed={70}
              direction="right"
              className="moveRight"
              autoFill="true"
              pauseOnHover="true"
            >
              {Object.keys(payload.categories)
                .slice(0, 5)
                .map((category, index) => (
                  <div
                    key={category}
                    className={`categoryCard`}
                    style={{ color: colors[index % colors.length] }}
                  >
                    <h4 className="categoryHead">{category}</h4>
                    <p className="categoryDeets">
                      {payload.categories[category]}
                    </p>
                  </div>
                ))}
            </Marquee>

            <Marquee
              speed={70}
              direction="left"
              className="moveLeft"
              autoFill="true"
              pauseOnHover="true"
            >
              {Object.keys(payload.categories)
                .slice(5)
                .map((category, index) => (
                  <div
                    key={category}
                    className={`categoryCard`}
                    style={{ color: colors[index % colors.length] }}
                  >
                    <h4 className="categoryHead">{category}</h4>
                    <p className="categoryDeets">
                      {payload.categories[category]}
                    </p>
                  </div>
                ))}
            </Marquee>
            <button className="btn">
              <img
                src={retryIcon}
                alt="retry icon"
                style={{
                  display: { xs: "none", md: "flex" },
                  marginRight: 3,
                  color: "#5B8E7D",
                  width: "2rem",
                  height: "auto",
                }}
              />
              Retry
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Info;
