import Navbar from "./components/Navbar";
import "./styles/info.css";
import Marquee from "react-fast-marquee";

const Info = () => {
  const payload = {
    score: 2,
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
      <div className="scoreContainer">{payload.score}/10</div>
      <div className="listContainer">
        {/* <div className="ingredientList">
          <h3 className="infoHead">Your Ingredients</h3>

          <ul className="ingredientListItems">
            <li>Rice Meal: 42.7</li>
            <li>Edible Vegetable Oil (Palmolein Oil): 8.89</li>
            <li>Corn Meal: 19.7</li>
            <li>Spices and condiments: 8.89</li>
            <li>Gram Meal: 3.3</li>
            <li>Salt: 8.89</li>
            <li>Sugar: 8.89</li>
            <li>Tomato Powder: 0.1</li>
            <li>Citric Acid (330): 8.89</li>
            <li>Dextrose: 8.89</li>
            <li>Milk Solids: 8.89</li>
            <li>Edible Starch: 8.89</li>
          </ul>
        </div> */}
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
          </div>
        </div>
      </div>
    </div>
  );
};

export default Info;
