import comfy

class LoraLoaderFromWeight:
    def __init__(self):
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "model": ("MODEL",),
                              "clip": ("CLIP", ),
                              "lora": ("LoRA", ),
                              }}
    RETURN_TYPES = ("MODEL", "CLIP")
    FUNCTION = "load_lora_from_weight"

    CATEGORY = "lora_merge"

    def load_lora_from_weight(self, model, clip, lora):
        lora_weight = lora["lora"]
        strength_model = lora["strength_model"]
        strength_clip = lora["strength_clip"]

        if strength_model == 0 and strength_clip == 0:
            return (model, clip)

        model_lora, clip_lora = comfy.sd.load_lora_for_models(model, clip, lora_weight, strength_model, strength_clip)
        return (model_lora, clip_lora)