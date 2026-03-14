-- 🏰 Imperial Asset Sovereignty Schema
-- To be executed in Supabase SQL Editor

-- 1. Create Categories Table
CREATE TABLE IF NOT EXISTS public.asset_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 2. Create Assets Table
CREATE TABLE IF NOT EXISTS public.assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    category_id UUID REFERENCES public.asset_categories(id),
    source_url TEXT, -- Cloud Link (OneDrive/GDrive)
    local_path TEXT, -- Physical path on D: drive
    size_bytes BIGINT,
    extension TEXT,
    cloud_status TEXT CHECK (cloud_status IN ('sync_pending', 'synced', 'error')),
    local_status TEXT CHECK (local_status IN ('download_pending', 'stored', 'missing')),
    last_scanned_at TIMESTAMPTZ DEFAULT now(),
    metadata JSONB, -- For extra data (Version, Author, etc.)
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(name, source_url)
);

-- 3. Initial Categories Seed
INSERT INTO public.asset_categories (name, description) VALUES
('After Effects', 'Templates and projects for AE'),
('Premiere Pro', 'Templates and transitions for PR'),
('Plugins', 'Installers and extensions (ZXP, EXE)'),
('Audio', 'Sound effects and music packs'),
('Graphic Design', 'PSD, Images, Overlays, Brushes'),
('3D/Blender', 'Models, Scenes, and Textures')
ON CONFLICT (name) DO NOTHING;

-- 4. Enable RLS (Optional, but recommended for Sovereignty)
ALTER TABLE public.assets ENABLE ROW LEVEL SECURITY;
-- For now, allow full access for the Service Role/Administrator
CREATE POLICY "Full access for authenticated users" ON public.assets FOR ALL USING (true);
