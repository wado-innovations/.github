import bpy

# Optimisation rendu Blender (aucune animation / keyframes)

# --- PARAMÈTRES SORTIE / PERF ---
FPS = 60
RES_X, RES_Y = 1920, 1080  # 3840, 2160 pour du 4K (plus long)

# Cycles
SAMPLES = 256              # 128–512 typiquement mieux pour du web
USE_DENOISE = True
USE_MOTION_BLUR = False    # off = plus net + moins coûteux (active si besoin)
SHUTTER = 0.5

# Export vidéo
OUTPUT_PATH = "//rendus/wado"  # dossier + base name (relatif au .blend)
CRF = "HIGH"  # bon compromis qualité/poids pour le web (alternative: "MEDIUM")

scene = bpy.context.scene
scene.render.fps = int(FPS)
scene.render.resolution_x = RES_X
scene.render.resolution_y = RES_Y
scene.render.resolution_percentage = 100

# Moteur
scene.cycles.device = "GPU"  # CPU si pas de GPU supporté
scene.cycles.samples = SAMPLES
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.02
scene.cycles.use_denoising = USE_DENOISE

# Motion blur
scene.render.use_motion_blur = bool(USE_MOTION_BLUR)
scene.render.motion_blur_shutter = float(SHUTTER)

# Color management "web safe" (évite HDR / espaces exotiques pour un MP4 classique)
try:
    scene.view_settings.view_transform = "Filmic"
except Exception:
    scene.view_settings.view_transform = "Standard"
scene.sequencer_colorspace_settings.name = "sRGB"

# Sortie : un fichier vidéo (pas une séquence d'images)
scene.render.use_file_extension = True
scene.render.filepath = OUTPUT_PATH
file_format_enum = scene.render.image_settings.bl_rna.properties["file_format"].enum_items.keys()
has_ffmpeg = "FFMPEG" in file_format_enum

try:
    scene.render.image_settings.file_format = "FFMPEG" if has_ffmpeg else "PNG"
except TypeError:
    # Certaines builds Blender n'exposent pas FFmpeg même si la détection est incohérente
    has_ffmpeg = False
    scene.render.image_settings.file_format = "PNG"

if has_ffmpeg:
    ff = scene.render.ffmpeg
    ff.format = "MPEG4"
    ff.codec = "H264"
    ff.audio_codec = "AAC"
    ff.constant_rate_factor = CRF  # qualité (plus haut = fichier plus lourd)
    # Compatibilité lecture web (Safari / mobiles)
    try:
        ff.use_max_b_frames = True
    except Exception:
        pass
    try:
        ff.ffmpeg_preset = "GOOD"
    except Exception:
        pass
    try:
        ff.video_profile = "HIGH"
    except Exception:
        pass
    try:
        ff.colorspace = "BT709"
    except Exception:
        pass

    # GOP ~ 2 s (bon pour seek / streaming)
    ff.gopsize = max(1, int(round(FPS * 2)))
else:
    # Fallback universel: séquence d'images (à encoder ensuite avec ffmpeg/Blender sur une build avec FFmpeg)
    scene.render.image_settings.color_mode = "RGB"
    scene.render.image_settings.color_depth = "8"