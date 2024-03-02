import json
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from gemini import askgemini

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    try:
        contents = await image.read()
        with open(image.filename, "wb") as f:
            f.write(contents)
        # result = ocr_scan(image.filename)  
        result = {
            'Rice Meal': 42.7,
            'Edible Vegetable Oil (Palmolein Oil)': 8.89,
            'Corn Meal': 19.7,
            'Spices and condiments': 8.89,
            'Gram Meal': 3.3,
            'Salt': 8.89,
            'Sugar': 8.89,
            'Tomato Powder': 0.1,
            'Citric Acid (330)': 8.89,
            'Dextrose': 8.89,
            'Milk Solids': 8.89,
            'Edible Starch': 8.89
            }
        print('Analysis Started. Please wait.')
        score = await getscore(result)
        cat = await getcategories(result)
        cat = json.loads(cat)
        os.remove(image.filename)
        return JSONResponse(content={"score": int(score), "categories": cat}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)




async def getscore(data):
    prompt = f'''{str(data)} are the ingredients of a food product with their proportions.
                    Scoring Criteria:
                    1. Score 1:   - Contains unhealthy fats, high levels of sugar or artificial sweeteners, and/or artificial additives. Best consumed rarely due to negative health impacts.
                    2. Score 2:   - Highly processed with minimal nutritional value, high in empty calories, and/or loaded with artificial additives. Consumption should be limited.
                    3. Score 3:   - Contains some nutritional value but also significant unhealthy components. Best consumed occasionally.
                    4. Score 4:   - Moderately healthy but may contain moderate levels of unhealthy components. Fine to consume occasionally in moderation.
                    5. Score 5:   - Average nutritional value, balanced in some aspects but may have room for improvement. Suitable for regular consumption in moderation.
                    6. Score 6:   - Relatively healthy with good nutritional value and balanced macronutrients. Can be consumed regularly as part of a balanced diet.
                    7. Score 7:   - Above-average nutritional value, low in unhealthy components, and may offer additional health benefits. Suitable for regular consumption.
                    8. Score 8:   - Very healthy with excellent nutritional value, low in unhealthy components, and may offer notable health benefits. Can be consumed daily.
                    9. Score 9:   - Exceptionally healthy, nutrient-dense, and may provide significant health benefits. Recommended for daily consumption.
                    10. Score 10:    - Outstandingly healthy, rich in essential nutrients, and devoid of unhealthy components. Can be consumed daily in any quantity without concern for health impacts
                    NOW ACCORING TO CRITERIA ABOVE,GIVE A SCORE OUT OF 10 AND RETURN ONLY SCORE I.e NUMBER IN THE RESPONSE'''
    response = await askgemini(prompt)
    print('Score retrieved')
    return response

async def getcategories(data):
    prompt = f"""{str(data)} are the ingredients of a food product with their proportions.
    are the ingredients of a food product with their proportions.
    now provide following info about this product in the response in this specific formatonly response: 
    {{ "Nutritional Value": "High in essential nutrients (e.g., vitamins, minerals) or Low in unhealthy components (e.g., saturated fats, added sugars)", "Natural vs. Processed": "Contains mostly natural, whole ingredients or Contains highly processed or artificial additives", "Caloric Density": "Low in calories per serving or High in empty calories or high-calorie density", "Macronutrient Balance": "Balanced ratio of carbohydrates, proteins, and fats or Imbalanced ratio, such as high in unhealthy fats or refined carbohydrates", "Allergens and Sensitivities": "Free from common allergens (e.g., gluten, dairy) or Contains allergens or potential irritants", "Glycemic Index": "Low glycemic index (slow-release energy) or High glycemic index (rapid increase in blood sugar)", "Added Sugar and Sweeteners": "No added sugars or sweeteners or High in added sugars or artificial sweeteners", "Fiber Content": "High in dietary fiber or Low in dietary fiber", "Sodium Content": "Low in sodium or High in sodium or salt content", "Processing Level": "Minimally processed or Heavily processed with additives and preservatives" }}
    """
    response = await askgemini(prompt)
    print('Categories retrieved')
    return response

@app.get("/")
def welcome():
    return "Welcome to Snapgredient"
