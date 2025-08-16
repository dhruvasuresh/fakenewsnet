import numpy as np
import re
from PIL import Image
import os
import logging
from typing import Dict, Any

# Import the actual trained models
from .fake_news_detector import FakeNewsDetector
from .disaster_classifier import DisasterClassifier

class SimpleMultimodalClassifier:
    """Multimodal Classifier using actual trained models"""
    
    def __init__(self):
        self.classes = ['fake', 'real_wildfire', 'real_flood', 'real_hurricane', 'real_earthquake']
        
        # Initialize actual trained models
        self.fake_news_detector = FakeNewsDetector()
        self.disaster_classifier = DisasterClassifier()
        
        # Load the models
        self.fake_news_detector.load_model()
        self.disaster_classifier.load_model()
        
        # Keywords for additional analysis
        self.fake_keywords = [
            'fake', 'hoax', 'conspiracy', 'government hiding', 'aliens', 'chemtrails',
            'fake news', 'false', 'misinformation', 'disinformation', 'clickbait',
            'BREAKING', 'SHOCKING', 'YOU WON\'T BELIEVE', 'VIRAL', 'MUST SHARE'
        ]
        
        self.disaster_keywords = {
            'wildfire': ['fire', 'wildfire', 'burning', 'flame', 'smoke', 'blaze', 'forest fire'],
            'flood': ['flood', 'water', 'rain', 'overflow', 'drowning', 'submerged', 'water level'],
            'hurricane': ['hurricane', 'storm', 'wind', 'tropical', 'cyclone', 'typhoon', 'gale'],
            'earthquake': ['earthquake', 'quake', 'shaking', 'tremor', 'seismic', 'magnitude', 'epicenter']
        }
        
        # Image analysis patterns (simplified)
        self.image_patterns = {
            'wildfire': ['orange', 'red', 'fire', 'smoke', 'burning'],
            'flood': ['blue', 'water', 'flooded', 'submerged', 'rain'],
            'hurricane': ['gray', 'storm', 'clouds', 'wind', 'tropical'],
            'earthquake': ['gray', 'debris', 'cracked', 'damaged', 'destruction']
        }
        
        logging.info("Multimodal classifier initialized with trained models")
    
    def analyze_text(self, text):
        """Analyze text using actual trained models"""
        text_lower = text.lower()
        
        # Use actual fake news detector
        fake_news_result = self.fake_news_detector.predict(text)
        
        # Use actual disaster classifier if text is classified as real
        disaster_result = None
        if fake_news_result['prediction'] == 'real':
            disaster_result = self.disaster_classifier.predict(text)
        
        # Additional keyword-based analysis for confidence boosting
        fake_score = 0
        for keyword in self.fake_keywords:
            if keyword.lower() in text_lower:
                fake_score += 1
        
        # Check for disaster types
        disaster_scores = {}
        for disaster_type, keywords in self.disaster_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            disaster_scores[disaster_type] = score
        
        # Additional fake news detection based on writing style
        caps_ratio = sum(1 for char in text if char.isupper()) / len(text) if text else 0
        if caps_ratio > 0.3:  # More than 30% caps
            fake_score += 1
        
        exclamation_count = text.count('!')
        if exclamation_count > 2:  # More than 2 exclamation marks
            fake_score += 1
        
        sensational_words = ['BREAKING', 'SHOCKING', 'INCREDIBLE', 'AMAZING', 'UNBELIEVABLE']
        if any(word.lower() in text_lower for word in sensational_words):
            fake_score += 1
        
        return fake_news_result, disaster_result, fake_score, disaster_scores
    
    def analyze_image_simple(self, image_path):
        """Simple image analysis using basic color and pattern detection"""
        try:
            if not image_path or not os.path.exists(image_path):
                return None
            
            # Load image
            image = Image.open(image_path)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Get image size
            width, height = image.size
            
            # Simple color analysis
            colors = image.getcolors(maxcolors=1000)
            if not colors:
                return None
            
            # Analyze dominant colors
            dominant_colors = []
            for count, color in colors:
                if count > (width * height * 0.01):  # More than 1% of pixels
                    dominant_colors.append(color)
            
            # Simple pattern detection based on colors
            pattern_scores = {}
            for disaster_type, patterns in self.image_patterns.items():
                score = 0
                for color in dominant_colors:
                    r, g, b = color
                    # Simple color-based pattern matching
                    if disaster_type == 'wildfire' and (r > 150 and g < 100):
                        score += 1
                    elif disaster_type == 'flood' and (b > 150 and r < 100):
                        score += 1
                    elif disaster_type == 'hurricane' and (r < 100 and g < 100 and b < 100):
                        score += 1
                    elif disaster_type == 'earthquake' and (r < 120 and g < 120 and b < 120):
                        score += 1
                pattern_scores[disaster_type] = score
            
            return {
                'dominant_colors': dominant_colors[:5],
                'pattern_scores': pattern_scores,
                'image_size': (width, height)
            }
            
        except Exception as e:
            logging.error(f"Error analyzing image: {e}")
            return None
    
    def classify(self, text: str, image_path: str = None) -> Dict[str, Any]:
        """Main classification method using actual trained models"""
        try:
            # Analyze text with trained models
            fake_news_result, disaster_result, fake_score, disaster_scores = self.analyze_text(text)
            
            # Analyze image if provided
            image_analysis = None
            if image_path:
                image_analysis = self.analyze_image_simple(image_path)
            
            # Determine final prediction
            if fake_news_result['prediction'] == 'fake':
                prediction = 'fake'
                confidence = fake_news_result['confidence']
                modality = 'text'
                explanation = fake_news_result['explanation']
                
                # Boost confidence if keyword analysis supports fake classification
                if fake_score > 2:
                    confidence = min(confidence + 0.1, 1.0)
                    explanation += " Additional fake news indicators detected in text."
                
            else:  # Real disaster
                if disaster_result:
                    disaster_type = disaster_result['prediction']
                    prediction = f"real_{disaster_type}"
                    confidence = disaster_result['confidence']
                    modality = 'text'
                    explanation = disaster_result['explanation']
                    
                    # Boost confidence if image analysis supports disaster type
                    if image_analysis and image_analysis['pattern_scores'].get(disaster_type, 0) > 0:
                        confidence = min(confidence + 0.05, 1.0)
                        modality = 'multimodal'
                        explanation += " Image analysis supports disaster classification."
                else:
                    prediction = 'real'
                    confidence = fake_news_result['confidence']
                    modality = 'text'
                    explanation = "Classified as real but disaster type unclear."
            
            # Prepare probabilities
            probabilities = {
                'fake': 0.0,
                'real_wildfire': 0.0,
                'real_flood': 0.0,
                'real_hurricane': 0.0,
                'real_earthquake': 0.0
            }
            
            if prediction == 'fake':
                probabilities['fake'] = confidence
            elif prediction.startswith('real_'):
                disaster_type = prediction.split('_')[1]
                probabilities[f'real_{disaster_type}'] = confidence
            
            return {
                'prediction': prediction,
                'confidence': confidence,
                'modality': modality,
                'explanation': explanation,
                'probabilities': probabilities,
                'fake_news_result': fake_news_result,
                'disaster_result': disaster_result,
                'image_analysis': image_analysis
            }
            
        except Exception as e:
            logging.error(f"Error in multimodal classification: {e}")
            return {
                'prediction': 'unknown',
                'confidence': 0.0,
                'modality': 'text',
                'explanation': 'Error occurred during analysis',
                'probabilities': {
                    'fake': 0.5,
                    'real_wildfire': 0.125,
                    'real_flood': 0.125,
                    'real_hurricane': 0.125,
                    'real_earthquake': 0.125
                }
            }

# Create a singleton instance
simple_multimodal_classifier = SimpleMultimodalClassifier() 