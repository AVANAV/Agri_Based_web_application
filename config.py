# AgriMarket Configuration File

import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # MongoDB
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/'
    MONGO_DBNAME = 'agri_app'
    
    # Application
    DEBUG = False
    TESTING = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Agricultural settings
    INSURANCE_PREMIUM_RATE = 0.05  # 5%
    MIN_WHOLESALE_ORDER = 10  # Minimum units for wholesale
    
    # Crop types
    CROP_TYPES = [
        'rice', 'wheat', 'corn', 'cotton', 'sugarcane',
        'vegetables', 'fruits', 'pulses', 'spices', 'dairy'
    ]
    
    # Product categories
    PRODUCT_CATEGORIES = [
        'seeds', 'fertilizer', 'vegetables', 'fruits',
        'grains', 'pulses', 'spices', 'dairy', 'processed_goods'
    ]
    
    # Disease types
    DISEASE_DATABASE = {
        'rice': {
            'leaf_blast': {
                'symptoms': 'Diamond-shaped lesions on leaves',
                'remedy': 'Use resistant varieties, improve drainage, apply fungicides'
            },
            'brown_spot': {
                'symptoms': 'Brown circular spots on leaves',
                'remedy': 'Use certified seeds, improve ventilation'
            },
            'bacterial_leaf_blight': {
                'symptoms': 'Yellow-green lesions with brown edges',
                'remedy': 'Plant resistant varieties, manage water'
            }
        },
        'wheat': {
            'powdery_mildew': {
                'symptoms': 'White powder on leaves',
                'remedy': 'Improve air circulation, apply sulfur fungicides'
            },
            'rust': {
                'symptoms': 'Red-brown pustules on leaves',
                'remedy': 'Plant resistant varieties, apply fungicides'
            },
            'septoria_nodorum_blotch': {
                'symptoms': 'Gray lesions with dark borders',
                'remedy': 'Remove infected debris, apply fungicides'
            }
        },
        'corn': {
            'common_rust': {
                'symptoms': 'Red-brown pustules on leaves',
                'remedy': 'Plant resistant varieties, apply fungicides early'
            },
            'northern_leaf_blight': {
                'symptoms': 'Long narrow lesions on leaves',
                'remedy': 'Use resistant hybrids, manage moisture'
            },
            'gray_leaf_spot': {
                'symptoms': 'Gray rectangular spots',
                'remedy': 'Rotate crops, apply fungicides'
            }
        },
        'tomato': {
            'early_blight': {
                'symptoms': 'Brown spots with concentric rings',
                'remedy': 'Remove infected leaves, apply copper fungicides'
            },
            'late_blight': {
                'symptoms': 'Water-soaked lesions',
                'remedy': 'Improve air flow, use resistant varieties'
            },
            'powdery_mildew': {
                'symptoms': 'White powdery coating',
                'remedy': 'Apply sulfur or potassium bicarbonate'
            }
        }
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'dev-secret-key-insecure-change-this'

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    MONGO_DBNAME = 'agri_app_test'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # In production, always set these via environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGO_URI = os.environ.get('MONGO_URI')

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
