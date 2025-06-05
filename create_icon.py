from PIL import Image, ImageDraw, ImageFont
import os

# Create a 192x192 icon with indigo background and white "S" letter
def create_icon():
    # Create image
    img = Image.new('RGB', (192, 192), color='#4f46e5')  # Indigo background
    draw = ImageDraw.Draw(img)
    
    # Try to use a font, fallback to default if not available
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 120)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position for centering
    text = "S"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (192 - text_width) // 2
    y = (192 - text_height) // 2 - 10  # Slight adjustment for visual centering
    
    # Draw the "S" in white
    draw.text((x, y), text, fill='white', font=font)
    
    # Save the icon
    os.makedirs('static/icons', exist_ok=True)
    img.save('static/icons/icon-192x192.png')
    print("Icon created successfully at static/icons/icon-192x192.png")

if __name__ == "__main__":
    create_icon() 