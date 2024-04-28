import comfy
import folder_paths
from .lora_merge import merge
from .lora_load_weight_only import LoraLoaderWeightOnly

class LoraLoadAndConcat(LoraLoaderWeightOnly):
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
				"lora_1": ("LoRA",),
                "lora_name": (folder_paths.get_filename_list("loras"), ),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
            }
        }
    RETURN_TYPES = ("LoRA", )
    FUNCTION = "lora_load_and_concat"

    CATEGORY = "lora_merge"

    def lora_load_and_concat(self, lora_1, lora_name, strength_model, strength_clip):
        lora_2 = self.load_lora_weight_only(lora_name, strength_model, strength_clip, "")[0]
        lora_merged = merge(lora_1, lora_2, "concat", 16, 1.0, "cuda", "float32")
        return (lora_merged,)