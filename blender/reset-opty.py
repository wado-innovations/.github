import bpy


def _has_enum(prop, value: str) -> bool:
    try:
        return value in prop.enum_items.keys()
    except Exception:
        return False


def _set_if_enum(obj, attr: str, value: str) -> bool:
    prop = obj.bl_rna.properties.get(attr)
    if not prop or prop.type != "ENUM":
        return False
    if not _has_enum(prop, value):
        return False
    setattr(obj, attr, value)
    return True


def reset_render_optimizations(scene: bpy.types.Scene) -> None:
    r = scene.render

    # FPS / résolution (valeurs "standard" plutôt que 4K/60)
    r.fps = 24
    r.resolution_x = 1920
    r.resolution_y = 1080
    r.resolution_percentage = 100

    # Moteur: tenter Eevee (selon version), sinon ne pas toucher
    _set_if_enum(r, "engine", "BLENDER_EEVEE_NEXT") or _set_if_enum(r, "engine", "BLENDER_EEVEE")

    # Color management: Filmic par défaut (si disponible)
    vs = scene.view_settings
    _set_if_enum(vs, "view_transform", "Filmic")

    # Séquenceur: sRGB si possible
    try:
        scene.sequencer_colorspace_settings.name = "sRGB"
    except Exception:
        pass

    # Motion blur: off par défaut
    r.use_motion_blur = False
    try:
        r.motion_blur_shutter = 0.5
    except Exception:
        pass

    # Sortie: revenir à une sortie image standard
    r.use_file_extension = True
    r.filepath = "//"
    img = r.image_settings
    img.file_format = "PNG"
    try:
        img.color_mode = "RGB"
        img.color_depth = "8"
    except Exception:
        pass

    # Cycles: remettre des valeurs neutres (si Cycles existe dans ce build)
    if hasattr(scene, "cycles"):
        c = scene.cycles
        try:
            c.device = "CPU"
        except Exception:
            pass
        try:
            c.samples = 128
        except Exception:
            pass
        try:
            c.use_adaptive_sampling = False
        except Exception:
            pass
        try:
            c.adaptive_threshold = 0.01
        except Exception:
            pass
        try:
            c.use_denoising = False
        except Exception:
            pass


reset_render_optimizations(bpy.context.scene)
