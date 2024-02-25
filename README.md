# ComfyUI-Advanced-Latent-Control

**This custom node helps to transform latent in different ways.**

## Custom Nodes
### LatentMirror
This node can flip latent and merge original and flipped version

**Input:** 
- latent

**Fields:**
- direction – `vertically`, `horizontally` or `both`
- multiplier – multiply latent by specified number

**Output:**
- latent

**Usage:**
![sample](https://i.imgur.com/YMyYorQ.png)
![sample](https://i.imgur.com/W5BasCO.png)

### LatentShift
This node can shift latent along x and y axes

**Input:** 
- latent

**Fields:**
- x_shift – float number from -1 to 1
- y_shift – float number from -1 to 1

**Output:**
- latent

**Usage:**
![sample](https://i.imgur.com/1Dp5dSw.png)
