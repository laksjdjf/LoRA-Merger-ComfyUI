from .lora_merge import LoraMerger
from .lora_load_from_weight import LoraLoaderFromWeight
from .lora_load_weight_only import LoraLoaderWeightOnly
from .lora_save import LoraSave
from .lora_load_and_concat import LoraLoadAndConcat

NODE_CLASS_MAPPINGS = {
    "LoraMerge": LoraMerger,
    "LoraLoaderFromWeight": LoraLoaderFromWeight,
    "LoraLoaderWeightOnly": LoraLoaderWeightOnly,
    "LoraSave": LoraSave,
	"LoraLoadAndConcat": LoraLoadAndConcat
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoraMerge": "Merge LoRA",
    "LoraLoaderFromWeight": "Load LoRA from Weight",
    "LoraLoaderWeightOnly": "Load LoRA Weight Only",
    "LoraSave": "Save LoRA",
	"LoraLoadAndConcat": "Load and concat LoRA"
}

__all__ = [NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS]
