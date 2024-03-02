import Navbar from "./components/Navbar";
import "./styles/info.css";
import Marquee from "react-fast-marquee";
import { CircularProgressbar } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";
import retryIcon from "./public/retry.png";
const Info = () => {
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
      <div className="scoreContainer" style={{ width: 200, height: 200 }}>
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
