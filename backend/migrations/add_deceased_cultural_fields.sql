-- Migration: Add Vietnamese cultural fields to deceased_profiles table
-- Date: 2024-01-19
-- Description: Add missing fields to support Vietnamese cultural features

-- Add new fields for cultural compatibility
ALTER TABLE deceased_profiles 
ADD COLUMN IF NOT EXISTS english_name VARCHAR(200),
ADD COLUMN IF NOT EXISTS common_name VARCHAR(100),
ADD COLUMN IF NOT EXISTS gender VARCHAR(20),
ADD COLUMN IF NOT EXISTS birth_date DATE,
ADD COLUMN IF NOT EXISTS death_date DATE,
ADD COLUMN IF NOT EXISTS birth_date_lunar VARCHAR(50),
ADD COLUMN IF NOT EXISTS death_date_lunar VARCHAR(50),
ADD COLUMN IF NOT EXISTS birth_place VARCHAR(300),
ADD COLUMN IF NOT EXISTS death_place VARCHAR(300),
ADD COLUMN IF NOT EXISTS resting_place VARCHAR(500),
ADD COLUMN IF NOT EXISTS occupation VARCHAR(200),
ADD COLUMN IF NOT EXISTS education VARCHAR(300),
ADD COLUMN IF NOT EXISTS cultural_info JSONB DEFAULT '{}';

-- Remove old constraint and add new ones
ALTER TABLE deceased_profiles DROP CONSTRAINT IF EXISTS name_required;

-- Add new constraints
ALTER TABLE deceased_profiles 
ADD CONSTRAINT vietnamese_name_required 
CHECK (vietnamese_name IS NOT NULL AND length(vietnamese_name) > 0);

ALTER TABLE deceased_profiles 
ADD CONSTRAINT valid_schema_dates 
CHECK (death_date IS NULL OR birth_date IS NULL OR death_date >= birth_date);

-- Make first_name and last_name nullable since we now have alternatives
ALTER TABLE deceased_profiles 
ALTER COLUMN first_name DROP NOT NULL,
ALTER COLUMN last_name DROP NOT NULL;

-- Add comment
COMMENT ON TABLE deceased_profiles IS 'Vietnamese memorial profiles with cultural features support';