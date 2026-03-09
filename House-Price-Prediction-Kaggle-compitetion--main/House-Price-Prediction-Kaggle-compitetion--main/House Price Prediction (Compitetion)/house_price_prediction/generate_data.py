import csv
import random

def generate():
    header = [
        'area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 
        'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 
        'parking', 'prefarea', 'furnishingstatus', 'price'
    ]
    
    with open('data/raw/housing.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for _ in range(545):
            area = random.randint(1500, 15000)
            bedrooms = random.randint(1, 5)
            bathrooms = random.randint(1, 4)
            stories = random.randint(1, 4)
            mainroad = random.choice(['yes', 'no'])
            guestroom = random.choice(['yes', 'no'])
            basement = random.choice(['yes', 'no'])
            hotwaterheating = random.choice(['yes', 'no'])
            airconditioning = random.choice(['yes', 'no'])
            parking = random.randint(0, 3)
            prefarea = random.choice(['yes', 'no'])
            furnishingstatus = random.choice(['furnished', 'semi-furnished', 'unfurnished'])
            
            # Simple pricing logic
            price = (area * 350 + 
                     bedrooms * 50000 + 
                     bathrooms * 100000 + 
                     stories * 80000 + 
                     (100000 if airconditioning == 'yes' else 0) + 
                     parking * 40000 + 
                     random.randint(-50000, 50000))
            
            writer.writerow([
                area, bedrooms, bathrooms, stories, mainroad, 
                guestroom, basement, hotwaterheating, airconditioning, 
                parking, prefarea, furnishingstatus, price
            ])

if __name__ == "__main__":
    generate()
