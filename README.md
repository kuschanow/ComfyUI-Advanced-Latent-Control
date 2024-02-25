# ComfyUI-Advanced-Latent-Control

**This custom node helps to transform latent in different ways.**

## Custom Nodes
### LatentMirror
This node can flip latent and merge original and flipped version

**Input:** 
- `latent`

**Fields:**
- `direction` – can be `vertically`, `horizontally` or `both`
- `multiplier` – multiply latent by specified number

**Output:**
- `latent`

**Usage:**
![sample](https://i.imgur.com/YMyYorQ.png)
![sample](https://i.imgur.com/W5BasCO.png)

### LatentShift
This node can shift latent along x and y axes

**Input:** 
- `latent`

**Fields:**
- `x_shift` – a number between -1 and 1 that indicates how much the latent should be shifted
- `y_shift` – a number between -1 and 1 that indicates how much the latent should be shifted

**Output:**
- `latent`

**Usage:**
![sample](https://i.imgur.com/1Dp5dSw.png)

### KSampler (Latent Control)
This node can multiply, mirror and shift latent during generation

**Input:**  
exactly matches the base KSampler

**Fields:**
- base KSampler fields
- `start_mirror_at` – a number between 0 and 1 that indicates at what point the sampler will start mirroring
- `stop_mirror_at` – a number between 0 and 1 that indicates at what point the sampler will stop mirroring
- `mirror_mode` – can be `replace` or `combine`. `replace` will replace the latent with the transformed one, `combine` will add the original and the transformed latent and divide by 2
- `mirror_direction` – can be `none`, `vertically`, `horizontally`, `both`, `90 degree rotation` or `180 degree rotation`
- `start_shift_at` – a number between 0 and 1 that indicates at what point the sampler will start shifting
- `stop_shift_at` – a number between 0 and 1 that indicates at what point the sampler will stop shifting
- `shift_mode` – can be `replace` or `combine`. `replace` will replace the latent with the transformed one, `combine` will add the original and the transformed latent and divide by 2
- `x_shift` – a number between -1 and 1 that indicates how much the latent should be shifted
- `y_shift` – a number between -1 and 1 that indicates how much the latent should be shifted
- `start_multiplier_at` – a number between 0 and 1 that indicates at what point the sampler will start multiplying
- `stop_multiplier_at` – a number between 0 and 1 that indicates at what point the sampler will stop multiplying
- `multiplier_mode` – can be `replace` or `combine`. `replace` will replace the latent with the transformed one, `combine` will add the original and the transformed latent
- `multiplier` – multiply latent by specified number

**Output:**
exactly matches the base KSampler

**Usage:**  
**You also can use those params together**  
![sample](https://i.imgur.com/RMJTnWF.png)  
![sample](https://i.imgur.com/fQ7UWuS.png)  
![sample](https://i.imgur.com/pxWupAx.png)  
![sample](https://i.imgur.com/1YkERDu.png)  

