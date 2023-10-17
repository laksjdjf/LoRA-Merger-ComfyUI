import comfy
import folder_paths

import re

def extract_numbers(s):
    return [int(num) for num in re.findall(r'\d+', s)]

def expand_lbw(weight_list):
    length = len(weight_list)
    if length == 17:
        new_list = []
        j = 0
        for i in range(26):
            if i in LBW17TO26:
                new_list.append(0.0)
            else:
                new_list.append(weight_list[j])
                j += 1
    elif length == 12:
        new_list = []
        j = 0
        for i in range(20):
            if i in LBW12TO20:
                new_list.append(0.0)
            else:
                new_list.append(weight_list[j])
                j += 1
    else:
        new_list = weight_list
    return new_list

LBW17TO26 = [2, 5, 8, 11, 12, 13, 15, 16, 17]
LBW12TO20 = [2, 3, 4, 5, 8, 18, 19, 20]

MID_ID = {26:14, 20:11}

class LoraLoaderWeightOnly:
    def __init__(self):
        self.loaded_lora = None
        self.lbw = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "lora_name": (folder_paths.get_filename_list("loras"), ),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                "lbw": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
            }
        }
    RETURN_TYPES = ("LoRA", )
    FUNCTION = "load_lora_weight_only"

    CATEGORY = "lora_merge"

    def load_lora_weight_only(self, lora_name, strength_model, strength_clip, lbw):
        lora_path = folder_paths.get_full_path("loras", lora_name)
        lora = None

        if self.loaded_lora is not None:
            if self.loaded_lora[0] == lora_path:
                lora = self.loaded_lora[1]
            else:
                temp = self.loaded_lora
                self.loaded_lora = None
                del temp

        if lora is None or self.lbw != lbw:
            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
            if lbw != "":
                weight_list = [float(weight) for weight in lbw.split(",")]
                weight_list = expand_lbw(weight_list)
                length = len(weight_list)

                strength_clip = strength_clip * weight_list[0]

                up_keys = [key for key in lora.keys() if "lora_up" in key and not "lora_te" in key]

                for key in up_keys:
                    ids = extract_numbers(key)
                    if "input_blocks" in key:
                        block_id = ids[0] + 1
                    elif "middle_block" in key:
                        block_id = MID_ID[length]
                    elif "output_blocks" in key:
                        block_id = ids[0] + MID_ID[length] + 1
                    elif "down_blocks" in key:
                        block_id = ids[0]*3 + ids[1] + 1 + 1
                        if "down_sampler" in key:
                            block_id += 2
                    elif "mid_block" in key:
                        block_id = MID_ID[length]
                    elif "up_blocks" in key:
                        block_id = ids[0]*3 + ids[1] + MID_ID[length] + 1
                        if "up_sampler" in key:
                            block_id += 2
                    else:
                        block_id = 0
                    lora[key] = lora[key] * weight_list[block_id]
            
            self.loaded_lora = (lora_path, lora)
            self.lbw = lbw

        return ({"lora": lora, "strength_model": strength_model, "strength_clip": strength_clip}, )
